# Tasks: add-neutral-product-standalone-operability

Status: draft

Dependency-ordered. **Group 1 is the authoring THIS change performs and it
touches no code.** Groups 2-11 are the post-ratification realization, one group
per requirement, each in the repository named in its heading and each carrying
the FALSIFICATION COMMAND that closes it — an exact invocation with its checkout
preconditions and its expected result, so the archive gate's evidence under
`release-realization` is a command re-run and quoted rather than a description
believed. Where a box names `<the entry point from 10.1>`, that placeholder is
resolved by group 10 and written out in full at that point.

House rule: OpenSpec ratifies, Speckit builds. No group below is started before
ratification, no group is started without its own claim on
`opensoft/openxFactory#656` per lane-collision-protocol Rule 1, and this change
merges nothing anywhere.

Baselines, measured on `openxFactory` `main` `4f92d651` before this packet:
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict` -> `Totals: 109 passed,
1 failed (110 items)`; `python3 scripts/validate-openspec-cli-pin.py --all
--no-cache` -> exit 0, `0 UNDISPOSITIONED failures`, 1 accepted exception
(`add-chain-attestation`, ratified disposition). This packet must add +1 item,
+1 passed and ZERO new failures.

## Group 1 — Authoring (THIS change; no code byte)

- [x] 1.1 Author `.openspec.yaml` — ad-hoc origin, the drafting-provenance shape
  with NO approval pair (`add-drafted-proposal-origin`), naming the archived
  packet's unclosed residue as the origin.
- [x] 1.2 Author `proposal.md`: the owner's goal in his own words from `#656`;
  the two-products measurement; the repository-choice FINDING; the G-to-
  requirement table; the explicit "what openxFactory keeps" section; honest
  `code_surface:` / `target_release:` front-matter.
- [x] 1.3 Author the `## ADDED Requirements` delta creating
  `neutral-product-standalone-operability` — 10 requirements, 30 scenarios,
  domain-neutral, openDox as the measured instance.
- [x] 1.4 Author `design.md`: D1-D7 and **Q-G3**, the one question put to Brett
  with three options, the measured cost of each and a recommendation.
- [ ] 1.5 `OPENSPEC_TELEMETRY=0 openspec validate add-neutral-product-standalone-operability --strict`
  and `--all --strict` pass with no NEW failure against the baseline above.
- [ ] 1.6 `python3 scripts/proposal-support.py . verify add-neutral-product-standalone-operability`
  passes; the `tests/sequenced_after/corpus-ledger.yaml` row is machine-seeded
  (`scripts/validate-sequenced-after.py --seed-ledger --moved-by … --moved-on …`),
  and the README "OpenSpec Records" *Active changes* bullet is added.
- [ ] 1.7 **RULING Q-G3.** Human-gated, Brett Heap. `design.md` § Q-G3 carries the
  three options and the recommendation (c). Nothing in group 5 starts until it is
  answered; every other group is actionable without it.
- [ ] 1.8 On ratification: `Status: ratified` + `Ratified by:` on all three
  lifecycle documents; `## Ratification record` in `proposal.md`; the approval
  pair ADDED beside the fixed origin in `.openspec.yaml`, never substituted.

## Group 2 — Requirement 2 / G1: imports with no consumer, publisher or host (openDox-code)

The highest-leverage box: TWO import statements, 1,232 of 1,298 measured errors
at `f8a1ece`, zero passed. An AST census of `src/` finds exactly two import-time
reaches (`serve.py:199`, `serve.py:206`) and two deferred ones; every other
mention in the package is prose.

- [ ] 2.1 Remove the module-level `from ideation_dashboard import
  serve_openxfactory_lanes` (`src/opendox/serve.py:199`) and the
  `from ideation_dashboard.serve_openxfactory_lanes import (…)` re-export block
  (`:206`). The five names (`ACTIONS_APPLY_REGISTER_EDITS_ROUTE`,
  `ACTIONS_DTN_SEED_ROUTE`, `ACTIONS_REFRESH_ROUTE`,
  `ACTIONS_STAGING_SEED_ROUTE`, `COMMITTED_INTENTS_ROUTE`) belong to
  openxFactory's lanes surface, filed `stays_openxfactory_adapter`. All five are
  plain route strings (`"/committed-intents.json"`, `"/actions/refresh"`,
  `"/actions/apply-register-edits"`, `"/actions/dtn-seed"`,
  `"/actions/staging-seed"`).
- [ ] 2.1a **DO NOT VENDOR the module.**
  `scripts/ideation_dashboard/serve_openxfactory_lanes.py` itself imports
  `from openxdox import snapshot_registry` (`:70`) and
  `from openxdox.serve_projection import hosted_ref_refused` (`:77`), so copying
  it into openDox re-creates the consumer dependency BUILD slice 2b removed.
