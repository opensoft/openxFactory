# Tasks: add-neutral-product-standalone-operability

Status: ratified
Ratified by: add-neutral-product-standalone-operability — 2026-09-24, Brett Heap, "ratify #1144, land the follow-ons, (a) on C1–C5" (`#656` comment `5815412869`), over PR #1144's final head `19237b91` as landed at `94b6f7f1` (record `review/ratification-2026-09-24.md`)

**Group 1 is the authoring THIS change performs and it touches no code.**
Groups 2-16 are the post-ratification realization, each in the repository named
in its heading and each carrying the FALSIFICATION COMMAND that closes it — an
exact invocation with its checkout preconditions and its expected result, so the
archive gate's evidence under `release-realization` is a command re-run and
quoted rather than a description believed. **The groups keep the numbers they
were filed under, because every falsifier and every review thread cites them.
The ORDER they are built in is the release map below** (RULED `5799646419`, as
corrected by `5800995035`).

**Groups 2-12, 15 and 16 take one requirement each; TWO groups take more than one,**
because their requirements are satisfied by one act and splitting them would
produce boxes that cannot be closed independently: **Group 13** takes
requirements 12 and 13 (the install brings its datastore AND its identity mode —
one install story), and **Group 14** takes requirements 6, 14 and 15 (the store
that holds a finding, the loop that fixes it, and the exception that suppresses
it — one schema and one loop). Requirement 6 is therefore reached TWICE, by
Group 6 for the check itself and by Group 14 for where its results live, which is
the amendment the ruling of 2026-09-22 made to it. The requirement-to-group map is
the group headings, read as written; nothing below claims a bijection.

**Three classes of verb appear in the commands, and the difference matters.**

1. **Verbs that EXIST today**: `generate`, `generate-and-open`, `create` and
   `edit`, in the exact shapes task 10.1's table records against the parser. The
   arc packages and unblocks them; it does not change them.
2. **Verbs this arc CREATES**, each declared by name and shape in ONE numbered
   box: `submit` (12.4a), `land` (12.6a), and `health run|list|fix|accept`
   (14.5). A falsification that uses one is an acceptance test for surface the
   realization must add, not a re-run of surface that exists.
3. **Prerequisites by name.** A group MAY use a verb, or a surface, that a group
   BUILT EARLIER declares (the release map below gives the order), and it says so.
   Group 15 runs Group 14's `health run`
   and `health list`, so Group 15 cannot close before 14.5 lands. Groups 14 and
   15 store their results in Group 13's bundled datastore, and each falsifier
   selects it with `OPENDOX_INSTALL_MODE=local` in a fresh `OPENDOX_STATE_DIR`.
   12.5 needs Group 9, because the whole suite must first be runnable.

**The rule:** no box closes on a command whose verb is neither in 10.1's table
nor declared by its own group or by an earlier one it names.