- [ ] 2.2 Contribute those routes through the EXISTING seam —
  `serve.build_server(route_extensions=)` / `route_extension.RouteBinding` — from
  openxFactory's side, per the carve `design.md`'s own specification. No new
  mechanism is designed here.
- [ ] 2.3 Sweep every remaining module-level reach: grep `src/` for
  `ideation_dashboard`, `corpus_adapter_openxfactory`, `doc_health` and
  `openxdox` at import position, and close or defer each with a recorded reason.
- [ ] 2.4 Add a test in openDox-code's own suite that imports EVERY module of the
  package in a checkout with no sibling installed, failing with the name of the
  first module that still needs one.
- [ ] 2.5 Remove `validate.yml`'s three `--noconftest` steps and their enumerated
  file lists; the suite collects whole. Today they run **31 of 53** test modules
  and 22 are collected by no required command. The autouse fixture that produces
  the 1,298 setup errors is `tests/session_fixtures.py:413`, whose body is
  `from opendox import cli as cli_mod`.
- [ ] 2.6 Correct openDox-code's `README.md:39-42`, which still gives the
  narrowing's reason as *"Until the BUILD arc … inverts the openDox → openXdox
  dependency"*. That dependency IS inverted at import time; the live cause is
  `ideation_dashboard`.
- [ ] **FALSIFIED BY:** in a checkout of openDox-code alone,
  `python -c "import opendox.serve"`, `python -c "import opendox.cli"` and
  `python -c "import opendox.notebook_action"` each exit 0. Today all three raise
  `ModuleNotFoundError: No module named 'ideation_dashboard'`.

## Group 3 — Requirement 3 / G2: a default domain profile (openDox-code)

- [ ] 3.0 **RATIFICATION READ FIRST.** Requirement 3 revisits the PREMISE of RULED
  ASK-2 option (2) (`#656` comment `5628886636`) — not its reasoning. An EMPTY
  default stays refused; what changes is the refusal text's premise that *"openDox
  … ships no profile of its own"*. If the ratification read takes ASK-2 to
  foreclose this, requirement 3 is struck and the other nine stand. See
  `design.md` § D5.
- [ ] 3.1 Ship a default profile for openDox's OWN domain — documents and ideas —
  carrying none of openxFactory's status taxonomy or change/spec/delta nouns
  (RULING C2, DIRECTION Q5). Note the standalone problem this closes: the only
  host that exists, openxFactory's `scripts/opendox_host.py`, builds a composite
  whose base class is `openxdox.domain_profile.DomainProfile`, so today's only
  real profile needs BOTH siblings present.
- [ ] 3.2 `build_parser()` and `build_server()` fall back to it when no host has
  called `domain_profile.register()`, and a registered profile still replaces it.
  `profile_proxy.py`'s refusal is kept for the case it was written for — an
  ambiguous registration — and is NOT weakened into an empty tuple.
- [ ] 3.3 Record in the carve manifest that the `deleted_at_carve` row for
  `profile_openxfactory.py` is UNCHANGED by this: openxFactory's profile stays
  deleted from the core and `scripts/opendox_host.py` remains openxFactory's host.
- [ ] **FALSIFIED BY** (openDox-code checkout, `pip install -e .`, no sibling):

      python -c "from opendox.cli import build_parser; build_parser(); print('OK')"
      python -c "from opendox.serve import build_server; build_server(); print('OK')"

  Both print `OK`. Today both raise `domain_profile.ProfileNotRegistered`. Then
  `pytest tests/test_profile_registration.py` proves a registered profile still
  replaces the default.

## Group 4 — Requirement 5 / G4: the deferred reach resolves through the seam (openDox-code)

- [ ] 4.1 Replace `src/opendox/authoring.py:318`'s
  `from corpus_adapter_openxfactory import home_corpus` with a resolution of the
  REGISTERED corpus adapter through openDox's own `corpus_adapter` seam.
- [ ] 4.2 Where no adapter is registered, refuse naming the seam and the remedy —
  never a `ModuleNotFoundError` raised from inside a function.
- [ ] 4.3 Sweep the nineteen deferred reaches the ratchet declares today
  (`branch_session.py` 7, `serve_workbench.py` 7, `serve.py` 2,
  `serve_project.py` 2, `cli.py` 1) and classify each: resolvable through a
  declared seam, or genuinely owed to the consumer and therefore staying
  late-bound with its reason. The import-time column is already `0` — do not
  re-do it.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling, no
  `corpus_adapter_openxfactory` importable):

      python -c "import opendox.authoring as a; a.required_header_fields()"

  Returns the fields through the registered adapter, or raises openDox's own named
  refusal. It MUST NOT raise `ModuleNotFoundError`. Today it raises
  `ModuleNotFoundError: No module named 'corpus_adapter_openxfactory'` while
  `python -c "import opendox.authoring"` exits 0.

## Group 5 — Requirement 4 / G3: openDox generates its own snapshot (BLOCKED on ruling 1.7)

- [ ] 5.1 **AUDIT FIRST, BEFORE ANY CODE MOVES.** Classify each corpus-shaped site
  in `generator.py` (974), `snapshot.py` (223), `snapshot_registry.py` (1,318),
  `completeness.py` (548) and `corpus_root.py` (101) as (i) a PATH literal
  re-expressible as a declared artifact kind, or (ii) reasoning about what an
  openxFactory artifact MEANS. Record the count of each. `design.md` § Q-G3 names
  this as the finding that would overturn the recommendation.
- [ ] 5.2 Realize the mechanism Brett rules — (a) move as-is, (b) protocol
  injection, or (c) move parameterized by a domain mapping declaration.
- [ ] 5.3 Whichever is ruled: openXdox keeps its corpus adapter and its
  declaration, and continues contributing its routes and subcommands through the
  existing seams. The consumer loses no capability.
- [ ] **FALSIFIED BY** (openDox-code checkout, `pip uninstall -y openxdox` so that
  `python -c "import openxdox"` raises, over a fixture directory of plain `.md`
  documents carrying none of openxFactory's governance vocabulary):

      <the entry point from 10.1> generate --corpus tests/fixtures/plain-documents --out /tmp/snap.json
      python -c "import json;d=json.load(open('/tmp/snap.json'));print(len(d['documents']))"

  A snapshot is written, its document count is non-zero, and
  `grep -iE 'openspec|proposal[.]md|ratified' /tmp/snap.json` finds nothing.

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
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling):

      python -c "from opendox import workbench; print(workbench.run_scoped_doc_health('.', ['README.md'])['status'])"

  Prints a real status. Today it prints `not-available` with
  `detail = doc-health machinery unavailable: No module named 'doc_health'`.

## Group 7 — Requirement 7 / G6: a validator openDox can run (openDox-code)

- [ ] 7.1 Resolve the three-way schema split so one checkout carries the set
  openDox's validator reads; schemas openxFactory OWNS arrive by the declared pin
  and are read from the pinned checkout, never by a sibling path literal.
  Measured: the validator's `SCHEMA_FILENAMES` names **10** schemas, split
  **openXdox-spec 3 / openDox-spec 3 / openxFactory 4**; both code legs and both
  assembly roots carry **zero**. The script itself
  (`openXdox-code/scripts/validate-ideation-dashboard-contracts.py`) derives
  `SCHEMAS_DIR` from `__file__` (`:114-115`) and so looks for a
  `contracts/schemas/` its own leg does not have — it exits 2 with
  `ERROR .../contracts/schemas not found` run from its OWN repository.
- [ ] 7.2 openDox-code has **no `scripts/` directory at all** and one console
  script. Whatever validator it gains is new surface at the code leg, not a
  relocated one.
- [ ] 7.3 **Three carve-broken defects in `openxdox/snapshot.py` are unclaimed
  and belong to this box**, registered by the archived packet's § 5.5 residue and
  owed to *"a follow-up act with its own claim"* that nobody holds: `SCHEMAS_DIR`
  resolves to an absent directory; `VALIDATOR_RELPATH` names a path openxFactory
  shed; and **`find_validator`'s parent walk ADOPTS AN ENCLOSING PRE-SHED
  CHECKOUT** — which is exactly the "reaching into a host tree instead of an
  injected adapter" class this arc exists to close, appearing a second time.
  Claim them here or hand them on by name; do not leave them unowned again.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling):

      <the entry point from 10.1> validate tests/fixtures/plain-documents/example.md; echo "rc=$?"

  Returns a verdict with `rc=0`, and the same command over a deliberately malformed
  fixture returns non-zero naming the rule. Neither run may fail on an unresolvable
  schema path.

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

- [ ] 9.1 openDox-code's required check runs the whole suite, no `--noconftest`,
  no file list (follows group 2).
- [ ] 9.2 openXdox-code the same, with `OPENDOX_BACK_IMPORTS` lowered as each
  deferred reach closes. The import-time column is ALREADY zero and stays there.
- [ ] 9.2a **Add the missing instrument.** No gate watches the openDox →
  openxFactory direction — the ratchet measures openDox → openXdox only, which is
  how two import-time reaches into the publisher survived a completed inversion
  under a green check. Requirement 2's third scenario is that instrument.
- [ ] 9.3 Behaviours needing both legs become declared INTEGRATION tests naming
  the pin they compose at, rather than being dropped from both suites — including
  the 31-entry assembled `--help` tree the carve manifest records as one
  *"which after the carve neither leg produces alone"*
  (`docs/opendox-carve-manifest.yaml:3088`). Nothing anywhere reproduces it today.