**Fixture corpora are DIRECTORIES in the code leg's checkout, never
repositories**, and none exists today — `git ls-tree` over openDox-code's
`tests/fixtures/` at `3c3a9e31` lists four files, none of them a corpus. Each is
shipped by the first group that needs it (5.0, 7.0, 14.9, 15.6a). **Every
falsification that needs a repository COPIES its fixture into a fresh `git init`
first**, so no command below can create a branch or a commit inside the checkout
it is testing, and a git adapter pointed at a fixture reads that fixture rather
than the enclosing repository. Each block carries its own three setup lines and
its own commit identity, so every group runs from a fresh shell on its own.
**Setup steps are ONE COMMAND PER LINE, never chained with `&&`.** Under
`set -e` a failure anywhere but the LAST command of an `&&` list does not stop
the shell. A failed `git init` or `python -m venv` would therefore be skipped
silently, and the acceptance would go on to run against a directory that is
not a repository, or against whatever `opendox` is already on the PATH.
**Scratch space is resolved at run time, never named.** Each block that needs
scratch space starts with `W=$(mktemp -d)` and keeps every venv, capture file
and throwaway repository under `$W`. No committed command therefore names a
host-absolute path (the constitution's Principle IV), and two runs cannot
collide. The kernel's own interfaces are named as interfaces: `/dev/null`,
`/dev/tty` and `/proc` are the same on every Linux host and describe no host's
layout, and neither does the `--tmpfs /tmp` that bwrap mounts INSIDE a pack's
sandbox (15.1b).

House rule: OpenSpec ratifies, Speckit builds. No group below is started before
ratification, no group is started without its own claim on
`opensoft/openxFactory#656` per lane-collision-protocol Rule 1, and this change
merges nothing anywhere.

Baselines. The invariant is a DELTA, not a count: against the `main` it lands on,
this packet adds **+1 item and +1 passed, with ZERO new failures**, under
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and the pinned gate
`python3 scripts/validate-openspec-cli-pin.py --all --no-cache` exits 0 with
`0 UNDISPOSITIONED failures` and its one accepted exception
(`add-chain-attestation`, ratified disposition). Absolute counts move whenever
another change lands, so each record below is paired with the `main` it was
measured on:

| measured on `main` | `main` alone | with this packet | delta |
|---|---|---|---|
| `4f92d651` (filing, 2026-09-22) | 109 passed / 1 failed of 110 | 110 / 1 of 111 | +1 item, +1 passed, 0 new failures |
| `a151e462` (after merging #1141 and #1143) | 111 / 1 of 112 | 112 / 1 of 113 | +1 item, +1 passed, 0 new failures |
| `d52b4199` (after #1116, #1145, #1112, #1119, #1147 and #1146) | 110 / 1 of 111 | 111 / 1 of 112 | +1 item, +1 passed, 0 new failures |

**The gate that matters is the one run at landing, against the `main` of that
moment.** The PR description publishes the latest row, and the archive gate
re-measures the same delta rather than trusting either row.

## The release map — two releases, five phases, one change (RULED)

**RULED** by Brett Heap, `#656` comment `5799646419` (2026-09-23T17:30:26Z),
*"a, phases 1-3 as the first release"*, and comment `5800995035` (18:56:33Z),
*"the four 1144 questions, go with recomendations"*, which answered the four
questions this packet raised against the first ruling's phase-1 wording.
`design.md` § D13 carries the reasoning. **The map orders the build. It changes
no requirement and no scenario.**

| release | phase | what it delivers | groups and boxes |
|---|---|---|---|
| 1 — standalone operation | 1, it runs | the reach-back cut (G1, G4), a neutral default host profile, openDox's own default corpus adapter registered at startup, each leg green alone, the console script | Group 2; Group 3; 4.1, 4.1a, 4.2 and 4.3's eight reaches into openxFactory; Group 9 but 9.5; 10.1 |
| 1 | 2, it is useful alone | openDox's own neutral generator over the six words, and its own validator | Group 5; Group 7 |
| 1 | 3, it installs | bundled Postgres, the local identity mode, the served and documented bundle, chat's model configuration | Group 13; 10.2, 10.3 and Group 10's falsifier; Group 16 |
| 2 — the document tool and self-maintenance | 4 | local merge and the governed pull-request path, the neutral submission step, one interface for both | Group 12 |
| 2 | 5 | the health engine: the additive `0003_` migration, the neutral checks, the Health view and CLI, the fix loop, exceptions in git, the check-pack interface | Group 6; Group 14; Group 15 |
| every phase | — | the guard, and the pins | Group 11; 9.5 |
| outside both | — | openDox-spec's re-promotion, and the follow-ons | Group 8; F1-F4 |

**Release 1 is STANDALONE OPERATION, not a declared standalone product.**
Requirement 8 keeps that declaration for when openDox-spec has promoted the
requirements the carve assigned it, which is Group 8, outside both releases.

**Phase 1 moves nothing out of openxFactory.** Its lane actions and its host
wiring stay where requirement 1 keeps them, and 11.1's guard stands with its
declared surfaces as written (`5800995035`, answer 1, which corrects the first
ruling's phase-1 wording).

**4.3's nineteen reaches into openXdox are routed within release 1**, each no
later than the phase whose surface calls it: the generator's and the snapshot
registry's with 5.4's seam in phase 2, and `serve_workbench.py`'s seven — the
doxBench thread, chat, abstract and model-approval handlers — by phase 3, where
Group 16's chat must answer with no consumer installed. Group 4's falsifier reads
the whole package, so it closes with the last of them. This placement is the
packet's reading of "standalone operation", not a ruling: a verb that fails on a
missing consumer module in front of a user is not standalone operation.

**Group 10's one falsifier closes in phase 3**, because it serves 10.2's bundle
over 5.0's fixture. 10.1's own proof in phase 1 is that falsifier's first
assertion, `opendox --help`.

**AMENDED — T007 Batch F (`5850003126`; Ruled R1Q25 (b)):** 9.2 closes in
phase 3, although the map puts Group 9 in phase 1. Its whole-suite check lands
in phase 1, and the box closes where its ratchet reaches `(0, 0)`, in phase 3,
because 9.2 lowers `OPENDOX_BACK_IMPORTS` *"as each deferred reach closes"*
and 4.3's nineteen reaches into openXdox close by then. 7.3 stays in phase 2,
beside openDox's own validator, as the map has it. Nothing else in the map
moves. Carried out by T043, T086 and T097.

**AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q1 (a),
read with CF-1, `6013547504`):** A non-normative reading of phase 4's cell,
which changes no cell of the map. *"One interface for both"* (`:108`; and
`design.md` § D13's *"submission behind one interface"*, `:799-800`) means one
USER-FACING interface. The `submit` and `land` verbs and routes, and the Health
view's land action, are the same in every mode. Behind them the protocols stay
split, as 12.1 and 12.6a require, and each is bound as this change already
says: `submit`'s port comes from 12.4's bindings, and is `LocalGitSubmissions`
when nothing is injected; the governance query binds the lander alone,
`landing_factory` under `standalone`, the host's own instrument under
`governed`, and nothing under `unknown`. "Every mode" means every GOVERNANCE
mode (`standalone`, `governed`, `unknown`) under openDox's own profile (CF-1).
A host profile that replaces the default carries none of `submit`, `land` or
`health` in release 2 (R2Q3 (a)), and a `governed` repository with no
instrument refuses `land` by name ("governed-without-an-instrument", 12.6a).
`design.md` § D13 carries a parallel addendum. Carried out by plan 038's T015
and T016.

**AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6013547504`; Ruled N-6 (a)):**
A reading of *"The ORDER they are built in is the release map"* (`5799646419`)
for release 2's two phases, which moves no cell of the map. Brett Heap's
multi-choice word of 2026-10-06, verbatim *"Allow the overlap (Recommended)"*:
phase 5's openDox-code slices may land once the openDox root has pinned phase
4's openDox-code commit (plan 038's T027), and they do not wait for phase 4's
checkpoint (its T033). A phase-4 repair that then needs a further openDox-code
change rides phase 5's pin. Carried out by plan 038's phase-5 order, whose
T041, T042, T043 and T050 follow T027.

**Release 2's rulings are SEQUENCED, not deferred, reopened or weakened.** The
rulings recorded for phases 4 and 5 — `5783934499` (the neutral submission step),
`5784155201` (merge authority, and health in the store; its install half is phase
3's), `5784247356` (the fix loop) and `5784295745` (the check-pack interface) —
stand exactly as encoded. Requirements 6, 11, 14, 15 and 16 are this change's as
written.

**One change, and its archive needs BOTH releases.** `release-realization` admits
ONE `target_release:` per proposal, so "release 1" and "release 2" are sequencing
inside this change and not release identifiers, and `target_release: implemented`
does not move. The change archives only on merged, green realization evidence for
release 1 AND release 2 (`5800995035`, answer 2), so landing release 1 archives
nothing and promotes nothing. Splitting release 2 into its own change stays open
for later.

## Group 1 — Authoring (THIS change; no code byte)

- [x] 1.1 Author `.openspec.yaml` — ad-hoc origin, the drafting-provenance shape
  with NO approval pair (`add-drafted-proposal-origin`), naming the archived
  packet's unclosed residue as the origin.
- [x] 1.2 Author `proposal.md`: the owner's goal in his own words from `#656`;
  the two-products measurement; the repository-choice FINDING; the G-to-
  requirement table; the explicit "what openxFactory keeps" section; honest
  `code_surface:` / `target_release:` front-matter.
- [x] 1.3 Author the `## ADDED Requirements` delta creating
  `neutral-product-standalone-operability` — 17 requirements, 75 scenarios,
  domain-neutral, openDox as the measured instance.
- [x] 1.4 Author `design.md`: D1-D8 and **R-G3** — filed as Q-G3, the one question
  put to Brett with three options and a recommendation; RULED the same day and
  rewritten as the record of the decision, the options as they were put, and the
  CORRECTION to this packet's own pricing of the rejected option.
- [x] 1.5 `OPENSPEC_TELEMETRY=0 openspec validate add-neutral-product-standalone-operability --strict`
  and `--all --strict` pass with no NEW failure against the baseline above.
- [x] 1.6 `python3 scripts/proposal-support.py . verify add-neutral-product-standalone-operability`
  passes; the `tests/sequenced_after/corpus-ledger.yaml` row is machine-seeded
  (`scripts/validate-sequenced-after.py --seed-ledger --moved-by … --moved-on …`),
  and the README "OpenSpec Records" *Active changes* bullet is added.
- [x] 1.7 **RULING G3 — GIVEN.** Brett Heap, `#656` comment `5783335210`,
  2026-09-22T20:08:59Z: *"yes, openDox gets its own neutral generator."* Group 5
  is no longer blocked and requirement 4 is written to the ruling. `design.md`
  § R-G3 records the options as they were put, what was ruled, and the CORRECTION
  to this packet's own pricing of option (a) — `generator.py:66-68` imports
  `doc_health`, which this packet had not measured when it recommended (c).
- [x] 1.8 On ratification: `Status: ratified` + one sanctioned ratification
  citation on all three lifecycle documents (`Ratified:` on `proposal.md`,
  `Ratified by:` on `design.md` and `tasks.md`); `## Ratification record` in
  `proposal.md`; the approval pair ADDED beside the fixed origin in
  `.openspec.yaml`, never substituted. *(As filed, this box named `Ratified by:`
  on all three. `document-lifecycle` sanctions both spellings, one citation per
  document, and the split below is the one the lane's #1140 and #1141 carried.)*
  **Done on the word of 2026-09-24** (`#656` comment `5815412869`):
  - `Status: ratified` and one citation on each of the three lifecycle
    documents, split as the heading above says.
  - `## Ratification record` in `proposal.md`.
  - The approval pair ADDED under `origin:` after `proposed_on`. `kind`, `id`,
    `reason`, `proposed_by` and `proposed_on` do not move.
  - The record, `review/ratification-2026-09-24.md`.
- [x] 1.9 **THE RULINGS OF 2026-09-23 — GIVEN AND ENCODED.** `5799494355`
  (*"keep the direct arrow, revisit after phase 1"*): RULING OQ-2's pin chain is
  unchanged, carried as a non-normative note in `design.md` § D13 and as
  follow-on F4. `5799646419` (*"a, phases 1-3 as the first release"*): the
  release map above. `5800995035` (*"the four 1144 questions, go with
  recomendations"*): requirement 1 kept and the first ruling's phase-1 wording
  corrected; one change, whose archive needs both releases' evidence;
  requirement 17 and Group 16 for chat's model configuration; release 1 named
  standalone operation. Requirement 17 is ADDED, and no requirement or scenario
  that was already here changed.

## Group 2 — Requirement 2 / G1: imports with no consumer, publisher or host (openDox-code)

The highest-leverage box: TWO import statements, 1,232 of 1,298 measured errors
at `f8a1ece`, zero passed. An AST census of `src/` finds exactly two import-time
reaches (`serve.py:199`, `serve.py:206`) and two deferred ones; every other
mention in the package is prose.

- [x] 2.1 Remove the module-level `from ideation_dashboard import
  serve_openxfactory_lanes` (`src/opendox/serve.py:199`) and the
  `from ideation_dashboard.serve_openxfactory_lanes import (…)` re-export block
  (`:206`). The five names (`ACTIONS_APPLY_REGISTER_EDITS_ROUTE`,
  `ACTIONS_DTN_SEED_ROUTE`, `ACTIONS_REFRESH_ROUTE`,
  `ACTIONS_STAGING_SEED_ROUTE`, `COMMITTED_INTENTS_ROUTE`) belong to
  openxFactory's lanes surface, filed `stays_openxfactory_adapter`. All five are
  plain route strings (`"/committed-intents.json"`, `"/actions/refresh"`,
  `"/actions/apply-register-edits"`, `"/actions/dtn-seed"`,
  `"/actions/staging-seed"`).

  **Landed 2026-09-27** (T011): openDox-code#46 → `0e88454a` removes
  `serve.py:199` and the `:206` re-export block; F2.1's sweep and 2.4's named
  test pass with no sibling installed (that PR's body;
  `evidence/checkpoint-phase1.md` § 1, exit 0). Correction (research R16 item 7,
  non-normative): Group 2's opening figures, 1,298 errors of which 1,232 name
  `ideation_dashboard` at `f8a1ece`, read 1,305 and 1,239 at `1e4a57fb`
  (research R2). The head moved, and the cause did not.
- [x] 2.1a **DO NOT VENDOR the module.**
  `scripts/ideation_dashboard/serve_openxfactory_lanes.py` itself imports
  `from openxdox import snapshot_registry` (`:70`) and
  `from openxdox.serve_projection import hosted_ref_refused` (`:77`), so copying
  it into openDox re-creates the consumer dependency BUILD slice 2b removed.

  **Landed 2026-09-27** (T011): openDox-code#46 → `0e88454a`. The lanes module
  is not vendored: its five route names left `serve.py`, and F2.1's sweep
  imports every module of the package with `openxdox`, `ideation_dashboard`,
  `doc_health` and `corpus_adapter_openxfactory` all absent
  (`evidence/checkpoint-phase1.md` § 1).
- [x] 2.2 Contribute those routes through the EXISTING seam —
  `serve.build_server(route_extensions=)` / `route_extension.RouteBinding` — from
  openxFactory's side, per the carve `design.md`'s own specification. No new
  mechanism is designed here. **Measured: openxFactory's half already exists.**
  `scripts/profile_openxfactory.py:101-105` puts
  `serve_openxfactory_lanes.LaneRoutesExtension()` (`:456`) in the
  `ROUTE_EXTENSIONS` tuple that `build_server` reads on every start, and the five
  names are that module's own constants (`ACTIONS_REFRESH_ROUTE` at `:93`). What
  remains is openDox-code's half: 2.1's removal, with every openDox-side reader of
  the five re-exported names moved to the lanes column's own spelling or to a
  neutral one.

  **AMENDED — T007 Batch A (`5817152735`; Ruled R1Q1 (a)):** An addendum. The
  routes still travel through the `RouteBinding` seam. The methods they name
  travel through a handler-contribution facet that openDox declares, which
  D4's "no new mechanism" did not foresee. openxFactory's half gains the
  `LaneRoutes` declaration. A parallel addendum is recorded at `design.md`
  § D4. Carried out by T010, T011, T045.

  **Landed 2026-09-29** (T010, T011, T045): openDox-code#40 → `0f10b1f5`
  declares the handler-contribution facet, openDox-code#46 → `0e88454a` drops
  the reach, and openxFactory#1181 → `f56c87c6` declares `LaneRoutes` in
  openxFactory's profile (T007 batch A's 2.2 addendum, R1Q1 (a)); the
  route-handler tests and openxFactory's `pytest-suite` pass with the five lane
  routes served.
- [x] 2.3 Sweep every remaining module-level reach: grep `src/` for
  `ideation_dashboard`, `corpus_adapter_openxfactory`, `doc_health` and
  `openxdox` at import position, and close or defer each with a recorded reason.

  **Landed 2026-09-27** (T032): openDox-code#49 → `68be484a`. The sweep leaves
  no import-time reach and 19 deferred reaches, all into `openxdox`, each
  recorded closed or deferred with its reason (F4.1's scan: that PR's body;
  `evidence/checkpoint-phase1.md` § 7).
- [x] 2.4 Add a test in openDox-code's own suite that imports EVERY module of the
  package in a checkout with no sibling installed, failing with the name of the
  first module that still needs one.

  **Landed 2026-09-27** (T030, in T011's PR): openDox-code#46 → `0e88454a`.
  `tests/test_imports_standalone.py::test_every_module_imports_with_no_sibling`
  first asserts the four siblings absent, then imports every module, failing
  with the first that still needs one (`evidence/checkpoint-phase1.md` § 1).
- [x] 2.5 Remove `validate.yml`'s three `--noconftest` steps and their enumerated
  file lists; the suite collects whole. Measured at `f8a1eced` by extracting the
  `run:` blocks that invoke pytest: **four blocks name 37 distinct test modules of
  the 63 in the tree** (`tests/` 53 + `tests_runtime/` 10), three of them under
  `--noconftest`; **26 modules are named by no pytest step at all**. This is the
  figure the whole packet uses — an earlier reading of "31 of 53" counted only the
  `--noconftest` blocks over `tests/`. The autouse fixture that produces
  the 1,298 setup errors is `tests/session_fixtures.py:413`, whose body is
  `from opendox import cli as cli_mod`.

  **Landed 2026-09-27** (T036): openDox-code#52 → `55194335`. The three
  `--noconftest` steps and their file lists are gone and the suite collects
  whole (`testpaths` = `tests` and `tests_runtime`); F9.1 exits 0,
  `2468 passed, 11 skipped` (`evidence/checkpoint-phase1.md` § 3). Correction
  (research R16 item 1, non-normative): *"26 modules are named by no pytest step
  at all"* is right for that claim, but the number no CI step reached was
  **22**, because the `runtime` job ran `tests_runtime/` whole (research R4,
  measured at openDox-code `1e4a57fb`, 2026-09-24). T036 removed the file lists,
  so the whole suite now collects.
- [x] 2.6 Correct openDox-code's `README.md:39-42`, which still gives the
  narrowing's reason as *"Until the BUILD arc … inverts the openDox → openXdox
  dependency"*. That dependency IS inverted at import time; the live cause is
  `ideation_dashboard`.

  **Landed 2026-09-27** (T031, in T036's PR): openDox-code#52 → `55194335`.
  `README.md:39-42` now states the live cause of the narrowing,
  `ideation_dashboard`, not the openDox → openXdox inversion.
- [x] **FALSIFIED BY** (a checkout of openDox-code alone, installed WITH every
  extra it declares — `.[runtime,test]` — so that any `ImportError` left is a
  reach into a sibling and not a missing third-party package):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv "$W/v2"
      . "$W/v2/bin/activate"
      pip install ".[runtime,test]"
      for sibling in openxdox ideation_dashboard doc_health corpus_adapter_openxfactory; do
        if python -c "import $sibling" 2>/dev/null; then echo "FAIL: $sibling is importable"; exit 1; fi
      done
      # EVERY module of the package, generated, not a hand-picked three:
      python3 - <<'PY'
      import importlib, pkgutil, sys, opendox
      failed = []
      for m in pkgutil.walk_packages(opendox.__path__, "opendox."):
          try:
              importlib.import_module(m.name)
          except Exception as e:                            # noqa: BLE001 - every failure is a finding here
              failed.append(f"{m.name}: {type(e).__name__}: {e}")
      if failed:
          sys.exit("FAIL: modules that still need a sibling:\n  " + "\n  ".join(failed))
      print("every module of opendox imports with no sibling")
      PY
      # ...and 2.4's own test, by name, so the suite keeps the sweep after the arc:
      python -m pytest -q "tests/test_imports_standalone.py::test_every_module_imports_with_no_sibling"

  **The sweep is generated, not listed.** `pkgutil.walk_packages` visits every
  module the package has: 57 `.py` files under `src/opendox/` at `3c3a9e31`. A
  module added later is covered without editing this command, and a fourth
  module keeping an import-time reach cannot pass beside three that were fixed.
  The absence of each sibling is ASSERTED first. Today the sweep fails on
  `opendox.serve`, `opendox.cli` and `opendox.notebook_action` at least, each with
  `ModuleNotFoundError: No module named 'ideation_dashboard'`.

  **Landed 2026-09-29** (T049, openxFactory#1204 → `9d2e5bc3`): F2.1 exits 0 at
  openDox-code `2d116415`; none of `openxdox`, `ideation_dashboard`,
  `doc_health` or `corpus_adapter_openxfactory` imports, and every module of
  `opendox` does (`evidence/checkpoint-phase1.md` § 1).

## Group 3 — Requirement 3 / G2: a default domain profile (openDox-code)

- [x] 3.0 **RATIFICATION READ FIRST.** Requirement 3 revisits the PREMISE of RULED
  ASK-2 option (2) (`#656` comment `5628886636`) — not its reasoning. An EMPTY
  default stays refused; what changes is the refusal text's premise that *"openDox
  … ships no profile of its own"*. If the ratification read takes ASK-2 to
  foreclose this, requirement 3 is struck and the other **sixteen** stand. See
  `design.md` § D5. **Read at ratification, 2026-09-24** (`5815412869`): the word
  ratifies the packet whole and strikes nothing, so requirement 3 stands and the
  other sixteen with it (`review/ratification-2026-09-24.md` § 2).
- [x] 3.1 Ship a default profile for openDox's OWN domain — documents and ideas —
  carrying none of openxFactory's status taxonomy or change/spec/delta nouns
  (RULING C2, DIRECTION Q5). Note the standalone problem this closes: the only
  host that exists, openxFactory's `scripts/opendox_host.py`, builds a composite
  whose base class is `openxdox.domain_profile.DomainProfile`, so today's only
  real profile needs BOTH siblings present.

  **Landed 2026-09-27** (T015): openDox-code#38 → `a435aecf`. The default
  profile carries none of openxFactory's `Status:` taxonomy or change/spec/delta
  nouns (the vocabulary test) and declares `RuntimeSubcommand` in its
  `SUBCOMMAND_EXTENSIONS` (the second test); it imports under a plain install
  (openDox-code#48 → `796838e8`).
- [x] 3.2 `build_parser()` and `build_server()` fall back to it when no host has
  called `domain_profile.register()`, and a registered profile still replaces it.
  `profile_proxy.py`'s refusal is kept for the case it was written for — an
  ambiguous registration — and is NOT weakened into an empty tuple.

  **AMENDED — T007 Batch A (`5817152735`; Ruled R1Q3 (a), (i), (ii); (ii)'s
  after-build half per RN-1 (a), `5850003126`, #1170):** "fall
  back to it" becomes "register it", because the default is a registration
  the entry point makes. The refusal `profile_proxy.py` keeps is the one it
  was written for, NOTHING REGISTERED (`profile_proxy.py:42-46`). It is not
  "an ambiguous registration": that case is `AlreadyRegistered`. A host
  registration made BEFORE a build replaces the default; RN-1 (a) rules that
  one made AFTER a build is refused instead (`AlreadyRegistered`), landed as
  spec.md's fifth scenario (#1170) — so 3.2 now covers both halves of (ii).
  Carried out by T016.

  **Landed 2026-09-27** (T016): openDox-code#42 → `19370adc`, with batch A's
  amendment (openxFactory#1171 → `bca4a260`) and RN-1 (a)'s after-build scenario
  (openxFactory#1170 → `79a720a2`). `build_parser()`, `build_server()` and
  `main()` register the default where nothing is registered; a host registration
  before a build replaces it and one after a build is refused
  (`AlreadyRegistered`). F3.1 line 2 as amended and
  `tests/test_profile_registration.py` pass
  (`evidence/checkpoint-phase1.md` § 2). Correction (research R16 item 4,
  non-normative): the proxy's refusal was written for NOTHING REGISTERED
  (`profile_proxy.py:42-46`), not for "an ambiguous registration", which is
  `AlreadyRegistered` (R1Q3 (i)); batch A's amendment above carries it.
- [x] 3.3 Leave the carve manifest's `deleted_at_carve` row for
  `scripts/ideation_dashboard/profile_openxfactory.py` BYTE-IDENTICAL:
  openxFactory's profile stays deleted from the core and `scripts/opendox_host.py`
  remains openxFactory's host. The row is `not_moved` and carries no `edits[]`
  entry, so 11.1's guard admits no note on it; an earlier form of this box, which
  asked for the fact to be recorded in the manifest, would have failed that
  guard. The record is this box and requirement 3's own text.

  **Landed 2026-10-05** (T017, read at T018, T065 and T098): the carve
  manifest's `deleted_at_carve` row for
  `scripts/ideation_dashboard/profile_openxfactory.py` stays byte-identical,
  `not_moved` with no `edits[]`, and `scripts/opendox_host.py` remains
  openxFactory's host. F11.1's content check refuses any row change, and each
  phase's interim run prints `requirement 1 holds`, with 0 notes annotated and
  every other path a declared surface: phase 1's amended run at T047's landing
  (T018, openxFactory#1202 → `e81eed62`, `evidence/f11.1-phase1.txt`), phase 2's
  at T064's (T065, openxFactory#1217 → `1f670bc3`, `evidence/f11.1-phase2.txt`)
  and phase 3's at T094's, `36908480` (T098, openxFactory#1237 → `20ce593e`,
  `evidence/f11.1-phase3.txt`). Phases 1 and 3 also record T017's check of the
  row itself. Phase 3's compares it at the manifest's introducing commit
  `17167481` and at that tip, raw text and parsed, equal both ways, and at
  `main` `20ce593e` it reads the same.
- [x] **FALSIFIED BY** (openDox-code checkout, no sibling):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v3"                       # a FRESH environment: nothing already installed stands in
      . "$W/v3/bin/activate"
      pip install ".[test]"
      python -c "from opendox.cli import build_parser; build_parser(); print('OK')"
      python -c "from opendox import domain_profile as d; print('OK', d.name_of(d.current()))"
      python -m pytest -q tests/test_profile_registration.py   # a REGISTERED profile still replaces the default

  Both lines print `OK`, the second with the default profile's name. Today both
  raise `domain_profile.ProfileNotRegistered` (`domain_profile.py:220`). The
  second line asks `domain_profile.current()`, the call every consumer of the
  profile makes. An earlier draft called `build_server()` with no arguments, but
  it takes three required positional ones (`web_dir`, `snapshot_path`,
  `checkout_root`), so that line would have failed with a `TypeError` whatever
  the profile did.

  **AMENDED — T007 Batch A (`5817152735`; Ruled R1Q3 (a)):** F3.1's line 2 is
  amended. The line asks after `build_parser()`: `python -c "from opendox.cli
  import build_parser; from opendox import domain_profile as d;
  build_parser(); print('OK', d.name_of(d.current()))"`. The prose under it
  adds that a bare process that builds nothing still meets
  `ProfileNotRegistered`, which `tests/test_profile_registration.py` asserts.
  Carried out by T016, T049.

  **Landed 2026-09-29** (T049, openxFactory#1204 → `9d2e5bc3`): F3.1, with line
  2 as amended by batch A, exits 0 at openDox-code `2d116415`: `build_parser()`
  builds on the default profile and `domain_profile.current()` names it
  (`evidence/checkpoint-phase1.md` § 2).

## Group 4 — Requirement 5 / G4: the deferred reach resolves through the seam (openDox-code)

- [x] 4.1 Replace `src/opendox/authoring.py:318`'s
  `from corpus_adapter_openxfactory import home_corpus` with a resolution of the
  REGISTERED home corpus through openDox's own `corpus_adapter` seam. The
  registration point is declared here, beside `domain_profile.register()`:
  `corpus_adapter.register_home(factory)`, where `factory` has `home_corpus`'s
  own shape (`adapter, ref = factory(root)`, as `authoring.py:324` calls it), and
  `corpus_adapter.home()` returns what was registered. openxFactory's host
  registers `corpus_adapter_openxfactory.home_corpus` at start, as it registers
  its profile.

  **Landed 2026-09-29** (T020, T021, T046): openDox-code#37 → `e295b1a9`
  declares `register_home(factory)` and `home()`, openDox-code#44 → `9d13bd16`
  routes `authoring.py:318` through `corpus_adapter.home()`, and
  openxFactory#1181 → `f56c87c6` registers
  `corpus_adapter_openxfactory.home_corpus` in the host. F4.1's first block
  (exactly one outcome, `CorpusRefused` of kind `ADAPTER_NOT_REGISTERED`) and
  the named registered-adapter test pass.
- [x] 4.1a **openDox's OWN default corpus adapter, registered at startup**
  (RULED `5800995035`, answer 1). Where no host has called `register_home`,
  `build_parser()` and `build_server()` register a factory of `home_corpus`'s
  shape over the conformant implementation openDox already ships,
  `LocalGitCorpus` (`src/opendox/runtime/local_git_adapter.py`, RULING C3's plain
  local git repository), exactly as Group 3's default profile stands in for an
  unregistered host, and a host that registers its own replaces it. A process in
  which no entry point was built and nothing registered anything — an import, a
  test, a library caller — still refuses with 4.2's `ADAPTER_NOT_REGISTERED`, so
  the default is a registration the entry point makes and never a fallback
  inside the seam.

  **Landed 2026-09-27** (T022): openDox-code#45 → `255514df`. The entry points
  register a `home_corpus`-shaped factory over `LocalGitCorpus` where no host
  has; a bare process still refuses with `ADAPTER_NOT_REGISTERED`; the named
  test passes.
- [x] 4.2 Where nothing is registered, `corpus_adapter.home()` raises the
  interface's ONE exception, `CorpusRefused` (`corpus_adapter.py:164`), with a
  NEW refusal kind, `ADAPTER_NOT_REGISTERED`, added to `REFUSAL_KINDS` (`:135`).
  Its `subject` names the seam (`opendox.corpus_adapter`) and its `detail` names
  the remedy (`corpus_adapter.register_home(...)`). It is never a
  `ModuleNotFoundError` raised from inside a function, and never any other
  exception.

  **Landed 2026-09-26** (T020): openDox-code#37 → `e295b1a9`. With nothing
  registered `corpus_adapter.home()` raises `CorpusRefused` of the new kind
  `ADAPTER_NOT_REGISTERED` (subject `opendox.corpus_adapter`, detail naming
  `register_home(...)`), never a `ModuleNotFoundError` (the seam tests; F4.1's
  first block).
- [x] 4.3 **Route EVERY deferred reach through a seam the product declares. None
  stays late-bound by name.** Requirement 5 admits no exception for a reach
  "owed to the consumer": a reach that names a consumer or publisher package by
  module name is exactly what keeps the product from standing alone. Measured at
  openDox-code `1e4a57fb` by the scan below, there are **27** deferred reaches.
  **19** go into openXdox, and they are the ratchet's (`branch_session.py` 7,
  `serve_workbench.py` 7, `serve.py` 2, `serve_project.py` 2, `cli.py` 1). **8**
  go into openxFactory, and no ratchet counts them: `authoring.py:318` (4.1);
  `doc_health` at `workbench.py:746` and `:1407-1409`, and at `serve.py:713`;
  and `ideation_dashboard` at `doxbench_packet.py:177` and `serve_wire.py:1369`.
  Each resolves through an existing seam (the `corpus_adapter` Protocol, the
  domain-profile registry, the route and subcommand extension points) or through
  one declared for it, as 5.4 declares the generator's. None of the twenty-seven
  reaches the submission surface. Their targets are the home corpus,
  `doc_health`, two `ideation_dashboard` names, and openXdox's generator,
  snapshot registry, cross-reference register, kickoff, corpus root, gate console
  and routes, and doxBench scope, so none waits on Group 12's bindings, which are
  release 2's. With nothing registered, a verb refuses naming its seam and its
  remedy, which is 4.2's discipline. `workbench.py`'s four are the reaches
  `run_scoped_doc_health` makes (6.2). Once routed here, they refuse until Group
  6 registers openDox's own check. `consumer_reach.py` is the late stand-in whose
  own text calls this injection BUILD-arc work, and it is retired with its last
  name. openXdox-code's ratchet (`OPENDOX_BACK_IMPORTS`) is tightened to `(0, 0)`
  in the same landing. The import-time column is already `0` for the consumer,
  and the two import-time reaches into the publisher (`serve.py:199`, `:206`) are
  Group 2's. **Phase placement (the release map above):** the eight reaches into
  openxFactory are phase 1's reach-back cut; the nineteen into openXdox are
  routed within release 1, each no later than the phase whose surface calls it,
  and this box closes with the last of them.

  **AMENDED — T007 Batch A (`5817152735`; Ruled R1Q9 (a)):** Of `workbench.py`'s
  four reaches, only three (`:1407-1409`) are the ones `run_scoped_doc_health`
  makes. The fourth, `session_documents` (`:746`), resolves through the
  registered adapter's `list_documents` in phase 1, and the hosted membership
  rule is unchanged. Carried out by T025, T026, T046.

  **AMENDED — T007 Batch G (`5850003126`; Ruled R1Q10 (a)):** An addendum.
  Every consumer mechanism on release 1's path gets an openDox-owned neutral
  default, which the entry points register where no host has, in R1Q3 (a)'s
  pattern (`5817152735`), the one 4.1a already sets for the home corpus.
  openXdox contributes its governed one through the same seam, in R-G3's
  pattern. The mechanisms are the ones that the nineteen reaches into
  openXdox and `consumer_reach.py`'s names reach, as R1Q10 measures them
  (`specs/034-opendox-standalone-operation/clarify-questions.md`), among them
  the snapshot registry, the generator (5.4's seam), the doxBench scope and
  the gate primitives behind chat's Save. For the two reaches into
  openxFactory's `ideation_dashboard`, the doxBench contracts at
  `serve_wire.py:1369` and the status-exemption rail at
  `doxbench_packet.py:177`, openDox's default validators run over its spec
  leg's two chat schemas, `xfactory-workbench-chat-turn` and
  `xfactory-workbench-model-catalog`, and there is no status exemption by
  default. The three reaches `run_scoped_doc_health` makes (T007 Batch A)
  keep this box's own rule above: they refuse until Group 6 registers
  openDox's own check. A bare process still refuses, naming the seam (4.2),
  because a default is a registration an entry point makes and never a
  fallback inside the seam. Carried out by T052, T055, T059, T084, T085 and
  T086.

  **AMENDED — T007 Batch L (`5920216845`, item 1):** An addendum, on what the
  served `/capabilities` payload claims. Measured at openDox-code `main`
  `047bb4fa`, over a standalone serve of the plain fixture, the payload's
  `actions` map answers `gate` and `refresh` true, while every
  `POST /actions/gate/<verb>` and `POST /actions/refresh` answers
  `404 unknown_action`. The gate flag follows the checkout's git identity
  alone (`compute_capabilities`, `serve.py:464`, called at `:1957`), and the
  route bindings the assembly collected (`:1900`) are never passed to it.
  A flag in that `actions` map whose affordance is a route this server
  serves IS TO be true only where such a route answers it. `gate` and
  `refresh` govern routes a host contributes through the route bindings
  (`/actions/gate/<verb>` and `/actions/refresh`), so each is true only when
  the assembled bindings carry a route it governs. Standalone, with no host
  contributing them, both read false, and a composed host that contributes
  them reads exactly as today. `notebook`, `edit` and `session` govern core
  routes and keep their conditions. `intent` governs a POST to another
  plane's intent API, a route that plane answers and this server does not
  serve, so its condition, the served plane, stands. The
  workbench's session controls read `actions.gate`
  (`sessionActionsLive`, `web/views/staging-workbench-model.js:1068`), so a
  false `gate` standalone also hides session controls that no route
  answers. That is the half of the fix a user sees. The same measurement
  found three of this box's nineteen reaches into openXdox ending a request
  with a dropped connection, because nothing contributes the names they
  import: `serve_workbench.py:1219` and `:2611`, and `serve_project.py:271`,
  at `047bb4fa`. Each of the three IS TO answer through its seam, from
  openDox's default where one serves the request (batch G's addendum
  above), or else with a structured refusal that names the seam. That is
  4.2's discipline: never a dropped connection, and never a
  `ModuleNotFoundError` raised from inside a function. The realization's
  named test carries the check both ways, over a standalone server and over
  a composed host whose other conditions hold. It asserts that `gate` and
  `refresh` read false standalone and true on the composed host, and that
  each follows its own routes: a host that contributes only one of the two
  sets only its flag. Then, on
  each, it asserts that for every `actions` key that reads true, a route it
  governs does not answer `unknown_action`. So a plane that switched every
  flag off would fail it. This bookkeeping amendment does not itself touch
  the Python below. Carried out by T084.

  **Landed 2026-10-05** (T012, T021, T025, T026, T027, T046, T055, T084, T085,
  then T086): the eight reaches into openxFactory closed in phase 1
  (openDox-code#47 → `27683028`, openDox-code#44 → `9d13bd16`, openDox-code#43 →
  `c46430fb`, openDox-code#39 → `582ed073`, openDox-code#41 → `8017cd52`, with
  the host half openxFactory#1181 → `f56c87c6`); the nineteen into openXdox
  resolve through openDox's seams (openDox-code#59 → `fa140875` with its
  follow-up openDox-code#70 → `75bd8703`, openDox-code#71 → `2680eb5e`, whose
  falsifier T081's openDox-code#74 → `9a490405` completed, and openDox-code#77 →
  `e49b17c3`, which retires `consumer_reach.py`); and T086 (openXdox-code#37 →
  `56e1c238`), the consumer half, contributes openXdox's governed columns at
  those seams and empties `OPENDOX_BACK_IMPORTS` to `(0, 0)` in the same landing
  that moves its pin to openDox-code `dede32b4`, the commit T087 pins. At that
  pin `tests/test_dependency_direction.py` reads `17 passed`, with an empty
  census (openXdox-code#37's body). F4.1 whole is T089's run at phase 3's tip.
  Correction (research R16 item 3, non-normative): of `workbench.py`'s four
  reaches into openxFactory, `run_scoped_doc_health` makes three (`:1407-1409`),
  and the fourth is `session_documents` at `:746` (research R5, R1Q9 (a)). T007
  batch A (openxFactory#1171 → `bca4a260`) carries the amendment above.
  `session_documents` resolves through the registered adapter's `list_documents`
  (T025, openDox-code#43 → `c46430fb`), and the three through the health-check
  seam (T026, openDox-code#39 → `582ed073`).
- [x] **FALSIFIED BY** (openDox-code checkout, no sibling, no
  `corpus_adapter_openxfactory` importable):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v4"                       # a FRESH environment: nothing already installed stands in
      . "$W/v4/bin/activate"
      pip install ".[test]"
      if python -c "import corpus_adapter_openxfactory" 2>/dev/null; then echo "FAIL: the publisher's adapter is importable"; exit 1; fi
      python3 - <<'PY'
      import opendox.authoring as a
      from opendox import corpus_adapter as ca
      try:                                                  # NOTHING is registered in this process (4.2)
          got = a.required_header_fields()
      except ModuleNotFoundError as e:
          raise SystemExit(f"FAIL: the deferred reach still imports a publisher module: {e}")
      except ca.CorpusRefused as e:                         # the interface's ONE exception, and nothing else
          r = e.refusal
          assert r.kind == ca.ADAPTER_NOT_REGISTERED, f"refused for another reason: {r.kind!r}"
          assert "corpus_adapter" in r.subject, f"the refusal does not name the seam: {r.subject!r}"
          assert "register_home" in r.detail, f"the refusal does not name the remedy: {r.detail!r}"
      else:
          raise SystemExit(f"FAIL: nothing is registered, yet the verb answered {got!r}")
      PY
      # ...a REGISTERED adapter answers through the seam, not through a name (4.1):
      python -m pytest -q "tests/test_authoring_seam.py::test_required_header_fields_come_from_the_registered_adapter"
      # ...and an ENTRY POINT registers openDox's own LocalGitCorpus where no host has (4.1a):
      python -m pytest -q "tests/test_authoring_seam.py::test_an_entry_point_registers_the_local_git_corpus_when_no_host_has"
      # ...and NO deferred reach anywhere in the package names the consumer or the publisher (4.3):
      if [ -e src/opendox/consumer_reach.py ]; then echo "FAIL: the late stand-in consumer_reach.py survives"; exit 1; fi
      python3 - src/opendox <<'PY'
      import ast, pathlib, sys
      FOREIGN = ("openxdox", "ideation_dashboard", "corpus_adapter_openxfactory", "doc_health")
      def named(node):
          if isinstance(node, ast.Import):
              return [a.name for a in node.names]
          if isinstance(node, ast.ImportFrom):
              return [node.module] if node.level == 0 and node.module else []
          if isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) \
                  and getattr(node.func, "attr", getattr(node.func, "id", "")) in ("import_module", "__import__"):
              return [node.args[0].value] if isinstance(node.args[0].value, str) else []
          return []
      def deferred(tree):                                   # every reach written INSIDE a function body
          for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))):
              for node in ast.walk(fn):
                  yield from ((node.lineno, name) for name in named(node))
      hits = sorted({f"{p}:{line}: {name}"
                     for p in pathlib.Path(sys.argv[1]).rglob("*.py")
                     for line, name in deferred(ast.parse(p.read_text(), str(p)))
                     if any(name == f or name.startswith(f + ".") for f in FOREIGN)})
      assert not hits, f"{len(hits)} deferred reach(es) still name the consumer or the publisher:\n  " + "\n  ".join(hits)
      print("no deferred reach names the consumer or the publisher")
      PY

  **With nothing registered, the block accepts exactly ONE outcome**:
  `CorpusRefused` of kind `ADAPTER_NOT_REGISTERED`, naming the seam and the
  remedy. Any other exception fails it, an unrelated `TypeError` included, and so
  does an answer. The named test then registers a stand-in adapter and requires
  the fields to be the ones that adapter declares, so the answer is proved to
  come through the registry and not through a name. The second named test
  builds the parser with no host registered and requires the home corpus to be
  openDox's own `LocalGitCorpus`, so 4.1a's default is a registration an entry
  point makes. **The scan reads the whole
  package**, not the ratchet's five modules. It is a static reading of every
  import and every `import_module`/`__import__` call with a literal name, written
  inside a function body, and it needs no sibling installed to find one. Run
  against `1e4a57fb` before this box was written, it names the 27 reaches above
  and exits non-zero. Retiring `consumer_reach.py` closes the one dynamic path the
  scan cannot read, a name held in a variable. Today `required_header_fields()`
  raises `ModuleNotFoundError: No module named 'corpus_adapter_openxfactory'`
  while `python -c "import opendox.authoring"` exits 0.

  **Landed 2026-10-05** (T089): openxFactory#1238 → `fab575ad`. F4.1, extracted
  byte for byte from #1144 and run unchanged in a fresh worktree of openDox-code
  at `dede32b4`, T087's pin, exits 0: its two named tests read `1 passed` each,
  `consumer_reach.py` is absent, and the scan prints
  `no deferred reach names the consumer or the publisher`
  (`evidence/checkpoint-phase3.md` § 1).

## Group 5 — Requirement 4 / G3: openDox's own neutral projection (RULED, openDox-code)

**RULED: openDox gets its OWN neutral generator. `generator.py` does not move.**
The audit this box used to open with is spent — it would have priced a relocation
nobody is doing — and its decisive finding is recorded instead: `generator.py`
imports `doc_health` at `:66-68`, so relocating it was never lawful under
`corpus-adapter-seam` whatever its literals said.

- [x] 5.0 **Ship `tests/fixtures/plain-documents`** — first needed here, and
  Groups 7 and 13 read it too: a handful of `.md` documents spread across the six
  neutral stages, carrying NONE of openxFactory's governance vocabulary, which is
  what lets the assertion below mean something. That vocabulary is DECLARED data,
  not a hand-picked sample. It is the eight document-lifecycle `Status:` words
  (`brainstorm`, `staged`, `draft`, `ratified`, `standard`, `superseded`,
  `retired`, `record`) and the change/spec/delta nouns (`openspec`,
  `proposal.md`, `tasks.md`, `design.md`, `ADDED Requirements`, `MODIFIED
  Requirements`). A test keeps the fixture free of all of them.

  **Landed 2026-09-29** (T050): openDox-code#53 → `dc3765dd`.
  `tests/fixtures/plain-documents` spreads documents across the six neutral
  stages and carries none of the declared vocabulary; the vocabulary test keeps
  it so (F5.3 reads it: `documents: 8`, `evidence/checkpoint-phase2.md` § 3).
- [x] 5.1 Write openDox's SMALL NEUTRAL PROJECTION over the `CorpusAdapter`
  protocol already declared at `src/opendox/corpus_adapter.py` (a
  `@runtime_checkable` `Protocol`, six closed members: `resolve`,
  `list_documents`, `read`, `classify`, `check`, `write_back`). New neutral code
  written to openDox's needs — NOT 3,164 lines re-expressed, and NOT a copy of
  openXdox's.

  **Landed 2026-09-30** (T053, T054, T056): the neutral snapshot contract
  (openDox-spec#16 → `f7ee3c76`; root pin and `dox-v1.1` bundle openDox#14 →
  `52005213`, changelog openDox#15 → `66758438`), openDox's small projection
  (openDox-code#57 → `a691e4e4`) and the standalone generate path end to end
  (openDox-code#66 → `a23e4224`). F5.3 exits 0 with neither sibling importable
  (`evidence/checkpoint-phase2.md` § 3).
- [x] 5.2 Bind `src/opendox/runtime/local_git_adapter.py` (2,796 lines, RULING
  C3's plain local git repository) as the conformant implementation, so the
  projection has a real corpus to read with nothing else installed.

  **Landed 2026-09-30** (T054): openDox-code#57 → `a691e4e4`. The projection is
  bound to `LocalGitCorpus` and reads a fresh `git init` of the fixture with
  neither `openxdox` nor `doc_health` importable (F5.3,
  `evidence/checkpoint-phase2.md` § 3).
- [x] 5.3 Render `NEUTRAL_DISPLAY`'s SIX WORDS and no others — `sources`,
  `groups`, `candidates`, `selections`, `submissions`, `completed` (RULED
  *"keep those six words"*, same comment; the sixth is **`completed`** by RULING
  `5784654370`, *"2, keep completed"*, which corrected this packet's earlier
  `completions` — the DECLARED value in `display_profile.py`, not the docstring
  that narrated it). **No word is re-authored and no workflow is designed.**
  `src/opendox/display_profile.py` is unchanged by this group.

  **AMENDED — T007 Batch G (`5850003126`; Ruled R1Q11 (a)):** The closing
  sentence above, *"`src/opendox/display_profile.py` is unchanged by this
  group"*, is amended. `display_profile.py` changes in ONE place, where
  `SNAPSHOT_VALUES`' defaults become the neutral snapshot's values.
  openDox's own generator writes the neutral snapshot kind that T053 adds,
  whose stage values are the six role keys (7.1 as this batch amends it), so
  the defaults move with it and the product's own views match its own
  snapshot. No word is re-authored and no workflow is designed: the six
  words above stand. The governed values move to openXdox's facet, in the
  `values` block that 5.3a's addendum admits (T007 Batch I, `5851950767`;
  R1Q26 (a)), which R1Q11 (a) also implies. Carried out by T054.

  **Landed 2026-09-30** (T054): openDox-code#57 → `a691e4e4`. The projection
  renders the six words only; `display_profile.py` changes in the one place
  batch G names (`SNAPSHOT_VALUES`' defaults become the neutral snapshot's
  values); F5.3's vocabulary assertion finds no leak
  (`evidence/checkpoint-phase2.md` § 3).
- [x] 5.3a **openXdox declares the estate's FIRST `DISPLAY` facet — partial, one
  stage** (openXdox-code; RULED `5784683830`, *"1, keep completed and overlay
  implemented"*): the `completion` stage labelled **"implemented"**, the
  governed lifecycle's own word, in its `short` AND its `label` field (measured:
  a facet giving `short` alone leaves `label` at `completed`), and NOTHING ELSE —
  openDox fills every other role and field from `NEUTRAL_DISPLAY`. The neutral
  word does not move. **It LANDED before the arc, and not where this box first
  put it.** openXdox-code#26 → `195276b7` (2026-09-23T01:03:07Z) declares it as a
  MODULE VALUE, `src/openxdox/view_extensions.py`'s `DISPLAY`, and NOT on
  `src/openxdox/domain_profile.py`'s `DomainProfile`. openxFactory's composite
  host (`scripts/opendox_host.py`) forwards a facet only when attribute lookup
  fails, and its `build_profile()` refuses a facet named like a profile field,
  so a `DISPLAY` on the dataclass would never be forwarded and would stop that
  composite being built. The falsifier below reads the facet where it landed.
  Being earlier than the arc, the landing carries no 11.0 trailer; the box
  closes when the falsifier is run against the realized openDox. It reaches a
  served page since openxFactory#1146 → `d52b4199`, which composes it into this
  repository's profile facet. **A later ruling widened the same entry**: RULED
  `5801057769` (2026-09-23, *"yes, overlay implemented items too"*), and
  openXdox-code#27 → `626f2c8d` adds its item nouns, `one` and `many`
  ("implemented item", "implemented items"), served since openxFactory#1148 →
  `f1c690b8` (F3). The facet now words four fields of that one entry and still no
  other stage, which is what the falsifier below asserts.

  **Landed 2026-09-30** (T060): openXdox-code#34 → `c41063d6`. openXdox's
  `DISPLAY` facet carries the governed snapshot values in its `values` block
  beside its one stage (batch I); `tests/test_gate_loop_views.py` is green with
  the one reviewed edit T060 made, entered in the allow-list it created,
  `tests/protected_suite_respellings.yaml` (T059 made the second); F5.1 passes
  (`evidence/checkpoint-phase2.md` § 1).
- [x] **FALSIFIED BY** (openXdox-code checkout with openDox installed):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      : "${OPENDOX_CODE:?set OPENDOX_CODE to an openDox-code checkout at the tip of the arc}"
      python -m venv --clear "$W/v5a"
      . "$W/v5a/bin/activate"
      pip install ".[test]"
      pip install --force-reinstall --no-deps "$OPENDOX_CODE"   # the REALIZED openDox wins over any pinned one
      python3 - <<'PY'
      from opendox.display_profile import STAGE_ROLES, normalize_display
      from openxdox.view_extensions import DISPLAY as facet  # a MODULE value (#26), never a DomainProfile field
      assert facet, "openXdox declares no DISPLAY facet"
      merged, neutral = normalize_display(facet), normalize_display(None)
      done = merged["stages"]["completion"]
      assert done["short"] == "implemented" and done["label"] == "implemented", done
      assert neutral["stages"]["completion"]["short"] == "completed"   # the neutral word stands
      for role in (r for r in STAGE_ROLES if r != "completion"):
          assert merged["stages"][role] == neutral["stages"][role], f"{role} was overlaid too"
      PY

  Three things, each an assertion: the facet names the stage "implemented" in
  both of its rendered names; a host with no facet — and a standalone install —
  sees "completed"; and the facet is PARTIAL, the other five stages
  byte-identical to the neutral ones, so an overlay cannot quietly grow into a
  second vocabulary. Run as written against openXdox-code `195276b7` with
  openDox-code `1e4a57fb` installed over it, it passes, and it passes against
  `626f2c8d` as well. The earlier form, which
  read `host_display(DomainProfile)`, answers `None` against the same trees.

  **AMENDED — T007 Batch I (`5851950767`; Ruled R1Q26 (a), with R1Q11 (a),
  `5850003126`):** openXdox's facet also carries a `values` block beside its
  one stage, holding the governed snapshot's values, because 5.3's defaults
  become the neutral snapshot's values (T007 Batch G). `display_profile.py`
  already lets a host override those values, so no openDox code changes for
  the block. The facet stays partial in its stages, and the falsifier above
  reads only the stages, so it is unchanged. The two tests of
  `tests/test_gate_loop_views.py` that pin the facet as it was are edited
  under 12.5's falsifier as this batch amends it. openxFactory composes the
  block into its own profile, in a non-arc act that holds at both pins.
  Carried out by T060, T059 and T066.

  **Landed 2026-09-30** (T060, openXdox-code#34 → `c41063d6`; run again at T063,
  openxFactory#1218 → `a883bbf6`): F5.1 exits 0 against the realized openDox:
  the facet words the completion stage `implemented` in both its names, the
  other five stages stay byte-identical to the neutral ones, and a host with no
  facet reads `completed` (`evidence/checkpoint-phase2.md` § 1).
- [x] 5.4 **DECLARE THE GENERATOR SEAM — it does not exist and `CorpusAdapter` is
  not it.** `src/opendox/corpus_adapter.py`'s Protocol is CLOSED at six members
  (`resolve`, `list_documents`, `read`, `classify`, `check`, `write_back`) and its
  own docstring says *"Six methods. Nothing else, ever"* — none of them is a
  generator handoff, so "contribute it through the same seam" would name nothing
  and let two incompatible implementations both claim conformance. This box
  declares the seam: the operation handed over, the registration point (beside
  `domain_profile.register()`, which is the shape the product already uses), and
  the conformance a contributed generator must satisfy. `consumer_reach.py` says
  the corresponding injection *"does not exist yet and is BUILD-arc work"* — this
  is that work.

  **Landed 2026-09-29** (T052): openDox-code#54 → `fa8862cc`. The generator seam
  is declared (the operation handed over, the registration point beside
  `domain_profile.register()`, the conformance a contribution must meet);
  `CorpusAdapter` stays closed at six members; the entry points register
  openDox's own generator where no host has.
- [x] 5.4a openXdox KEEPS `generator.py`, `snapshot.py`, `snapshot_registry.py`,
  `completeness.py` and `corpus_root.py`, and contributes its governed generator
  through the seam 5.4 declares. The publisher's corpus is projected exactly as
  today and the consumer loses no capability — requirement 4's third scenario is
  the check.

  **Landed 2026-09-30** (T059): openXdox-code#35 → `839492d9`. openXdox keeps
  `generator.py`, `snapshot.py`, `snapshot_registry.py`, `completeness.py` and
  `corpus_root.py` and contributes them through
  `openxdox.projection_contributions.register()`; its generator suites run in
  F5.2's environment (openxFactory composed at a named commit). As landed, that
  run deselects the consumer-schema cases (the seven reds at both pins, and
  `tests/test_snapshot.py`'s two) and the three pre-arc reds of
  `tests/test_session_snapshot.py`, as T059's record and that PR's body (its
  rulings 4 and 6) state, so F5.2 whole is T086's and T089's (T063 quotes it red
  on those three, `evidence/checkpoint-phase2.md` § 2). The arc's
  protected-suite edits are entered in the reviewed allow-list. Host line:
  openxFactory#1215 → `fcb45380`.
- [x] **FALSIFIED BY** (5.4a; an openXdox-code checkout with the realized openDox
  installed and Group 9 landed): the governed projection's own suites pass, and the
  arc did not edit them.

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      : "${OPENDOX_CODE:?set OPENDOX_CODE to an openDox-code checkout at the tip of the arc}"
      python -m venv --clear "$W/v5b"
      . "$W/v5b/bin/activate"
      pip install ".[test]"
      pip install --force-reinstall --no-deps "$OPENDOX_CODE"   # the REALIZED openDox wins over any pinned one
      ls tests/test_generator.py tests/test_snapshot*.py tests/test_session_snapshot.py > "$W/gen-suites.txt"
      while read -r f; do python -m pytest -q "$f"; done < "$W/gen-suites.txt"
      : "${ARC_BASE:?set ARC_BASE to the commit of this repository before the first landing of the arc here}"
      git log --first-parent --format=%H --grep='^Arc: neutral-product-standalone-operability$' "$ARC_BASE..HEAD" > "$W/x-arc.txt"   # LANDINGS (11.0)
      test -s "$W/x-arc.txt"                                # 11.0: the arc DID land here (9.2 at least), so empty means a dropped trailer
      : > "$W/x-paths.txt"
      while read -r c; do                                   # each landing against main before it
        git diff --name-only "$c^1" "$c" >> "$W/x-paths.txt"
      done < "$W/x-arc.txt"
      python3 - "$W/x-paths.txt" "$W/gen-suites.txt" <<'PY'
      import sys
      touched = {l.strip() for l in open(sys.argv[1]) if l.strip()}
      suites = {l.strip() for l in open(sys.argv[2]) if l.strip()}
      edited = sorted(touched & suites)
      if edited:
          sys.exit("FAIL: the arc edited the governed projection's own proofs: " + ", ".join(edited))
      PY

  Requirement 4's third scenario says the consumer loses no capability, and these
  are the suites that already pin the governed snapshot, including its
  determinism. Six exist at `ab04453d`: `test_generator.py`, `test_snapshot.py`,
  `test_snapshot_determinism.py`, `test_snapshot_registry.py`,
  `test_snapshot_validation_launch.py` and `test_session_snapshot.py`. The set is
  taken by glob rather than typed out, and a suite the arc rewrote would prove
  nothing, so edits to them are refused through 11.0's trailer.

  **AMENDED — T007 Batch C (`5817152735`; Ruled R1Q7 (a)):** F5.2 and 12.5's
  falsifier both take this amendment. The "unedited by the arc" check IS TO
  SUBTRACT the edits entered in a reviewed allow-list in openXdox-code, such
  as `tests/protected_suite_respellings.yaml` — a file this amendment does
  not itself create. T019 already gives the file its owner
  (`specs/034-opendox-standalone-operation/tasks.md`, T019's re-plan
  bullets, verbatim): *"the first task that makes an admitted edit to a
  protected suite creates the file in its own PR. An entry names its
  landing by that PR's number, since the landing's commit is not known
  inside it."* This amendment does not name that task itself — WHICHEVER
  task turns out to be first, per T019's own rule, creates the file; that
  ownership question belongs to T019's re-plan, not to this bookkeeping
  amendment. Each entry names the suite, the landing, the reference it
  respelled, its review, AND the exact old/new text (or a diff/content
  digest) of the respelling; no edit that weakens an assertion is entered,
  and the PR that adds an entry is reviewed on exactly that basis. Because
  the check subtracts by PATH, not by line, a landing that respells the
  named reference while ALSO weakening a different assertion in the same
  suite would otherwise pass unnoticed: T059/T086 must validate, before
  trusting any subtraction, that the landing's actual diff for that path
  contains ONLY the entry's recorded text; a path whose landing diff does
  not match stays refused, exactly like an unentered edit. This bookkeeping
  amendment does NOT itself touch the Python above: `edited = touched &
  suites` still computes and refuses on every
  intersection exactly as written, with no allow-list read, until the file
  exists (T019's rule names its owner) and T059/T086 wire the subtraction
  into both falsifiers' checks. Carried out by whichever task T019 names as
  the file's first owner, plus T059, T086.

  **AMENDED — T007 Batch F (`5850003126`; Ruled R1Q14 (a)):** The reviewed
  allow-list that R1Q7 (a) admits for this falsifier (`5817152735`; T007
  Batch C) also admits the two edits F7.1 requires. Each is entered with its
  reason, and neither as a respelling: the added
  `tests/test_snapshot.py::test_the_validator_is_the_installed_consumers_own`,
  and the revised
  `tests/test_snapshot_validator_home.py::test_a_start_outside_the_product_is_refused_not_walked`,
  whose expected answer 7.3 now governs. The second file is a suite the glob
  above selects: lane 4's C3 added it (openXdox-code#28, `e28930bf`), so the
  glob selects seven suites there. This bookkeeping amendment does not itself
  touch the Python above. Carried out by T061 and T063.

  **AMENDED — T007 Batch G (`5850003126`; Ruled R1Q23 (a)):** F5.2's
  environment line is amended. Its environment also composes openxFactory at
  a NAMED commit: after the two installs, the block IS TO require
  `OPENXFACTORY`, an openxFactory checkout, put `"$OPENXFACTORY/scripts"` on
  `PYTHONPATH`, and quote that checkout's commit. `doc_health` lives in that
  directory. Four of the suites the glob selects (`test_generator.py`,
  `test_snapshot_determinism.py`, `test_snapshot_registry.py` and
  `test_session_snapshot.py`) fail on `doc_health`, which openXdox's
  `generator.py` and `snapshot_registry.py` import at module level (R1Q23's
  measurement), and R1Q6 (d) (`5817152735`) leaves that reach to the
  direction arc (T008). Composed this way, they can run where this falsifier
  runs them. It is the declared-composition pattern of requirement 9's second
  scenario, and the setting requirement 4's third scenario names. Nothing
  else in the block changes by this amendment: the glob and the loop over
  the suites stand as written, and the arc-landing check stands as T007
  Batches C and F amend it. This bookkeeping amendment does not itself touch
  the command above: the runs that use F5.2's environment (T059, T061 and
  T063) use this one and quote the commit. Carried out by T059, T061 and
  T063.

  **AMENDED — T007 Batch K (`5916000030`, item 4; entries under R1Q7 (a),
  `5817152735`):** The reviewed allow-list that R1Q7 (a) admits for this
  falsifier (`5817152735`; T007 Batch C, extended by T007 Batch F) also
  admits ten more edits, all of them T061's (openXdox-code#36). Each is
  entered as its own reviewed entry with its reason, and none as a
  respelling. Each keeps its test's real assertions and changes only the
  premise that a validator is found by walking up from a start, which 7.3
  removes: the test plants its stub as the distribution's own validator,
  or, where it needs none, the distribution carries no validator of its
  own. Nine are in
  `tests/test_snapshot_validation_launch.py`:
  `test_the_default_shaped_launch_validates_from_the_repo_root`,
  `test_a_run_dir_beside_a_checkout_still_uses_that_one_first`,
  `test_when_neither_root_reaches_a_validator_the_message_names_both`,
  `test_missing_validator_dependencies_warn_and_the_server_still_starts`,
  `test_the_dependency_warning_carries_the_pip_remedy_and_clears_the_corpus`,
  `test_a_non_conformant_snapshot_still_blocks_and_blames_the_snapshot`,
  `test_strict_makes_an_unrunnable_validator_fatal`,
  `test_strict_is_fatal_when_no_validator_is_reachable_either` and
  `test_the_classifier_reads_the_exit_code_not_the_dependency_sentence`. The
  tenth is
  `tests/test_snapshot.py::test_a_missing_validator_is_unavailable_not_a_verdict`,
  whose call and `search_from` are unchanged. One of the ten changes its
  expected answer: in
  `test_a_run_dir_beside_a_checkout_still_uses_that_one_first`, the
  validator of another tree beside the run dir is never adopted, and the
  distribution's own validates, as 7.3 answers. Its name is kept, because
  an entry admits an edit inside one named test, and a rename is not that.

  T061 is ONE landing, which edits `tests/test_snapshot.py` twice (Batch
  F's added test and the tenth case) and
  `tests/test_snapshot_validation_launch.py` nine times. Batch C's check
  requires that *"the landing's actual diff for that path contains ONLY the
  entry's recorded text"*, which reads as one entry per suite per landing,
  and T059's check (openXdox-code#35, `scripts/protected_suites.py`) holds
  that rule in so many words. For this falsifier, this batch reads Batch
  C's sentence as the recorded texts of several entries together. Several
  entries, applied in the order they are listed, may together admit one
  landing's edits to one suite. Each is still exactly one edit inside its
  own named test, and they chain by git blob: the first entry's
  `before_blob` is the suite before the landing, the last entry's
  `after_blob` is the suite at the landing, and each blob between is the
  blob id of the text the entries before it leave. The landing's diff for that suite must still be exactly those
  entries' recorded texts and nothing else. Each entry still admits one
  landing, and nothing wider is admitted. F5.2's check, as T059 wires it,
  takes a chain only when asked to: its last step runs
  `python3 scripts/protected_suites.py --chains --landings="$(cat "$W/x-arc.txt")" --suites="$(cat "$W/gen-suites.txt")"`.
  12.5's falsifier is not amended. Its call passes no `--chains`, so it
  keeps one entry per suite per landing and refuses a chain, and neither
  file is one of its governed suites (its `git grep` selects the same 16
  files at openXdox-code `main` `c41063d6` and at T059's head `4feb8009`).
  This bookkeeping amendment does not itself touch the Python above.
  Carried out by T061 (openXdox-code#36) and T063.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6016648451`; Ruled "Amend
  F12.1 with --chains"):** Brett Heap's multi-choice word of 2026-10-06,
  verbatim *"Amend F12.1 with --chains (Recommended)"*. Batch K's sentences
  above, *"12.5's falsifier is not amended. Its call passes no `--chains`, so
  it keeps one entry per suite per landing and refuses a chain"*, no longer
  hold: 12.5's falsifier now passes `--chains` too, the mechanism batch K gave
  F5.2 here, under the same rule (batch Q's note at 12.5's falsifier). Batch K's
  ratified text is not rewritten, and the rest of its paragraph stands: F5.2's
  call is unchanged, and neither of T061's two files is one of 12.5's governed
  suites. This bookkeeping amendment does not itself touch the Python above.
  Carried out by plan 038's T026 and T029.

  **Landed 2026-10-05** (T086, then T089): T086 (openXdox-code#37 → `56e1c238`)
  repairs, under R1Q7 (a)'s allow-list, the three pre-arc reds in
  `tests/test_session_snapshot.py` that `evidence/checkpoint-phase2.md` § 2
  quotes. T089 (openxFactory#1238 → `fab575ad`) then runs F5.2 whole, as batches
  C, F, G and K amend it, at openXdox-code `56e1c238` with openDox-code
  `dede32b4` installed over it and `OPENXFACTORY` at openxFactory `36908480`. It
  exits 0: the seven suites pass whole (`45 passed`, `23 passed`, `18 passed`,
  `6 passed`, `40 passed`, `9 passed` and `12 passed`), `test -s` holds, and the
  `--chains` step prints five `admitted:` lines, then
  `ok: 5 protected edit(s), each entered and holding`
  (`evidence/checkpoint-phase3.md` § 5). The box closes at phase 3's checkpoint
  (RULED `5962785556`, item 1).
- [x] 5.5 Lower `consumer_reach.py`'s generator-facing deferred reaches as the
  projection replaces them; the import-time column stays at zero.

  **Landed 2026-09-30** (T055): openDox-code#59 → `fa140875`, then its follow-up
  openDox-code#70 → `75bd8703`. The snapshot source and registry, the
  corpus-root predicate and the writer and validator lookups have openDox
  defaults the entry points register; the seven `consumer_reach` names that T055
  lists, `snapshot_registry` and `find_validator` among them, are retired, and
  the import-time column stays zero.
- [x] 5.6 **Do NOT author the view-wiring slice here** — and it can no longer be
  duplicated: it was CLAIMED on openDox-code under actor `viewwire` (RULED *"wire
  the views and land it"*, same comment) and LANDED as **openDox-code#35 →
  `3c3a9e31`** (2026-09-22T21:39:18Z), converting the hardcoded
  `stage-brainstorm` / `stage-staged` / `stage-realized` spellings in
  `src/opendox/web/views/` to role lookups and joining `lens.js` to the display
  facet. Ticked on that landing, which is the evidence; nothing in this arc
  re-does it. The ruling is explicit that the generator is not in that claim.
- [x] **FALSIFIED BY** (openDox-code checkout, `pip uninstall -y openxdox` so that
  `python -c "import openxdox"` raises, AND `python -c "import doc_health"` raises
  too — the neutral projection must reach neither the consumer nor the publisher
  — over a fixture directory of plain `.md` documents carrying none of
  openxFactory's governance vocabulary):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v5"                       # a FRESH environment: nothing already installed stands in
      . "$W/v5/bin/activate"
      pip install ".[test]"
      for sibling in openxdox doc_health; do                # a FRESH environment makes them absent; ASSERT it
        if python -c "import $sibling" 2>/dev/null; then echo "FAIL: $sibling is importable"; exit 1; fi
      done
      # the MODULE, not the console script, so this proof does not depend on
      # 10.1's packaging line: the module is importable once group 2 lands, and
      # that is what this falsifier uses.
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      R=$(mktemp -d)/plain-documents
      cp -r tests/fixtures/plain-documents "$R"   # 5.0's fixture, as a FRESH repository
      git -C "$R" init -q
      git -C "$R" add -A
      git -C "$R" commit -qm fixture
      python -m opendox.cli generate --repo-root "$R" --repository fixture --output "$W/snap.json"
      python3 - "$W/snap.json" <<'PY'
      import json, re, sys
      d = json.load(open(sys.argv[1]))
      assert d["documents"], "snapshot is empty"
      WORDS = ["brainstorm", "staged", "draft", "ratified", "standard", "superseded", "retired", "record",
               "openspec", "proposal.md", "tasks.md", "design.md", "added requirements", "modified requirements"]
      pat = re.compile(r"\b(" + "|".join(re.escape(w) for w in WORDS) + r")\b")
      def values(o):                                        # string VALUES only: keys are the product's own structure
          if isinstance(o, dict):
              for v in o.values(): yield from values(v)
          elif isinstance(o, list):
              for v in o: yield from values(v)
          elif isinstance(o, str):
              yield o
      leaks = sorted({m.group(1) for v in values(d) for m in pat.finditer(v.lower())})
      assert not leaks, f"openxFactory's vocabulary leaked into the neutral projection: {leaks}"
      print("documents:", len(d["documents"]))
      PY

  Under `set -euo pipefail` the sequence exits non-zero on any step; the
  assertions are IN the command rather than in prose, so the check is
  machine-detectable. `python -m opendox.cli` is an entry point that EXISTS:
  `cli.py:30-58` runs under `__main__` and hands over to the package copy's
  `main()`, so this command reaches `cmd_generate` exactly as 10.1's console
  script does. Every option follows the verb, as 10.1's table records
  against the parser.

  **Landed 2026-10-02** (T063, openxFactory#1218 → `a883bbf6`): F5.3 exits 0 at
  openDox-code `047bb4fa` with neither `openxdox` nor `doc_health` importable:
  `documents: 8`, and no declared word leaks into the neutral snapshot
  (`evidence/checkpoint-phase2.md` § 3).

## Group 6 — Requirement 6 / G5: a health check over openDox's own documents (openDox-code)

- [ ] 6.1 **Expect to find almost nothing generic, and plan for that.** A strict
  measurement — comments and docstrings stripped, so only executable code counts
  — finds exactly ONE of `scripts/doc_health/`'s 37 Python modules free of
  openxFactory/OpenSpec identifiers: `lines.py`, 133 lines of 31,437 (0.4%).
  About 13 modules mix a reusable mechanism with hard-coded corpus identifiers
  (`corpus.py:39,59,92-93`; `inventory.py:37,52`; `preflight.py:20-25,180-185`),
  and about 23 are corpus operations by subject. **There is no extractable
  generic doc-health core**, so requirement 6 is satisfied by openDox growing its
  own check over its own declaration — not by relocating families.
- [ ] 6.1a Where a module genuinely mixes both, relocate the generic part into a
  module both sides depend on BEFORE either side moves — `corpus-adapter-seam`'s
  relocation rule applied inside a module.
- [ ] 6.2 openDox carries a health check over its own documents, reading its own
  declaration. **No openxFactory check family moves** (requirement 1). The seam
  already exists and is DEAD: `src/opendox/workbench.py:1389`'s
  `run_scoped_doc_health` (families `status-validity`, `tag-hygiene`) catches the
  `ImportError` and records `status = not-available`,
  `detail = doc-health machinery unavailable: No module named 'doc_health'`. Give
  it something to call.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q9 (a),
  item 1):** The description of the seam above, from *"The seam already exists
  and is DEAD"* to the `detail` it quotes (`:1138-1142` at `main` `92010d3e`),
  is SUPERSEDED, as F6.1's "Today" sentence is struck below. Plan 034's T026
  (openDox-code#39 → `582ed073`) routed the call's three reaches through
  openDox's health-check seam, as 4.3's landing records. Measured at
  openDox-code `a9ac96f9`: `run_scoped_doc_health` is at `workbench.py:1666`,
  and the registration call, `register_health_check`, at `:1622`. With nothing
  registered the call answers `not-available` with the seam's own detail,
  `HEALTH_CHECK_NOT_REGISTERED` (`:1594`), which names the seam and the call
  that fills it, and `tests/test_health_check_seam.py:143-144` asserts that
  neither `doc_health` nor `No module named` appears in it. The box's rule
  stands: openDox carries its own check over its own documents, no openxFactory
  family moves, and the seam is given something to call, openDox's own check,
  which an entry point registers. Carried out by plan 038's T052.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v6"                       # a FRESH environment: nothing already installed stands in
      . "$W/v6/bin/activate"
      pip install ".[test]"
      python3 - <<'PY'
      from opendox import workbench
      r = workbench.run_scoped_doc_health(".", ["README.md"])
      assert isinstance(r, workbench.ActionResult), type(r)
      assert r.status == "completed", f"the check did not run: status={r.status!r} detail={r.detail!r}"
      assert isinstance(r.findings, list) and r.reference, f"no result shape: {r!r}"
      PY

  The call returns an `ActionResult` DATACLASS (`workbench.py:1339`) whose
  `status` is one of `completed | not-available | skipped`, so the assertion is on
  the one value that means the check RAN — not merely on the call returning. The
  earlier form of this command printed the status and exited 0 whatever it was,
  and it subscripted the result (`['status']`), which a dataclass refuses with a
  `TypeError`: it could neither fail for the right reason nor pass. Today the
  assertion fails on `status='not-available'`, with
  `detail = doc-health machinery unavailable: No module named 'doc_health'`.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q9 (a),
  item 1):** F6.1 builds an ENTRY POINT before the call, as batch A amended
  F3.1's line 2. A bare process still refuses, naming the seam, because a
  default is a registration an entry point makes and never a fallback inside
  the seam (4.3, batch G's addendum), and openDox-code's
  `tests/test_health_check_seam.py` pins that. So the heredoc builds the parser
  first, and the entry point registers openDox's own check at the seam. Its
  first lines read:

      from opendox import workbench
      from opendox.cli import build_parser
      build_parser()                                        # an ENTRY POINT registers openDox's own check (4.3, batch G)
      r = workbench.run_scoped_doc_health(".", ["README.md"])

  and its three assertions stand as written. The sentence above that begins
  *"Today the assertion fails on `status='not-available'`"* (`:1163-1165` at
  `main` `92010d3e`) is STRUCK. At openDox-code `a9ac96f9` a bare call answers
  `not-available` with the seam's `HEALTH_CHECK_NOT_REGISTERED` detail, which
  names neither `doc_health` nor `No module named` (6.2 as this batch notes
  it). This bookkeeping amendment does not itself touch the command above.
  Carried out by plan 038's T052, and run by its T065.

## Group 7 — Requirement 7 / G6: a validator openDox can run (openDox-code; 7.3 in openXdox-code)

- [x] 7.0 **Ship `tests/fixtures/malformed`**: 5.0's `plain-documents` with
  EXACTLY ONE rule violation the validator must name, so the falsification below
  can tell "refused for that rule" from "refused for anything". The fixture
  carries a file `EXPECTED_RULE` holding the IDENTIFIER the validator reports for
  that violation, so the acceptance asserts the rule itself and not a wording it
  guesses at.

  **AMENDED — T007 Batch G (`5850003126`; Ruled R1Q11 (a), R1Q12 (a)):** The
  one violation is of a rule of the neutral snapshot schema that T053 adds to
  openDox-spec (7.1 as this batch amends it), and `EXPECTED_RULE` holds that
  rule's identifier. The generate verbs validate the snapshot they write
  against that schema, so the refusal F7.2 asserts is for a rule of
  openDox's own contract. Carried out by T051 and T053.

  **Landed 2026-09-29** (T051): openDox-code#56 → `86647320`.
  `tests/fixtures/malformed` holds exactly one violation, the neutral schema's
  rule `title-and-summary-are-text` (an empty title), and `EXPECTED_RULE` holds
  that identifier (F7.2 names it, `evidence/checkpoint-phase2.md` § 5).
- [x] 7.1 **NARROW THE INPUT SET FIRST, then acquire what remains.** The existing
  validator's `SCHEMA_FILENAMES` names **ten** schemas and they have three
  different owners, so "give openDox the whole set" is the wrong shape:

  | owner | count | schemas |
  |---|---|---|
  | `opensoft/openDox-spec` | 3 | `ideation-workbench`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` |
  | `opensoft/openXdox-spec` | 3 | `ideation-dashboard-snapshot`, `ideation-dashboard-snapshot-index`, `gate-action-record` |
  | `openxFactory` | 4 | `ideation-possibles-register`, `project-register`, `demotion-execution-receipt`, `gate-intent` |

  Ownership is settled, not inferred: `docs/contract-versioning-policy.md`
  § 1047-1053 records openxFactory DIVESTING the first six to the two spec legs
  by canonical home, leg commit and unchanged `sha256`. Both code legs and both
  assembly roots carry **zero** schema files.

  **The default direction, and the one this task recommends:** openDox's
  validator validates openDox's OWN document kinds — its spec leg's **three** —
  which are openDox's own spec leg's. **How they reach the code leg is the part
  requirement 7 constrains and this box must settle, because the two obvious
  answers contradict each other.** `AGENTS-shape.md` puts a contract the code
  READS but does not OWN in the SPEC leg, reached from the assembly root with
  `CONTRACTS_DIR` — but `docs/project-repo-schema.md:54-58` puts the assembly and
  the code leg in DIFFERENT repositories, so an assembly-root read cannot satisfy
  requirement 7's one-checkout rule in a code-leg-only checkout. **The resolution
  this box takes: the INSTALLED product is the checkout requirement 7 means.** The
  three schemas ship as PACKAGE DATA of the openDox distribution, so
  `pip install openDox-code` puts them on disk beside the validator and the
  assembly root remains their source of truth for editing. The falsifications
  below therefore run against an INSTALLED product, not a bare clone. If that
  packaging is refused, the alternative is to run the validator from the assembly
  root and amend requirement 7's scenario to say so — recorded here so the choice
  is visible rather than discovered at implementation. The
  openXdox-spec three belong to the CONSUMER's validator and openDox never needs
  them. Only if a measured openDox verb genuinely needs one of openxFactory's
  four does it arrive as the DIGEST-PINNED VENDORED COPY `neutral-product-pin`
  admits — a CONSUMED manifest member, and note that capability admits **ONE**,
  so needing more than one is itself a finding to raise rather than a thing to do.

  **AMENDED — T007 Batch G (`5850003126`; Ruled R1Q11 (a), R1Q12 (a)):** "its
  spec leg's **three**" becomes FOUR. openDox's validator validates its spec
  leg's four kinds: the three of the table's first row, and the neutral
  snapshot schema that T053 adds to openDox-spec, whose stage values are the
  six role keys. That neutral kind is the snapshot openDox's generate verbs
  write. openXdox's governed generator keeps writing
  `ideation-dashboard-snapshot`, which stays the consumer's, as the table's
  second row has it, and openXdox-spec does not change. The four travel as
  package data, as this box resolves: the code leg carries digest-checked
  copies of them, and a test holds each copy to the spec-leg commit the
  openDox root pins (`contracts/spec-pin.yaml`). The same copies serve the
  doxBench chat validators that this batch's 4.3 addendum names. F7.2's
  command is unchanged: it installs the product, so the packaged set it
  exercises is these four. Carried out by T053, T057 and T058.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q22
  (a); with N-15, `6013547504`):** An addendum to batch G's. R2Q22 (a) gives
  openDox's spec leg THREE more schemas: the finding's neutral shape,
  `health/packs.yaml` (15.1a) and the exceptions file,
  `health/dispositions.yaml` (14.8). They travel as batch G's four do, so the
  code leg's digest-checked package-data copies become SEVEN, each held by the
  same test to the spec-leg commit the openDox root pins. The two FILE kinds,
  the manifest and the exceptions file, join the validator's kinds, so
  openDox's validator validates its spec leg's six kinds. The finding's neutral
  shape is a copy the engine reads and NOT a validator kind: a finding's `kind`
  field is its family, so no `kind` constant can name the schema (N-15).
  openDox-code's `tests/test_validator_input_set.py` therefore reads "the
  validator's kinds plus the finding shape". 7.1b stands, and F7.2's command is
  unchanged. The bundle that carries the three is 9.5's (batch Q's addendum
  there). Carried out by plan 038's T040, T041, T047 and T054.

  **Landed 2026-09-30** (T053, T057): openDox's validator validates its spec
  leg's four kinds (7.1's three and the neutral snapshot schema, batch G): the
  schema (openDox-spec#16 → `f7ee3c76`; root bundle openDox#14 → `52005213`,
  changelog openDox#15 → `66758438`) and the four digest-checked package-data
  copies (openDox-code#58 → `8ec08e91`).
- [x] 7.1b **AND TWO OF THOSE FOUR ARE NOT AVAILABLE BY THAT ROUTE AT ALL.**
  `gate-intent.schema.yaml` is an INTENT-PLANE schema — the carve manifest lists
  it among the validator's contract files (`docs/opendox-carve-manifest.yaml:459`)
  and requirement 1 keeps the intent-plane schemas with openxFactory. Vendoring
  it would satisfy requirement 7 by breaching requirement 1, which requirement 7's
  fifth scenario now refuses in terms. The same reasoning covers
  `ideation-possibles-register.schema.yaml`, filed
  `stays_openxfactory_adapter` as openxFactory's own candidate register. **If the
  narrowing in 7.1 is done properly, openDox needs neither**; if an openDox verb
  appears to need one, raise it as a finding about the boundary rather than
  copying the schema.

  **Landed 2026-09-30** (T057): openDox-code#58 → `8ec08e91`. A test asserts
  `gate-intent` and `ideation-possibles-register` are not in the validator's
  set, so requirement 1 is not breached.
- [x] 7.1a Record why the existing script cannot simply be reused: it derives
  `SCHEMAS_DIR` from `__file__` (`validate-ideation-dashboard-contracts.py:114-115`)
  and so looks for a `contracts/schemas/` its own leg does not have — run from
  openXdox-code it exits 2 with `ERROR .../contracts/schemas not found`. That is
  the G6 defect in one line, and it is the consumer's to fix for its own set.

  **Landed 2026-09-30** (T057): openDox-code#58 → `8ec08e91`. The reason the old
  script cannot be reused (it derives `SCHEMAS_DIR` from `__file__`) is recorded
  and the packaged validator replaces it.
- [x] 7.2 openDox-code has **no `scripts/` directory at all** and one console
  script. Whatever validator it gains is new surface at the code leg, not a
  relocated one.

  **Landed 2026-09-30** (T057, T058): openDox-code#58 → `8ec08e91` adds the
  validator as new surface at the code leg and openDox-code#68 → `047bb4fa`
  wires it into the generate verbs (`--strict`, `--no-validate`). F7.2 passes
  (`evidence/checkpoint-phase2.md` § 5).
- [x] 7.3 **THE CONSUMER'S HALF, in openXdox-code — not openDox-code.** Three
  carve-broken defects sit in the validator lookup openXdox KEEPS with
  `snapshot.py` (design R-G3). They were registered by the archived packet's
  § 5.5 residue and owed to *"a follow-up act with its own claim"* that nobody
  holds. Measured at openXdox-code `195276b7`:
  - `VALIDATOR_RELPATH` (`src/openxdox/snapshot.py:29`) names
    `openxFactory/scripts/validate-ideation-dashboard-contracts.py`, a path in
    the PUBLISHER's tree that openxFactory shed (`cc4ae9d3`), although
    openXdox-code carries its own `scripts/validate-ideation-dashboard-contracts.py`.
  - **`find_validator` (`:61`) walks up from the working directory until it
    finds one, so it ADOPTS AN ENCLOSING CHECKOUT.** That is the "reaching into a
    host tree instead of an injected adapter" class this arc exists to close,
    appearing a second time.
  - The validator it would find derives `SCHEMAS_DIR` from its own `__file__`,
    which 7.1a shows resolving to a directory that is absent.
  The fix is the consumer's, as 7.1a says of its schema set. openXdox's validator
  and its three schemas (7.1's openXdox-spec three) are located through the
  INSTALLED openXdox distribution, and no parent walk remains. This box is
  claimed as its own openXdox-code act on `#656`, like every group here, so it is
  not left unowned again.

  **Landed 2026-09-30** (T061): openXdox-code#36 → `6a3b93b9`. The consumer's
  validator and its own three schemas ship as package data and `find_validator`
  ignores its start, so no parent walk remains; twelve allow-list entries were
  made (R1Q7 (a), batches F and K).
- [x] **FALSIFIED BY** (7.3; an openXdox-code checkout, installed into a fresh
  venv, running the lookup from inside a planted PRE-SHED tree):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v7x"                      # a FRESH environment: nothing already installed stands in
      . "$W/v7x/bin/activate"
      pip install ".[test]"
      mkdir -p "$W/preshed/openxFactory/scripts" "$W/preshed/work"
      printf 'raise SystemExit(0)\n' > "$W/preshed/openxFactory/scripts/validate-ideation-dashboard-contracts.py"
      python3 - "$W/preshed" <<'PY'
      import sys
      from pathlib import Path
      from openxdox import snapshot
      planted = Path(sys.argv[1]).resolve()
      found = snapshot.find_validator(planted / "work")     # the lookup starts INSIDE the planted tree
      assert found is not None, "the consumer found no validator of its own"
      assert planted not in Path(found).resolve().parents, f"it adopted the enclosing tree's validator: {found}"
      PY
      python -m pytest -q \
        "tests/test_snapshot.py::test_the_validator_is_the_installed_consumers_own" \
        "tests/test_validate_ideation_dashboard_contracts.py::test_every_schema_the_consumer_validates_is_on_disk"

  The planted tree is exactly the shape the parent walk adopts today: an
  `openxFactory/scripts/validate-ideation-dashboard-contracts.py` above the
  working directory, which exits 0 whatever it is given. The assertion is on
  WHERE the validator came from, so a lookup that still walks up fails even when
  the planted script would have "passed" every snapshot.

  **AMENDED — T007 Batch I (`5851950767`; Ruled R1Q27 (a)):** The consumer's
  validator validates its own three kinds (7.1's openXdox-spec three) from its
  installed distribution, wherever it runs. It validates the family's other
  kinds only where the tree it runs from supplies their schemas, reading that
  tree's own `contracts/` first, as openxFactory's composed validator does
  today. So the openxFactory contract rows that name it stay true, and no
  contract changes. The second named test reads accordingly: every schema
  THIS INSTALL validates is on disk, its own three always, and another kind's
  only where the running tree supplies it. Carried out by T061 and T063.

  **Landed 2026-09-30** (T061, openXdox-code#36 → `6a3b93b9`; run again at T063,
  openxFactory#1218 → `a883bbf6`): F7.1 exits 0 from the planted pre-shed tree
  and both named tests pass (`2 passed`, `evidence/checkpoint-phase2.md` § 4);
  at #35's head it exits 1.
- [x] **FALSIFIED BY** (openDox-code checkout, no sibling, **INSTALLED into a
  fresh venv**, because 7.1 settles that the three schemas travel as PACKAGE
  DATA and a bare clone therefore cannot exercise the packaged set this box is
  about). Validation is the
  POST-RENDER step inside the generate verbs — there is no `validate` verb and
  this packet adds none — so it is exercised through `--strict`, which also makes
  a validator that could not RUN fatal instead of a warning:

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv "$W/v7"
      . "$W/v7/bin/activate"
      pip install .   # PACKAGE DATA on disk (7.1)
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      OK=$(mktemp -d)/plain-documents
      cp -r tests/fixtures/plain-documents "$OK"
      git -C "$OK" init -q
      git -C "$OK" add -A
      git -C "$OK" commit -qm fixture
      BAD=$(mktemp -d)/malformed
      cp -r tests/fixtures/malformed "$BAD"
      git -C "$BAD" init -q
      git -C "$BAD" add -A
      git -C "$BAD" commit -qm fixture
      python -m opendox.cli generate --repo-root "$OK" --repository fixture --strict --output "$W/ok.json"
      if python -m opendox.cli generate --repo-root "$BAD" --repository fixture --strict --output "$W/bad.json" 2>"$W/err"; then
        echo "FAIL: a malformed corpus validated"; exit 1
      fi
      RULE=$(cat tests/fixtures/malformed/EXPECTED_RULE)
      test -n "$RULE"
      grep -qF -- "$RULE" "$W/err"                          # refused for THE rule the fixture breaks
      rc=0; grep -q "No such file or directory" "$W/err" || rc=$?
      test "$rc" -eq 1                                      # ABSENT: not refused for a missing path

  The first exits 0; the second exits NON-ZERO and the sequence asserts that
  rather than printing it, so a validator returning zero on a malformed corpus
  fails the check. **The refusal must carry the fixture's own rule identifier.**
  A validator that failed for a missing schema, a generic error, or with empty
  stderr would not produce it, so the positive `grep -qF` is what proves the
  intended rule ran. The negative line only closes the one failure this box
  measured today. The last check is a NEGATIVE one, asserted as grep's exit
  status 1 exactly: not `! grep -q`, which `set -e` never stops on, and not
  `grep -qv`, which would have succeeded on any single non-matching line and so
  passed a mixed "missing schema AND rule error" stderr. **Neither may fail on an unresolvable schema path** — today
  that is exactly how it fails, because `--strict` makes "the validator is
  unreachable" fatal and the validator is unreachable.

  **Landed 2026-10-02** (T058, openDox-code#68 → `047bb4fa`; T063,
  openxFactory#1218 → `a883bbf6`): F7.2 exits 0: the good fixture validates, the
  malformed one exits non-zero naming `title-and-summary-are-text` with no
  `No such file or directory` (`evidence/checkpoint-phase2.md` § 5; also
  openDox-code#68's body).

## Group 8 — Requirement 8 / G7: openDox-spec governs openDox (openDox-spec) — BLOCKED

**These boxes carry the reserved `[~]` marker, not `[ ]`, and that is deliberate.**
They are NOT this packet's act — they are openDox-spec's, in a repository this
packet cannot write — so a literal unchecked box would make this packet
unarchivable for work it was never entitled to do. The marker is the corpus's own
(`split-opendox-two-layer-product` closed at 67 [x] / 0 [ ] / 5 [~]).
**Owner: whoever holds openDox-spec's instance.**
**Exit condition: requirement 8's third scenario — when openDox-spec has promoted
the requirements the carve's map assigns it, these boxes close there and this
packet's interim arrangement ends.**

- [~] 8.1 openDox-spec promotes the requirements the carve's ratified
  per-requirement map assigns to openDox (the map's split: **71 openDox / 16
  openXdox / 15 openxFactory**; the 16 were carried into openXdox by the carve's
  § 6.1 and § 6.5 closures, and the 15 were re-promoted here by
  `repromote-engineering-vocabulary` under RULING DQ-1 — only openDox's 71 have
  no home). Measured by normalized-title scan of every `spec.md` in openDox-spec:
  **68 of the 71 appear nowhere in the repository**, and the three that do appear
  only inside `## MODIFIED` blocks of draft changes.
- [~] 8.1a **Unblocks openDox-spec's own backlog, which is why this is not
  housekeeping.** Three of its four active changes carry `## MODIFIED` blocks
  against `ideation-dashboard`, a spec that does not exist there, so **they can
  never be archived** — the loop is open at both ends: nothing can be promoted
  because nothing has been archived, and nothing can be archived because nothing
  has been promoted. Promoting the 71 is what breaks it.
- [~] 8.1b **Raise openDox-spec's CLI pin while doing it.** Both spec legs pin
  `@fission-ai/openspec@1.2.0`; openxFactory pins 1.12.0 by content address. Run
  against the same tree, **1.2.0 emits none of the three "Archive would refuse
  this delta" notices** that 1.12.0/1.13.x report. openDox-spec's gate cannot see
  the defect in 8.1a.
- [~] 8.2 On that landing, requirement 8's third scenario fires and work scoped to
  openDox is authored in openDox-spec. This packet's interim arrangement ends.
- [~] **FALSIFIED BY** (openDox-spec checkout):

      OPENSPEC_TELEMETRY=0 openspec list --specs
      OPENSPEC_TELEMETRY=0 openspec validate --all --strict

  The first lists the promoted capabilities; the second passes with no "Archive
  would refuse this delta" notice under a CLI at or above the openxFactory pin.
  Today the first answers `No specs found.`, and three of four changes carry the
  notice under 1.12.0 while their own gate at 1.2.0 cannot see it.

## Group 9 — Requirement 9 / G8: each leg's suite green alone (both legs)

- [x] 9.1 openDox-code's required check runs the whole suite, no `--noconftest`,
  no file list (follows group 2).

  **Landed 2026-09-27** (T034, T035, T036): openDox-code#50 → `71b631bc` repairs
  the nine files, openDox-code#51 → `80acead1` empties `collect_ignore`, and
  openDox-code#52 → `55194335` makes the required check run the whole suite.
  F9.1 exits 0 (`evidence/checkpoint-phase1.md` § 3).
- [x] 9.2 openXdox-code the same, with `OPENDOX_BACK_IMPORTS` lowered as each
  deferred reach closes. The import-time column is ALREADY zero and stays there.

  **AMENDED — T007 Batch B (`5817152735`; Ruled R1Q6 (d)):** An addendum
  (T006): for release 1, openXdox-code's whole suite runs less T041's
  declared exclusion, `tests/declared_exclusion.yaml`, which is reported as
  an open extraction with its count and each entry's reason. T097 ticks 9.2
  with that note, and requirement 9 stays open for openXdox-code until the
  direction arc (T008) lands. Carried out by T041, T043 and T097.

  **AMENDED — T007 Batch F (`5850003126`; Ruled R1Q24 (a), R1Q25 (b)):** For
  release 1, the declared exclusion that openXdox-code's whole suite runs less
  (R1Q6 (d), `5817152735`; T007 Batch B) also holds the files that reach
  openxFactory's status-exemption rail or its contracts, and
  `tests/test_snapshot.py` until 7.3 lands. Each entry carries its own reason
  and is reported as an open extraction. The whole-suite check lands in phase
  1, and the box closes in phase 3, as this batch's addendum to the release
  map records. Carried out by T041, T043, T061, T086 and T097.

  **Landed 2026-10-05** (T040, T041, T043, then T086): openXdox-code's whole
  suite runs less T041's declared exclusion, `tests/declared_exclusion.yaml`,
  reported as an open extraction with its count and each entry's reason
  (openXdox-code#29 → `d84b5048`, openXdox-code#30 → `5fbd188e`,
  openXdox-code#32 → `4610bca5`). At T086's landing (openXdox-code#37 →
  `56e1c238`, pin openDox-code `dede32b4`) `OPENDOX_BACK_IMPORTS` reads
  `(0, 0)`, its import-time column still `0`. The declaration then holds 66
  files, carrying 68 reasons (60 `doc_health`, 3 `status-exemption-rail`, 5
  `openxfactory-contracts`), T086 having added
  `tests/test_column_contributions_governed.py` under `doc_health`. CI's
  `validate` at that PR's head, whose tree landed unchanged (run 37307785866),
  prints `open extraction: the declared exclusion` with those 66 files and each
  reason, reads `selected=1099 passed=1095 skipped=4`, and leaves out the
  32-entry help-tree node as its own open extraction (batch O). Requirement 9
  stays open for openXdox-code until the direction arc (T008) lands (batch B's
  addendum).
- [x] 9.2a **Add the missing instrument.** No gate watches the openDox →
  openxFactory direction — the ratchet measures openDox → openXdox only, which is
  how two import-time reaches into the publisher survived a completed inversion
  under a green check. Requirement 2's third scenario is that instrument.

  **Landed 2026-09-27** (T030, T036): openDox-code#46 → `0e88454a` adds the
  instrument and openDox-code#52 → `55194335` makes a required check run it, so
  a reach into the publisher can no longer survive a green check.
- [x] 9.3 Behaviours needing both legs become declared INTEGRATION tests naming
  the pin they compose at, rather than being dropped from both suites — including
  the 31-entry assembled `--help` tree the carve manifest records as one
  *"which after the carve neither leg produces alone"*
  (`docs/opendox-carve-manifest.yaml:3088`). Nothing anywhere reproduces it today.
  **They live in openXdox-code's `tests/integration/`**, because that
  repository's `pyproject.toml` is where the composition is declared: its one
  `opendox` dependency is pinned by full commit (`opendox @
  git+https://github.com/opensoft/openDox-code@5c137a90…`, measured at
  `195276b7`). They sit inside the whole suite that 9.2's required check runs, so
  CI runs them without a file list.

  **Landed 2026-09-27** (T035, T042): openXdox-code#31 → `4e16db95` creates
  `tests/integration/` at the declared composition, each test naming the pin it
  composes at: the 31-entry assembled `--help` tree test and T037's two
  both-legs cases; openDox-code#51 → `80acead1` lists each module it removed
  with its destination, and T049's arrival check finds all 19 where that list
  sends them (`evidence/checkpoint-phase1.md` § 8). The 31-entry test is left
  out of the required check until T008 (RULED `5859927858`, `5870594693`) and
  F9.2 stays red on it alone (`evidence/checkpoint-phase1.md` § 5).
- [x] 9.4 **Restore the margin, and stop the skips carrying the gap.** Both legs
  pass their floors with ZERO margin (openDox `1114/1111/3`, openXdox
  `539/533/6`), and every one of openXdox's six skips carries the same reason —
  *"doc_health reachability is BUILD-arc work (§ 3.5/3.6) … this test will assert
  for real once that lands"*. Two of openDox's three are the mirror image. **The
  whole-product assertions are precisely the ones that skip**, which is why both
  legs report green while neither product runs.

  **AMENDED — T007 Batch B (`5817152735`; Ruled R1Q6 (d)):** An addendum:
  each of openXdox's six skips either asserts, or its file joins the
  declared exclusion.

  T044 (openXdox's half) moved all six: the three seam suites
  (`tests/test_evidence_provenance_surface_seam.py`,
  `tests/test_model_scenario_workbench_seam.py`,
  `tests/test_role_authority_projection_seam.py`) drop their `doc_health`
  guard and the two cases each it skipped; those cases now assert for real —
  composed, they pass, and alone they fail on `doc_health` only — moved into
  `tests/test_seam_assembly_beside_gate_and_projection.py`, a file T044
  created, which the declaration lists under `doc_health`. The three suites
  keep their other cases, losing only the guard and gaining a pointer
  paragraph to the new file. This corrects T044's own `Ruled` line: the two
  moved skips came to sit in a CREATED file, not a carved one — the three
  seam suites themselves are carved and stay carved. The floors re-pin over
  the whole suite less that file, at `885/881/4`, margin zero, ON CI's
  reading. openDox-code's mirror-image two (T037, its half) assert for real
  with no declared exclusion of its own (openDox-code carries none, R1Q8
  (a)); its floors restore at `2476/2465/11`, THREE BELOW CI's reading — the
  holder's decision for that leg, where openXdox's sit ON it instead, as 9.4
  and T044's own text read. Carried out by T044.

  **Landed 2026-09-28** (T037, T044): openDox-code#55 → `2d116415` restores
  openDox-code's floors to `2476/2465/11` (three below CI's reading) and
  openXdox-code#33 → `6158151e` makes openXdox-code's six `doc_health` skips
  assert for real, re-pinning to `885/881/4` (CI's reading, margin 0).
  Correction (research R16 item 2, non-normative): openXdox-code's floors read
  `564/558/6` at `626f2c8d` (research R10, 2026-09-24), not the `539/533/6` the
  box records, because openXdox-code#26 and #27 had raised them. They have since
  been re-pinned to `890/880/10` by T043 (openXdox-code#32 → `4610bca5`) and to
  `885/881/4` by T044, and openDox-code's to `2476/2465/11` by T037.
- [ ] 9.5 **The pins that compose the legs advance with the arc, each by its
  owner's ordinary pin-sync act.** This packet moves none of them, and the
  realization cannot be exercised without moving them. Measured on 2026-09-23:
  - openXdox-code's `pyproject.toml` pins openDox-code at `5c137a90`, nine
    commits behind `main`.
  - The openDox root's `code` gitlink and `contracts/code-pin.yaml` name
    `d816cf06`.
  - The openXdox root's `contracts/opendox-pin.yaml`, and openxFactory's
    `contracts/opendox-pin.yaml` with its `openDox` gitlink, name the openDox
    root at `dc7aa08f`.
  - The openXdox root's `code` gitlink and `contracts/code-pin.yaml` name
    openXdox-code `626f2c8d`, and openxFactory's `contracts/openxdox-pin.yaml`
    with its `openXdox` gitlink names the openXdox root at `2f3f857d`. That is the
    route openXdox#17/#18 → openxFactory#1146/#1148 took, and it is how a leg's
    code reaches the roots the code surface names (`design.md` § D15).
  Each advances in the landing that needs the arc's code. openXdox-code's moves
  first, because 9.3's integration run means nothing at a pin that predates the
  arc. openxFactory's pins move before the host wiring of 4.1 and 4.3 can call a
  seam that exists. Each of openxFactory's two pairs — the `openDox` gitlink with
  `contracts/opendox-pin.yaml`, and the `openXdox` gitlink with
  `contracts/openxdox-pin.yaml` — moves in ONE commit, which
  `scripts/verify-opendox-pin.py` and `scripts/verify-openxdox-pin.py` check.
  Every one is an ancestor move, not a fork, and none cuts a contract bundle or
  owes a release tag.

  **AMENDED — T007 Batch G (`5850003126`; Ruled R1Q11 (a)):** An addendum.
  *"None cuts a contract bundle or owes a release tag"* stays true of every
  pin move above. Phase 2 adds one move that does both: it cuts ONE contract
  bundle, a `dox-v1.x` minor at the openDox root, because T053 adds an
  openDox-spec contract, the neutral snapshot schema (7.1 as this batch
  amends it). A bundle is the legs at the commits the root pins, so the
  root's `spec` gitlink and `contracts/spec-pin.yaml`, which name
  openDox-spec `8fe8c4c7` (measured 2026-09-29), move to T053's commit for
  the cut. The root cuts it under its own four-value rule (its
  `contracts/CHANGELOG.md`): the manifest's `contract_bundle_version`, the
  manifest's entries, the matching CHANGELOG entry, and an annotated
  `dox-v<major>.<minor>` tag over the root commit that names both legs, so
  this move owes its tag as well. The proposal says the same of the
  realization, that it *"cuts no bundle and owes no tag"* (its
  `code_surface:` and § What Changes). That sentence is read with this one
  exception, and this bookkeeping edits no line of the proposal.
  openDox-spec joins the arc's repositories, a sixth beside the five 11.0
  names, and its landings carry 11.0's trailer. Carried out by T053, T062
  and T090.

  **AMENDED — T007 Batch O (`5962754358`, item 1; `5963162921`):** A second
  exception to *"cuts no bundle and owes no tag"*, beside batch G's. Brett
  Heap's multi-choice words of 2026-10-02, verbatim *"Publish to PyPI at the
  cut (Recommended)"* and *"0.1.0 (Recommended)"*, publish openDox's first
  public release, version 0.1.0, to PyPI as `opendox` at release 1's cut, by
  trusted publishing, so no token is stored. The install line 10.3 documents
  (`pip install "opendox[local]"`, as batch H amends it) then works as
  written. That release owes ONE tag, as plan 034's T099 publishes it. At
  the cut, once AT-R1 has passed and on Brett Heap's publish word, the
  holder creates the tag `v0.1.0` in openDox-code at the commit the openDox
  root's `contracts/code-pin.yaml` names, and dispatches the release
  workflow on it. That commit is the version bump to 0.1.0, the last
  phase-3 openDox-code landing that changes the shipped package, which the
  root pins in phase 3. The workflow publishes only that commit. Every pin
  move above other than batch G's still owes no release tag, and this
  bookkeeping edits no line of the proposal. Carried out by T101 (the
  release workflow and the bump), T087 (the pin) and T099 (the tag and the
  publish).

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q22
  (a)):** A third exception to *"None cuts a contract bundle or owes a release
  tag"*, in batch G's form. Release 2 cuts ONE more contract bundle, a
  `dox-v1.y` minor, `dox-v1.2`, at the openDox root, because R2Q22 (a) gives
  openDox-spec three schemas (7.1 as batch Q amends it). The root's `spec`
  gitlink and `contracts/spec-pin.yaml` move to the openDox-spec commit that
  holds them, and the root cuts the bundle under its own four-value rule, as
  batch G's cut did: the manifest's `contract_bundle_version`, the manifest's
  entries, the matching CHANGELOG entry, and an annotated `dox-v1.2` tag over
  the root commit that names both legs. The cut is made on Brett Heap's cut
  word, as `dox-v1.1`'s was (RULED `5894235642`). No repository joins:
  openDox-spec is already the arc's sixth (batch G). The proposal's *"cuts no
  bundle and owes no tag"* is read with this exception too, and this
  bookkeeping edits no line of the proposal. Carried out by plan 038's T040 and
  T060.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q23
  (a)):** A fourth exception, in batch O's form. R2Q23 (a) publishes `opendox`
  0.2.0 to PyPI at release 2's cut, through the existing trusted-publishing
  workflow, so no token is stored, and the install line 10.3 documents then
  brings release 2. That release owes ONE tag. After AT-R2 has passed, and on
  Brett Heap's publish word, the holder creates the tag `v0.2.0` in
  openDox-code at the commit the openDox root's `contracts/code-pin.yaml` names
  in phase 5, which is the version bump to 0.2.0, the last phase-5
  openDox-code landing that changes the shipped package, and dispatches the
  release workflow on it. The workflow publishes only that commit. Every pin
  move above other than batch G's cut and the `dox-v1.2` cut still owes no
  release tag, and this bookkeeping edits no line of the proposal. Carried out
  by plan 038's T061 (the bump), T062 (the pin) and T084 (the tag and the
  publish).

  **Recorded by T097, a non-normative correction** (research R16 item 6; the box
  stays open for the arc's close, T090): openXdox-code's openDox pin
  (`5c137a90`) was 11 commits behind openDox-code `main` (`1e4a57fb`) on
  2026-09-24 (research R13), where the box measured 9 on 2026-09-23. It has
  moved with each phase: to `2d116415` by T040 (openXdox-code#29 → `d84b5048`),
  to `047bb4fa` by T059 (openXdox-code#35 → `839492d9`), and T086
  (openXdox-code#37 → `56e1c238`) moved it to `dede32b4`, the openDox-code
  commit T087 pins, in phase 3.
- [x] **FALSIFIED BY** (each leg's own checkout, no sibling installed):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v9"                       # a FRESH environment: nothing already installed stands in
      . "$W/v9/bin/activate"
      pip install ".[test]"
      python -m pytest -q                                   # NOT --noconftest, NOT a file list
      test "$(grep -c -- --noconftest .github/workflows/validate.yml)" -eq 0
      # AND no pytest step enumerates a subset: a named file list with no
      # --noconftest would otherwise pass the assertion above.
      python - <<'EOF'
      import re, sys, pathlib
      w = pathlib.Path(".github/workflows/validate.yml").read_text()
      body = "\n".join(l.split("#")[0] for l in w.split("\n"))
      named = set(re.findall(r'tests(?:_runtime)?/test_[A-Za-z0-9_]+\.py', body))
      sys.exit(0 if not named else (print("FAIL: workflow still enumerates", len(named), "test files"), 1)[1])
      EOF

  All three statements must succeed: `set -e` propagates a failing suite (a passing
  `grep` after a failing `pytest` must not make the sequence exit zero), and the
  `test` asserts the exclusion count is ZERO rather than leaving it to a reader.
  Today openDox-code gives 1,298 errors / 0 passed and openXdox-code 1,089 / 0.

  **AMENDED — T007 Batch B (`5817152735`; Ruled R1Q6 (d)):** `python -m
  pytest -q` collects the whole suite less the files in T041's declared
  exclusion file, `tests/declared_exclusion.yaml`. The falsifier asserts
  three things: the file's count equals its entries, every entry carries its
  reason, and the run prints the exclusion as an open extraction — its own
  title line reads `open extraction: the declared exclusion`. The two
  `validate.yml` assertions stay. openDox-code's F9.1 is unchanged (R1Q8
  (a)).

  Measured at landing: T041 wrote all four admitted reasons' entries at
  once, not the two-step split its own task line had planned (T041 writes
  the `doc_health` entries; T043's triage adds the rest).
  `status-exemption-rail` and `openxfactory-contracts` (R1Q24 (a)), and
  `consumer-schemas`, named for `tests/test_snapshot.py` alone (R1Q25 (b))
  — all three `5850003126`, T007 Batch F's — were already in T041's file
  when it landed, so T043's triage of the same pin found the same red results
  across the same files and became a re-run rather than an addition, which
  the holder accepted. `count` moved from 66 to 67 only later, at T044,
  with the `tests/test_seam_assembly_beside_gate_and_projection.py` entry,
  under `doc_health`. This file's four reasons are distinct from, and do
  not include, the assembled-help-tree test that T007 Batch J separately
  rules out of F9.1's realized falsifier line (`5870594693`, citing
  `5859927858`); T008 retires both together. CI's own reading of the triple
  (selected/passed/skipped) is `885/881/4`, at margin zero. Carried out by
  T041, T043 and T049.

  **AMENDED — T007 Batch F (`5850003126`; Ruled R1Q24 (a), R1Q25 (b)):** For
  openXdox-code, the declared exclusion that R1Q6 (d) admits (`5817152735`;
  T007 Batch B) takes three more reasons, and each entry names its own:
  openxFactory's status-exemption rail and openxFactory's contracts, both
  pending the `doc_health` direction arc (T008), and the consumer's schemas
  until 7.3 lands, for `tests/test_snapshot.py` alone. Every entry is reported
  as an open extraction, as the `doc_health` entries are, and the checks this
  falsifier makes of the exclusion apply to every entry. The
  `tests/test_snapshot.py` entry leaves when 7.3 lands, in phase 2.
  openDox-code's run is unchanged. Carried out by T041, T043, T049 and T061.

  **AMENDED — T007 Batch J (`5870594693`; citing `5859927858`):** The
  declared exclusion above (R1Q6 (d), `5817152735`; T007 Batch B, already
  extended by three more reasons, `5850003126`; T007 Batch F) takes a
  fourth: the assembled-surface test
  `tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records`,
  deselected for T042's own reason — `cli_gate` imports openxFactory's
  `doc_health` at load time — pending the same `doc_health` direction arc
  (T008). It is reported as an open extraction, as the other three entries
  are, and the checks this falsifier makes of the exclusion apply to it as
  well. T008 removes this entry together with the workflow's own deselect,
  the same act that closes the other three. openDox-code's run is
  unchanged. Carried out by T043.

  **AMENDED — T007 Batch O (`5970917267`):** Batch J's fourth entry names
  the assembled-tree node by its 31-entry name, which the composition carries
  through phase 2. From the pin move past T100 the node asserts 32 entries
  (10.1 as this batch amends it) and is renamed
  `tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_32_entry_tree_the_manifest_records`.
  The entry names it from then on. The landing that renames the node also
  moves openXdox-code's `validate.yml` `LEFT_OUT` entry, which names the node
  verbatim and which the whole-suite step passes to `--deselect`, so the
  deselect never names a test that does not exist (the holder's ruling of
  2026-10-03 on plan 034's analyze). The entry's reason, its report as an
  open extraction, and its removal by T008 are unchanged. Carried out by
  T086.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003918488`; Ruled ARC-Q2
  (a)):** In batch B's form, for openXdox-code. Brett Heap's multi-choice word
  of 2026-10-05, verbatim *"Composed CI in openXdox-code (Recommended)"*. What
  stays composed runs in openXdox-code's own CI against a pinned openxFactory:
  phase 4's composed workflow (U-9), made PERMANENT. The files of the declared
  exclusion that a lone checkout cannot run, the governed-behaviour tests and
  R1Q24's three status-exemption-rail files and five openxFactory-contracts
  files among them, are DECLARED INTEGRATION TESTS. Each entry keeps its
  reason and the declaration keeps its count. The declaration names the
  openxFactory commit that the composed workflow pins, and that workflow runs
  them, so they are not dropped from both suites. Requirement 9 CLOSES FOR
  openXdox-code BY THAT DECLARATION. The three checks this falsifier makes of
  the declaration stand as batches B, F, J and O wrote them, and the lone
  checkout's run still reports the declaration under batch B's title line.
  Batch B's addendum at 9.2, *"requirement 9 stays open for openXdox-code until
  the direction arc (T008) lands"*, is read with this ruling: the arc is
  decided (`6003918488`) and realized in its own change (ARC-Q3 (a)), and F9.2,
  requirement 9's third scenario, is ARC-5's (batch Q's note there).
  openDox-code's F9.1 is unchanged. This bookkeeping amendment does not itself
  touch the command above. Carried out by plan 038's T029 and T073, which
  re-runs F9.1.

  **Landed 2026-09-29** (T049, openxFactory#1204 → `9d2e5bc3`): F9.1 exits 0 in
  each leg: openDox-code `2d116415`, with the DSN exported, gives
  `2468 passed, 11 skipped`, and openXdox-code `6158151e`, as batches B and F
  amend it with batch J's one `--deselect`, gives
  `881 passed, 4 skipped, 1 deselected`
  (`evidence/checkpoint-phase1.md` §§ 3 and 4).
- [ ] **FALSIFIED BY** (9.3, and requirement 9's third scenario: an openXdox-code
  checkout, the composition's declared home, with openDox arriving ONLY through
  the pin):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v9i"                      # a FRESH environment: nothing already installed stands in
      . "$W/v9i/bin/activate"
      pip install ".[test]"                                 # openDox arrives at the pin pyproject.toml declares
      python3 - <<'PY'
      import importlib.metadata as md, json, pathlib, re, tomllib
      deps = tomllib.loads(pathlib.Path("pyproject.toml").read_text())["project"]["dependencies"]
      pins = [d for d in deps if re.match(r"opendox\s*@", d)]
      assert len(pins) == 1 and re.search(r"@[0-9a-f]{40}$", pins[0]), f"the composition names no full-commit pin: {pins}"
      got = json.loads(md.distribution("opendox").read_text("direct_url.json") or "{}").get("vcs_info", {}).get("commit_id")
      assert got == pins[0].rsplit("@", 1)[1], f"the installed openDox is {got!r}, not the pinned commit"
      PY
      ls tests/integration/test_*.py > "$W/integration.txt"  # a DECLARED integration suite exists
      while read -r f; do python -m pytest -q "$f"; done < "$W/integration.txt"
      python -m pytest -q "tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records"

  **The two legs' isolation runs above, and the leg-alone falsifiers of Groups 10,
  12, 14 and 15, are requirement 9's FIRST half.** This command is its third
  scenario: the assembled surface is exercised as well. It proves three things.
  The composition names a full-commit pin. The openDox actually installed is the
  pinned one, read from the `direct_url.json` that pip records for a VCS install
  rather than assumed. And a declared integration suite exists, runs green, and
  carries the named proof of the one surface neither leg produces alone. `ls`
  exits non-zero when `tests/integration/` holds no test, so an absent suite
  FAILS the command rather than passing it vacuously.

  **AMENDED — T007 Batch O (`5970917267`):** The command's last line names the
  assembled-tree node by its 31-entry name, which the composition carries
  through phase 2. From phase 3's pin, the pin move past T100, the tree has
  32 entries (10.1 as this batch amends it), and the line reads:

      python -m pytest -q "tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_32_entry_tree_the_manifest_records"

  F9.2 stays red on that test until T008 (`5859927858`), as batch J records.
  9.3's "31-entry" quotes the carve manifest's record of the tree at the
  carve, and stands as written. This bookkeeping amendment does not itself
  touch the command above. Carried out by T086.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6013547504`; Ruled ARC-5
  (a)):** Brett Heap's multi-choice word of 2026-10-06, verbatim *"Archive with
  F9.2 open (Recommended)"*. F9.2's ruled notes keep it open until the
  `doc_health` direction arc lands (`5859927858`, *"It runs again once the
  doc_health direction arc (T008) lands"*; `5870594693`), and ARC-Q3 (a)
  (`6003918488`), the later ruling, says the arc gates neither release 2's
  close nor #1144's archive. Read together, #1144 MAY ARCHIVE WITH F9.2 OPEN,
  reported in R1Q6 (d)'s form. F9.2's later closure is recorded in the arc
  change's own evidence (plan 038's T076), and #1144's archived `tasks.md` is
  never edited. If #1144 is still active when T076 runs, T076 ticks F9.2 here,
  under its own Rule 6 window. The command, its 32-entry node (batch O) and
  its expected result are unchanged, and the archive act stays the holder's.
  Carried out by plan 038's T076.

  **How the archive gate admits it.** `archive_change()` refuses any `tasks.md`
  line that matches `^- [ ]`, with `change has incomplete tasks`
  (`scripts/proposal-support.py:4631-4633` at `main` `92010d3e`). It has no
  per-box exception, and none is built or claimed for F9.2. So if #1144
  archives before T076 runs, its archive pull request ticks this box `[x]` with
  a disposition written beneath it: NOT PERFORMED at the archive, reported in
  R1Q6 (d)'s form, and carried by the direction arc's own change, whose
  evidence records F9.2's closure (T076). The open obligation is then not
  written down only inside an archived packet. THE TICK IS A DISPOSITION, NOT A
  PERFORMANCE. This is the form the gate leaves for a box that a ruling lets an
  archive pass unperformed, as `add-declared-former-id`'s archive used it on
  Brett Heap's ruling of 2026-09-15
  (`openspec/changes/archive/2026-09-15-add-declared-former-id/tasks.md:568-581`).

## Group 10 — Requirement 10 / G9, G10: one entry point (openDox-code + openDox root)

- [x] 10.1 A `[project.scripts]` entry point for the DOCUMENT surface. **The verbs
  are NOT invented here — `src/opendox/cli.py` already declares them** and group 2
  is what makes them reachable; the entry point is the missing packaging line:

      opendox = "opendox.cli:main"

  and the surface it exposes is the one already in the tree, named here so every
  falsification below is executable rather than a placeholder:

  | verb | shape, as `cli.py` declares it today |
  |---|---|
  | `generate` | `generate --repo-root <corpus> --repository <id> --output <path>` (`:880-883`) |
  | `generate-and-open` | `generate-and-open --repo-root <corpus> --repository <id> [--run-dir P] [--host H] [--port N] [--no-open] [--no-serve]` (`:885-909`) |
  | `create`, `edit` | `create --repo-root <repo> --title … --summary … --topics … --repository-context …`; `edit --repo-root <repo> <path>` (`:911`, `:927`) |
  | every generation verb | `--repo-root` AND `--repository` are REQUIRED; `--strict`, `--no-validate`, `--source-revision`, `--generated-at`, `--project-register`, `--possibles` are accepted — declared ONCE, in `_add_generate_args` (`:822-849`) |

  **Every option FOLLOWS its verb.** The parser (`build_parser`, `:852`) declares
  NO top-level option at all — `--repo-root`, `--repository` and `--strict` are
  SUBCOMMAND arguments — so `opendox --repo-root X generate …` is refused by
  argparse before any code of this product runs. An earlier draft of this table
  put them before the verb and every acceptance command below inherited that; the
  table and the commands were corrected together, against the parser itself.
  `--repository` is the snapshot's canonical repository id, and the commands pass
  `fixture`. `python -m opendox.cli` is a real entry point today:
  `cli.py:30-58` runs under `__main__` and HANDS OVER to the package copy's
  `main()` before the rest of the file executes, so the commands of Groups 5 and 7
  need no console script and no hedge.

  **There is no `serve` verb and no `validate` verb**, and this packet does not
  add either: serving is `generate-and-open`, and validation is a POST-RENDER
  step inside the generate verbs, hardened by `--strict` and skipped by
  `--no-validate`. Today the only console script is
  `opendox-runtime = "opendox.runtime.cli:main"` — a subsystem, not the product —
  and there is no `__main__.py` anywhere under `src/`. **RULED Q-R4 already places this work in THIS act** (`#656` comment
  `5701772032`, Brett Heap, 2026-09-16, recorded at `runtime/cli.py:40-46`): *"the
  verbs are wired into `opendox.cli` in the BUILD-arc act that repairs
  `opendox.serve`, and `opendox-runtime` is the spelling until then."* So 10.1
  follows group 2 and discharges Q-R4's condition.

  **AMENDED — T007 Batch A (`5817152735`; Ruled R1Q5 (a)):** An addendum.
  Q-R4's condition is discharged through the default profile's
  `SUBCOMMAND_EXTENSIONS` (`RuntimeSubcommand`). `opendox-runtime` stays as an
  alias, and a host's own profile keeps the 31-entry tree. Carried out by
  T038, T042.

  **AMENDED — T007 Batch O (`5970917267`):** An addendum to batch A's. Brett
  Heap's multi-choice word of 2026-10-03, verbatim *"Amend to 32
  (Recommended)"*. The assembled `--help` tree has 31 sections through phase
  2. From phase 3's pin it has 32, because T100 adds
  `opendox model-binding trust` (16.3a, T007's batch M). So a host's own
  profile keeps the assembled tree, at 31 entries through phase 2 and at 32
  from phase 3's pin.
  - openXdox-code's assembled-tree test, the node F9.2 runs and batch J's
    F9.1 entry deselects, moves to 32 at the pin move past T100. It is
    renamed
    `tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_32_entry_tree_the_manifest_records`
    in that landing, with its `LEFT_OUT` entry.
  - openxFactory's help golden reads the tree at 32 from phase 3's pin. It
    is no surface 11.1 declares, so no arc landing regenerates it. A
    non-arc openxFactory PR ahead of T094, in T066's both-pins form, adds
    the phase-3 golden under `tests/domain_profile/fixtures/`, regenerated
    from T087's commit. That golden also carries T070's `--local`, T079's
    and T080's `--model` and auth-kind changes, and T084's program rename
    to `opendox` (the holder's ruling E1 (a), recorded with `5970369724`).

  This bookkeeping amendment does not itself touch a falsifier. Carried out
  by T086, and by the non-arc PR ahead of T094.

  **Landed 2026-09-27** (T038): openDox-code#48 → `796838e8`.
  `[project.scripts] opendox = "opendox.cli:main"`; the runtime verbs are
  reached through the default profile's `SUBCOMMAND_EXTENSIONS` (batch A's
  addendum) and `opendox-runtime` stays an alias; `opendox --help` exits 0
  (`evidence/checkpoint-phase1.md` § 6). Correction (research R16 item 5,
  non-normative): Q-R4 is recorded at `runtime/cli.py:39-42`, where the box
  cites `:40-46`. The same landing rewrote that record to say where the verbs
  were wired.
- [x] 10.2 The web bundle is served by that entry point and is reachable in a
  browser from an openDox-only install. openDox-code carries **42** web files,
  self-contained by declaration (`src/opendox/web/index.html`: *"All assets are
  local/vendored: no CDN, no external fonts, no remote scripts"*), and **nothing
  serves them**: `serve.py` will not import, and `runtime/app.py` mounts no
  `StaticFiles` — its routes are `/livez`, `/readyz` and `/api/v1`. The bundle is
  not the gap; the door is.

  **Landed 2026-10-03** (T075): openDox-code#73 → `9197ccdd`. The installed
  entry point serves all 42 bundle files, `vendor/.gitkeep` included
  (`web/**/.*` added to the package data); an installed wheel run outside a
  checkout fetches each file with the tree's bytes
  (`evidence/f10.1-run.md` § 2).
- [x] 10.2a `intent-feed.js` stays at openxFactory under RULED OQ-F and is NOT
  owed to openDox; openDox's replacement is `views/intent-binding.js`. Do not
  count it as a missing file.

  **Landed 2026-10-03** (T075): openDox-code#73 → `9197ccdd`. 10.2a is a
  declaration: `views/intent-feed.js` stays at openxFactory (RULED OQ-F) and is
  not owed; `views/intent-binding.js` reaches it only by a dynamic `import()`,
  and the module graph walk stays inside the 42-file bundle.
- [x] 10.3 **The assembly root DOCUMENTS the entry point; it does not host it.**
  `openDox/Makefile` carries a row in `contracts/shape-pin.yaml` (`:49-50`), and
  `AGENTS-shape.md` § "Never edit a file that has a row" is explicit: *"An edit
  in place is reported as DRIFT and refused."* A `run`/`serve` target added there
  would red `make pins`, and the lawful route would be an upstream change in
  `opensoft/openRepoShape` binding EVERY project that carries the shape. So the
  entry point is a `[project.scripts]` console script at the CODE leg (10.1),
  which is where the shape's own "What goes where" puts *"the implementation and
  its tests"*; the root's `README.md` has no shape-pin row and is the project's
  own to edit, so it documents and points at the command.

  **AMENDED — T007 Batch H (`5850003126`; Ruled R1Q15 (b), R1Q16 (iii)):**
  The command the root's `README.md` documents is the standalone install and
  its one start: `pip install "opendox[local]"`, then
  `opendox generate-and-open --local …`. The flag selects the local mode
  explicitly (13.4 as this batch amends it), and the `local` extra carries
  the bundled server that mode starts (13.1 as this batch amends it). After
  the install, that start is the single command requirement 10's second
  scenario has a user run. The entry point is still the code leg's console
  script, and no `Makefile` target is added, for the reason above. Carried
  out by T070 and T076.

  **Landed 2026-10-05** (T076, T101, then T099): the openDox root's `README.md`
  documents the standalone install and its one start,
  `pip install "opendox[local]"` then `opendox generate-and-open --local …`, and
  adds no `make` target (T076, openDox#17 → `504324de`). T101 adds the release
  workflow and the version bump to 0.1.0 (openDox-code#78 → `d59f3f26`,
  openDox-code#79 → `dede32b4`), and T099 publishes that commit at the cut. The
  annotated tag `v0.1.0` names openDox-code `dede32b4`, the commit the openDox
  root pins, and openDox-code's `release` run 37339111713, dispatched on that
  tag, succeeds in all four of its jobs: `build and verify`,
  `publish to TestPyPI (the dry run)`, `install opendox[local] from TestPyPI`
  and `publish to PyPI`, with its step
  `PyPI serves the files the build job verified`. PyPI serves `opendox` 0.1.0 as
  `opendox-0.1.0-py3-none-any.whl` (sha256 `8ecea00db6f9…`) and
  `opendox-0.1.0.tar.gz` (sha256 `56869b6208a8…`). The root README PR,
  openDox#19 → `d77f8cbf`, then replaces the stand-in paragraph: the install
  line now resolves from PyPI as written, and no paragraph says that no release
  is published.
- [x] **FALSIFIED BY** (clean checkout of openDox-code ONLY, fresh venv, no
  sibling installed — the server is started in the BACKGROUND with a readiness
  wait so the sequence runs to completion unattended):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v10"                      # a FRESH environment: nothing already installed stands in
      . "$W/v10/bin/activate"
      pip install .
      if python -c "import openxdox" 2>/dev/null; then echo "FAIL: sibling present"; exit 1; fi
      opendox --help >/dev/null                       # the console script MUST exist
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      R=$(mktemp -d)/plain-documents
      cp -r tests/fixtures/plain-documents "$R"   # a FRESH repository (preamble)
      git -C "$R" init -q
      git -C "$R" add -A
      git -C "$R" commit -qm fixture
      opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8080 &
      SERVER=$!
      trap 'kill "$SERVER" 2>/dev/null || true' EXIT   # cleanup cannot mask the verdict
      ready=0
      for _ in $(seq 1 30); do
        if curl -sf http://127.0.0.1:8080/ >/dev/null; then ready=1; break; fi
        sleep 1
      done
      test "$ready" -eq 1                              # a server that never started FAILS here
      curl -sf http://127.0.0.1:8080/ > "$W/bundle.html"   # no pipeline: curl's status is the status
      grep -qi '<html' "$W/bundle.html"                # and it is really the bundle

  `opendox --help` exits 0, the readiness loop must SUCCEED within 30s or `test`
  fails the sequence, and the fetched body must really be HTML — the earlier form
  of this box could pass with a server that never started, because `kill` masked
  the preceding status and `curl | head` hid a failed fetch. Today `opendox` does not exist as a
  console script, there is no `__main__.py`, and nothing serves `web/` — the
  runtime's `app.py` mounts no `StaticFiles` and declares only `/livez`,
  `/readyz` and `/api/v1`.

  **AMENDED — T007 Batch H (`5850003126`; Ruled R1Q15 (b), R1Q16 (iii)):**
  F10.1's install line and its start line are amended, and `opendox --help`
  stays its first assertion. `pip install .` becomes
  `pip install ".[local]"`, and the start becomes
  `opendox generate-and-open --local …`: the flag follows the verb, as every
  option does (10.1), and the rest of that line stands as written. The
  install line follows from R1Q15 (b) together with R1Q16 (iii): the start
  passes `--local`, and the local mode's server arrives only with the extra
  (13.1 as this batch amends it). F13.1 installs the same extra, so the two
  still share one install line. F13.1's last probe sets neither the flag nor
  the setting, and it still refuses, naming `OPENDOX_OIDC_ISSUER`, so the two
  falsifiers no longer collide (R1Q15). This bookkeeping amendment does not
  itself touch the command above: T077 runs it as amended. Carried out by
  T070 and T077.

  **Landed 2026-10-03** (T077, openxFactory#1223 → `f261fefa`): F10.1, extracted
  byte for byte from #1144 with batch H's two lines (`pip install ".[local]"`,
  `generate-and-open --local`), exits 0 from a fresh clone at openDox-code
  `8e377823`: the bundled PostgreSQL migrates `['0001', '0002']`, the snapshot
  validates with 0 violations, and `/` is byte-identical to
  `src/opendox/web/index.html` (`evidence/f10.1-run.md`).

## Group 11 — Requirement 1: the guard holds (openxFactory)

- [ ] 11.0 **Every commit this arc lands, in EVERY repository it touches —
  openxFactory, openDox-code, openXdox-code, openDox and openXdox — carries the trailer
  `Arc: neutral-product-standalone-operability`**, checked at each PR's review
  like the `Lane:` line. The falsifiers in 5.4a and 12.5 read it in
  openXdox-code, and they assert the set is NON-EMPTY there, because the arc must
  land at least 9.2's whole-suite check and 5.4a's generator contribution in that
  repository; 5.3a's facet landed before the arc, as openXdox-code#26. An empty
  set would mean the
  trailer was dropped, not that nothing was edited. **Every LANDING carries it
  too**: a squash commit because the PR body does, and a merge commit because
  the lander writes it into the merge message. The three guards measure each
  landing on `main` against `main` before it, so the landing is the commit that
  must name the arc. That trailer is how the guard below finds THE ARC'S OWN
  landings. The alternative, diffing `main` between two commits, measures
  everything that reached `main` in between, and in a shared repository that is
  every other lane's work. Such a guard would flag unrelated landings, or, with a
  pathspec narrow enough to avoid them, miss the arc's own edits outside it.

  **AMENDED — T007 Batch A (`5817152735`; Ruled R1Q20 (a)):** An addendum.
  Bookkeeping is not an arc landing and carries no `Arc:` trailer: the
  Speckit feature files, #1144's ticks, evidence notes and amendments, and
  interim guard output. Carried out by T091.
- [ ] 11.1 At the close of the arc, a diff of openxFactory across every group
  shows: no `scripts/doc_health/` family moved, no `openspec/specs/` capability
  removed, no corpus document moved, no intent-plane schema moved, and no
  integration test moved. openxFactory's edits are exactly three kinds, and none
  moves anything. First, carve-manifest ANNOTATIONS recording each closed reach.
  Each is prose in the `note` that an `edits[]` entry already admits
  (`scripts/validate-carve-manifest.py:689`, `EDIT_KEYS`), added where there was
  none or extended, never rewritten, so the manifest's closed grammar does not
  widen to hold them. Second, the HOST WIRING of 4.1 and 4.3, in
  `scripts/opendox_host.py` and `scripts/profile_openxfactory.py`, with its tests
  under `tests/domain_profile/`. Third, the PIN PAIRS of 9.5, one per assembly
  root: the `openDox` gitlink with `contracts/opendox-pin.yaml`, and the
  `openXdox` gitlink with `contracts/openxdox-pin.yaml`.

  **Addendum (Copilot, opensoft/openxFactory#1202; the "exactly three
  kinds" above is UNCHANGED prose, per T007's own rule that an amendment
  touches no requirement text): two more kinds joined it, each already
  RULED and each recorded as its own AMENDED paragraph below the guard —
  never here, so this sentence's original count stays exactly what it
  said the day #1144 landed.** Fourth, NAMED openxFactory composition
  tests (`COMPOSITION_TESTS`; T007 batch A, R1Q2 (a)). Fifth, the SEVEN
  paths T007 batch E found on no surface at all, each admitted by name
  (`ADMITTED_ARC_EDITS`; RULED, `#656` comment `5890601202`, "Named
  closed list"). Both are edited-or-added-never-removed, exactly as the
  three above; see the guard for the exact, current, five-way `elif`.
- [ ] **FALSIFIED BY** (openxFactory checkout, at the close of the arc).
  **`PACKET_MERGE` is THIS PACKET'S OWN MERGE COMMIT, not a pre-authoring
  commit.** The guard measures what the ARC does to openxFactory. The packet's
  own filing artifacts are the FILING, not the arc: the `openspec/changes/`
  directory, the README bullet and the machine-seeded
  `tests/sequenced_after/corpus-ledger.yaml` row. Defining the base any earlier
  makes the command self-failing, because this packet necessarily edits the
  ledger it would then flag:

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      # THE ARC'S OWN LANDINGS (11.0), not everything that reached main meanwhile:
      : "${PACKET_MERGE:?set PACKET_MERGE to the merge commit of this packet on main}"
      : "${ARC_TIP:?set ARC_TIP to the last realization commit before the archive act}"
      git log --first-parent --format=%H --grep='^Arc: neutral-product-standalone-operability$' \
        "$PACKET_MERGE..$ARC_TIP" > "$W/arc-commits.txt"       # the arc's LANDINGS on main (11.0)
      test -s "$W/arc-commits.txt"                          # 11.1's annotations exist, so an empty list measured nothing
      : > "$W/arc-changes.tsv"
      while read -r c; do                                   # each landing against main before it: WHOLE repository, no pathspec
        git diff --no-renames --name-status "$c^1" "$c" > "$W/arc-one.txt"   # a rename reads as a deletion plus an addition
        while IFS=$'\t' read -r s p; do printf '%s\t%s\t%s\n' "$c" "$s" "$p" >> "$W/arc-changes.tsv"; done < "$W/arc-one.txt"
      done < "$W/arc-commits.txt"
      python3 - "$W/arc-changes.tsv" <<'PY'
      import copy, subprocess, sys, yaml
      MANIFEST = "docs/opendox-carve-manifest.yaml"
      HOST = {"scripts/opendox_host.py", "scripts/profile_openxfactory.py"}   # 11.1's host wiring
      HOST_TESTS = "tests/domain_profile/"
      PIN_PAIRS = {"openDox", "contracts/opendox-pin.yaml",                  # 9.5, each pair in one commit
                   "openXdox", "contracts/openxdox-pin.yaml"}
      # T007 batch A (5817152735; R1Q2 (a); R1Q22 (a)) landed here by T093
      # (P1-L, T017/T018): a fourth declared surface, named openxFactory
      # composition tests. T007 batch E (openxFactory#1183, LANDED) named
      # the final four paths phase 1 moved, edited or found.
      COMPOSITION_TESTS = {
          "tests/ideation-dashboard/test_extension_point_parity.py",         # batch A
          "tests/ideation-dashboard/test_serve_column_split.py",             # batch A
          "tests/ideation-dashboard/test_authoring_classify_derivation.py",  # P1-K (#1181)
          "tests/ideation-dashboard/test_doxbench_status_exemption.py",      # P1-K (#1181)
      }
      # RULED (Brett Heap, `#656` comment `5890601202`, 2026-09-29T12:46:55Z:
      # "Named closed list (Recommended)"), landed here by T093 (P1-L,
      # T017/T018): a fifth declared surface, the seven arc edits T007 batch
      # E found on no F11.1 surface, each admitted in principle by
      # `5856475254` (the first two) or by P1-K's writer's committed-pin
      # measurement (the other five). A CLOSED list: later phases extend it
      # only by a further ruling, never by this guard's own code alone.
      ADMITTED_ARC_EDITS = {
          "scripts/route_extension.py",                       # resynced 34802071->7781665d (T047 4303e67c); manifest row docs/opendox-carve-manifest.yaml:2993 carries no edits[], left untouched; cures 260 of 267 committed-pin reds
          "scripts/sync-notebooklm-books.py",                  # session_source_set() now calls register_openxfactory() first (same commit); no carve-manifest row, no prior surface
          "scripts/ideation_dashboard/dashboard_refresh_lane.py",   # RENDER_LEG_MODULES gains corpus_adapter/doxbench_packet/serve_wire/workbench (paired with the seal test below); red at ANY pin, a standing #1166 gap
          "tests/ideation-dashboard/test_dashboard_source_seal.py", # RENDER_UNIT_IMPORTS gains the same four modules T046's opendox_host.seams() imports (paired with dashboard_refresh_lane.py above)
          "tests/openxdox_pin/test_openxdox_pin_verifier.py",  # test_ruling_q7_two_direct_upstreams_in_lockstep's snapshot literal moves on every pin bump by its own comment's design (dc7aa08f->663ac683 here)
          "docs/opendox-carve-admissions.yaml",                # gains created: entries (each since: the landing commit) for every file this PR newly places under a declared surface (paired with the arrival test below)
          "tests/carve_arrival/test_verify_carve_arrival.py",  # the arrivals-registry verifying suite moves with docs/opendox-carve-admissions.yaml above
      }
      def manifest_at(rev):
          out = subprocess.run(["git", "show", f"{rev}:{MANIFEST}"], check=True, capture_output=True, text=True).stdout
          return yaml.safe_load(out)
      def notes(doc):
          return [[e.get("note") for e in (row.get("edits") or [])] for row in doc["rows"]]
      def without_notes(doc):
          doc = copy.deepcopy(doc)
          for row in doc["rows"]:
              for e in row.get("edits") or []:
                  e.pop("note", None)
          return doc
      breach, annotated = [], 0
      for c, s, p in (l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()):
          if s not in ("A", "M"):                       # requirement 1's third scenario: a far side is never deleted
              breach.append(f"{c[:12]}: {'deleted' if s == 'D' else 'changed the type of'} {p}")
          elif p in HOST or p.startswith(HOST_TESTS) or p in PIN_PAIRS or p in COMPOSITION_TESTS or p in ADMITTED_ARC_EDITS:
              continue                                  # a declared surface of the arc (11.1)
          elif p != MANIFEST:
              breach.append(f"{c[:12]}: touched {p}")
          else:
              before, after = manifest_at(f"{c}^1"), manifest_at(c)
              if without_notes(before) != without_notes(after):
                  breach.append(f"{c[:12]}: changed the manifest beyond an edit's note (a row, a field, a digest)")
                  continue
              for old_row, new_row in zip(notes(before), notes(after)):
                  for old, new in zip(old_row, new_row):
                      if old != new:
                          annotated += 1
                          if old is not None and not (new or "").startswith(old):
                              breach.append(f"{c[:12]}: rewrote an existing note instead of extending it")
      if breach:
          sys.exit("FAIL: the arc changed what requirement 1 keeps:\n  " + "\n  ".join(breach))
      print(f"requirement 1 holds: {annotated} note(s) annotated, every other path a declared surface (11.1)")
      PY

  **The guard reads CONTENT, not only names. It covers the WHOLE repository, and
  only the arc.** There is no pathspec, so a change to `README.md`, `.github/`,
  `pyproject.toml` or any other root path is seen. The commits measured are the
  arc's LANDINGS: the commits on `main`'s first-parent line that carry 11.0's
  trailer. Another lane's landing in the same window is therefore not mistaken
  for the arc's. **Each landing is diffed against `main` before it**, so what is
  measured is the whole of what that landing brought, whatever its shape. A
  squash commit's diff is its PR. A merge landing's diff against its first
  parent is the PR's net change, and that includes every commit on the branch,
  an untrailered one included, and any change the merge made itself. That is
  why the guard walks landings and not branch commits. A branch commit that
  forgot the trailer would be skipped by a commit walk. A combined diff (`git
  diff-tree -c`) of the merge that lands it would then omit the change too,
  because the result matches one parent. Merges of `main` into an arc branch
  never appear here at all, because they are not on `main`'s first-parent line,
  so no other lane's content is charged to the arc.

  Every path must be one of 11.1's three declared surfaces: the host wiring
  (`scripts/opendox_host.py`, `scripts/profile_openxfactory.py`, and tests under
  `tests/domain_profile/`), the two pin pairs (the `openDox` gitlink with
  `contracts/opendox-pin.yaml`, and the `openXdox` gitlink with
  `contracts/openxdox-pin.yaml`, which `scripts/verify-opendox-pin.py` and
  `scripts/verify-openxdox-pin.py` hold together), or
  `docs/opendox-carve-manifest.yaml`. The manifest is then
  compared by CONTENT against `main` before the landing. With every `edits[].note`
  removed, the two documents must be EQUAL. No row is added, removed or
  reordered, and no disposition, destination, line list or digest moves. A note
  that already existed may only be EXTENDED, so an annotation cannot erase the
  record it annotates.

  **A declared surface may be EDITED and never REMOVED.** Each landing is read
  with `--name-status --no-renames`, so a rename reads as a deletion plus an
  addition, and a deletion or a change of file type is a breach whatever the
  path, a host-wiring file or a pin file included. Requirement 1's third
  scenario refuses closing a reach by deleting the far side, and a host deleted
  instead of rewired is exactly that; an allow-list that let a declared path be
  deleted would admit it.

  **Nothing is exempt.** The ledger row this packet seeds landed with the filing,
  before `PACKET_MERGE`. An arc landing that touches
  `tests/sequenced_after/corpus-ledger.yaml` is therefore a breach like any other.
  So is one that touches a promoted spec: the archive act that promotes this
  capability is the FILING's bookkeeping, like this packet's own merge, and lies
  outside `ARC_TIP`.

  Every intermediate list is captured to a file first, so a failing `git` fails
  under `set -e` instead of handing the check an empty list that would read as a
  pass. The parse needs PyYAML, which `scripts/validate-carve-manifest.py` itself
  imports.

  The guard was run as committed against a scratch repository carrying the real
  manifest. It passed a squash landing of host wiring and a note, another lane's
  untrailered landings, a merge of `main` into an arc branch, and a trailered
  merge landing. It refused an untrailered edit to a check family hidden inside
  a trailered merge landing, a ledger edit, and — since the deletion rule — a
  landing that deletes a host-wiring file, one that renames it, one that deletes
  a host test and one that deletes the pin file. The content check's refusals of
  a rewritten note and of a changed digest were run the same way, and were re-run
  with the deletion rule in place. With both pin pairs declared, the scratch
  repository carries the `openDox`, `openXdox` and one undeclared gitlink as real
  gitlinks. The guard passed landings that move each pair in one commit, and it
  refused one that deletes `contracts/openxdox-pin.yaml`, one that deletes the
  `openXdox` gitlink and one that moves the undeclared gitlink. The guard before
  the openXdox pair was declared refused the openXdox pair's move.

  **AMENDED — T007 Batch A (`5817152735`; Ruled R1Q2 (a); R1Q22 (a); amends
  11.1 and this falsifier, F11.1):** A fourth declared surface: NAMED
  openxFactory composition tests, which may be edited or added and are never
  removed. The guard IS TO GAIN `COMPOSITION_TESTS =
  {"tests/ideation-dashboard/test_extension_point_parity.py",
  "tests/ideation-dashboard/test_serve_column_split.py"}` beside `HOST` — this
  bookkeeping amendment records that future edit; it does NOT itself touch
  the executable Python above, which still checks only `HOST`, `HOST_TESTS`
  and `PIN_PAIRS` until it lands. T045, T093 and T094 add the set (and the
  `elif p in HOST or ... or p in COMPOSITION_TESTS:` arm that reads it) when
  they land; until then, an edit to either named composition test is still
  correctly reported as `touched ...` by the falsifier as written. Batch E
  adds a path before the landing that adds it (T034, T035), or that T047's
  `pytest-suite` run finds. Also an addendum to 11.1: the manifest records
  the carve as it arrived, so an arc edit to a carved file needs no
  declared-edit act. Carried out by T045, T093, T094.

  **LANDED — T093 (P1-L, T017/T018), 2026-09-29:** the executable Python
  above now carries `COMPOSITION_TESTS` (the four paths batch E names
  below) and its `elif` arm, beside a fifth declared surface,
  `ADMITTED_ARC_EDITS`, RULED by Brett Heap (`#656` comment `5890601202`,
  2026-09-29T12:46:55Z: "Named closed list (Recommended)") for the seven
  paths batch E found on no surface at all. See that ruling, and the
  amended runs it required, where batch E's text below used to read
  "UNRESOLVED".

  **AMENDED — T007 Batch E (`5817152735`; Ruled R1Q2 (a), R1Q22 (a); the
  specific paths and edits below are `5856475254` (P1-K's three questions),
  T035's own hand-off (openDox-code#51), and P1-K's writer's committed-pin
  measurement (openxFactory#1181, `PROGRESS-T047.md` § "THE COMMITTED-PIN
  RED-TEST LIST", runs T1/T3/T4), each addressed to this batch by name):**
  Batch A widened the guard to `COMPOSITION_TESTS`; this batch names every
  path phase 1 has actually moved, edited or found, now that the full
  committed-pin measurement is in. At openDox `663ac683` (code `2d116415`)
  and openXdox `6495ba98` (code `6158151e`), `pytest tests/ -q -m "not
  postgres"` gives 266 failed, 1 collection error with #1181's host wiring
  alone and nothing else (run T1); at #1181's fixing commits merged with
  `main` `e369cb25` (run T4, head `f79a72f3`), it gives 8886 passed, 6
  skipped, 0 failed, 0 errors — the same 6 skips `main` has. Every one of
  the 267 committed-pin reds is one of the causes below.

  **Four paths join `COMPOSITION_TESTS`** — batch A's original two,
  unchanged, plus P1-K's two, each re-described below at the fuller cause
  its writer's measurement found:

  - `tests/ideation-dashboard/test_authoring_classify_derivation.py::test_the_gate_reaches_the_corpus_only_through_the_two_public_names`.
    T020/T021 made `authoring.py` reach the home corpus through the
    REGISTERED seam, `corpus_adapter.home()`, alone: at the pinned leg it
    binds no name out of the adapter package (`bound == []`, was
    `["home_corpus"]`), and a new second assertion checks the two public
    names it takes from the interface module instead
    (`sorted(interface) == ["DocumentId", "home"]`).
  - `tests/ideation-dashboard/test_doxbench_status_exemption.py`. TWO
    edits, not one: (i)
    `test_the_dependence_on_the_carved_rail_sits_at_exactly_one_line`'s
    assertion moves from "exactly one import" to `seam_lines == []` — T027
    removed the packet module's only import of the status-exemption rail;
    the host registers it now (T046) and the module reads the
    registration — plus a new assertion naming the rail's only readers
    (`_status_exemption`, beside the three registration calls). (ii) A
    separate cause the committed-pin run alone found: importing this file
    now runs openXdox-code `6158151e`'s own
    `from conftest import assert_not_at_this_leg, carved_module_path`
    (through its `test_doxbench_packet` import), and this directory's
    conftest has neither, which stopped collection outright. The fix lends
    both names onto this directory's conftest module as refusals, for the
    one import, inside a `try`/`finally` that removes them again straight
    after — nothing here can call them, and the conftest is left as it was.

  Both files stay in `tests/ideation-dashboard/`, are edited, not moved or
  created, and each pins something openDox- or openXdox-owned — the
  adapter seam's public names, and the registered status-exemption rail —
  so both are compositions in the deep sense, not only the structural one.

  **Six more paths — T034's two, T035's four — do NOT join
  `COMPOSITION_TESTS`, correcting this batch's own earlier, WRONG
  proposal.** T034 (openDox-code#50 → `71b631bc`) moves four cases (the
  outline model's `doc_health` case, and three memory-gateway roster
  cases); T035 (openDox-code#51 → `80acead1`) moves nine more and adds one
  fresh, into four destinations its own PR body addresses to this batch by
  name. This batch's first proposal put all six destinations under
  `tests/ideation-dashboard/`, naming each in `COMPOSITION_TESTS`. **P1-K's
  writer's measurement found that proposal INFEASIBLE, not merely
  unwise**: `scripts/validate-carve-manifest.py` REFUSES
  `carve-file-undeclared` for any NEW file under `tests/ideation-dashboard/`,
  because the carve's `moved_paths:` surface already covers the whole
  directory, closed to undeclared arrivals — a different refusal from
  anything a `COMPOSITION_TESTS` entry could admit. The six land under
  `tests/domain_profile/` instead, same basenames, verified directly on
  #1181's head:

  - `tests/domain_profile/test_outline_template_agreement.py` — T034's
    outline case.
  - `tests/domain_profile/test_memory_gateway_roster.py` — T034's three
    memory-gateway cases.
  - `tests/domain_profile/test_workbench_manifest_validation.py` — T035, 3
    cases (from `test_workbench.py`); the pinned validator openXdox-code
    now carries.
  - `tests/domain_profile/test_workbench_scoped_doc_health.py` — T035, 3
    cases (same source file); the registered `doc_health` seam (T026/T046)
    and its `base-repo` fixture.
  - `tests/domain_profile/test_session_worktree_book_scan.py` — T035, 2 of
    its 3 proposed cases
    (`test_session_worktrees_never_reach_a_lifecycle_book`,
    `test_pinned_factory_paths_never_admits_a_worktree_container`).
    **`test_worktree_container_is_gitignored_in_the_aggregation_repo` is
    HELD OUT**: it SKIPS wherever no aggregation checkout exists, which is
    every CI run, and landing it would move `pytest-suite`'s
    `EXPECT_SKIPPED` from 5 to 6 (opensoft/openxFactory#1195 has since
    landed the hermeticity-probe repair, moving the pin 6 → 5; this was
    "6 to 7" before that landing). Held, not decided against; a later task
    takes it up. *(Taken up at T049, 2026-09-29: the phase-1 checkpoint
    found the case in no suite, so on the holder's decision it landed in
    this file by opensoft/openxFactory#1203 → `08e97c27`, which moved
    `EXPECT_SKIPPED` from 5 to 6.)*
  - `tests/domain_profile/test_doxbench_chat_ceiling.py` — T035's one
    moved case, plus one it adds fresh
    (`test_the_browser_ceiling_equals_the_servers_ceiling`, pinning one
    side of a triangle whose openXdox-code twin T041's exclusion hides for
    now). *(Corrected at T049, 2026-09-29: T035 added that fresh case to
    openDox-code's own `tests/test_doxbench_chat_view.py`, where `2d116415`
    still carries it, not to this file, which holds only the moved case.)*

  None of these six needs a `COMPOSITION_TESTS` entry: `tests/domain_profile/`
  is already `HOST_TESTS`, F11.1's SECOND declared surface
  (`p.startswith(HOST_TESTS)`), covering every path under it
  unconditionally, new or edited. **This is a correction, not an update** —
  this batch's first text asked for six entries at paths that could never
  have been created there.

  **T035's fifth destination, `test_hermeticity_probe_routes.py`, still
  does NOT join anything here** — reaffirming this batch's SECOND answer
  to T035's open question (reversed from its first, on an earlier Copilot
  finding at this PR: see the branch's commit history). It pins nothing
  about the composition; it lands as a plain, non-`Arc:`-trailered
  openxFactory test in its own PR (T066's precedent), unclaimed as of this
  writing. P1-K's writer's measurement found it already: two of its three
  cases fail today and the third passes, all through
  `tests/notebooklm/test_hermeticity_guard.py:87`'s stale
  `find_spec("ideation_dashboard.workbench")` probe — a fourth
  `EXPECT_SKIPPED` question that PR must answer, not this one.

  Once T045, T093 and T094 land it, `COMPOSITION_TESTS` reads:

      COMPOSITION_TESTS = {
          "tests/ideation-dashboard/test_extension_point_parity.py",         # batch A
          "tests/ideation-dashboard/test_serve_column_split.py",             # batch A
          "tests/ideation-dashboard/test_authoring_classify_derivation.py",  # P1-K (#1181)
          "tests/ideation-dashboard/test_doxbench_status_exemption.py",      # P1-K (#1181)
      }

  — unchanged in SIZE from batch A's own first proposal, though not in
  content: `test_extension_point_parity.py` and `test_serve_column_split.py`
  are ALSO among the 260 reds the stale `route_extension.py` replica
  causes (below), an ordinary edit inside the composition each already
  names, not a new cause.

  **LANDED — T093 (P1-L, T017/T018), 2026-09-29** (superseding this
  paragraph's original close, "this bookkeeping amendment does not itself
  touch the executable Python above, which still checks batch A's two-path
  set until T045, T093 and T094 land it"): the executable Python above now
  carries exactly this four-path `COMPOSITION_TESTS`.

  **Seven paths sit on NO F11.1 surface at all, and each is an ADMITTED
  arc edit, not a composition test.** `5856475254` items 1-2 name the
  first two; P1-K's writer's committed-pin measurement found the other
  five. Every one is admitted IN PRINCIPLE — no further ruling is needed
  before T047 lands them — but each still needs a GUARD-CODE mechanism
  this paragraph records the NEED for and does not itself supply:

  - **`scripts/route_extension.py`**: openDox-code#40 (T010, `0f10b1f5`)
    changed `src/route_extension.py` from blob
    `34802071d5b9e417f6c29c6929db69f518f91cce` to
    `7781665d9ae0d4be298cd7d9cbe625666f7481ee` (62817 bytes, sha256
    `d81124e62dba9df33abe44f3eb467188c98156f002cc7a92e297cd689da87515`), so
    both carved replicas of the route-extension seam were stale. **260 of
    the 267 committed-pin reds share this ONE cause**
    (`AttributeError: module 'route_extension' has no attribute
    'collect_handler_contributions'`), across 11 files including two
    `COMPOSITION_TESTS` paths already named above (an ordinary edit inside
    a composition each already admits, not a new cause). T047's resync
    (`4303e67c`) cures every one. openxFactory's copy is a
    `not_moved / replicated_at_destination` row
    (`docs/opendox-carve-manifest.yaml:2993-2996`) whose ONLY field is
    `evidence:` — **verified directly on #1181's resync commit: the row is
    LEFT UNTOUCHED, no `edits:` block added.** R1Q22 (a) ("no declared-edit
    act precedes an arc edit to a carved file") removes the need for a
    SEPARATE RULING before the resync; it does not by itself make F11.1's
    `elif p != MANIFEST: breach` branch admit this path — and, now
    confirmed rather than merely suspected, the resync does not go through
    the manifest at all. The row's `edits:` grammar (RULED Q-L7 (a);
    `docs/opendox-carve-manifest.yaml:114-120`) would in any case only
    cover lines permitted to diverge from the blob AT THE CARVE COMMIT, a
    narrower shape than a wholesale resync to a later upstream commit.
    T045, T093 and T094 (or a further ruling, if the mechanism itself needs
    Brett's word) choose the actual guard-code path when T047 lands; this
    paragraph records only that the edit is admitted, not the mechanism.
    **openXdox-code's twin replica has already LANDED the same resync**
    (openXdox-code#29, merged `d84b5048`), re-verified directly on that
    repo's `main` today at `6158151e` — a different repository's own arc
    edit, outside this guard, recorded here only so the pair reads as one
    repair.
  - **`scripts/sync-notebooklm-books.py`**: its `--session-ref` path now
    calls `register_openxfactory()` before reaching
    `workbench.session_documents` (`4303e67c`, the same commit as the
    resync above). No carve-manifest row, no current surface — not `HOST`,
    `HOST_TESTS`, a `PIN_PAIR`, `COMPOSITION_TESTS` (it is not a test) or
    the manifest.
  - **`scripts/ideation_dashboard/dashboard_refresh_lane.py`** and
    **`tests/ideation-dashboard/test_dashboard_source_seal.py`**: two
    cases
    (`test_the_render_leg_modules_are_what_the_render_unit_imports_by_name`,
    `test_the_serve_leg_modules_are_what_the_serve_entry_imports_by_name`)
    broke when openxFactory#1166 merged with T046: `opendox_host.seams()`
    imports `corpus_adapter`, `doxbench_packet`, `serve_wire` and
    `workbench`, none yet named in the seal's
    `RENDER_UNIT_IMPORTS`/`RENDER_LEG_MODULES`. Fixed (`b05175f7`) by
    adding all four. **Red at ANY pin** — a standing gap #1166 left, not
    something T047's specific pin bump caused, found only because this
    measurement ran the whole suite.
  - **`tests/openxdox_pin/test_openxdox_pin_verifier.py::test_ruling_q7_two_direct_upstreams_in_lockstep`**:
    a snapshot literal that its own comment says moves on every pin bump,
    `dc7aa08f` → `663ac683` (`b05175f7`).
  - **`docs/opendox-carve-admissions.yaml`** and
    **`tests/carve_arrival/test_verify_carve_arrival.py`**: the arrivals
    registry gains `created:` entries (each with `since:` the landing
    commit) for every file this PR newly places under a declared surface,
    and its own verifying suite moves with it. Neither sits on a current
    F11.1 surface either.

  **RESOLVED — RULED (Brett Heap, `#656` comment `5890601202`,
  2026-09-29T12:46:55Z: "Named closed list (Recommended)"):** F11.1 is
  amended to carry an `ADMITTED_ARC_EDITS` set naming exactly these seven
  paths, each with the reason a bullet above gives, beside `HOST`,
  `HOST_TESTS`, `PIN_PAIRS` and `COMPOSITION_TESTS`. Any other path still
  fails the guard, and later phases extend this list only by a further
  ruling, never by this guard's own code alone. T093 (P1-L, T017/T018)
  landed the amendment in the executable Python above and proved it both
  ways at ARC_TIP `f56c87c6b8d7374d93facd7dfbbf02bd89a86a8b`: FAIL before
  the amendment (`evidence/f11.1-phase1.txt`, the original run, matching
  this paragraph's finding exactly — the same seven paths, no others), PASS
  after it, and FAIL again on a planted eighth path (a negative control,
  never pushed). Carried out by T093.

  *(Kept for the record, superseded by the ruling above rather than
  deleted — this paragraph's finding as first written, 2026-09-28:
  "UNRESOLVED, plainly: no guard-code mechanism exists yet for any of these
  seven — F11.1's falsifier, as it stands, still checks only batch A's
  original two-path `COMPOSITION_TESTS` set (widened to four above), with
  no branch that admits a `route_extension.py`-shaped or
  `sync-notebooklm-books.py`-shaped edit at all. T045, T093 and T094 (or a
  further ruling, where a mechanism needs Brett's word) must choose how the
  guard admits these seven before T047 can pass F11.1 clean; this paragraph
  records only that each edit is admitted IN PRINCIPLE, and why, not the
  mechanism, and does not itself close that gap.")*

  **A carried-over risk, recorded and not actioned** (T035's "Notes for the
  destinations," none of which blocked T035 itself): openxFactory's OWN
  `tests/hermeticity.py` (root-level, not under `tests/ideation-dashboard/`)
  runs the same `find_spec` seam-probe SHAPE that T035 just retired in
  openDox-code's copy. Here it already names the post-carve seams
  (`find_spec(f"opendox.{name}")`, `tests/hermeticity.py:472-484`), and it
  resolves today only because `scripts/ideation_dashboard/` (with
  `carved_reach.py`'s path injection) still sits in this tree. No phase-1
  task removes `scripts/ideation_dashboard/` from openxFactory, so nothing
  acts on this now; T035's writer's own words are the flag for whichever
  future task does: *"When `scripts/ideation_dashboard/` leaves openxFactory,
  its layer 2 goes off just as silently as it was off here"* — silently,
  because a `find_spec` probe that finds nothing degrades to a notice rather
  than a failure, the same escape T035 closed in openDox-code.

  **Every input is now landed and MEASURED; no red is unaccounted for, and**
  (RESOLVED — RULED `#656` comment `5890601202`, 2026-09-29, see above) **the
  guard-code mechanism for that one class of them is now closed, by a named
  list.** T034 (openDox-code#50 → `71b631bc`), T035 (openDox-code#51 → `80acead1`),
  T039 (openDox#13 → `663ac683`, pinning `code` to `2d116415`) and T044
  (openXdox-code#33 → `6158151e`) have all landed; T044 supplies no
  composition-test path (its declared exclusion, at the triple 885/881/4,
  is entirely openXdox-code's own). P1-K's writer's `pytest-suite` run at
  those committed pins (run T1, above) found exactly the 267 reds this
  paragraph accounts for — the four `COMPOSITION_TESTS` edits, the six
  relocated files, the seven admitted arc edits, and T035's held-out
  cases — and the same run at #1181's fixing commits (run T4) finds none.
  That inventory is closed, and so, now, is the guard-code mechanism for
  the seven admitted arc edits — RULED (`#656` comment `5890601202`), landed
  by T093 (P1-L) in the executable Python above. Carried out by T045, T047,
  T093, T094.

## Group 12 — Requirement 11: the neutral submission step (RULED, openDox-code)

**RULED** by Brett Heap, `#656` comment `5783934499`, 2026-09-22T20:49:40Z:
*"add a neutral publish step to the build arc"*. Named **submission** in the
delta, after the fifth of the six ruled words, for the reasons in `design.md`
§ D9 — "publisher" is already taken in this capability for the repository that
publishes the corpus and the contract bundle.

The seam is NOT invented here: `src/opendox/session_pr.py:98-99` already declares
`@runtime_checkable class PullRequestPort(Protocol)` with `push`, `open_or_update`
and `find_open`, and `FakePullRequests` (`:116`) is already a second
implementation. What is missing is a NEUTRAL implementation and a default binding
that does not name a platform.

- [ ] 12.1 **SPLIT THE PROTOCOL; do not bend the platform's one.**
  `PullRequestPort`'s `open_or_update` and `find_open` return a `PullRequest`
  carrying `url`, `number` and `state`. A plain push can implement neither
  operation nor produce that record, so a neutral class that claimed to be a
  `PullRequestPort` would be lying about two-thirds of its interface. The neutral
  act therefore gets its OWN protocol: `session_pr.SubmissionPort`, a
  `@runtime_checkable` `Protocol` with ONE operation, `submit(branch) ->
  Submission`. **`PullRequestPort` is UNCHANGED**: its three operations, its
  `push(self, branch: str) -> None` (`session_pr.py:103`), and FR-030's *"three
  operations, and the absence of every other one"* (`session_pr.py:99-101`). It
  remains the governed host's platform protocol, used by `gate open-pr`, and
  `FakePullRequests` and every existing test keep their meaning.
- [ ] 12.1a **`Submission` is the report requirement 11's third scenario needs.**
  It names the DESTINATION THE WORK REACHED: `remote`, `ref`, and the remote's
  `url` as git resolves it, WITH ANY CREDENTIAL IT CARRIES REDACTED. A git remote
  may embed userinfo (`https://user:<token>@host/…`) or a token in its query
  string, and the verb prints this report (12.4a), so the report names where the
  work went and never what the remote holds. The same holds for a refused or
  failed push's message. Scenario 3 is then asserted rather than inferred from a
  side effect, and scenario 4's refusal is distinguishable from a silent success
  by what `submit` returns, not only by its logs.
- [ ] 12.2 Ship the NEUTRAL DEFAULT **as a named class in `opendox.session_pr`,
  `LocalGitSubmissions`, implementing `SubmissionPort` and constructed exactly as
  `GhPullRequests` is — `LocalGitSubmissions(Path(checkout_root))`, one positional
  argument (`serve.py:934`).** On a plain git repository with a remote attached,
  `submit` pushes the session branch there and returns the 12.1a `Submission`. The
  runtime already models the remote — `runtime/repository_act.py:1131`'s
  `attach_remote(..., executable="git")` takes ANY git remote and writes no
  object, *"which is what makes the eventual move a push, not a migration"*.
- [ ] 12.3 With NO remote attached, say so plainly. Not an opaque failure, not a
  reported success. This is the same refusal discipline `corpus-adapter-seam`
  requires of an unresolvable corpus, applied to an unresolvable destination.
  **The refusal is a named exception, `session_pr.NoSubmissionTarget`, whose
  message names what is missing** — named here so the falsification can catch that
  type and nothing else, which is what separates "refused for the right reason"
  from "raised something".
- [ ] 12.4 **The product's OWN submission binding names no platform.** It is a
  NEW pair of bindings for `SubmissionPort`: `submission_factory` beside
  `pull_request_factory` (`serve.py:766`), and `_submission_port` beside
  `_pull_request_port` (`cli.py:800`). Each defaults, when nothing is injected, to
  `LocalGitSubmissions`. A governed host MAY contribute its own `SubmissionPort`
  through them, for example one that pushes and then opens its pull request. The
  existing `PullRequestPort` bindings keep serving the governed verb they serve
  today. `cli.py:812-814` and `serve.py:933-934` still import and construct
  `GhPullRequests`, but only openXdox's `gate open-pr` reaches them (12.4a), so
  after this box no path of the product's own names a platform. *(An earlier
  draft of this box repointed `pull_request_factory` itself. That would have
  bound a push-only class to a protocol whose other two operations it cannot
  perform.)* `serve.py:1507` records
  that an unset injection *"builds the real `GhPullRequests`"*. The unset default
  becomes the neutral implementation; `GhPullRequests` becomes ONE contributed
  implementation. **NAME THE SUBMISSION REGISTRATION POINT, and keep it SEPARATE
  from the generator's.** The submission seam ALREADY EXISTS and is
  `pull_request_factory` — `serve.py:766` declares it, `:931-932` calls it, and
  `:1505` describes it as *"the same kind of seam"* — so this box repoints its
  UNSET DEFAULT to the neutral implementation rather than inventing a seam. The
  generator seam that task 5.4 declares is a DIFFERENT interface that does not
  exist yet; the two are contributed through the same PATTERN, not through the
  same registration point, and conflating them would make neither implementable.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q2 (a),
  with R2Q3 (a)):** A note on the box's two readings. The NEW pair,
  `submission_factory` and `_submission_port`, is the product's own binding,
  and its unset default is `LocalGitSubmissions`. `pull_request_factory` and
  `_pull_request_port` KEEP `GhPullRequests` as their unset default, and serve
  `gate open-pr` unchanged. The repoint sentences above, from *"The unset
  default becomes the neutral implementation"* to *"this box repoints its
  UNSET DEFAULT to the neutral implementation"* (`:2513-2519` at `main`
  `92010d3e`), and their twins in `design.md` (§ D9's *"requirement 11
  repoints its unset default"*, `:476-478`, and R-G3's *"requirement 11
  repoints its unset DEFAULT"*, `:1059-1061`), are read as the residue of the
  withdrawn draft that the box's own parenthesis records. They move no binding.
  openXdox-code's protected `tests/test_session_snapshot.py:893-916`, which
  asserts that the server's unset port IS `GhPullRequests`, stands. With R2Q3
  (a), no governed host contributes `GhPullRequests` in release 2, so two texts
  go unrealized in release 2, and Brett Heap accepted that by choosing (a) with
  R2Q3 (a): ruling `5783934499`'s third bullet, *"contributed by the governed
  host"*, and 12.5's *"With the host's implementation registered"*. This note
  edits neither, and no line of `design.md`. Carried out by plan 038's T014 and
  T019.
- [ ] 12.4a **GIVE openDox ITS OWN SUBMIT ACT — today it has none, whatever port
  is bound.** Measured at openDox-code `3c3a9e31` and openXdox-code `ab04453d`:
  the ACT of submitting is openXdox's. The CLI verb is `gate open-pr`
  (`src/openxdox/cli_gate.py:634`, `cmd_gate_open_pr`), the engine is
  `execute_open_pr` (`src/openxdox/gate_routes.py:2417`), and the route is
  `POST /actions/gate/open-pr` — all in the governance column. openDox owns the
  port (`session_pr.py`), branch sessions, and both default bindings, and NEITHER
  binding has a caller in openDox: `cli.py:800`'s `_pull_request_port` is reached
  only from openXdox's `cmd_gate_open_pr` (`cli_gate.py:674`), and
  `serve.py:911`'s `_session_pull_requests` only from the gate route. **So a
  standalone openDox cannot submit at all, `gh` or no `gh`**, and repointing a
  default (12.4) that nothing in the product calls would change nothing a
  student can reach. This box adds the neutral verb and route in openDox's OWN
  surface, not under `gate`: CLI `submit --repo-root <repo> --branch
  <session-branch>` and route `POST /actions/session/submit`. Their engine
  obtains its `SubmissionPort` through the bindings 12.4 declares, then returns
  and prints the 12.1a `Submission`. openXdox's `gate open-pr` is UNTOUCHED by this
  box; 12.5 proves it.

  **The route is a SESSION VERB, gated exactly as the governed one is.**
  Measured at openXdox-code `195276b7`: `_handle_gate_action`
  (`src/openxdox/serve_gate.py:68`) refuses, in this order and before any body
  byte is read, a request off loopback (`:73`), a request without the capability
  or a resolved actor (`:78`), and, for a session-bearing verb such as `open-pr`
  (`gate_routes.py:111`), a request that `_not_the_human_console()` (`:105`) finds
  is not the console. The submit route takes the same three clauses in the same
  order, from openDox's own `serve.py` at `1e4a57fb`. The first two are the
  `session` capability, which `compute_capabilities` grants only to a loopback
  bind with a real checkout and a RESOLVED HUMAN ACTOR (`:498`, `:504`). The third
  is the human-console test (`:1224`): the per-serve token, a trusted loopback
  `Host`, a JSON submission, and no foreign `Origin` or `Referer`. **It takes NO
  repository from the request.** It submits a branch of the checkout
  `build_server` was started on, as `gate open-pr` passes
  `checkout_root=Path(self.checkout_root)` (`serve_gate.py:158`), so no caller can
  name another checkout. The hosted plane is the multi-user one, and it carries
  no `session` capability, so the route refuses there before anything else. That
  is deliberate: a push spends the invoking user's own git credentials, and a
  personal credential is what `compute_capabilities`' own docstring says a hosted
  plane must never hold (FR-034, D22). The CLI verb runs as that user, in that
  user's checkout.

  **AMENDED — T007 Batch N (`5963851934`):** An addendum, on where the
  human-console test's per-serve token comes from. Brett Heap's multi-choice
  word of 2026-10-03, verbatim *"Token via the opened URL (Recommended)"*,
  answers adversarial review 2's finding M5. Measured at openDox-code `main`
  `1130e996`, a serve that grants `session` mints the token
  (`mint_console_token`, `serve.py:617`, called at `:1977`) and publishes it
  on `/capabilities` (`:1980`), and the web bundle reads it from there
  (`web/app.js:1459-1471`, `web/views/edit.js:10-26`). So any loopback
  caller can ask for it, another OS user of the same machine included. On a
  STANDALONE plane, the one built from openDox's own default profile, the
  token IS TO reach the page only through the URL the page is opened with.
  The details are the holder's approved design of 2026-10-03:
  - `/capabilities` carries no `console_token`;
  - the entry point that starts the serve writes a private copy, an opener
    file at `<state_dir>/console/<port>.html` under `OPENDOX_STATE_DIR`, the
    state directory 16.3a's trust file uses. The file is mode 0600, in a
    directory of mode 0700. Each missing directory is made by descriptor, the
    file is created without following a link, and the whole path is checked as
    openDox-code#69's bundle checks its own tree. A file already at the copy's
    path is replaced only when it is this user's own regular file of mode 0600
    with one link, an earlier copy for that port. Anything else there (a
    symbolic link, a directory, another user's file, a hard-linked or a
    loosened file) refuses the start by name, and is never followed or
    replaced, and a copy that fails the same checks is refused when it is
    read, at once, since the reader never blocks on what it opens (a FIFO with
    no writer included). The copy never sits where the plane serves files, so
    the state directory and the roots the plane serves do not overlap in
    either direction. A state directory that is, or lies inside, a served root
    is refused by name, which is the holder's own ruling on #1220's review
    (Copilot `r4171166321`, 2026-10-03), beside `5963851934`. So is a served
    root that is, or lies inside, the state directory, such as
    `<state_dir>/console` itself, on the holder's ruling on batch N's review
    (Copilot `r4174345203`, 2026-10-03). A link inside a served root that
    points at the state directory reaches nothing. `/source` already refuses a
    path that leaves its root through a symbolic link
    (`default_registry.resolve_within`, openDox-code `main` `e49b17c3`). The
    static bundle's route follows links inside the bundle's directory, because
    a composed host's web root is made of them, so it answers 404, for GET and
    HEAD, files and listings alike, to any request whose resolved target, the
    file it would finally serve (an automatic index file included), is the
    private copy's directory or lies inside it;
  - the copy forwards to the page with the token in the URL's FRAGMENT,
    `…/index.html#console_token=<token>`, and never in its query, so no
    request line, server log or `Referer` carries it;
  - the start writes the copy, and prints its location as a `file://` URL,
    with or without `--no-open`, and never prints the token or a URL that
    carries it, so standard output and CI logs stay clean. The copy is
    removed when the server stops, and a copy that cannot be written safely
    refuses the start by name, before anything is written, so the server
    never serves.

  A composed host's plane keeps its delivery on `/capabilities` unchanged.
  Every route that requires the token still requires it. So the human-console
  test above is unchanged, and so are the submit route's three refusals in
  their order, and F12's named test of a submission without the token. A
  test that needs a standalone plane's token reads it from the private copy,
  never from `/capabilities`. No falsifier of this change reads the token
  from `/capabilities`: F10.1 fetches only `/`, and F13.1 reads only the
  payload's `install` block, each with its state directory outside the root
  it serves. A tab that kept an earlier serve's token is refused by the next
  serve until the page is opened again through the new copy, and the design
  accepts that limit. The realization's test asserts each point above on a
  standalone serve, the stale-tab limit aside, since that is a limit and not
  a promise, and a composed run shows that a host's `/capabilities` still
  carries the token. This bookkeeping amendment does not itself touch a
  falsifier. Carried out by T104.

  **AMENDED — T007 Batch P (`5982436447`, item 1):** An accepted limit, and
  one more printed line. Brett Heap's multi-choice word of 2026-10-04,
  verbatim *"Hint line, accepted limit (Recommended)"*, answers finding B3
  of the holder's adversarial review of T104 (openDox-code#84). Some
  browsers cannot open the private copy's `file://` URL while the state
  directory is the hidden default (`~/.local/state/opendox`): Ubuntu's
  default snap browser, a Flatpak browser, and a Windows browser opened from
  WSL. The token is never printed, so such a browser has no other way in.
  So the start prints ONE more line, with no token and no URL that carries
  one, saying that a browser which cannot open the file should be used with
  `OPENDOX_STATE_DIR` set to a folder that is not hidden. The openDox root's
  README documents it, and release 1 ships with the limit. Nothing above
  moves: the copy's place, its modes and its checks, the printed `file://`
  location, and the rule that standard output never carries the token. This
  bookkeeping amendment does not itself touch a falsifier. Carried out by
  T104 (the line) and T076 (the README).

  **AMENDED — T007 Batch P (`5982436447`, the holder's ruling B7):** An
  accepted limit within the design above, with no code change. Once the page
  has read the token from the fragment, it drops the fragment from the
  address bar with `history.replaceState`. That cleans only the tab's
  session history. A browser's persistent history, Chromium's
  `Default/History` among them, can still hold
  `…/index.html#console_token=<token>`. That history is this same user's
  data, as the 0600 private copy is, so it hands the token to no one the
  copy does not, and release 1 accepts it. The fragment still never reaches
  a request line, a server log or a `Referer`. This bookkeeping amendment
  does not itself touch a falsifier. Carried out by T104.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q9 (a),
  item 7):** The CLI verb's shape gains `--local`, the same flag
  `generate-and-open` takes (13.4 as batch H amends it): `submit --repo-root
  <repo> --branch <session-branch> [--local]`. It follows the verb, as every
  option does (10.1), and it selects the local install exactly as
  `OPENDOX_INSTALL_MODE=local` does. A flag and a setting that disagree are
  refused, naming both. The route and its three refusals are unchanged. F12.2
  is NOT amended: its `submit` passes neither the flag nor the setting, and it
  runs as ratified, since the CLI verb reads no install mode and only
  `--local` set against `OPENDOX_INSTALL_MODE=hosted` refuses (plan 038's
  N-17). This bookkeeping amendment does not itself touch a falsifier. Carried
  out by plan 038's T015.
- [ ] 12.5 **THE GOVERNED FLOW IS UNCHANGED.** With the host's implementation
  registered, openxFactory's GitHub pull-request flow behaves exactly as today.
  This is a generalization, not a replacement, and 12.5 is the box that proves it.
  **Measured: nothing proves it today.** Sixteen openXdox-code test files drive
  `gate open-pr` through the registered host path or inject `FakePullRequests`
  (`git grep -l` at `ab04453d`), `test_session_verbs.py`,
  `test_session_lifecycle.py` and `test_branch_session.py` among them. **None of
  the sixteen is among the 16 test files openXdox-code's `validate.yml` runs**,
  so the governed flow has no running regression check at all. This
  box's acceptance runs them, and needs Group 9 by name, since the whole suite
  must first be runnable.
- [ ] **FALSIFIED BY** (openXdox-code checkout with the realized openDox installed
  and Group 9 landed; openXdox's registered host path, `FakePullRequests`
  injected, so no network is reached):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      : "${OPENDOX_CODE:?set OPENDOX_CODE to an openDox-code checkout at the tip of the arc}"
      python -m venv --clear "$W/v12b"
      . "$W/v12b/bin/activate"
      pip install ".[test]"
      pip install --force-reinstall --no-deps "$OPENDOX_CODE"   # the REALIZED openDox wins over any pinned one
      # the WHOLE governed set, computed: every suite that drives open-pr or injects the fake
      git grep -l -e 'open-pr' -e 'open_pr' -e 'FakePullRequests' -- 'tests/test_*.py' > "$W/governed.txt"
      test "$(wc -l < "$W/governed.txt")" -ge 16            # 16 at ab04453d; fewer means a proof vanished
      while read -r f; do python -m pytest -q "$f"; done < "$W/governed.txt"
      # ...and not by editing those proofs: no landing of THIS arc (11.0's trailer) touches them
      : "${ARC_BASE:?set ARC_BASE to the commit of this repository before the first landing of the arc here}"
      git log --first-parent --format=%H --grep='^Arc: neutral-product-standalone-operability$' "$ARC_BASE..HEAD" > "$W/x-arc.txt"   # LANDINGS (11.0)
      test -s "$W/x-arc.txt"                                # 11.0: the arc DID land here (9.2 at least), so empty means a dropped trailer
      : > "$W/x-paths.txt"
      while read -r c; do                                   # each landing against main before it
        git diff --name-only "$c^1" "$c" >> "$W/x-paths.txt"
      done < "$W/x-arc.txt"
      python3 - "$W/x-paths.txt" "$W/governed.txt" <<'PY'
      import sys
      touched = {l.strip() for l in open(sys.argv[1]) if l.strip()}
      edited = sorted(touched & {l.strip() for l in open(sys.argv[2]) if l.strip()})
      if edited:
          sys.exit("FAIL: the arc edited the governed flow's own proofs: " + ", ".join(edited))
      PY

  The suites must pass AND must be unedited by the arc, because a regression
  proof the change under test may rewrite proves nothing. **The set is computed,
  not typed.** Every openXdox test file that drives `open-pr` or injects
  `FakePullRequests` is included: 16 at `ab04453d`, where an earlier draft of
  this box listed five of them. The floor of 16 catches a proof that disappears.
  Files are read from a list one per line, so the command behaves the same under
  bash and zsh, which does not word-split a variable. The measurement behind 12.5
  stands: none of the 16 is among the files openXdox's `validate.yml` runs.

  **AMENDED — T007 Batch C (`5817152735`; Ruled R1Q7 (a)):** This falsifier
  and F5.2 both take this amendment. The "unedited by the arc" check IS TO
  SUBTRACT the edits entered in a reviewed allow-list in openXdox-code, such
  as `tests/protected_suite_respellings.yaml` — a file this amendment does
  not itself create. T019 already gives the file its owner
  (`specs/034-opendox-standalone-operation/tasks.md`, T019's re-plan
  bullets, verbatim): *"the first task that makes an admitted edit to a
  protected suite creates the file in its own PR. An entry names its
  landing by that PR's number, since the landing's commit is not known
  inside it."* This amendment does not name that task itself — WHICHEVER
  task turns out to be first, per T019's own rule, creates the file; that
  ownership question belongs to T019's re-plan, not to this bookkeeping
  amendment. Each entry names the suite, the landing, the reference it
  respelled, its review, AND the exact old/new text (or a diff/content
  digest) of the respelling; no edit that weakens an assertion is entered,
  and the PR that adds an entry is reviewed on exactly that basis. Because
  the check subtracts by PATH, not by line, a landing that respells the
  named reference while ALSO weakening a different assertion in the same
  suite would otherwise pass unnoticed: T059/T086 must validate, before
  trusting any subtraction, that the landing's actual diff for that path
  contains ONLY the entry's recorded text; a path whose landing diff does
  not match stays refused, exactly like an unentered edit. This bookkeeping
  amendment does NOT itself touch the Python above: `edited = touched &
  {...}` still computes and refuses on every
  intersection exactly as written, with no allow-list read, until the file
  exists (T019's rule names its owner) and T059/T086 wire the subtraction
  into both falsifiers' checks. Carried out by whichever task T019 names as
  the file's first owner, plus T059, T086.

  **AMENDED — T007 Batch I (`5851950767`; Ruled R1Q26 (a)):** The reviewed
  allow-list that R1Q7 (a) admits for this falsifier (`5817152735`; T007
  Batch C) also admits the two edits to `tests/test_gate_loop_views.py` that
  5.3a's `values` block requires. Each is entered with its reason, and
  neither as a respelling:
  `test_the_display_facet_declares_one_stage_entry_and_nothing_else`, which
  then admits the `values` block beside the one stage, and
  `test_the_overlay_changes_four_words_and_the_named_absence_and_nothing_else`,
  whose changed leaves then include the block's `values.*` leaves once 5.3's
  defaults are neutral. No other assertion of the suite changes. This
  bookkeeping amendment does not itself touch the command above. Carried out
  by T060 and T059.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q8 (a),
  read with ARC-Q2 (a), `6003918488`, as CF-5, `6013547504`):** F12.1 runs
  composed, as F5.2 does under R1Q23 (a); ARC-Q2 (a) (`6003918488`) makes the
  composition its permanent home. Its environment line is amended as batch G
  amended F5.2's: after the two installs, the block IS TO require
  `OPENXFACTORY`, an openxFactory checkout with its submodules initialized, put
  `"$OPENXFACTORY/scripts"` on `PYTHONPATH`, and quote that checkout's commit.
  R2Q8 (a) measured why: fifteen of the 16 suites are entries of openXdox-code's
  declared exclusion under `doc_health` (9.2) and fail to import alone, and
  composed, at openXdox-code `56e1c238`, the 16 read 174 red. R2Q8 (a) said
  *"until the direction arc's realization lands"*; ARC-Q2 (a), the later
  ruling, makes openXdox-code's composed workflow, against a pinned
  openxFactory, the PERMANENT home of what stays composed, the
  governed-behaviour suites among them, so the line does not expire when the
  arc lands (CF-5). The 174 reds are repaired in phase 4 without editing the 16
  suites, except through the reviewed allow-list (batch C, and the CF-4 and
  R-1 (a) notes below, chained as the `--chains` note below says). Nothing else
  in the block changes under this note: the computed set, the floor of 16, the
  loop and the arc-landing check stand as written and as batch C amends it. R1Q6 (d)'s condition, the direction arc DECIDED before this falsifier
  needs the suites, is met by `6003918488`. This bookkeeping amendment does not
  itself touch the command above. Carried out by plan 038's T020 to T029,
  whose composed workflow becomes a required check of openXdox-code after its
  first green run on `main` (N-7b, `6013547504`), and run by its T032 and T063.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6013547504`; Confirmed CF-4,
  H-2):** The reviewed allow-list that R1Q7 (a) admits for this falsifier
  (`5817152735`; batch C, extended by batch I) also admits SEVENTEEN entries
  that respell names the split-opendox CARVE moved before the arc, in commits
  that carry no `Arc:` trailer: `cmd_gate_*` 7, `hosted_index` 3, share paths
  2, Group W 1 and Group S2 4. They are pre-arc carve residue, admitted under
  batch C on the precedent of `5962785556` item 1, where three pre-arc
  carve-residue tests of F5.2's set were repaired under the same allow-list.
  Two readings of batch C were set out, and Brett Heap confirmed this record of
  it (CF-4; *"Accept all as recommended (Recommended)"*): one reads batch C's
  text as admitting any pure respelling, so nothing widens; the other reads
  R1Q7 (a)'s *"a reference to a moved seam"* in its release-1 context as the
  arc's moves, so this stretches batch C. Either way each entry is what batch
  C requires: it names the suite, the landing, the reference it respells, its
  review and the exact old and new text, it weakens no assertion, and the
  landing's diff for that path is exactly the entries' recorded texts (chained,
  as the `--chains` note below says). This bookkeeping amendment does not
  itself touch the command above. Carried out by plan 038's T026.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6013547504`, with
  `6016648451`; Ruled R-1 (a), with W-1 (A)):** Brett Heap's multi-choice
  words of 2026-10-06, verbatim *"Admitted edit kind (Recommended)"* and, on its
  scope, *"Widen the spans, served display (Recommended)"*. For this falsifier,
  the reviewed allow-list also admits a new kind of `edit: admitted` entry, of
  R1Q26 (a)'s sort, that reaches a NAMED MODULE-LEVEL SPAN of a governed suite
  rather than text inside one named test. It exists for
  `tests/test_staging_workbench.py`, one of the 16, whose Node harness text and
  the helpers that copy it sit at module level, outside any test, so no in-test
  entry reaches them. The admitted spans are SIX, at openXdox-code `56e1c238`:
  - the harness constants `_CREATE_HARNESS` (`:492-553`), `_SESSION_HARNESS`
    (`:1008-1094`) and `_HOSTILE_HARNESS` (`:1950-1981`);
  - the three copy helpers `_run_create` (`:562-574`), `_run_session`
    (`:1239-1257`) and `_hostile_descriptors` (`:1997-2008`).

  The helpers copy the model's siblings and hand each harness the SERVED
  governed display. That the served display is reachable in the test process
  is INFERRED, and plan 038's T026 measures it. The governed host's
  registration (plan 038's T020) covers this suite, through T020's
  `tests/conftest.py` and the scan in `tests/test_host_plane.py`, edited in
  T026 after T020 lands. The oracle's `_inside_the_test` rule (openXdox-code
  `scripts/protected_suites.py:294`) is amended to accept such an entry, and
  each such edit is entered and reviewed in U-7's PR. Batch C's other
  conditions hold for it: it names its span, the landing, its reason and its
  review, it carries the exact old and new text, and it weakens no assertion.
  With W-1 (A), *"Model import-free again (Recommended)"*, which makes openDox's
  `staging-workbench-model.js` import-free again and so reverses carve slice
  S7's model import by that word, all 26 of the suite's `PROTECTED-CONFLICT`
  nodes close, and the suite stays in this falsifier's governed set. The
  harness nodes close through the spans only together with W-1, because they
  first fail on the `./display.js` import. The widened spans close the last
  nine of them and the traced `SystemExit: 2` node, as ruled
  (`6016648451`, answering lane openXfactory-3's points 2 and 3 of
  `6016415390`), and T026 measures it. The two route claims (`:1291`,
  `:1333`) lie inside their own named tests (`:1262-1300`, `:1305-1343`), so
  in-test entries reach them and they need no span. The
  'cluster' node takes an ordinary in-test entry that respells its expected
  label to `'group neighbourhood'`, S7's neutral word, as measured (the
  holder's ruling recorded with `6016648451`). Several entries for this one
  suite land together under the `--chains` note below. This bookkeeping
  amendment does not itself touch the command above. Carried out by plan 038's
  T020, T025 and T026.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6016648451`; Ruled "Amend
  F12.1 with --chains"):** Brett Heap's multi-choice word of 2026-10-06,
  verbatim *"Amend F12.1 with --chains (Recommended)"*. This falsifier's check
  takes a CHAIN of entries, the mechanism batch K gave F5.2. Its last step, as
  T059 wired it (openXdox-code `scripts/protected_suites.py:24-25` at
  `56e1c238`, whose usage text at `:27` still calls `--chains` F5.2's alone),
  runs with `--chains` added:

      python3 scripts/protected_suites.py --chains --landings="$(cat "$W/x-arc.txt")" --suites="$(cat "$W/governed.txt")"

  So several entries, applied in the order they are listed, may together admit
  one landing's edits to one governed suite, under batch K's rule unchanged:
  - each entry is still exactly one edit inside its own named test, or, under
    R-1 (a) (the note above), inside its named span;
  - the entries chain by git blob: the first entry's `before_blob` is the suite
    before the landing, the last entry's `after_blob` is the suite at it, and
    each blob between is the blob id of the text the entries before it leave;
  - the landing's diff for each suite is exactly the chain's recorded texts.

  Nothing wider is admitted, and each entry still admits one landing. So U-7's
  entries, under batch C, CF-4 and R-1 (a) (the three notes above), land as
  ONE pull request, plan 038's T026 (openXdox-code#43). Batch K's sentence at
  F5.2 that this falsifier passes no `--chains` takes a dated note there. This
  bookkeeping amendment does not itself touch the Python above. Carried out by
  plan 038's T026 and T029.
- [ ] 12.6 **MERGE AUTHORITY — RULED, HOLD RELEASED.** Brett Heap, `#656` comment
  `5784155201`, 2026-09-22T21:06:01Z: *"merge yes"* — landing authority follows
  whoever governs the repository. A GOVERNED host reserves landing and routes it
  to the governance's own instrument (openxFactory's flow unchanged); a STANDALONE
  owner IS the governance and openDox may land. **Three guardrails in EVERY mode,
  none configurable:** explicit human act, conflicts SHOWN, and a merge that is a
  COMMIT and therefore revertible. Implement all three as tests, not as prose.
  *(Superseded instruction, kept so the change of direction is legible:)* An earlier draft made the absence of `merge`, `approve`,
  `review`, `self_review`, `bypass_protection` and `enable_auto_merge` binding and
  refused a merging implementation in a scenario; **both were withdrawn from the
  delta** on Brett Heap's question of 2026-09-22 — *"if we are going to have
  openDox be standalone, then it will need to merge documents."* The two readings
  were set out for the operator and the packet recommended neither; the ruling
  above answers them. The GOVERNED host's implementation still declares no merge
  and openxFactory's flow is still unchanged (12.5) — that half was never in
  question.
- [ ] 12.6a **DECLARE THE LANDING SEAM. The guardrail tests need something to
  exercise, and today nothing in openDox lands.** The submission port KEEPS its
  three operations. FR-030's *"the absence of every other one"*
  (`session_pr.py:99-101`) stays true of `PullRequestPort`, and a governed host's
  implementation still declares no merge. Landing is a SEPARATE protocol,
  `session_pr.LandingPort`, with ONE operation, `land(branch, *, confirmation) ->
  Landed`. A GOVERNANCE QUERY decides whether it is bound at all:
  `session_pr.repository_governance(checkout_root)` answers `standalone`,
  `governed` or `unknown`, and **it FAILS CLOSED**. `standalone` requires TWO
  things at once. The install must be the explicit local one
  (`OPENDOX_INSTALL_MODE=local`, 13.4). The repository must carry a COMMITTED
  declaration, `.opendox/governance.yaml` with `governance: standalone`, **read
  from the tip of the DEFAULT BRANCH at the moment of landing**
  (`git show <default-branch>:.opendox/governance.yaml`). It is never read from the
  branch being landed or from the working tree. A branch cannot decide its own
  landing: a session branch that ADDS a standalone declaration to a repository
  whose default branch has none is still `unknown` and is refused. Precedence runs
  one way. A registered host profile that declares an instrument makes the
  repository `governed` whatever any file says. The default branch's declaration
  decides only in the absence of such a host. A branch's contents never decide.
  Because the declaration is a committed file, changing it is a landing like any
  other: in a governed repository it passes through that governance. `governed`
  is what a registered host profile declares, or what the committed declaration
  says. Everything else is `unknown`: no declaration, a host profile that fails
  to load, or a declaration that disagrees with the install mode. `unknown` is
  treated as governed-without-an-instrument, so NO lander is bound and `land`
  refuses, naming what is missing. A land request under `governed` is routed to
  the host's own instrument. Under
  `standalone` the neutral lander is bound through `landing_factory`, declared
  beside `pull_request_factory` (`serve.py:766`): the same pattern with its own
  registration point, like every seam in this packet. **The three guardrails are
  the operation's CONTRACT, not its options.** `confirmation` is a CAPABILITY,
  not a value a caller builds. It is an opaque, single-use token that only two
  issuers mint. One is the `land` verb's prompt, which reads the typed branch
  name from the CONTROLLING TERMINAL (`/dev/tty`, never stdin) and refuses when
  there is none. The other is the view's confirm control, which receives a nonce
  the loopback server issued for that branch. Each token is bound to the branch
  AND its head sha, and it is spent on use. `land` verifies all of it: a token
  constructed directly, minted for another branch or another head, or presented
  twice is refused, as is a `land` whose stdin is not a terminal. **Its limit is
  stated rather than hidden.** An in-process boundary cannot stop code the user
  runs on purpose. What it stops is the PRODUCT's own paths (the fix loop,
  scheduling, automation), because none of them can reach an issuer, and a test
  asserts that no module outside the two interactive layers calls one. Packs run
  out of process (15.1b), so they cannot reach one either. A conflict raises `MergeConflict` carrying the
  conflicting paths and leaves the default branch where it was. A landing is a
  `--no-ff` MERGE COMMIT whose sha `Landed` returns, so `git revert -m 1 <sha>`
  undoes it. The CLI verb is `land --repo-root <repo> --branch
  <session-branch>`, interactive by construction.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q9 (a),
  item 7):** The CLI verb's shape gains `--local`, as 12.4a's does: `land
  --repo-root <repo> --branch <session-branch> [--local]`. It selects the local
  install exactly as `OPENDOX_INSTALL_MODE=local` does, so it meets the first
  of the two things `standalone` requires above, the explicit local install,
  and the second, the default branch's committed declaration, is unchanged. A
  flag and a setting that disagree are refused, naming both. The verb stays
  interactive by construction, and the guardrails and the governance query are
  unchanged. F12.2 is not amended. This bookkeeping amendment does not itself
  touch a falsifier. Carried out by plan 038's T012 and T016.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling, installed IN the block
  below, and `gh` NOT installed, which is the student's machine):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v12"                       # a FRESH environment: nothing already installed stands in
      . "$W/v12/bin/activate"
      pip install ".[test]"
      if command -v gh >/dev/null 2>&1; then                # the precondition, ASSERTED: the student's machine
        echo "FAIL: gh is installed; this acceptance must run without it"; exit 1
      fi
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      git init -q "$W/plain"
      git -C "$W/plain" commit -q --allow-empty -m seed
      git -C "$W/plain" branch sess-1                       # the SESSION BRANCH must exist to be pushed
      git init -q --bare "$W/remote"
      git -C "$W/plain" remote add origin "$W/remote"
      # submit through the PRODUCT'S OWN VERB (12.4a), so the REAL default binding runs:
      opendox submit --repo-root "$W/plain" --branch sess-1 > "$W/submit.out"
      git -C "$W/remote" rev-parse --verify sess-1          # the branch ARRIVED
      grep -qF -- "$W/remote" "$W/submit.out"               # and the verb REPORTED where it went (12.1a)
      # ...and the binding that verb used is the NEUTRAL one, returning a Submission:
      python3 - "$W" <<'PY'
      import sys
      from pathlib import Path
      from opendox import cli, session_pr
      W = Path(sys.argv[1])
      port = cli._submission_port(W / "plain")              # the CLI's default (12.4), no injection
      assert isinstance(port, session_pr.LocalGitSubmissions), f"the default names a platform: {type(port)}"
      assert isinstance(port, session_pr.SubmissionPort)
      assert not isinstance(port, session_pr.PullRequestPort), "a push-only class claims the platform protocol"
      r = port.submit("sess-1")                             # idempotent: already there
      assert r is not None and r.ref.endswith("sess-1") and str(W / "remote") in r.url, r
      PY
      # the SERVER's unset default binds the same class — a named test, so its absence fails:
      python -m pytest -q "tests/test_submission_default.py::test_server_unset_submission_factory_binds_the_neutral_default"
      # a credential in the remote's URL never reaches the report, the output or a refusal (12.1a):
      python -m pytest -q "tests/test_submission_default.py::test_a_credential_in_the_remote_url_never_reaches_the_report"
      # the ROUTE is a session verb, gated as the governed one is (12.4a) — each refusal a NAMED test:
      python -m pytest -q \
        "tests/test_submit_route.py::test_submit_route_is_refused_off_loopback" \
        "tests/test_submit_route.py::test_submit_route_is_refused_without_a_resolved_actor" \
        "tests/test_submit_route.py::test_submit_route_is_refused_without_the_console_token" \
        "tests/test_submit_route.py::test_submit_route_is_refused_from_a_foreign_origin" \
        "tests/test_submit_route.py::test_submit_route_takes_no_repository_from_the_request"
      # and the NO-REMOTE case, through the same verb (scenario 4):
      git -C "$W/plain" remote remove origin
      rc=0; opendox submit --repo-root "$W/plain" --branch sess-1 > "$W/none.out" 2>&1 || rc=$?
      test "$rc" -ne 0                                      # refused, never a reported success
      grep -qi "remote" "$W/none.out"                       # naming what is missing
      rc=0; grep -q "Traceback" "$W/none.out" || rc=$?
      test "$rc" -eq 1                                      # ABSENT: plainly refused, not an opaque error

  **The acceptance runs the product's own verb, not a class it constructs by
  hand**, so it exercises the default binding a student's install really uses.
  The CLI binding is also asserted to BE the neutral class. The server binding
  has a named test, because a hand-built class passing proves nothing about what
  the product binds when nothing is injected. On the remote path two things are
  asserted: the branch arrived, and the verb REPORTED where it went. That second
  assertion is requirement 11's third scenario, and a `None`-returning `push`
  could not satisfy it however well the push worked. The no-remote path fails in
  BOTH wrong directions scenario 4 forbids. A silent success exits 0 and fails
  `test`. An opaque error leaves a traceback, and the traceback check refuses it.
  Each of the five route tests also asserts that the remote is unchanged, so a
  refusal that pushed anyway fails. The redaction is a named test too, because
  the bare local remote this block pushes to carries no credential and so cannot
  show a leak. The test configures a remote whose URL carries both a userinfo
  credential and a query-string token. It asserts that neither secret appears in
  `Submission.url`, in the verb's printed report, or in the message of a refused
  or failed push, and that the report still names the remote's host and path.

  **And the three guardrails are asserted, now that 12.6 is RULED — by NAME**, so
  a missing test FAILS the command rather than being quietly absent from it. 12.6
  owes these thirteen tests, and pytest exits non-zero (`ERROR: not found`) for any
  node that does not exist, so today the command fails:

      python -m pytest -q \
        "tests/test_landing_guardrails.py::test_land_requires_an_explicit_human_act" \
        "tests/test_landing_guardrails.py::test_land_shows_a_conflict_and_does_not_resolve_it" \
        "tests/test_landing_guardrails.py::test_a_landed_merge_is_a_commit_that_git_revert_undoes" \
        "tests/test_landing_guardrails.py::test_no_configuration_enables_automatic_landing" \
        "tests/test_landing_guardrails.py::test_a_governed_repository_binds_no_lander" \
        "tests/test_landing_guardrails.py::test_an_unknown_governance_binds_no_lander" \
        "tests/test_landing_guardrails.py::test_a_host_profile_that_fails_to_load_binds_no_lander" \
        "tests/test_landing_guardrails.py::test_a_branch_cannot_declare_its_own_governance" \
        "tests/test_landing_guardrails.py::test_a_registered_host_outranks_any_declaration" \
        "tests/test_landing_guardrails.py::test_a_directly_constructed_confirmation_is_refused" \
        "tests/test_landing_guardrails.py::test_a_confirmation_for_another_branch_or_head_is_refused" \
        "tests/test_landing_guardrails.py::test_a_spent_confirmation_is_refused" \
        "tests/test_landing_guardrails.py::test_only_the_interactive_layers_call_an_issuer"

  Each node exercises 12.6a's seam. The first builds a `confirmation` every way
  that is not a human act (a flag, a config key, a non-TTY stdin) and expects
  every one refused. The second lands a branch that conflicts and expects
  `MergeConflict` with the paths and an unmoved default branch. The third lands,
  then reverts with `-m 1`, and expects the tree restored. The fourth walks the
  configuration surface and fails if any key can switch a guardrail off: the
  "none configurable" clause made testable. The fifth registers a governed host
  and expects NO `LandingPort` bound. The sixth and seventh prove the query FAILS
  CLOSED: with no committed declaration, or with a host profile that fails to
  load, no lander is bound. The eighth lands a branch that ADDS a standalone
  declaration to a repository whose default branch has none, and expects a
  refusal. The ninth registers a governing host beside a standalone declaration,
  and expects the host to win. The last four test the capability itself.
  A token built directly is refused. So is one minted for another branch or
  another head, and so is one presented a second time. A static check proves
  that no module outside the `land` prompt and the view's confirm route calls an
  issuer. Naming test nodes in an ACCEPTANCE command is not the defect Group 9
  removes from `validate.yml` — CI must run the whole suite, and this command runs
  thirteen named proofs in addition to it.

  Today none of this is reachable: the only implementation is `GhPullRequests`,
  which shells `["gh", "pr", ...]` (`:367`) against `_GITHUB_HOST = "github.com"`
  (`:233`), so a machine without `gh` and a repository without a GitHub remote
  have no submission path at all.


## Group 13 — Requirements 12, 13: the standalone install's shape (RULED, openDox-code)

**RULED** `#656` `5784155201`, 2026-09-22T21:06:01Z: *"bundled postgres, local
identity yes"*. `design.md` § D10 carries the measurements and the two
amendments.

- [x] 13.1 **Bundle Postgres with the standalone install** so a user installs the
  product and not a database. The pieces exist: `pyproject.toml:134` pins
  `psycopg[binary,pool]>=3.2` and `deploy/compose/docker-compose.yaml:25` is
  already `image: postgres:16`. But `psycopg` is a CLIENT and `pip install` starts
  no container, so neither piece brings a server by itself. This box makes the
  LOCAL install bring one: with `OPENDOX_INSTALL_MODE=local` (13.4) the product
  starts a PostgreSQL SERVER shipped inside the install and supplies BOTH DSNs
  itself. **The server's IDENTITY is fixed here; its packaging is the
  realization's choice.** The data directory and the Unix socket live under the
  install's own state directory, `OPENDOX_STATE_DIR`, which defaults to a
  per-user directory the install owns. The server listens on that socket and on
  NO TCP port, so no pre-existing service can stand in for it. `runtime status`
  and the served `install` block (13.4a) report a `database_bundle` block naming
  `data_dir`, `socket_dir` and the server's `pid`. The acceptance checks the
  directories against the fresh state directory, and checks the "no TCP port"
  invariant at the OPERATING SYSTEM rather than by the bundle's own report: no
  socket the server process holds may appear in LISTEN state in
  `/proc/net/tcp` or `/proc/net/tcp6`. With `hosted` or unset, a missing
  `OPENDOX_DATABASE_URL` stays the refusal `config.py:13` already makes, so a
  hosted install can no more fall into a private local database than into local
  identity.

  **AMENDED — T007 Batch H (`5850003126`; Ruled R1Q16 (i)–(iv)):** An
  addendum. This box leaves the server's packaging to the realization, and
  the answer names it. The document server starts the bundled server as its
  own child and reports it (i), so the process a user reaches is the one
  that owns it (13.4a). Starting and migrating the store is all release 1
  asks of it, since the document surface reads nothing from it in release 1
  (ii). It ships as the `opendox[local]` extra, which carries the runtime's
  packages and the server's own (iii), and it stops with the entry point
  (iv). Everything else above is unchanged: both DSNs supplied by the
  product, the data directory and the socket under `OPENDOX_STATE_DIR`, no
  TCP port, and the `database_bundle` report. F13.1 installs `".[local]"`,
  as this batch's addendum there records. Carried out by T072 and T073.

  **Landed 2026-10-03** (T072): openDox-code#69 → `5e7ab003`.
  `opendox generate-and-open --local` starts `postgres` as a direct child of the
  serving process under `OPENDOX_STATE_DIR`, with no TCP listener, both DSNs
  supplied, `runtime status` reporting `database_bundle`; it stops with the
  entry point (R1Q16 (i)-(iv), `opendox[local]`). F13.1's blocks pass
  (`evidence/f13.1-run.md`).
- [x] 13.2 **Add no SQLite dialect**, and record the refusal where a future reader
  will look for it: a second dialect doubles every migration and every schema test
  forever, for a database that under RULING Q1 holds no document. **A non-PostgreSQL
  DSN is REFUSED by `load_settings`, and the refusal names the one dialect kept.**

  **Landed 2026-10-02** (T071): openDox-code#60 → `7ff434d9`. `load_settings`
  refuses a non-PostgreSQL DSN, naming the one dialect kept, and
  `load_migration_settings` takes the same refusal at configuration (F13.1's
  first `load_settings` assertion, `evidence/f13.1-run.md`).
- [x] 13.3 **Keep both DSNs.** `OPENDOX_MIGRATION_DATABASE_URL` for migrating and
  `OPENDOX_DATABASE_URL` for serving, with neither defaulted from the other —
  `config.py` already names the silent fallback as the thing not to do, and a
  single-user install is not a reason to serve from the migrating credential.
  **One credential given in both settings is REFUSED by `load_settings`, naming
  `OPENDOX_MIGRATION_DATABASE_URL`.** Today `load_settings` refuses only two DSNs
  that select different schemas (`_refuse_two_dsns_that_select_different_schemas`,
  `config.py:1291`, called at `:1411`), and it reads the migration DSN as
  OPTIONAL (`:1417`), so the collapse is not refused yet.

  **Landed 2026-10-02** (T071): openDox-code#60 → `7ff434d9`. One credential in
  both settings is refused, naming `OPENDOX_MIGRATION_DATABASE_URL`; the
  migration DSN is required only on the migrate path and never defaulted (RULED
  `5880893901`); F13.1's second `load_settings` assertion holds
  (`evidence/f13.1-run.md`).
- [x] 13.4 **A NAMED local single-user mode (AMENDS RULING Q2).** `config.py:89-92`
  makes `OPENDOX_OIDC_ISSUER` required — *"the Keycloak broker's issuer, pinned
  … (RULING Q2)"*. Add an explicit local mode that needs no broker. **The selector
  is `OPENDOX_INSTALL_MODE`, values `local` and `hosted`, read in
  `runtime/config.py` beside `OPENDOX_OIDC_ISSUER` and defaulting to `hosted`.**
  It selects the whole install shape at once, the identity mode here and the
  datastore source in 13.1, because requirements 12 and 13 both describe "the
  standalone install" and one deliberate choice should decide both. It is named
  here so the falsification below is executable, and so the default is the SAFE
  one: an install that sets nothing is hosted, and a hosted install with no
  issuer refuses (13.5). It is UNSET, not `local`, that must be safe. **And local
  mode binds LOOPBACK ONLY.** `generate-and-open` accepts `--host` (10.1), and
  local mode has no broker, so a local install bound to `0.0.0.0` would be an
  unauthenticated multi-user service wearing the word "local". A non-loopback
  `--host` under `local` is REFUSED, naming the loopback rule, and there is NO
  opt-in: an install that must be reachable from another machine is a hosted
  install with a broker. The server already treats a loopback bind as the
  precondition of its `session` capability (`serve.py:915`); this makes the same
  judgement at the mode's own boundary. *(An earlier
  draft called it `OPENDOX_IDENTITY_MODE`. Once it also chose the datastore, that
  name described half of what it selects.)*

  **AMENDED — T007 Batch H (`5850003126`; Ruled R1Q15 (b)):** An addendum.
  `generate-and-open --local` selects the local mode explicitly, as
  `OPENDOX_INSTALL_MODE=local` does. With neither, the install is hosted, as
  13.5 requires. The flag is an option of the verb and follows it, as every
  option does (10.1), and it is the selection the one documented command
  makes (10.3 and F10.1 as this batch amends them). Carried out by T070.

  **Landed 2026-10-03** (T070): openDox-code#67 → `66ff7257`.
  `OPENDOX_INSTALL_MODE` (`local` or `hosted`, default `hosted`) and
  `generate-and-open --local` select the local mode; it needs no broker and
  binds loopback only, refusing a non-loopback `--host` naming the rule (batch
  H's 13.4 addendum); the probes exit 1, not 124 (`evidence/f13.1-run.md`).
- [x] 13.4a **The serving process reports its own install shape.** The entry
  point's served `/capabilities` payload (the same crossing `display_manifest`
  already publishes, `display_profile.py:670`) gains an `install` block. It holds
  `mode` and `database_bundle` (`data_dir`, `socket_dir`, `pid`), read from the
  settings THAT PROCESS loaded. Requirement 10's one entry point is what makes
  this possible: the document surface and the runtime are one served product, so
  the process a user reaches is the process whose configuration is reported. A
  status probe from a second process could be right about the settings while the
  server ignored them.

  **Landed 2026-10-03** (T073): openDox-code#72 → `90ac7033`. `/capabilities`
  gains an `install` block (`mode`, `database_bundle`) read from the serving
  process's own settings; F13.1's `caps.json` block passes against the server on
  :8080 (`evidence/f13.1-run.md`).
- [x] 13.5 **A hosted install SHALL NOT fall into local mode by omission.** An
  unset issuer in a hosted install stays a REFUSAL naming the setting. This box
  is the safety of 13.4 and must land with it, not after it.

  **Landed 2026-10-03** (T070): openDox-code#67 → `66ff7257`. A hosted install,
  and the unset default, with no `OPENDOX_OIDC_ISSUER` refuse naming the
  setting; neither is started nor killed by the 30 s bound
  (`evidence/f13.1-run.md`).
- [x] 13.6 The hosted multi-user mode is UNCHANGED: same broker, same pinned
  issuer, a token from any other issuer still refused.

  **Landed 2026-10-03** (T070): openDox-code#67 → `66ff7257`. Hosted mode is
  otherwise unchanged (same broker, same pinned issuer); F13.1's hosted probes
  still refuse with no issuer, naming `OPENDOX_OIDC_ISSUER`
  (`evidence/f13.1-run.md`).
- [x] **FALSIFIED BY** (a machine with no database and no identity broker):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      # the install is group 10's, unchanged — one entry point, one command:
      python -m venv "$W/v13"
      . "$W/v13/bin/activate"
      pip install .
      unset OPENDOX_DATABASE_URL OPENDOX_MIGRATION_DATABASE_URL OPENDOX_OIDC_ISSUER OPENDOX_INSTALL_MODE   # NONE of them set
      export OPENDOX_STATE_DIR=$(mktemp -d)                 # a state directory NOTHING else has touched
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      R=$(mktemp -d)/plain-documents
      cp -r tests/fixtures/plain-documents "$R"   # this group's OWN corpus, not Group 12's
      git -C "$R" init -q
      git -C "$R" add -A
      git -C "$R" commit -qm fixture
      opendox --help >/dev/null
      # LOCAL mode starts, with no broker and no operator-supplied database:
      OPENDOX_INSTALL_MODE=local opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8080 &
      SERVER=$!; trap 'kill "$SERVER" 2>/dev/null || true' EXIT
      ready=0; for _ in $(seq 1 30); do curl -sf http://127.0.0.1:8080/ >/dev/null && { ready=1; break; }; sleep 1; done
      test "$ready" -eq 1
      # the SERVING process reports its OWN mode and datastore, so the claim is about the server
      # the user reached on :8080 and not about a second process that read the same settings:
      curl -sf http://127.0.0.1:8080/capabilities > "$W/caps.json"
      python3 - "$W/caps.json" <<'PY'
      import json, os, sys
      inst = json.load(open(sys.argv[1])).get("install") or {}
      assert inst.get("mode") == "local", f"the server on :8080 is not in local mode: {inst}"
      state = os.path.realpath(os.environ["OPENDOX_STATE_DIR"])
      for key in ("data_dir", "socket_dir"):
          got = os.path.realpath((inst.get("database_bundle") or {}).get(key, ""))
          assert got.startswith(state + os.sep), f"the served process uses {key} {got!r}, not the bundle under {state!r}"
      PY
      # and the bundled server has NO TCP listener, checked at the OS and not by self-report:
      python3 - "$W/caps.json" <<'PY'
      import json, os, re, sys
      pid = ((json.load(open(sys.argv[1])).get("install") or {}).get("database_bundle") or {}).get("pid")
      assert isinstance(pid, int), f"the bundle reports no server pid: {pid!r}"
      inodes = set()
      for fd in os.listdir(f"/proc/{pid}/fd"):
          try:
              m = re.match(r"socket:\[(\d+)\]", os.readlink(f"/proc/{pid}/fd/{fd}"))
          except OSError:
              continue
          if m:
              inodes.add(m.group(1))
      listening = [(tbl, row.split()[1]) for tbl in ("/proc/net/tcp", "/proc/net/tcp6")
                   for row in open(tbl).read().splitlines()[1:]
                   if row.split()[3] == "0A" and row.split()[9] in inodes]   # 0A = TCP LISTEN
      assert not listening, f"the bundled server listens on TCP: {listening}"
      PY
      # ...and what it answered from is the BUNDLED datastore, migrated (requirement 12):
      OPENDOX_INSTALL_MODE=local opendox-runtime runtime status --probe-timeout 10 > "$W/status.json"
      python3 - "$W/status.json" <<'PY'
      import json, os, sys
      s = json.load(open(sys.argv[1]))
      assert s.get("database") == "reachable", f"no bundled database answered: {s}"
      assert s.get("applied_migrations") and not s.get("pending_migrations"), f"not migrated: {s}"
      state = os.path.realpath(os.environ["OPENDOX_STATE_DIR"])
      bundle = s.get("database_bundle") or {}
      for key in ("data_dir", "socket_dir"):                 # the server that answered is the INSTALL'S OWN
          got = os.path.realpath(bundle.get(key, ""))
          assert got.startswith(state + os.sep), f"{key} {got!r} is not under the install's state dir {state!r}"
      PY
      kill "$SERVER"; wait "$SERVER" 2>/dev/null || true
      # LOCAL mode REFUSES a non-loopback bind, BOUNDED, naming the rule (13.4):
      rc=0
      OPENDOX_INSTALL_MODE=local timeout 30 opendox generate-and-open --repo-root "$R" --repository fixture --no-open --host 0.0.0.0 --port 8083 >/dev/null 2>"$W/bind.err" || rc=$?
      test "$rc" -ne 0                                      # refused, never started
      test "$rc" -ne 124                                    # and not merely killed by the bound
      grep -qi "loopback" "$W/bind.err"
      # ONE DIALECT, and the two connections NOT COLLAPSED (13.2, 13.3), asked of the
      # loader directly, with every other setting well-formed so the DSN is the only fault:
      python3 - <<'PY'
      from opendox.runtime.config import ConfigurationError, load_settings
      OK = {"OPENDOX_OIDC_ISSUER": "https://issuer.example.invalid/realms/fixture",
            "OPENDOX_OIDC_AUDIENCE": "fixture"}
      def refusal(**dsns):
          try:
              load_settings({**OK, **dsns})
          except ConfigurationError as e:
              return str(e)
          raise AssertionError(f"accepted: {dsns}")
      m = refusal(OPENDOX_DATABASE_URL="sqlite:///x.db", OPENDOX_MIGRATION_DATABASE_URL="sqlite:///x.db")
      assert "postgres" in m.lower(), f"a second dialect was refused for the wrong reason: {m}"
      one = "postgresql://one@127.0.0.1/opendox"
      m = refusal(OPENDOX_DATABASE_URL=one, OPENDOX_MIGRATION_DATABASE_URL=one)
      assert "OPENDOX_MIGRATION_DATABASE_URL" in m, f"a collapsed pair was refused for the wrong reason: {m}"
      PY
      # every setting a HOSTED install needs EXCEPT the issuer, so the issuer is the only fault:
      export OPENDOX_DATABASE_URL=postgresql://serve@127.0.0.1:1/opendox OPENDOX_MIGRATION_DATABASE_URL=postgresql://migrate@127.0.0.1:1/opendox OPENDOX_OIDC_AUDIENCE=fixture
      # a HOSTED install with no issuer REFUSES — same server path, BOUNDED, naming the setting:
      rc=0; OPENDOX_INSTALL_MODE=hosted timeout 30 opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8081 >/dev/null 2>"$W/hosted.err" || rc=$?
      test "$rc" -ne 0
      test "$rc" -ne 124   # refused: neither started, nor killed by the bound
      grep -q "OPENDOX_OIDC_ISSUER" "$W/hosted.err"
      # and the DEFAULT is hosted: the same install with the selector UNSET refuses identically:
      rc=0; timeout 30 opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8082 >/dev/null 2>"$W/default.err" || rc=$?
      test "$rc" -ne 0
      test "$rc" -ne 124
      grep -q "OPENDOX_OIDC_ISSUER" "$W/default.err"

  **Six assertions. The last four are the safety, and the last two are bounded.**
  The local probe proves the install starts with no broker and no
  operator-supplied database. `runtime status` then proves the datastore it
  answered from is the bundled one, reachable and migrated; it reports JSON with
  `database` and `pending_migrations` keys (`runtime/cli.py:621`). **The identity
  is checked, not assumed.** Its data directory and socket must both lie under a
  state directory created empty for this run, and the bundled server has no TCP
  port. So a PostgreSQL that happened to be running on the machine cannot pass
  this check in the bundle's place. The dialect
  and collapse checks go to `load_settings(env)` directly (`config.py:1391`
  takes the mapping). Every other setting is supplied well-formed, so each
  refusal must be about the DSN it names: an implementation that used SQLite, or
  served from one credential, fails here and not somewhere unrelated. The two
  negative probes take the SAME `generate-and-open` path the local probe takes,
  under `timeout 30`. A regression that silently STARTS a hosted server would
  otherwise block the command forever; with the bound it exits 124, and `test`
  rejects 124 as firmly as 0. Each probe must also NAME `OPENDOX_OIDC_ISSUER`. Both
  probes run with every setting a hosted install needs except the issuer, so the
  only difference between them is the selector, and the last probe proves the
  unset DEFAULT refuses exactly as `hosted` does.

  Today none of it is reachable. The runtime refuses without
  `OPENDOX_DATABASE_URL` and `OPENDOX_OIDC_ISSUER`, there is no local mode, and
  `load_settings` accepts a collapsed DSN pair (the migration DSN is optional
  there).

  **AMENDED — T007 Batch H (`5850003126`; Ruled R1Q16 (i)–(iv)):** F13.1's
  install line is amended: `pip install .` becomes `pip install ".[local]"`,
  the standalone install (13.1 as this batch amends it). It is still group
  10's install, since F10.1 installs the same extra. The local probe's
  `OPENDOX_INSTALL_MODE=local` is the same selection as `--local` (13.4 as
  this batch amends it), so that probe stands as written. So do the
  refusals: the last probe sets neither, and it still proves that the unset
  default refuses as `hosted` does. Nothing else in the block changes. This
  bookkeeping amendment does not itself touch the command above: T074 runs
  it as amended. Carried out by T074.

  **Landed 2026-10-03** (T074, openxFactory#1224 → `de2ab703`): F13.1, extracted
  byte for byte from #1144 with batch H's install line
  (`pip install ".[local]"`), exits 0 at openDox-code `90ac7033` from a fresh
  clone, in an `env -i` environment with no database and no broker: local probe
  starts and migrates the bundle, the served `install` block reads `local`, no
  TCP listener, `runtime status` `reachable`, and the three CLI refusals hold
  (`evidence/f13.1-run.md`).

## Group 14 — Requirements 6, 14, 15: health in the store, and the fix loop (RULED, openDox-code)

**RULED** `#656` `5784155201` (*"health in db"*) and `5784247356` (*"1, add the
fix loop to #1144"*). `design.md` §§ D10.4, D10.5 and D11.

- [ ] 14.1 **The health table arrives as `0003_`, NOT `0002_`.**
  `migrations/0002_migration_state.sql` already exists (the
  `opendox_schema_migrations` ledger). `0001` is applied verbatim behind
  `CANONICAL_MIGRATION_SHA256` and its own text says *"Changing the schema is
  therefore an ADDITIVE `0002_…`/`0003_…` file, never an edit here"*.
- [ ] 14.2 **DECLARE whether the health table is a DOMAIN table or install-owned,
  and say why.** This is the boundary claim, and the closure test is scoped to
  the CANONICAL migration only — which is why `0002`'s ledger table did not trip
  it. If DOMAIN: `identity.TABLES` and
  `tests_runtime/test_schema_shape.py`'s closure text move in the SAME change. If
  install-owned: the `0002` precedent already covers it and no closure text moves.
  **Either way the choice is stated in the open**, which is what
  `test_..._exactly_rulings_six_tables`'s message demands.
- [ ] 14.3 The store holds NO DOCUMENT and stays DISPOSABLE (Q1's principle,
  untouched): results are recomputable from git, so losing the store costs a
  recomputation.
- [ ] 14.4 **The neutral families**, as ruled: broken internal links, orphans,
  near-duplicates, missing neutral front matter from the adapter's fields, a
  declared stage that disagrees with the document's location among the six ruled
  words, and stale or empty stubs. On demand from dashboard and CLI, optionally on
  commit. Baseline-relative. Model-assisted checks only where a model is
  configured. **openxFactory's 23 governance families stay put** (requirement 1).

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6013547504`; Ruled I-2 (a),
  with R2Q12 (a) and R2Q7 (a), `6003486656`):** A reading of
  *"Baseline-relative"*. Brett Heap's multi-choice word of 2026-10-06, verbatim
  *"main, else HEAD's branch (Recommended)"*. R2Q12 (a) makes the baseline the
  previous run at the default branch's tip, held in the store, and R2Q7 (a)
  makes the default branch `main`. The BASELINE BRANCH is `main`, else the
  branch HEAD names; a detached HEAD in a repository with no `main` has none.
  R2Q7 (a)'s `main` still governs LANDING alone (12.6a). So the baseline holds
  in every repository, F14.1's included: F14.1 and F15.1 create theirs with
  `git init -q`, which names no branch, so on a runner whose
  `init.defaultBranch` is unset they have no `main`. F14.1 asserts no class, so
  it passes as written either way, and the baseline on `main` is exercised by
  the engine's own tests. This bookkeeping reading edits no line of the box.
  Carried out by plan 038's T046.
- [ ] 14.5 **The Health view, with CLI PARITY.** Every resolution action available
  in the view is available from the command line — requirement 14's last scenario
  exists because a standalone install may have no browser. **The verbs this arc
  adds to `opendox.cli`, named here so groups 14 and 15 close on an exact
  surface** (the preamble's rule: no box closes on a verb its own group did not
  declare):

  | verb | shape |
  |---|---|
  | `health run` | `health run --repo-root <corpus> [--pack ID] [--timeout SECONDS]` |
  | `health list` | `health list --repo-root <corpus> [--json]` |
  | `health fix` | `health fix --repo-root <corpus> --finding ID [--batch]` |
  | `health accept` | `health accept --repo-root <corpus> --finding ID --reason TEXT` |

  Options FOLLOW the verb, exactly as they do for every verb `cli.py` declares
  today (10.1).

  `health list --json` emits one object per finding, with `id`,
  `resolution_class`, `path` (the document the finding is about), `severity`,
  `evidence`, `pack_id` and `pack_version`. That is the shape the acceptances in
  Groups 14 and 15 read, declared here so they read a contract and not a guess.
  They are NEW surface — `cli.py` declares none of them today (10.1's table is the
  surface that exists) — and 14.6's applier is what `health fix` invokes. **The
  view's actions are published as DATA, so parity is a comparison and not a
  promise.** The `/capabilities` payload's health block lists every resolution
  action the Health view offers. The view is served by the entry point (10.2).
  Three named tests compare the two surfaces: the view is served, every view
  action has a CLI verb, and every CLI verb is offered by the view.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q9 (a),
  item 7):** Each of the four `health` shapes in the table above gains
  `[--local]`, the same flag `generate-and-open` takes (13.4 as batch H amends
  it), following the verb as every option does. It selects the local install
  exactly as `OPENDOX_INSTALL_MODE=local` does, and a flag and a setting that
  disagree are refused, naming both. F14.1 and F15.1 export the setting
  (`export OPENDOX_INSTALL_MODE=local`, in each block), so their `health` lines
  pass no `--local` and stand as written in this respect. The view, its actions
  and the three parity tests are unchanged. This bookkeeping amendment does not
  itself touch a falsifier. Carried out by plan 038's T046.
- [ ] 14.6 **The three resolution classes, spelled `auto-fix`, `assisted` and
  `human-only` — exactly as RULED (`5784247356`) and exactly as requirement 14
  declares them, in the store, the CLI, the view and the pack contract (15.2)
  alike**, because a pack must return an ENGINE-declared class and two spellings
  of one class are two classes. `auto-fix` for the mechanical findings (moved link
  target, derivable front matter, stage/location mismatch), written by the
  product; `assisted` (near-duplicates, empty stubs), proposed for the human to
  edit, model-written only where a model is configured; `human-only`, evidence
  shown.
  **THE APPLIER IS NEW WORK** — openxFactory CLASSIFIES
  (`scripts/doc_health/__init__.py:17-18`, `AUTO_FIXABLE`/`CONTESTED`) and
  `grep -rln 'def apply_fix|def autofix|def fix('` over `scripts/doc_health/`
  returns nothing. Nothing in this estate applies a fix today.
- [ ] 14.7 **Every repair is a DRAFT ON A BRANCH and lands only through the
  landing rule** (requirement 11, group 12): standalone owner lands in openDox, a
  governed repository gets the governance's instrument, and in every mode the
  landing is an explicit human act with conflicts shown and a revertible commit.
  **NOTHING auto-merges, not even a one-line fix.** Batching many repairs into ONE
  draft for ONE review is the pressure valve, and is allowed.
- [ ] 14.8 **EXCEPTIONS LIVE IN GIT, NOT THE STORE**, on the pattern of
  openxFactory's `health/dispositions.yaml` — whose semantics already match:
  `scripts/doc_health/families.py:370` reads *"removing its
  health/dispositions.yaml entry re-opens"* the finding. An exception is a
  judgement that exists nowhere else; the store is disposable, so an exception
  stored there is a judgement scheduled for deletion.
- [ ] 14.9 **Ship `tests/fixtures/health-corpus`**: a small corpus carrying ONE
  finding of EVERY kind requirement 14 names, and nothing else a neutral family
  would flag, so that every assertion below is about a finding the fixture put
  there on purpose. For `auto-fix`, one of each mechanical kind: `broken-link` (a
  moved link target), `derivable-front-matter`, and `stage-location-mismatch`.
  For `assisted`, `near-duplicate`. For `human-only`, `human-only-finding`. Plus
  the one it will accept, `accepted-finding`.
- [ ] **FALSIFIED BY** (openDox-code, installed, over 14.9's fixture corpus with a
  known broken link and a known accepted finding):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v14"                       # a FRESH environment: nothing already installed stands in
      . "$W/v14/bin/activate"
      pip install ".[test]"
      export OPENDOX_INSTALL_MODE=local                     # the store is Group 13's bundle: a prerequisite by name
      export OPENDOX_STATE_DIR=$(mktemp -d)
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      C=$(mktemp -d)/health-corpus
      cp -r tests/fixtures/health-corpus "$C"   # a FRESH repository: fix branches and commits land HERE
      git -C "$C" init -q
      git -C "$C" add -A
      git -C "$C" commit -qm fixture
      opendox health run --repo-root $C
      opendox health list --repo-root $C > "$W/h1.txt"
      grep -q 'broken-link' "$W/h1.txt"
      # a mechanical repair writes a DRAFT ON A BRANCH and never the default branch:
      before=$(git -C $C rev-parse HEAD)
      opendox health list --repo-root $C --json > "$W/h1.json"
      python3 - "$W/h1.json" "$W/paths.tsv" <<'PY'
      import json, sys
      want = {"broken-link": "auto-fix", "derivable-front-matter": "auto-fix", "stage-location-mismatch": "auto-fix",
              "near-duplicate": "assisted", "human-only-finding": "human-only"}
      found = json.load(open(sys.argv[1]))
      got = {x["id"]: x["resolution_class"] for x in found}
      wrong = {k: (v, got.get(k)) for k, v in want.items() if got.get(k) != v}
      assert not wrong, f"a finding is missing or carries the wrong class: {wrong}"
      with open(sys.argv[2], "w") as out:                   # each finding's own document, for the loop below
          for x in found:
              out.write(f"{x['id']}\t{x['path']}\n")
      PY
      for f in broken-link derivable-front-matter stage-location-mismatch near-duplicate; do
        opendox health fix --repo-root $C --finding "$f"    # EVERY auto-fix kind, and the assisted proposal
        test "$(git -C $C rev-parse HEAD)" = "$before"      # default branch UNMOVED, every time
        git -C $C rev-parse --verify --quiet "refs/heads/health-fix-$f"
        git -C $C diff --name-only "$before" "health-fix-$f" > "$W/fix-$f.txt"
        test -s "$W/fix-$f.txt"                           # the branch CARRIES a change, not merely a ref
        P=$(awk -F '\t' -v id="$f" '$1 == id { print $2 }' "$W/paths.tsv")
        test -n "$P"
        grep -qxF -- "$P" "$W/fix-$f.txt"                 # and the change is to the finding's OWN document
      done
      rc=0
      opendox health fix --repo-root $C --finding human-only-finding > "$W/ho.out" 2>&1 || rc=$?
      test "$rc" -ne 0                                      # human-only: the product proposes nothing it cannot justify
      test -z "$(git -C $C branch --list 'health-fix-human-only-finding')"
      # THE EXCEPTION IS PROVED TO EXIST BEFORE THE RESET, not merely absent after:
      opendox health accept --repo-root $C --finding accepted-finding --reason "fixture"
      test -n "$(git -C $C status --porcelain -- health/dispositions.yaml)" || { echo "FAIL: accept wrote nothing to git"; exit 1; }
      git -C $C add health/dispositions.yaml
      git -C $C commit -qm "accept fixture finding"
      opendox health run --repo-root $C
      opendox health list --repo-root $C > "$W/h2.txt"
      rc=0; grep -q 'accepted-finding' "$W/h2.txt" || rc=$?
      test "$rc" -eq 1                                      # ABSENT: suppressed BEFORE the reset
      # ...and it survives the store being dropped and rebuilt:
      opendox-runtime runtime reset --confirm yes-drop-the-coordination-database
      opendox-runtime runtime migrate
      opendox health run --repo-root $C
      opendox health list --repo-root $C > "$W/h3.txt"      # a FAILING list now fails the sequence
      grep -q 'broken-link' "$W/h3.txt"                     # the run really did produce findings
      rc=0; grep -q 'accepted-finding' "$W/h3.txt" || rc=$?
      test "$rc" -eq 1                                      # ABSENT: the exception still holds
      # CLI PARITY with the view, compared rather than promised (14.5):
      python -m pytest -q \
        "tests/test_health_parity.py::test_the_health_view_is_served" \
        "tests/test_health_parity.py::test_every_view_action_has_a_cli_verb" \
        "tests/test_health_parity.py::test_every_cli_verb_is_offered_by_the_view"

  Four things are proved in order, and the order is the point: the exception is
  written TO GIT (`git status --porcelain` must show the file, NEW or modified —
  `git diff` alone misses an untracked first write and would have failed a correct
  implementation),
  it suppresses the finding BEFORE the reset, the post-reset run really produced
  findings (`broken-link` is present, so an empty listing cannot masquerade as
  suppression), and only then is `accepted-finding` asserted absent. **Every
  listing is captured to a file first and grepped second**, so a `health list`
  that exits non-zero fails under `set -e` instead of being read as the desired
  absence — which is exactly what the earlier `if … | grep -q` form would have
  done. **An ABSENCE is asserted as grep's exit status 1 exactly, never as
  `! grep`.** Under `set -e` a `!`-inverted command never stops the sequence, so
  a `! grep -q` that is not the last line passes whatever it finds, and status 2
  (a grep that could not read its file) is not an absence either. The default
  branch must not move and the draft branch must exist.

  Today none of it exists: there is no health table, no health verb, and no
  applier anywhere in the estate.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q9 (a),
  item 2):** The block first STARTS THE DOCUMENT SERVER, as F13.1 does. R1Q16
  (i) and (iv) give the bundled server to the document server (13.1 as batch H
  amends it), and the local runtime verbs refuse `local-bundle-unverified`
  without it, so a `health` verb, like `runtime reset` and `runtime migrate`,
  reaches the running bundle and refuses by name without one. After the
  fixture's commit and before the first `health run`, the block runs, with the
  setting it already exports:

      opendox generate-and-open --repo-root "$C" --repository fixture --no-open --port 8084 &
      SERVER=$!; trap 'kill "$SERVER" 2>/dev/null || true' EXIT
      ready=0; for _ in $(seq 1 30); do curl -sf http://127.0.0.1:8084/ >/dev/null && { ready=1; break; }; sleep 1; done
      test "$ready" -eq 1                                   # a server that never started FAILS here

  Port 8084 is one that no other falsifier of this change uses. The rest of the
  block runs against that server, its `runtime reset` and `runtime migrate`
  included, and stands as written, but for the selection lines the next note
  amends. This bookkeeping amendment does not itself touch the command above.
  Carried out by plan 038's T046, and run by its T065.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q10
  (a)):** A finding's `id` is a STABLE, PACK-QUALIFIED KEY. The engine derives it
  from the pack's id, the family, the document's path and a locator the family
  supplies; it survives a reset, it is unique, and it maps to a valid ref name
  for `health-fix-*`; and `health list --json` also carries `kind`. So a literal
  id selects nothing, and every literal-id use in this block becomes a
  SELECTION BY THE PLANTED FINDING'S FIXTURE DOCUMENT. 14.9's fixture names each
  planted finding's document after its old literal id (`broken-link`,
  `derivable-front-matter`, `stage-location-mismatch`, `near-duplicate`,
  `human-only-finding`, `accepted-finding`). A selection reads `health list
  --json`, captured to a file first, and takes the ONE finding whose `path` is
  that document and, where the old id names a family, whose `kind` is that
  family. The `id` it yields is then the handle `--finding` takes and
  `health-fix-<id>` names. An absence is asserted as before, by a selection
  that finds nothing. The uses, by line at `main` `92010d3e`:
  - `grep -q 'broken-link'` over `"$W/h1.txt"` (`:3320`) and `"$W/h3.txt"`
    (`:3364`): the listing holds the planted broken link, selected by its
    document;
  - the `want` map and `x["id"]` (`:3326-3329`): `want` maps each of the five
    documents to its class, checked on its selected finding, with the
    `paths.tsv` map (`:3332-3334`) and its lookup (`:3342`) keyed by document
    and carrying the selected `id`;
  - the `for f in broken-link derivable-front-matter stage-location-mismatch
    near-duplicate` loop with `health-fix-$f` (`:3336-3340`): the loop runs over
    the four documents, and `--finding` and the branch take each one's
    selected `id`;
  - `--finding human-only-finding` and `health-fix-human-only-finding`
    (`:3347-3349`): the human-only document's selected `id`;
  - `--finding accepted-finding` (`:3351`): the accepted document's selected
    `id`, which `health/dispositions.yaml` then cites;
  - `grep 'accepted-finding'` over `"$W/h2.txt"` (`:3357`) and `"$W/h3.txt"`
    (`:3365`): the accepted document's selection finds nothing, before the
    reset and after it.

  Everything else in the block stands, the order of its four proofs included.
  This bookkeeping amendment does not itself touch the command above. Carried
  out by plan 038's T043 (the fixture documents), T053, T054 and T057, and run
  by its T065.


## Group 15 — Requirement 16: the check-pack interface (RULED, openDox-code)

**RULED** `#656` `5784295745`, 2026-09-22T21:16:17Z: *"1, add the pack interface
to #1144"*. `design.md` § D12.

- [ ] 15.1 Declare the NEUTRAL CHECK-PACK CONTRACT in openDox, on the
  `src/opendox/corpus_adapter.py` Protocol pattern (a `@runtime_checkable`
  Protocol with a CLOSED member set, for the reasons that file's own docstring
  gives: structural conformance lets an implementation authored elsewhere satisfy
  it without importing this product's tooling).
- [ ] 15.1a **DECLARE HOW A PACK IS FOUND AND PINNED, in one committed
  manifest.** The engine loads packs ONLY from `health/packs.yaml` in the corpus.
  It is committed beside `health/dispositions.yaml` for the same reason: which
  checks judge a corpus is a human decision about that corpus, not derived data.
  Each entry carries `id`, `version`, `source` and `digest`. The `version` is the
  one every finding the pack raises is attributed to (15.7), so a new pack
  version is a committed decision about the corpus like any other. A pack whose
  own declaration (15.2) names another version, or none, is REFUSED as a finding
  against its entry, and so is an entry whose `id` is the product's own,
  `opendox` (15.7). The digest is the source-tree
  digest `neutral-product-pin` already defines, and it is REQUIRED for every
  source. **`commit` depends on where the source lives.** A git-URL source MUST
  carry it. A corpus-relative source MUST NOT: its referent is the corpus commit
  that carries both the manifest and the source, because the two are committed
  together, so the corpus's own history pins the pack and the digest proves its
  bytes. A corpus-relative entry that DOES carry a `commit` is refused, because it
  would name a commit the corpus cannot check; copying the corpus into a fresh
  repository, as every acceptance here does, would orphan it. The engine
  verifies the pin before importing a single line of the pack. **No entry-point scanning and no import-path
  discovery**: a pack that is installed but not listed does not run. A listed pack
  whose source no longer matches its digest is REFUSED, and the refusal is a
  FINDING against that pack carrying the expected and actual digests. The pack is
  never skipped silently.
- [ ] 15.1b **RUN EVERY PACK IN AN OS-ENFORCED SANDBOX, never by convention.**
  For each run the engine exports the corpus commit into a directory it owns
  (`git archive <commit> | tar -x`). It then starts the pack inside a sandbox that
  the KERNEL enforces. `chmod -R a-w` and a working directory are not a sandbox,
  because the pack runs as the same user and can undo the first and ignore the
  second. The reference realization on Linux is `bwrap` (bubblewrap):
  `--unshare-all` (network, PID, IPC, UTS and user namespaces),
  `--die-with-parent`, `--new-session`, `--ro-bind <copy> /corpus`,
  `--ro-bind <pack> /pack`, read-only binds of only the interpreter paths the
  pack's runtime needs, a private `--tmpfs /tmp`, the sandbox's OWN `--proc
  /proc` and a minimal `--dev /dev`, and nothing of `$HOME` or of the checkout.
  The procfs is the one of the sandbox's own PID namespace, so `/proc/self/fd`
  shows the pack's descriptors and no one else's. That is what gives the
  escaping fixture's descriptor hunt (15.6a) something real to search, and
  requirement 16 names exactly these as the runtime support a pack may see. **The process state is cleared as well as the filesystem.** A
  namespace hides paths, but it does not hide what the pack inherits.
  `--clearenv` is followed by `--setenv` of an explicit allowlist (`PATH`,
  `LANG`, `PYTHONNOUSERSITE=1` and nothing else), so no token, DSN or credential
  in the engine's environment reaches the pack. The engine spawns the sandbox
  with `close_fds=True` and passes exactly stdin from `/dev/null` and the two
  output pipes, so no database connection, socket or open file of the engine's
  is readable through `/proc/self/fd`. The pack's only output is findings and patches on stdout, in the
  neutral shape. **The time budget is enforced on the TREE, not the process.**
  Under `--unshare-pid` the pack runs in its own PID namespace, so ending the
  sandbox's init on timeout ends every descendant the pack forked, and none
  outlives the finding that records the timeout. **Where no such sandbox exists
  on the platform, packs do not run**, and `health run` reports that as a
  finding against the install rather than running packs unsandboxed. Other
  platforms need their own kernel-enforced equivalent before packs run there.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q9 (a),
  item 5):** The corpus export CANNOT BE STEERED by the corpus's own
  `export-subst` or `export-ignore` attributes. `git archive` honours both, so
  the corpus being judged could rewrite or hide what a pack is given: either
  the export is not a plain `git archive`, or those attributes are refused. The
  tree exported is still the corpus commit's, and the rest of the box stands.
  Carried out by plan 038's T048.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q16
  (a)):** A reading of requirement 16's SANDBOX clause (from *"A pack SHALL RUN
  IN A SEPARATE PROCESS INSIDE AN OPERATING-SYSTEM-ENFORCED SANDBOX"* to
  *"packs SHALL NOT RUN, and the install says why"*, `spec.md:544-557` at
  `main` `92010d3e`), of its ATTRIBUTION clause (*"THE PRODUCT'S OWN CHECKS ARE
  ATTRIBUTED BY THE SAME RULE … as the one pack no manifest lists"*,
  `:585-589`), and of this box's *"RUN EVERY PACK"*, which changes none of
  them. TRUSTED INSTALLED CODE runs IN PROCESS, on every platform, and only the
  packs 15.1a's manifest lists run in the sandbox:
  - the PRODUCT'S OWN CHECKS, 14.4's neutral families, run in process and are
    attributed `opendox`, as 15.7 says;
  - a HOST'S CHECK registered through `register_health_check` runs in process
    too, but ONLY at the scoped seam, as release 1 left it (openxFactory's
    `scripts/opendox_host.py:524` registers one), and its results are NEVER
    STORED, as no scoped run is;
  - the SANDBOX clause, and this box, govern manifest-listed packs, and the
    ATTRIBUTION clause is attribution only: it says how a built-in finding is
    attributed, not where the product's checks run.

  So every finding in the store stays attributable, and no host's finding
  claims the product's id. Where a probe finds no sandbox (macOS, a restricted
  Linux, a container), packs do not run, and one finding against the install
  says why, as this box already says. Release 2 has no Seatbelt realization.
  15.7 carries a pointer to this note. Carried out by plan 038's T048, T052 and
  T056.
- [ ] 15.2 A pack DECLARES its own version, which must equal its manifest entry's
  (15.1a), and its check families: id, version, and which documents each
  applies to. It RETURNS findings in the neutral shape — severity, resolution
  class (`auto-fix` / `assisted` / `human-only`, 14.6's spellings and no
  other), evidence — and MAY return proposed
  fixes AS PATCHES ONLY.
- [ ] 15.2a **THE ENGINE VALIDATES EVERY PATCH BEFORE ANY BRANCH EXISTS.** The
  sandbox (15.1b) contains the pack while it runs. It cannot contain what the
  engine does next with a returned patch, and `health fix` is the engine
  writing. So the engine checks each patch itself, as a unified diff, before
  14.6's applier touches a branch. A patch is REFUSED when any of these holds:
  it edits a path other than the `path` its own finding names (a finding that
  names no document carries no patch); it names an absolute path, a path with a
  `..` component, or a path with a `.git` component in any letter case; its
  target is a symbolic link in the corpus or lies below one; it creates,
  deletes, renames, copies or re-modes a file, or is a binary patch, which the
  engine recognizes by the headers `new file mode`, `deleted file mode`,
  `rename from`, `copy from`, `old mode` and `GIT binary patch`; or it is larger
  than the engine's bound, 65,536 bytes by default (the order of the server's own
  `_MAX_BODY_BYTES`), which is declared here and never read from the pack. Each
  refusal is a finding against the pack that proposed it, whose `evidence` names
  the refused finding (`refused_patch`) and the check it failed (`reason`), and a
  refused patch creates NO branch. Only a patch that passes every check reaches
  `git apply --check` against the draft branch's base, and a patch that applies
  is still a draft on a branch (14.7).
- [ ] 15.3 A pack's labels resolve through the DISPLAY FACET
  (`src/opendox/display_profile.py`), never spelled into the neutral surface —
  the same rule slice S7 applied to the front end, and the reason
  `NEUTRAL_DISPLAY`'s six words stay openDox's own.
- [ ] 15.4 **THE ENGINE KEEPS**, identically for every pack: the Health view and
  its CLI parity, scheduling, the baseline, storage (results in the store,
  exceptions in git), and the fix loop with its landing rule.
- [ ] 15.5 **THE REFUSALS**, each as a test and not as prose: a pack that writes,
  commits or merges (15.1b: it cannot reach the checkout, and a refusal that
  surfaces as the pack failing is a finding); a pack consumed without its pin (15.1a: commit and digest, or
  digest alone for a pack the corpus carries); a pack that
  returns a class the engine does not declare, or declares its own baseline or
  landing rule; a patch beyond its own finding's document (15.2a); and a declared
  version that disagrees with the pack's manifest entry (15.1a).
- [ ] 15.6 **A PACK THAT CRASHES OR TIMES OUT IS A FINDING AGAINST THAT PACK**,
  and the other packs still run. Give it a time budget: `health run --timeout
  SECONDS` (14.5), default declared by this box, applied PER PACK and enforced by
  the engine rather than by the caller — a pack cannot opt out of it. So is a
  pack whose output the engine cannot parse as the neutral shape: none of that
  output is stored, and the finding says why. A health
  check whose failure mode is silence is worse than one that reports itself
  broken — the doc-health nightly failed silently every night from 2026-08-30 and
  nobody saw it.
- [ ] 15.6a **SHIP `tests/fixtures/pack-corpus`**: 14.9's `health-corpus` plus
  three fixture packs under `packs/`. `fixture-crashing-pack` raises on its
  first family, `fixture-slow-pack` sleeps past any timeout, and
  `fixture-writing-pack` tries to write, commit and merge in the tree it is given,
  and lets the operating system's refusal PROPAGATE, so that the failure is
  observable and the acceptance can require it to be reported. (A pack that
  swallowed the refusal would still be contained, and 15.1b does not promise to
  see it.) Two more test the SANDBOX rather than the contract.
  `fixture-escaping-pack` tries each escape in turn. It restores write
  permission and writes, follows a symlink planted to point out of its copy,
  opens a network connection, reads `$HOME`, looks for a CANARY variable the
  engine sets in its own environment before spawning, and walks `/proc/self/fd`
  for a CANARY descriptor the engine holds open. It reports which attempts succeeded,
  and the answer must be none. `fixture-forking-pack` forks a child that sleeps
  past the budget. Three more test what a pack RETURNS.
  `fixture-garbage-pack` writes bytes that are not the neutral shape to stdout and
  exits 0. `fixture-anonymous-pack` declares no version, while its manifest entry
  names one. `fixture-patching-pack` returns six findings, each naming its own
  document and carrying a patch: `patch-ok`, a valid edit of that document, and
  one of each kind 15.2a refuses — `patch-other-document`, `patch-traversal` (a
  `..` path), `patch-git-metadata` (`.git/config`), `patch-rename` and
  `patch-oversized`. A
  `health/packs.yaml` registers all eight through 15.1a's manifest by corpus-relative
  `source`, pinned by digest and carrying NO `commit`, as 15.1a requires of a
  source the corpus itself versions. Because packs and manifest travel INSIDE the corpus,
  copying the fixture into a fresh repository carries a valid registration with
  it, and the acceptance loads the packs through the product's real path rather
  than an in-process fake. A test keeps the fixture digests current. These are
  fixtures of the engine, not shipped packs, and they exist so 15.6 and 15.1a are
  falsifiable rather than asserted.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q9 (a),
  items 4 and 6):** Two of the fixture packs are made exact.
  `fixture-forking-pack` gives the child it forks ITS OWN PACK ID IN ARGV, so
  F15.1's `ps` check, which counts processes whose arguments name
  `fixture-forking-pack`, cannot pass vacuously on a child whose arguments name
  nothing. And `fixture-escaping-pack` counts its "restores write permission"
  attempt as a success only when a WRITE succeeds, never on the `chmod` alone.
  The other six packs, and their registration by digest with no `commit`,
  stand. Carried out by plan 038's T055.
- [ ] 15.7 **PACK ID AND PACK VERSION ON EVERY FINDING, in the SAME additive
  migration as the results table** (group 14.1 — `0003_`, since `0002_` is the
  ledger), so the table is not migrated twice. **The ENGINE stamps both, and the
  pack is not asked.** `pack_id` and `pack_version` are the manifest entry's that
  launched the run (15.1a), never values read from the findings the pack
  returns, so a pack cannot attribute its findings to another pack, and a
  refusal raised before a pack ever runs still carries its entry's id and
  version. Both columns are `NOT NULL` in `0003_`, so no path can store a
  finding without them: requirement 16's provenance scenario, enforced at the
  store and not only in the engine. **The product's own checks are the one pack
  no manifest lists.** A finding a neutral family (14.4) raises carries
  `pack_id` `opendox`, the distribution name `pyproject.toml` declares, and
  `pack_version` the installed version,
  `importlib.metadata.version("opendox")`. 15.1a refuses a manifest entry whose
  `id` is `opendox`, so no pack can pass as the product.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q16
  (a)):** A pointer. 15.1b's batch Q note reads requirement 16's attribution
  clause as attribution only. The product's own checks run in process and are
  attributed `opendox`, as this box says, and a host's check registered at the
  scoped seam runs in process and is never stored, so the store holds no
  finding of it to stamp. Nothing in this box moves. Carried out by plan 038's
  T042, T046 and T056.
- [ ] **FALSIFIED BY** (openDox-code, installed, over 15.6a's `pack-corpus`, whose
  manifest registers its eight fixture packs beside the neutral checks):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v15"                       # a FRESH environment: nothing already installed stands in
      . "$W/v15/bin/activate"
      pip install ".[test]"
      export OPENDOX_INSTALL_MODE=local                     # the store is Group 13's bundle: a prerequisite by name
      export OPENDOX_STATE_DIR=$(mktemp -d)
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      C=$(mktemp -d)/pack-corpus
      cp -r tests/fixtures/pack-corpus "$C"   # packs + manifest travel inside
      git -C "$C" init -q
      git -C "$C" add -A
      git -C "$C" commit -qm fixture
      FIXTURE_HEAD=$(git -C "$C" rev-parse HEAD)
      # the eight fixture packs of 15.6a are registered; the run is itself bounded,
      # so a hang is a FAILED FALSIFICATION and never a hung falsifier:
      timeout 120 opendox health run --repo-root $C --timeout 5
      # the WRITING pack reached only its isolated copy (15.1b): the user's tree is untouched
      test -z "$(git -C "$C" status --porcelain)"           # nothing in the checkout moved
      test "$(git -C "$C" rev-parse HEAD)" = "$FIXTURE_HEAD" # and no commit landed on it
      # the FORKING pack left no descendant past its budget: the sandbox ended the whole tree
      test "$(ps -eo args | grep -c '[f]ixture-forking-pack' || true)" -eq 0
      # the neutral checks still produced findings despite a crashing pack:
      opendox health list --repo-root $C > "$W/p1.txt"
      grep -q 'broken-link' "$W/p1.txt"
      # and EVERY pack that misbehaves in the run is itself a finding, attributed:
      opendox health list --repo-root $C --json > "$W/p1.json"
      python3 - "$W/p1.json" <<'PY'
      import json, sys
      f = json.load(open(sys.argv[1]))
      ids = {x['pack_id'] for x in f}
      assert 'fixture-crashing-pack' in ids, 'crashing pack not reported'
      assert 'fixture-slow-pack' in ids, 'timed-out pack not reported'
      assert 'fixture-writing-pack' in ids, "a writing pack's failed write was not reported (it lets the refusal propagate)"
      assert 'fixture-garbage-pack' in ids, 'unparseable pack output was not reported'
      assert 'fixture-anonymous-pack' in ids, 'a pack declaring no version was not refused as a finding'
      escaped = [x for x in f if x['pack_id'] == 'fixture-escaping-pack' and x.get('evidence', {}).get('succeeded')]
      assert not escaped, f"a pack got out of its sandbox: {escaped}"
      assert all(x.get('pack_id') and x.get('pack_version') for x in f), 'a finding has no provenance'
      builtin = {x['pack_id'] for x in f if x['id'] == 'broken-link'}
      assert builtin == {'opendox'}, f"a built-in finding is not attributed to the product itself: {builtin}"
      print('packs attributed:', sorted(ids))
      PY
      # what a pack RETURNS is checked before any branch exists (15.2a):
      for f in patch-other-document patch-traversal patch-git-metadata patch-rename patch-oversized; do
        rc=0
        opendox health fix --repo-root "$C" --finding "$f" > "$W/pf.out" 2>&1 || rc=$?
        test "$rc" -ne 0                                    # refused...
        test -z "$(git -C "$C" branch --list "health-fix-$f")"   # ...and no branch exists for it
      done
      opendox health fix --repo-root "$C" --finding patch-ok
      git -C "$C" rev-parse --verify --quiet refs/heads/health-fix-patch-ok   # the valid patch IS a draft
      test "$(git -C "$C" rev-parse HEAD)" = "$FIXTURE_HEAD" # and the default branch never moved
      opendox health list --repo-root "$C" --json > "$W/p1b.json"
      python3 - "$W/p1b.json" <<'PY'
      import json, sys
      f = json.load(open(sys.argv[1]))
      refused = {x['evidence'].get('refused_patch') for x in f
                 if x['pack_id'] == 'fixture-patching-pack' and isinstance(x.get('evidence'), dict)}
      want = {'patch-other-document', 'patch-traversal', 'patch-git-metadata', 'patch-rename', 'patch-oversized'}
      assert want <= refused, f'a refused patch is not a finding against its pack: {sorted(want - refused)}'
      assert 'patch-ok' not in refused, 'the valid patch was refused'
      PY
      # a pack whose source no longer matches its PIN is refused, AS A FINDING (15.1a):
      echo "# tampered after pinning" >> "$C/packs/fixture-slow-pack/__init__.py"
      git -C "$C" commit -qam "tamper with a pinned pack"
      timeout 120 opendox health run --repo-root $C --timeout 5
      opendox health list --repo-root $C --json > "$W/p2.json"
      python3 - "$W/p2.json" <<'PY'
      import json, sys
      f = json.load(open(sys.argv[1]))
      hit = [x for x in f if x['pack_id'] == 'fixture-slow-pack' and 'digest' in json.dumps(x.get('evidence', '')).lower()]
      assert hit, 'a tampered pack ran, or was skipped silently, instead of being refused as a finding'
      assert all(x.get('pack_id') and x.get('pack_version') for x in f), 'a refusal has no provenance'
      PY
      # and 15.5's REFUSALS, each a NAMED test — a missing node fails the command:
      python -m pytest -q \
        "tests/test_check_packs.py::test_a_pack_that_writes_reaches_only_its_isolated_copy" \
        "tests/test_check_packs.py::test_a_pack_cannot_restore_write_permission_on_its_copy" \
        "tests/test_check_packs.py::test_a_pack_cannot_follow_a_symlink_out_of_its_copy" \
        "tests/test_check_packs.py::test_a_pack_has_no_network" \
        "tests/test_check_packs.py::test_a_pack_cannot_read_the_users_home" \
        "tests/test_check_packs.py::test_a_pack_sees_no_inherited_environment" \
        "tests/test_check_packs.py::test_a_pack_inherits_no_open_descriptor" \
        "tests/test_check_packs.py::test_no_descendant_of_a_pack_outlives_its_budget" \
        "tests/test_check_packs.py::test_no_sandbox_on_the_platform_means_no_packs_run" \
        "tests/test_check_packs.py::test_an_unpinned_pack_is_refused" \
        "tests/test_check_packs.py::test_a_pack_returning_an_undeclared_class_is_refused" \
        "tests/test_check_packs.py::test_a_pack_declaring_its_own_baseline_or_landing_rule_is_refused" \
        "tests/test_check_packs.py::test_unparseable_pack_output_is_a_finding_against_the_pack" \
        "tests/test_check_packs.py::test_a_declared_version_that_disagrees_with_the_manifest_is_refused" \
        "tests/test_check_packs.py::test_provenance_is_stamped_from_the_manifest_not_the_pack" \
        "tests/test_check_packs.py::test_the_store_refuses_a_finding_without_provenance" \
        "tests/test_check_packs.py::test_a_builtin_finding_carries_the_products_own_id_and_version" \
        "tests/test_check_packs.py::test_a_manifest_entry_claiming_the_products_id_is_refused" \
        "tests/test_check_packs.py::test_a_patch_may_edit_only_its_own_findings_document" \
        "tests/test_check_packs.py::test_a_patch_outside_the_corpus_or_into_repository_metadata_is_refused" \
        "tests/test_check_packs.py::test_a_patch_through_a_symlink_is_refused" \
        "tests/test_check_packs.py::test_a_patch_that_creates_deletes_renames_or_remodes_is_refused" \
        "tests/test_check_packs.py::test_a_patch_over_the_size_bound_is_refused" \
        "tests/test_check_packs.py::test_a_refused_patch_creates_no_branch"

  Every finding carries a pack id and version, the refusals and the product's
  own findings included (a neutral `broken-link` is attributed to `opendox`
  itself). **Every
  pack that misbehaves in the run** — crashing, slow, writing, unparseable and
  unversioned — appears as a finding, rather than as a stack trace, a hang, or an
  edit to the user's tree, and the run completes. Each of the five refused patches
  leaves no branch and a finding that names it, and the one valid patch is a draft
  on a branch while the default branch stays at the fixture's own commit. The
  writing pack is checked where it runs: straight after the run, the checkout
  must be clean and still at the fixture's own commit. An in-process pack would already have moved it. The
  outer `timeout 120` is the difference between a falsifier that FAILS on a
  runaway pack and one that HANGS on it: without it, the very defect 15.6 exists
  to prevent would take the acceptance command down with it, and the box would
  look unfinished rather than failed. The JSON is captured to a file and read by
  `sys.argv[1]`, because a heredoc and a stdin redirect cannot both feed the same
  interpreter and the heredoc wins.

  Today none of this exists: there is no pack contract, no health run, and no
  findings store.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q9 (a),
  items 2 and 3):** Two steps join the block. First, it ASSERTS ITS PLATFORM
  PRECONDITION, a working kernel sandbox, and exits 1 naming it otherwise, as
  F12.2 asserts `gh` absent. Straight after the install:

      if ! bwrap --unshare-all --die-with-parent --ro-bind / / --proc /proc --dev /dev true >/dev/null 2>&1; then
        echo "FAIL: no working kernel sandbox (bwrap); packs cannot run here, so this acceptance cannot"; exit 1
      fi

  So a machine where packs do not run (15.1b) fails this falsifier rather than
  passing it on a finding against the install. Second, it STARTS THE DOCUMENT
  SERVER before the first `health run`, as F14.1 does under this batch and for
  the same reason, which here concerns the `health` verbs alone. After
  `FIXTURE_HEAD` is recorded, with the setting the block already exports:

      opendox generate-and-open --repo-root "$C" --repository fixture --no-open --port 8085 &
      SERVER=$!; trap 'kill "$SERVER" 2>/dev/null || true' EXIT
      ready=0; for _ in $(seq 1 30); do curl -sf http://127.0.0.1:8085/ >/dev/null && { ready=1; break; }; sleep 1; done
      test "$ready" -eq 1                                   # a server that never started FAILS here

  `generate-and-open` mints its run directory outside the corpus
  (openDox-code `a9ac96f9`, `cli.py:802-823`), so the writing pack's checks
  still read the corpus alone. The rest of the block stands as written, but for
  the selection lines the next note amends. This bookkeeping amendment does not
  itself touch the command above. Carried out by plan 038's T048 (the
  precondition), T046 (the server) and T058, and run by its T067 and T065.

  **AMENDED — T005 Batch Q (plan 038, 2026-10-06; `6003486656`; Ruled R2Q10
  (a)):** As F14.1's batch Q note says, a finding's `id` is a stable,
  pack-qualified key, so every literal-id use in this block becomes a
  SELECTION BY THE PLANTED FINDING'S FIXTURE DOCUMENT, read from `health list
  --json` captured to a file first. The patching pack's six findings name six
  documents of the corpus, each named after its old literal id (`patch-ok`,
  `patch-other-document`, `patch-traversal`, `patch-git-metadata`,
  `patch-rename`, `patch-oversized`), and the broken link's document is 14.9's.
  The uses, by line at `main` `92010d3e`:
  - `grep -q 'broken-link' "$W/p1.txt"` (`:3575`): the listing holds the
    planted broken link, selected by its document and `kind`;
  - `x['id'] == 'broken-link'` (`:3590`): `builtin` is taken over the findings
    whose `path` is that document and whose `kind` is `broken-link`, and it is
    still `{'opendox'}`;
  - the `--finding "$f"` loop over the five refused `patch-*` ids, with
    `health-fix-$f` (`:3595-3599`): the loop runs over the five documents, and
    `--finding` and the branch take the `id` selected for each one's
    `fixture-patching-pack` finding;
  - `--finding patch-ok` and `refs/heads/health-fix-patch-ok` (`:3601-3602`):
    the `patch-ok` document's selected `id`, and `refs/heads/health-fix-<id>`;
  - the `refused_patch` values (`:3608-3612`): each refusal's
    `evidence.refused_patch` names the refused finding by its `id`, so the
    check reads that finding's `path` and compares the five refused documents
    with `want`, and the `patch-ok` document is not among them.

  The rest of the block stands, its assertions over `pack_id` included. This
  bookkeeping amendment does not itself touch the command above. Carried out
  by plan 038's T055 (the fixture documents) and T058, and run by its T067 and
  T065.

## Group 16 — Requirement 17: chat's model configuration (RULED, openDox-code)

**RULED** `#656` `5800995035`, 2026-09-23T18:56:33Z, answer 3: any
OpenAI-compatible endpoint, configured as a URL, a model name and a credential
reference and never a raw key, covering hosted APIs and local servers; a clear
"no model configured" state, with the rest of openDox working; and
`doxbench_provider.py` remains the only module that may contact a provider.
Phase 3 of release 1. `design.md` § D14 carries the measurements.

**What exists and is kept, measured at `1e4a57fb`.** The record that holds a
model provider already has no secret in it: `src/opendox/doxbench_binding.py`'s
`ModelProviderBinding` is frozen and slotted, with nine fields, `credential_ref`
being the reference a broker resolves, and a record naming an unknown key is
refused (`:316`). The operator door exists (`model-binding
list|add|edit|remove|set-credential`, `src/opendox/cli_model_binding.py`), and
so does the console's intake flow (`doxbench_intake`). This group builds on them
and redesigns none of them.

- [x] 16.1 **The OpenAI-compatible grammar joins as a SECOND DIALECT.**
  `DIALECTS` is closed at one member today, `xfactory-prompt-v1`
  (`doxbench_binding.py:109-110`): a POST of `{"model", "prompt"}` answered by
  `{"assistant_prose"}` (`doxbench_provider.py:622-624`), which no
  OpenAI-compatible server speaks. The record's own docstring names the lawful
  widening — *"A second member joins here and an arm joins beside the first in
  `doxbench_provider`; the check is never loosened"* — and this box is exactly
  that: a member `openai-chat-v1`, the chat-completions request (`model`,
  `messages`) and its answer (`choices[0].message.content`), spoken by an arm in
  `doxbench_provider.py` alone. An unknown dialect is still refused when it is
  declared.

  **Landed 2026-10-02** (T078): openDox-code#61 → `8a98e317`. `DIALECTS` gains
  `openai-chat-v1` after `xfactory-prompt-v1`, spoken by an arm in
  `doxbench_provider.py` alone; an unknown dialect is still refused; F16.1's
  dialect assertion passes.
- [x] 16.2 **A MODEL NAME the provider receives.** The record has no model
  field. The catalog handle is the binding's `id`, and `_post_to_provider`
  (`doxbench_provider.py:633`) sends that handle as the request's `model`, so no
  provider model can be named today. The record gains `model`, sent as the
  request's model and set by `model-binding add|edit --model`. The field list
  grows from nine to ten, and still no field can hold a secret.

  **Landed 2026-10-03** (T079): openDox-code#62 → `2fc714d2`. The binding record
  gains `model` (nine fields to ten, none able to hold a secret), sent as the
  request's `model` and set by `model-binding add|edit --model`; F16.1's
  `BINDING_FIELDS` assertion passes.
- [x] 16.3 **The credential stays a REFERENCE, and a raw key is refused when it
  is declared.** Measured: the record checks the endpoint's scheme and nothing
  else (`ENDPOINT_SCHEMES`, `:116`), so `https://user:<key>@…` and
  `…?api_key=<key>` are both ACCEPTED today, into a file the module calls safe to
  commit, while an extra `api_key` field is refused. The product already has the
  detector: `runtime/local_git_adapter.py:1146`'s `carries_a_credential` flags
  both URLs and passes a clean one, and the record uses it. An endpoint that
  takes no credential, the usual local server, declares that explicitly and
  never by a field left out. **Named here, decided by the realization:** what
  resolves a reference in a standalone install. Every record today names a broker
  program (`broker_argv`, required), and the one broker that exists,
  openProfiler's `openprofiler-broker`, is a separate product (`design.md`
  § D14).

  **AMENDED — T007 Batch H (`5850003126`; Ruled R1Q17 (b), R1Q18 (a)):** An
  addendum. This box leaves two choices to the realization (`design.md`
  § D14), and the answers name them. What resolves a reference in a
  standalone install (R1Q17 (b)): a built-in resolver takes `env:NAME` and
  OS-keyring references, at call time and inside `doxbench_provider.py`
  only, and a record whose reference it takes needs no broker. How an
  endpoint that takes no credential declares so (R1Q18 (a)): a third auth
  kind, `none`, under which `broker_argv` and `credential_ref` are
  forbidden, so the absence is declared and never a field left out. `none`
  joins `AUTH_KINDS` after the two kinds that exist, `api_key` and `oauth`,
  so F16.1's `AUTH_KINDS[0]` is unchanged and still names a kind that takes
  a credential. The rest of the box stands: a reference is never a raw key,
  and a raw key is refused when it is declared. Carried out by T080.

  **AMENDED — T007 Batch K (`5916000030`, item 1; the loopback rule
  `5880893901`; the broker path `5890601202`):** A pointer. The amendment
  itself is the dated note in requirement 17's body in this change's spec
  delta, above its scenarios, and it narrows one thing: the route a
  credential travels by. A credential the built-in resolver resolves (the
  `env:` and `keyring:` references of batch H's addendum above) and a token
  a broker mints are each sent only over `https://`, or over `http://` to
  `127.0.0.1`, `[::1]` or `localhost`. A binding that would present either
  over `http://` to any other host is refused when it is declared
  (`ENDPOINT_NOT_PRIVATE`), before anything is resolved or minted. The
  request that presents a credential follows no redirect, and over plain
  `http://` it takes no proxy. The auth kind `none` presents nothing and
  keeps whatever route it declares. This group's RULED paragraph
  (`5800995035`, answer 3), which says "any OpenAI-compatible endpoint",
  reads with that note.
  The rest of the box stands, and so does F16.1: its control record names a
  broker reference on a loopback endpoint, which the rule accepts, and its
  three raw-key refusals are unchanged. This bookkeeping amendment does not
  itself touch the Python below. Carried out by T080 (openDox-code#63) and
  openDox-code#64, which is no task of plan 034.

  **Landed 2026-10-03** (T080): openDox-code#63 → `1130e996`. A key in the
  endpoint URL or in an extra field is refused when declared; `env:NAME` and
  keyring references take the built-in resolver at call time inside
  `doxbench_provider.py` alone; auth kind `none` forbids `broker_argv` and
  `credential_ref`; a credential travels only over `https://` or loopback
  `http://` (`ENDPOINT_NOT_PRIVATE`, batch K). The broker path's hardening, no
  task of the plan, landed as openDox-code#64 → `8e377823`.
- [x] 16.3a **A served repository's bindings are TRUSTED PER MACHINE.**
  **ADDED — T007 Batch M (`5962785556`, item 2):** Brett Heap's multi-choice
  word of 2026-10-02, verbatim *"Trust per machine (Recommended)"*, which
  asks for this amendment. The batch adds this box, a dated note in
  requirement 17's body in this change's spec delta, and F16.1's batch M
  block below. It rewrites no ratified line.

  **Measured at openDox-code `main` `047bb4fa`.** Both entry points read the
  bindings from the repository they SERVE. `cli.py:618` and `serve.py:2214`
  call `declared_model_port_factory` with the served root (`--repo-root`,
  `cli.py:567`), and the factory reads `bindings_path(checkout_root)`
  (`doxbench_install.py:316`), the root's
  `ideation/dashboard/model-provider-bindings.yaml` (`doxbench_binding.py:166`
  and `:554`). A binding written into that file by hand, or arriving with a
  clone, passes no approval, because the intake flow's pending list holds back
  only the bindings its own wizard wrote (`doxbench_install.py:324`). A
  hand-written binding whose `broker_argv` was `["/bin/sh", "-c", "id > …"]`
  was offered as available, and the first dispatch ran it before refusing:
  the file it named read `uid=1000(…)`. The adversarial review of 2026-10-02
  found the same on `main`, and on the phase-3 drafts that add 16.3's
  built-in resolver (T080, openDox-code#63, with #64 above it) it also sent a
  `credential_ref` of `env:ADV_UNRELATED_CLOUD_SECRET` to a listener the file
  named, as `Authorization: Bearer …`. `model-binding set-credential` runs a
  declared binding's broker too (`cli_model_binding.py:135-139`). Release 1
  publishes to PyPI (`5962754358`, item 1), so whoever serves a repository
  someone else wrote would meet each of these.

  **The rule.** A binding read from the served repository runs a broker, or
  resolves any credential reference (`env:`, `keyring:` or a broker's), ONLY
  after the operator has trusted THAT EXACT binding on THIS machine. It works
  like direnv. The rule holds on every path that runs such a broker: a chat
  turn and `model-binding set-credential`. The console intake's hand-off
  (`serve_workbench.py:1127`) also runs a broker the served repository
  declares, in `ideation/dashboard/model-declarations.yaml`
  (`doxbench_intake.py:154`), which is no binding, so no binding's trust
  admits it. Under the neutral default below it is refused by name. No
  command that trusts an intake declaration's broker is ruled, and
  standalone the intake surface already answers `offered: false`
  (`5961364221`, item 1). A host's own policy may admit it.
  - **Where trust lives.** In the operator's own state, never in the
    repository: a file under `OPENDOX_STATE_DIR`, the state directory that
    13.1's bundled server uses (openDox-code#69, T072). Unset, that is
    `$XDG_STATE_HOME/opendox` where that is absolute, and otherwise
    `~/.local/state/opendox`. The file holds no credential. It is written
    owner-only, and it is read only once it passes the checks #69's bundle
    makes of its own tree: the file and the directories that hold it are real
    (no symbolic link), owned by this user and writable by no one else, and
    each directory above them is this user's or root's, and sticky where
    another user can write it. A trust file that fails a check is refused by
    name, and every binding then reads untrusted. `config.state_dir()`
    accepts any absolute path free of `..`, so the trust file's resolved
    path is also checked against the served root: an `OPENDOX_STATE_DIR`
    equal to the served root, or nested under it, is refused by name before
    anything is written, and every binding then reads untrusted. No trust is
    ever written into, or read from, a tree a clone could carry.
  - **What a trust names.** The repository root's resolved path, the
    binding's id, and a digest of the binding's full record, every field of
    it. So any edit makes the binding untrusted again, and so does the same
    file under another root: a clone, a copy or a moved checkout.
  - **What records it.** `opendox model-binding add` and `edit` record trust
    for the binding they write. `opendox model-binding trust <id>` records it
    for a binding already declared. It first prints what will run (the broker
    argv) and where the credential goes (the endpoint, the auth kind and the
    credential REFERENCE), and never the credential itself. Each value it
    prints is escaped, in a JSON string's form, because each comes from a
    repository someone else may have written: a newline or a terminal
    control character in a field cannot forge or hide what is shown. The
    refusals, the factory's notice and `model-binding list` print the id the
    same way. It resolves no reference, runs no broker and contacts nothing,
    and it records trust for exactly the record it printed. It takes no `--yes`: running it is the
    consent, as `direnv allow` is, and the refusal below names it.
    `opendox model-binding set-credential` on a TRUSTED binding re-records
    trust for the record it rewrites with the broker's new reference, since
    the operator made that change on this machine. It never makes an
    untrusted binding trusted.
  - **What an untrusted binding gets.** It is refused BY NAME before any
    process is spawned, any credential is read or any endpoint is contacted.
    The refusal names the binding's id and the command that trusts it, and
    nothing secret. `set-credential` refuses it the same way, before its
    broker runs, and leaves it untrusted. The catalog lists it with
    `available: false`. The catalog's entry is a closed shape
    (`xfactory-workbench-model-catalog`, `additionalProperties: false`), so
    the reason is not a key in it: it is carried by the refusal a turn that
    names the binding receives, by the notice the factory writes where it
    already reports a pending binding, and by `opendox model-binding list`.
  - **Bindings stay committable.** The bindings document does not change,
    and no trust is ever read from it.
  - **Whose rule it is.** This is openDox's NEUTRAL default, and a strict
    one. Its consumers, the code that reads a served repository's bindings,
    register it lazily, the first time one asks and only where nothing is
    registered yet. So no entry point registers it, and a bare process is
    held to it too. A host's own registration wins: a host such as
    openxFactory may register a policy of its own.

  The rest of Group 16 stands, and so do 16.3's text and its batch H and K
  addenda. F16.1's batch M block below falsifies this box. Carried out by
  T100.

  **AMENDED — T007 Batch P (`5982436447`, item 2; `5983805990`):** Brett
  Heap's multi-choice word of 2026-10-04, verbatim *"Refuse in-repo programs
  (Recommended)"*, answers finding A2 of the holder's adversarial review of
  T100 (openDox-code#82, landed as `38d3350e`). A trust names a digest of
  the binding's record, and the record names a broker's program only by its
  path. So a trusted binding whose broker runs a program inside the served
  repository stayed trusted after a pull changed that program. The rule: a
  binding's command may not name a file inside the served repository, and
  the broker lives outside it. Every member of the command is judged, the
  program and each argument alike, so a script handed to an outside
  interpreter is caught too, and a relative path is judged against the
  served root. Such a binding is refused by name, both where
  trust is recorded (`add`, `edit`, `trust` and `set-credential`) and where
  trust is checked, before any process is spawned. The refusal names the
  remedy, a broker installed outside the repository, and never a secret, and
  the binding reads untrusted. A shell or interpreter wrapper would carry
  the same attack through an inline script, `["sh", "-c", "exec
  ./tools/broker.py"]`, so Brett Heap's second word on it (`5983805990`,
  verbatim *"Refuse inline scripts (Recommended)"*) extends the rule:
  - a binding whose program is a shell or an interpreter given an inline
    script, such as `sh -c`, `bash -c`, `python -c` or `node -e`, is
    refused by name in the same places and the same way;
  - the program must be a real file outside the served repository. Every
    member of the command that names a path, the program and each argument
    alike, is judged both as named and as it resolves: links are followed,
    the program, when it is a bare name, is looked up on `PATH`, and a
    relative path is taken against the served root. Both must lie outside
    the repository, when trust is recorded and again before any spawn. So
    neither a link outside the repository nor a `PATH` entry inside it can
    bring the program or its script back in, and a link inside the
    repository, which a pull could retarget, is refused even when it points
    outside;
  - *"a real file"* is read by what it forbids to RUN (the holder's ruling
    `5985553609`, which neither narrows nor extends `5983805990`): no
    binding whose program is not a real file outside the served repository
    ever runs. An inline script, or a file inside the repository (as named
    and as resolved, through a launcher, a link, a `PATH` entry or an
    option's value), is refused by name where trust is recorded and again
    before any spawn, as this addendum says. A program that cannot be found
    (not on `PATH`, no such file) runs nothing: it is not refused where
    trust is recorded, and when its broker is started the start fails and
    the binding is refused by the existing named refusal
    `broker_unreachable` (the broker could not be started). A broker installed later is judged
    before it is started, like any other. A check at trust that the program exists is
    not ruled; it stays open for Brett Heap as a follow-on that would move
    no box of release 1, and F16.1 carries no case for a missing program;
  - a common launcher (`env`, `nice`, `nohup`, `timeout`, `stdbuf`,
    `setsid`, `xargs` and the like, with their flags) is unwrapped to the
    program it starts, and the inline-script and path rules apply to THAT
    program (the holder's ruling `5984069416`, implementing `5983805990`).
    A launcher's own options are judged with it, read by GNU
    `getopt_long`'s grammar (the holder's ruling `5985046107`, C1 and C4,
    which applies those two and extends neither):
    - a long option matches by its unambiguous prefix, in the
      `--option=value` and the `--option value` forms, so `env --chd=…` is
      `env --chdir`, and a short-option cluster parses the getopt way
      (`-iS…`, `-vC/dir`, `-0u NAME`). An ambiguous or unknown option of an
      unwrapped launcher is refused by name;
    - an option that names a path, such as the directory `env --chdir`
      (`-C`) starts the program in, or the file `xargs -a` (`--arg-file`)
      reads its arguments from, in any spelling, is judged as the
      command's paths are, both as named and as it resolves. So a launcher
      cannot start the broker inside the repository, nor let the
      repository decide the broker's arguments;
    - the string `env -S` (`--split-string`) carries is split into the
      arguments it names, which are then unwrapped and judged, ONLY when it
      holds no backslash and no `$`. Otherwise it is refused as unreadable,
      as an inline script is. GNU `env`'s own escape and `${VAR}` grammar
      is not modelled: an accepted limit, refused rather than guessed;
  - every broker also starts with its working directory outside the served
    repository, as defence in depth, and with an environment that points
    away from it: `PWD` and `OLDPWD` are dropped, and so is every other
    variable whose value is a path inside the served repository, while a
    path list (`PATH`, `PYTHONPATH`, `NODE_PATH` and the like) loses each
    entry that lies inside it, so a runtime cannot load code from the
    repository through its search path. Each such path is judged, as the
    command's paths are, both as named and as it resolves, and so is each
    assignment a launcher makes (`env NAME=value`): one whose value is a
    path inside the repository, or a path list with an entry inside it, is
    refused;
  - a path given to the program that finally runs as an option's value is
    judged as the command's paths are, both as named and as it resolves,
    and refused when it lies inside the repository: the value after `=` in
    one member (`--require=<repo>/x`), and the remainder after the option
    letter of a single-dash option with its value attached
    (`-I<repo>/lib`, `-a<repo>/args`; the holder's `5985046107`, C4). An
    output path into the repository is refused too, an accepted
    strictness;
  - an ACCEPTED release-1 limit: a general program outside the repository
    that runs code from its own arguments (`awk`, `find -exec`, …) is not
    judged by the argv check, and any other path embedded inside an option
    string given to the program that finally runs, such as one carried in
    a variable (`NODE_OPTIONS=--require=…`), is one the argv check does
    not promise to find. A known launcher's own options are never part of
    this limit; the launcher bullet above judges them. The trusted argv is
    digested, and the working directory and the environment point away
    from the repository, so a relative path in such a string does not
    reach it;
  - a broker such as `sh -c "pass show key"` is declared as
    `["pass", "show", "key"]` instead, or as a script kept outside the
    repository.

  The rest of this box stands. A dated note in requirement 17's body in this
  change's spec delta, after batch M's, records both rulings, since they
  narrow batch M's note there, and F16.1's batch P cases below falsify
  them. Carried out by a
  T100 follow-on openDox-code PR (claim `5982447319`), which is no task of
  plan 034 and lands before T087.

  **AMENDED — T007 Batch P (`5982436447`, item 3):** A clarification of
  *"No trust is ever written into, or read from, a tree a clone could
  carry"* above. Brett Heap's multi-choice word of 2026-10-04, verbatim
  *"Served repo only, limit (Recommended)"*, answers finding A14 of the same
  review. The tree that sentence means is the SERVED repository. An
  `OPENDOX_STATE_DIR` equal to the served root, or nested under it, is
  refused by name, as the bullet above says, and no trust is written into
  or read from it. A state directory inside some OTHER git checkout is not
  refused, and release 1 accepts that as a limit. A check for any enclosing
  checkout would refuse a home directory kept in git (a dotfiles checkout),
  which holds the default state directory. No code changes for it, and this
  bookkeeping clarification edits no line of the box. Carried out by T100,
  as landed.

  **Landed 2026-10-05** (T100, openDox-code#82 → `38d3350e`; the T100 follow-on,
  openDox-code#86 → `651c35fe`, before T087): the follow-on carries out Brett
  Heap's `5982436447`, item 2, and `5983805990`, which batch P records, with the
  holder's `5984069416`, `5985046107` (C1 to C5) and `5985553609`, and the
  holder's A8; item 3 (A14) changes no code. Run by T089's runner against the
  follow-on's head `aecac805`, whose tree landed unchanged, F16.1's block as
  batch P amends it exits 0, with `532 passed` in
  `tests/test_model_binding_trust.py`, batch P's section 9 among them, as
  openDox-code#86's body records. T083's run at `38d3350e` read `135 passed`
  there (`evidence/f16.1-run.md` § 2). F16.1 whole is T089's run at T087's pin.
- [x] 16.4 **"No model configured" is a STATE, shown before any turn.**
  Measured: with no binding, `declared_model_port_factory(...)()` resolves the
  harness declaration, and its catalog offers `omp-local`, "Local harness model",
  as AVAILABLE with no `omp` on the PATH (`doxbench_install.py:106`). The entry
  turns unavailable only after the bridge finds its child dead or unstartable, so
  an install with no model reads as one with a model until a turn fails. The
  views already carry a no-model posture (`web/views/doxbench-chat.js:272`,
  `web/views/staging-workbench.js:286`); what is missing is a catalog that lets
  them reach it. With no model configured, the catalog offers no available entry,
  the chat surface shows "no model configured" and how to configure one, and a
  turn is refused `model_capability_unavailable` before any process is spawned or
  any endpoint is contacted. The harness route is not removed: an install whose
  harness is present still declares it.

  **Landed 2026-10-03** (T081, T085, T102): openDox-code#74 → `9a490405` makes
  "no model configured" a state. With no binding and no harness the catalog
  offers no available entry, a turn is refused `model_capability_unavailable`
  before anything is spawned or contacted, and the chat rail shows a line saying
  that no model is configured and how to configure one, while an install whose
  harness is present still declares it. openDox-code#71 → `2680eb5e` gives the
  served catalog route its standalone validators, and T102 (openDox-code#81 →
  `0116293a`) offers the chat rail by scope on a standalone workbench. In T083's
  run at openDox-code `38d3350e`, F16.1's catalog block prints
  `no model configured: the catalog offers nothing` and
  `tests/test_chat_model_configuration.py` reads `83 passed`
  (`evidence/f16.1-run.md` § 2). AT-R1's browser half (T096) opens the chat rail
  from a grouping tile in its own run.
- [x] 16.5 **Every other surface works with no model.** Documents, generation,
  the views, sessions and saving answer exactly as they do with a model
  configured, and nothing waits on, retries or reports a model. Group 10's
  falsifier already runs the whole product from a fresh install with no model
  configured; this box's named test keeps the property named.

  **Landed 2026-10-04** (T082): openDox-code#76 → `ca9e1bd5`. Section 6 of
  `tests/test_chat_model_configuration.py` serves one commit twice, standalone,
  once with no model and once with a binding, and requires every request about
  documents, generation, the views, sessions and saving to answer alike, in
  status, content type and body. openDox's own settings documents are kept out
  of the corpus, so adding a binding moves no snapshot. The named file reads
  `83 passed` at that landing, and again in T083's run at openDox-code
  `38d3350e` (`evidence/f16.1-run.md` § 2).
- [x] 16.6 **The boundary stays ONE module wide, and its instrument RUNS.** The
  property holds at `1e4a57fb`: an AST scan of `src/opendox/` finds three modules
  that touch a network client, and only `doxbench_provider.py` reaches a model
  provider (`runtime/oidc.py` fetches the identity broker's keys with `httpx`,
  and `session_git.py` calls only `socket.gethostname()`). The instrument does
  not hold. `tests/test_provider_boundary.py` is a standing red that no required
  check runs (`validate.yml:361-370` records it), and under `--noconftest` at
  `1e4a57fb` it fails 12 of 28, for three stale reasons. It still reads
  `snapshot_registry.py`, which the carve sent to openXdox. It pins by filename
  seven per-module scan suites this checkout does not carry: five went to
  openXdox-code with the carve, and two stayed in openxFactory. And its package
  sweep now reaches the runtime subpackage, where `runtime/app.py` and
  `runtime/oidc.py` carry `Authorization` and `Bearer ` for the identity broker
  and `runtime/config.py:282-285` names `access_token` among its secret
  parameter keys. Group 9 makes the whole suite green, so the file is repaired in
  phase 1, and this box keeps it green as 16.1's dialect joins the one module.

  **Landed 2026-10-04** (T034, T083): openDox-code#50 → `71b631bc` repaired
  `tests/test_provider_boundary.py` for this box's three stale reasons, and
  T083's run (openxFactory#1231 → `0e01ca85`) reads it `24 passed` at
  openDox-code `38d3350e`, from a fresh clone and unchanged since T034, with
  16.1's `openai-chat-v1` arm and T100's `doxbench_trust.py` in the package. The
  boundary is still one module wide, and two planted controls each turn the
  instrument red (`evidence/f16.1-run.md` §§ 1 and 3).
- [x] **FALSIFIED BY** (an openDox-code checkout alone, fresh venv, no sibling
  and no harness installed):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v16"                      # a FRESH environment: nothing already installed stands in
      . "$W/v16/bin/activate"
      pip install ".[test]"
      for sibling in openxdox ideation_dashboard; do        # chat is judged with no consumer and no publisher
        if python -c "import $sibling" 2>/dev/null; then echo "FAIL: $sibling is importable"; exit 1; fi
      done
      if command -v omp >/dev/null 2>&1; then echo "FAIL: a harness is installed, so no-model is not what this measures"; exit 1; fi
      # the boundary is ONE module wide, and its instrument passes WHOLE (16.6):
      python -m pytest -q tests/test_provider_boundary.py
      # the OpenAI-compatible dialect and the model name are declared (16.1, 16.2), and a raw key is refused (16.3):
      python3 - <<'PY'
      from opendox import doxbench_binding as b
      assert "openai-chat-v1" in b.DIALECTS, f"no OpenAI-compatible dialect: {b.DIALECTS}"
      assert "model" in b.BINDING_FIELDS, f"the record names no model: {b.BINDING_FIELDS}"
      rec = {f: "stand-in" for f in b.BINDING_FIELDS}
      rec.update(auth_kind=b.AUTH_KINDS[0], dialect="openai-chat-v1", endpoint="http://127.0.0.1:9/v1/chat/completions")
      if "broker_argv" in rec:
          rec["broker_argv"] = ["stand-in-broker"]
      b.ModelProviderBinding.from_record(rec)               # the control: a clean record is accepted
      for bad in (dict(rec, endpoint="https://user:sk-stand-in@api.example.invalid/v1"),
                  dict(rec, endpoint="https://api.example.invalid/v1?api_key=sk-stand-in"),
                  dict(rec, api_key="sk-stand-in")):
          try:
              b.ModelProviderBinding.from_record(bad)
          except b.BindingRefused:
              continue
          raise SystemExit(f"FAIL: a raw key was accepted in {[k for k in bad if bad.get(k) != rec.get(k)]}")
      print("dialect and model declared; a raw key is refused in a field and in the URL")
      PY
      # NO MODEL CONFIGURED is a state the catalog reports before any turn (16.4):
      python3 - "$W" <<'PY'
      import pathlib, sys
      from opendox import doxbench_install as inst
      root = pathlib.Path(sys.argv[1]) / "no-model"
      root.mkdir()
      port = inst.declared_model_port_factory(root / "sessions", checkout_root=root)()
      offered = [e.model_id for e in port.catalog().available_entries()]
      assert not offered, f"no model is configured, yet the catalog offers {offered}"
      print("no model configured: the catalog offers nothing")
      PY
      # ...a turn reaches a stand-in OpenAI-compatible server on loopback, and every other surface answers with none (16.1-16.5):
      python -m pytest -q tests/test_chat_model_configuration.py

  **Today it fails at its first assertion**, because `DIALECTS` holds only
  `xfactory-prompt-v1`. Run against `1e4a57fb` with today's dialect in place of
  the new one, the URL half fails too, since both keyed URLs are accepted, and the
  no-model block fails with `['omp-local']`. `tests/test_provider_boundary.py`
  fails 12 of 28 under `--noconftest` and errors whole under the root conftest.
  The named file is the acceptance suite the realization adds: a stand-in
  chat-completions server on loopback that records each request, so a turn is
  proved to reach it in that grammar and naming the configured model, and the
  no-model assertions over the views and every non-chat route. `omp` is
  `doxbench_bridge.HARNESS_COMMAND`, and the check on it is a precondition: a
  machine with the harness installed has a model, and would measure something
  else.

  **AMENDED — T007 Batch M (`5962785556`, item 2):** F16.1 also falsifies
  16.3a, the box this batch adds. The runs that use it (T083 and T089) also
  run one more line after its last, and quote it:

      # a served repository's bindings are trusted per machine (16.3a):
      python -m pytest -q tests/test_model_binding_trust.py

  The named file is the acceptance suite T100 adds. Each case serves its own
  fresh `git init` with its own fresh `OPENDOX_STATE_DIR`, so no run reads or
  writes the operator's own trust. Each runs over three bindings in turn: one
  whose broker writes a marker file when it runs; one whose `env:` reference
  names a variable the test sets to a known value; and one whose `keyring:`
  reference names an entry in a stand-in keyring backend that records every
  lookup. The second and third point at a loopback listener that records
  every request. It asserts, one test per case:
  - **An untrusted binding is refused by name, with nothing spawned or
    read.** A binding written into the bindings document by hand, as a clone
    delivers it, is listed by the catalog with `available: false`. A turn
    that names it is refused, and the refusal names its id and `opendox
    model-binding trust <id>`. The factory's notice and `opendox
    model-binding list` name the same id and command. No marker file
    exists, the variable is never read, the keyring records no lookup, the
    listener records no request, and the known value appears in no output.
    `set-credential` on it is refused the same way, no marker file exists,
    and the binding is still untrusted after it. With a stand-in host that
    offers the console intake and registers no policy of its own, the
    intake's hand-off refuses by name a broker that the served repository's
    `ideation/dashboard/model-declarations.yaml` names, and no marker file
    exists.
  - **`add` records trust.** The same binding declared through `opendox
    model-binding add` is offered as available, and a turn runs its broker,
    or reaches the listener with the known value, the `env:` one and the
    `keyring:` one alike.
  - **An edit untrusts.** A hand edit of any one field of a trusted binding,
    every field of the record in turn, each given a valid replacement value,
    makes it untrusted again, and it is refused as above. A binding
    rewritten through `opendox model-binding edit` is trusted, and so is a
    trusted binding whose reference `set-credential` rewrote from a stand-in
    broker's answer.
  - **`trust` records.** For the hand-written binding, `opendox
    model-binding trust <id>` prints its broker argv, its endpoint, its auth
    kind and its credential reference. The known value appears nowhere in
    its output, no marker file exists, the keyring records no lookup and
    the listener records no request. After it, the binding is offered as
    available. A hand-written binding whose id, label and one broker argv
    member carry a newline and a terminal escape (`\x1b[2J`) is printed
    with both escaped, by `trust`, by `list` and in the refusal, and no raw
    control byte reaches the output.
  - **A binding moved to another root is untrusted.** A trusted bindings
    document, copied byte for byte into a second fresh repository, reads
    untrusted there, and it is refused as above.
  - **The trust file is checked.** With the trust file, or a directory that
    holds it, replaced by a symbolic link or made writable by another user,
    every binding reads untrusted, and the refusal names the file. With
    `OPENDOX_STATE_DIR` equal to the served root, and again nested under
    it, `add`, `edit` and `trust` are refused naming the setting before
    anything is written, and every binding reads untrusted. Nothing under
    the served root but the bindings document is written by `add`, `edit`
    or `trust`.
  - **The policy seam.** In a bare process that registers nothing, the
    first consumer to ask registers the strict default, and a hand-written
    binding is refused as above. A host policy registered before that first
    use is the one consulted, and the default does not replace it.

  The block's other lines are unchanged. Its 16.3 records are built in
  process and never served, and its 16.4 block declares no binding, so no
  trust is consulted there.
  **Today the line fails**, because the named file does not exist. Its first
  case fails at `047bb4fa` too: a hand-written binding is offered as
  available, and its `broker_argv` runs on the first dispatch. This
  bookkeeping amendment does not itself touch the command above. Carried
  out by T100, and run with F16.1 whole by T083 and T089.

  **AMENDED — T007 Batch P (`5982436447`, the holder's ruling A8):** A note,
  and no line of the block changes. The block says that with the trust file,
  or a directory that holds it, replaced by a symbolic link, every binding
  reads untrusted. The state directory is such a directory. Finding A8 of
  the holder's adversarial review of T100 found that T100 as landed
  (`38d3350e`) read a state directory that is itself a symbolic link to this
  user's own 0700 directory. Its suite's case passed only because that
  case's target was writable by others. The holder ruled that the
  realization follows this block's ratified text: a state directory that is
  itself a symbolic link is refused by name, and it trusts nothing. The T100
  follow-on openDox-code PR (claim `5982447319`) aligns the code and adds
  that case, before T087. So T089's run of F16.1, at T087's pin, which
  carries the follow-on, holds the realization to the block as written.
  T083's run at `38d3350e` predates the follow-on, and plan 034 records that
  it does not show this case. This bookkeeping amendment does not itself
  touch the command above.

  **AMENDED — T007 Batch P (`5982436447`, item 2; `5983805990`):** F16.1
  also falsifies 16.3a's batch P addendum (A2, and its reach to inline
  scripts). The command is unchanged: the named file of
  batch M's line, `tests/test_model_binding_trust.py`, also asserts, one
  test per case, under the same fresh `git init` and `OPENDOX_STATE_DIR`:
  - **A binding whose command names a file inside the served repository is
    refused.** Its broker argv names a file under the served root, either
    as its program, such as `tools/broker.py`, or as an argument, such as
    the script an outside interpreter runs (`["python3",
    "tools/broker.py"]`, `["sh", "tools/broker.sh"]`). Each is tested
    with the path absolute and with it relative to the served root, and the
    script writes a marker file when it runs. `opendox
    model-binding add`, `edit`, `trust` and `set-credential` each refuse it
    by name, naming the remedy, a broker installed outside the repository,
    and record no trust. A trust recorded for it before the rule does not
    admit it, before or after its program is edited: it reads untrusted, so
    the catalog lists it with `available: false`, as batch M's block asserts
    of an untrusted binding, and a turn that names it is refused by name
    before any process is spawned, and no marker file exists.
  - **An inline script is refused.** A binding whose program is a shell or
    an interpreter given an inline script (`["sh", "-c", "exec
    ./tools/broker.py"]`, and `python -c` in the same form) is refused by
    name by the same four commands and before any spawn, as above, with no
    marker file, whatever the script names, and so is one that reaches an
    inline script through a launcher, the holder's `5984069416`. The
    launcher case runs once for each launcher named in 16.3a's addendum, in
    an option-bearing form wherever the launcher takes options:
    `["env", "-i", "python3", "-c", "…"]`, `["nice", "-n", "5",
    "python3", "-c", "…"]`, `["nohup", "python3", "-c", "…"]`,
    `["timeout", "-s", "KILL", "5", "python3", "-c", "…"]`, `["stdbuf",
    "-oL", "python3", "-c", "…"]`, `["setsid", "-w", "python3", "-c",
    "…"]` and `["xargs", "-n", "1", "python3", "-c", "…"]` (`xargs` joins
    the launchers by the holder's `5985046107`, C4), and once more for a
    nested chain, `["env", "nice", "-n", "5",
    "timeout", "5", "python3", "-c", "…"]`, so every layer is unwrapped,
    and once through a string that `env -S` splits, `["env", "-S",
    "python3 -c '…'"]`. A trust recorded for it before the rule does not
    admit it: it reads untrusted, and the catalog lists it with
    `available: false`.
  - **An alias is judged both as named and as it resolves.** Each of these
    is refused by the same four commands and before any spawn, with no
    marker file, for the program and for an interpreter's script argument
    alike (`["python3", "<link>"]`), except where noted:
    - a symbolic link outside the served root whose target lies inside it;
    - a bare program name that resolves through a `PATH` entry under the
      served root, as the program only, since an interpreter does not look
      its script argument up on `PATH`;
    - a symbolic link inside the served root whose target is a real file
      outside it, since a pull could retarget the link.

    A trust recorded while the binding's paths resolved outside the root
    does not admit it once a link or the `PATH` entry leads inside: it reads
    untrusted and the catalog lists it with `available: false`.
  - **A broker outside the repository is still reached.** The same binding
    with its program a real file outside the served root, once trusted,
    runs as batch M's block says. It runs with its working directory
    outside the served root: the test starts `opendox` with its own
    working directory at the served root, so a broker that inherited it
    would record a directory inside the root, and the broker records the
    directory it starts in and its environment. It finds neither `PWD` nor
    `OLDPWD`, no variable whose value is a path inside the served root, and
    no entry inside the root in a path list. The test starts `opendox` with
    `PATH`, `PYTHONPATH` and `NODE_PATH` each carrying an entry inside the
    served root, and with a scalar variable, such as `OPENDOX_TEST_HOME`,
    set to a directory inside it, so an inherited one would show. It does
    the same again through aliases, each for a `PYTHONPATH` entry and for a
    scalar variable: one names a symbolic link outside the served root whose
    target lies inside it, and one names a symbolic link inside the served
    root whose target lies outside it, which a pull could retarget. And a launcher's own assignment is refused by
    the four commands and before any spawn, with no marker file:
    `["env", "PYTHONPATH=tools", "python3", "<outside>/broker.py"]`, where
    `<outside>` is the case's own scratch directory outside the served root
    (made by `mktemp -d`), and `tools`, relative to the served root, holds a
    `sitecustomize.py` that writes the marker. The same refusal holds for
    an assignment through an alias: `["env",
    "PYTHONPATH=<outside>/alias", "python3", "<outside>/broker.py"]` and
    `["env", "OPENDOX_TEST_HOME=<outside>/alias", "python3",
    "<outside>/broker.py"]`, where `<outside>/alias` is a symbolic link to
    `tools` inside the served root, and the same two assignments naming
    `tools/out`, a symbolic link inside the served root to a directory
    outside it. A launcher's own working-directory option is refused the
    same way, by the four commands and before any spawn, and the outside
    broker, which writes a marker file when it runs, leaves none:
    `["env", "--chdir=<root>", "python3", "<outside>/broker.py"]`, where
    `<root>` is the served root's absolute path; the same with `"-C",
    "<root>"`; and the long form naming `<outside>/alias`, the link to
    `tools` inside the served root, and naming `tools/out`, the in-repo
    link to a directory outside it.
  - **A path an option carries, an unreadable split string and a launcher
    option that cannot be read are refused, and a launcher's options are
    read as GNU reads them** (the holder's `5985046107`, C1 and C4). Each
    command below is refused by name by the same four commands and before
    any spawn, and leaves no marker file. `<outside>/broker` is an
    executable in the case's scratch directory that writes one when it
    runs, and `<outside>/broker.pl` a Perl script there that does the same:
    - `["perl", "-I<root>/lib", "<outside>/broker.pl"]` is refused as a
      command that names a file inside the served repository, since the
      path attached to a single-dash option is judged;
    - `["xargs", "-a", "<root>/args", "<outside>/broker"]` is refused as a
      command that names a file inside the served repository, since the
      repository would decide the arguments;
    - `["env", "--chd=<root>", "<outside>/broker"]` is refused as a
      command that names a file inside the served repository, since
      `--chd` is the unambiguous prefix of `env`'s `--chdir`;
    - `["env", "-S", "sh\\_-c\\_id"]` (escaped as JSON: the string is
      `sh\_-c\_id`, which GNU `env` reads as `sh -c id`) is refused as an
      inline script, since a split string that holds a backslash or a `$`
      is unreadable;
    - `["<outside>/broker", "--config=<root>/conf"]` is refused as a
      command that names a file inside the served repository, since the
      value after `=` of the final program's option is judged;
    - `["<outside>/broker", "-o<root>/out"]` is refused the same way, since
      an output path into the repository is refused too, an accepted
      strictness;
    - `["env", "--i", "<outside>/broker"]` is refused by name, fail-closed,
      since `--i` is an ambiguous prefix (`--ignore-environment`,
      `--ignore-signal`);
    - `["env", "--no-such-option", "<outside>/broker"]` is refused by name,
      fail-closed, since `env` has no such option;
    - `["env", "--d", "<outside>/broker"]` is refused by name, fail-closed,
      since `--d` is an ambiguous prefix (`--debug`, `--default-signal`);
    - `["env", "-iS", "python3 -c '…'"]` is refused as an inline script,
      since the bundled cluster parses the getopt way: `-i`, then `-S`
      taking the next member as its string;
    - `["timeout", "--sig", "KILL", "5", "python3", "-c", "…"]` and
      `["stdbuf", "--out=L", "python3", "-c", "…"]` are each refused as an
      inline script, not as an unknown option, since `--sig` is `timeout`'s
      `--signal` and `--out` is `stdbuf`'s `--output`, so the program
      behind them is found;
    - `["env", "-S", "$BROKER"]` is refused as an inline script, since a
      split string that holds a `$` is unreadable. It is written without
      braces because a binding refuses, when it is declared, any `{name}`
      in its argv outside its closed placeholder vocabulary, before any
      broker rule is asked, so a `${VAR}` string would be refused by that
      rule instead.

  Until the T100 follow-on (claim `5982447319`) lands, these cases fail.
  T089 runs F16.1 at T087's pin, which carries it. T083's run at `38d3350e`
  predates both the follow-on and this addendum. This bookkeeping amendment
  does not itself touch the command above.

  **Landed 2026-10-05** (T083, then T089): F16.1, extracted byte for byte from
  #1144 with batch M's line, exits 0 in both runs. T083's run (openxFactory#1231
  → `0e01ca85`), at openDox-code `38d3350e`, prints `24 passed`,
  `dialect and model declared; a raw key is refused in a field and in the URL`,
  `no model configured: the catalog offers nothing`, `83 passed` and
  `135 passed` (`evidence/f16.1-run.md` § 2). T089's run (openxFactory#1238 →
  `fab575ad`) is at T087's pin, openDox-code `dede32b4`, which carries the T100
  follow-on (openDox-code#86 → `651c35fe`) and with it batch P's cases in
  `tests/test_model_binding_trust.py`: the six `test_F16_1_batch_p_*` tests and
  `test_A8_a_state_directory_that_is_a_link_trusts_nothing`. It prints
  `24 passed`, the same two lines, `83 passed` and `532 passed`
  (`evidence/checkpoint-phase3.md` § 4).

## Follow-ons named here and NOT authored here

- [~] F1 **Port openxFactory's 23 governance families into the openXdox pack.**
  An openXdox FOLLOW-ON with its own claim. Until it lands, requirement 1 keeps
  those families with openxFactory. **Owner: whoever claims it on `#656`.**
- [~] F2 **Each DomainxFactory's own pack**, pinned in that domain's `stack.yaml`.
  That domain's own work. **Owner: each domain.**
- [~] F3 **The wording overlays** (RULED `5799646419`, a follow-on outside both
  releases). Two have LANDED, both on 2026-09-23 and both on the one stage
  entry openXdox's partial `DISPLAY` facet words, `completion`.
  openxFactory#1146 → `d52b4199` (19:40:56Z) composes openXdox's
  `DISPLAY["stages"]` by copy into `scripts/profile_openxfactory.py`, so the
  governed host serves the stage word "implemented" (5.3a's facet,
  openXdox-code#26 → `195276b7`, through openXdox#17). openxFactory#1148 →
  `f1c690b8` (20:57:10Z) serves the same entry's item nouns, "implemented item"
  and "implemented items" (RULED `5801057769`, openXdox-code#27 → `626f2c8d`,
  through openXdox#18). Every other station stays neutral, and any further host
  overlay of the neutral words stays a follow-on. Each lands as its own act and
  not as an arc landing: it carries no `Arc:` trailer, so 11.1's guard does not
  read it, and the test such an overlay edits,
  `tests/test_engineering_profile_display_facet.py`, is not one of 11.1's
  declared surfaces. **Owner: the lane that claims it on `#656`.**
- [~] F4 **The direct-arrow revisit, after phase 1** (RULED `5799494355`, *"keep
  the direct arrow, revisit after phase 1"*, its trigger amended by
  `5800995035`). When phase 1 has landed, the holder re-measures openxFactory's
  direct `opendox` imports and brings Brett the question whether openxFactory
  routes through openXdox only, retiring its second pin and the lockstep
  `scripts/verify-opendox-pin.py` holds. `design.md` § D13 carries the note and
  the baseline it is measured against. **Owner: the holder.**