- [ ] 9.4 **Restore the margin, and stop the skips carrying the gap.** Both legs
  pass their floors with ZERO margin (openDox `1114/1111/3`, openXdox
  `539/533/6`), and every one of openXdox's six skips carries the same reason —
  *"doc_health reachability is BUILD-arc work (§ 3.5/3.6) … this test will assert
  for real once that lands"*. Two of openDox's three are the mirror image. **The
  whole-product assertions are precisely the ones that skip**, which is why both
  legs report green while neither product runs.
- [ ] 9.5 Note for whoever takes this box: openXdox pins openDox at `5c137a90`,
  nine commits behind openDox-code `main`, and the openDox root's gitlink and
  `contracts/code-pin.yaml` name `d816cf06`, two behind. Both are ancestors —
  nothing is forked — but the pins move before the integration run means
  anything.
- [ ] **FALSIFIED BY** (each leg's own checkout, no sibling installed):

      python -m pytest -q          # NOT --noconftest, NOT a file list

  Exits 0 in both legs with zero errors, and
  `grep -c noconftest .github/workflows/validate.yml` returns 0 in both. Today
  openDox-code gives 1,298 errors / 0 passed and openXdox-code 1,089 / 0.

## Group 10 — Requirement 10 / G9, G10: one entry point (openDox-code + openDox root)

- [ ] 10.1 A `[project.scripts]` entry point for the DOCUMENT surface. Today the
  only console script is `opendox-runtime = "opendox.runtime.cli:main"` — a
  subsystem, not the product — and there is no `__main__.py` anywhere under
  `src/`. **RULED Q-R4 already places this work in THIS act** (`#656` comment
  `5701772032`, Brett Heap, 2026-09-16, recorded at `runtime/cli.py:40-46`): *"the
  verbs are wired into `opendox.cli` in the BUILD-arc act that repairs
  `opendox.serve`, and `opendox-runtime` is the spelling until then."* So 10.1
  follows group 2 and discharges Q-R4's condition.
- [ ] 10.2 The web bundle is served by that entry point and is reachable in a
  browser from an openDox-only install. openDox-code carries **42** web files,
  self-contained by declaration (`src/opendox/web/index.html`: *"All assets are
  local/vendored: no CDN, no external fonts, no remote scripts"*), and **nothing
  serves them**: `serve.py` will not import, and `runtime/app.py` mounts no
  `StaticFiles` — its routes are `/livez`, `/readyz` and `/api/v1`. The bundle is
  not the gap; the door is.
- [ ] 10.2a `intent-feed.js` stays at openxFactory under RULED OQ-F and is NOT
  owed to openDox; openDox's replacement is `views/intent-binding.js`. Do not
  count it as a missing file.
- [ ] 10.3 **The assembly root DOCUMENTS the entry point; it does not host it.**
  `openDox/Makefile` carries a row in `contracts/shape-pin.yaml` (`:49-50`), and
  `AGENTS-shape.md` § "Never edit a file that has a row" is explicit: *"An edit
  in place is reported as DRIFT and refused."* A `run`/`serve` target added there
  would red `make pins`, and the lawful route would be an upstream change in
  `opensoft/openRepoShape` binding EVERY project that carries the shape. So the
  entry point is a `[project.scripts]` console script at the CODE leg (10.1),
  which is where the shape's own "What goes where" puts *"the implementation and
  its tests"*; the root's `README.md` has no shape-pin row and is the project's
  own to edit, so it documents and points at the command.
- [ ] **FALSIFIED BY** (empty machine, openDox-code only):

      pip install .
      opendox --help                    # the console script MUST exist
      <the single command the README documents>
      curl -sf http://localhost:<port>/ | head -c 200

  The help prints, the server starts, and the curl returns the web bundle's HTML
  with no sibling repository installed. Today `[project.scripts]` declares only
  `opendox-runtime`, there is no `__main__.py`, and nothing serves `web/`.

## Group 11 — Requirement 1: the guard holds (openxFactory)

- [ ] 11.1 At the close of the arc, a diff of openxFactory across every group
  shows: no `scripts/doc_health/` family moved, no `openspec/specs/` capability
  removed, no corpus document moved, no intent-plane schema moved, and no
  integration test moved. The only openxFactory edits are carve-manifest row
  annotations recording each closed reach.
- [ ] **FALSIFIED BY** (openxFactory checkout, at the close of the arc):

      git diff --name-only <arc-base>..<arc-tip> -- scripts/ contracts/ tests/ ideation/ docs/ openspec/specs/

  Every path it prints is either `docs/opendox-carve-manifest.yaml` or
  `openspec/specs/neutral-product-standalone-operability/spec.md`. Any other path
  is a breach of requirement 1 and must be reverted or declared.
