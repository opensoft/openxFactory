# Staged: the `doc_health` direction arc — openXdox-code's wrong-way import of openxFactory's governance tooling

Status: staged
Kind: architecture
Summary: openXdox-code — the CODE LEG of openXdox, the assembly root
`openxFactory` pins directly (`contracts/openxdox-pin.yaml`; the code and
spec legs are never separately pinned or mounted from openxFactory's side) —
imports `openxFactory`'s own `doc_health` package at module level in eight
places. That is the exact shape `corpus-adapter-seam`'s Requirement 1
refuses: *"no neutral product `openxFactory` pins SHALL import
`openxFactory`'s own tooling."* Plan 034 (`add-neutral-product-standalone-operability`, release 1)
measured the defect, could not fix it inside release 1's scope, and ruled a
named, counted, release-1-only reprieve (a declared exclusion, R1Q6 (d))
rather than conformance. This topic raises the DIRECTION question that
reprieve deferred: how the dependency should actually run, so the
`doc_health`-caused portion of requirement 9's exclusion stops being open for
openXdox-code. R1Q24 (a) (`#656` comment `5850003126`) put two more classes in
that same declared exclusion — the test files that need openxFactory's
status-exemption rail, and those that read openxFactory's contracts — and made
this arc their owner as well (claim 6). Neither is `doc_health`'s cause, so
lifting the `doc_health` entries alone does not empty the declaration or make
openXdox-code's suite green standalone.
Topics: doc_health, direction-arc, corpus-adapter-seam, dependency-direction, openxdox-code, neutral-tooling-home, R1Q6, R1Q24, declared-exclusion, opendox-standalone-operation, plan-034
Repository context: openxFactory owns `doc_health` and the governing
`corpus-adapter-seam` capability; openXdox-code is the consumer whose module-level
imports are in question; a resolution may also touch openDox-code, which
already carries the `corpus_adapter` / `domain_profile` registered-seam pattern
this topic's options borrow from; if the eventual shape is a genuinely neutral
package, a new root-level product (the `openXwallet` precedent: a neutral
standard openxFactory pins by commit and digest) is also in scope
Staging ID: openxFactory:staging:doc-health-direction-arc
Captured: 2026-09-26
Source: Raised by plan 034 (`specs/034-opendox-standalone-operation/tasks.md`
T008), on Brett Heap's ruling R1Q6 (d) (`#656` comment `5817152735`,
2026-09-24T15:31:46Z, verbatim *"(a) on all eleven, (d) on R1Q6"*). The interim
mechanics — the declared exclusion file, its count and its reason — are
#1144's (`add-neutral-product-standalone-operability`) T041/T043/T044 and T007
batch B's own bookkeeping of F9.1, and are NOT this topic's subject. This topic
is the direction question those tasks deferred.
Target capabilities: `corpus-adapter-seam` (governing, already ratified —
openXdox-code's imports are a live, currently-tolerated violation of its
Requirement 1). The eventual exit is most likely a REALIZATION change with no
spec text change (openXdox-code stops importing `doc_health` by name, through
a registered seam); a MODIFIED `corpus-adapter-seam` or `neutral-product-pin`
delta is in scope only if the ruled option needs new contract surface — for
example a packaged, pinned `doc_health` distribution, or a narrower
neutral-utility extraction that leaves the governance-specific families behind.

openXdox-code is the neutral, standalone-installable consumer product this
whole arc (plan 034) exists to realize. Its generator and seven other modules
(eight in all — claim 2 below names them) reach directly into `openxFactory`'s
`scripts/doc_health/` package by name —
not through a declared interface, not through a pinned, installable
distribution, but the same way two modules inside ONE repository would import
each other. `openxFactory` ships no `pyproject.toml`, so `doc_health` cannot be
`pip install`-ed at all; the import only resolves when openXdox-code's own
checkout happens to sit beside (or is composed with) an openxFactory checkout
on `PYTHONPATH`. Plan 034's requirement 9 says each repository runs its own
suite green, alone, with no sibling repository present — and openXdox-code
cannot, while this import stands. R1Q6 answered (d): declare the reach as a
counted, reasoned exclusion for release 1, and raise the direction question as
its own arc (this topic), due before release 2's 12.5 needs the sixteen
governed-flow suites to run. R1Q23 was answered (a) (`#656` comment
`5850003126`: phase 2's F5.2 environment composes openxFactory's tools at a
named commit), so phase 2 does not wait for this arc and the deadline stands.

## Claims

1. **The shape is already forbidden, not merely undesirable.**
   `corpus-adapter-seam`'s Requirement 1 states plainly: *"no neutral product
   `openxFactory` pins SHALL import `openxFactory`'s own tooling... The
   dependency points ONE WAY — a reader depends on the interface it
   implements, and never on the corpus's own check families."* openXdox-code
   is reached through exactly such a pin, one hop removed:
   `contracts/openxdox-pin.yaml` pins the openXdox ASSEMBLY ROOT directly
   (RULING F, `#656`, 2026-09-05, *"rule F openXdox only"* — the code and
   spec legs are "never separately pinned or mounted" from openxFactory's
   side), and the assembly root's OWN `openXdox/contracts/code-pin.yaml`
   pins openXdox-code in turn. The eight `doc_health` imports this topic
   measures live in openXdox-code's own source tree, reached through that
   chain rather than named in openxFactory's own pin file.
   `add-neutral-product-standalone-operability`'s own `design.md` invokes
   this same requirement when it rules out moving `openXdox`'s generator into
   `openDox`, because that move "would have put `import doc_health` inside the
   neutral core, which is the exact thing `corpus-adapter-seam`'s first
   requirement forbids." The direction question is not new law; it is
   bringing an existing consumer into conformance with a law already ratified
   for a sibling case.

2. **Eight modules, closed and tested as a surface.** `tests/test_dependency_direction.py:290-315`
   (`DOC_HEALTH_SURFACE`, openXdox-code) declares the reach *"lawful HERE and
   nowhere else in the estate"* over exactly eight modules: `cli_gate`,
   `completeness`, `corpus_root`, `gate_console`, `gate_routes`, `generator`,
   `round_trip` and `snapshot_registry`. Whatever this arc decides, the surface
   it must retarget is already enumerated and already guarded against growing
   silently.

3. **The cost is measured, not estimated.** In a fresh venv over an
   openXdox-code checkout alone (no openxFactory sibling), a plain run stops
   at 57 errors during collection, before any test body runs: 26 on
   `doc_health`, 28 on `ideation_dashboard` (a separate, already-planned fix —
   plan 034 Group 2), 3 on a missing `test_gate_routes` helper (of 87 test
   files in the current tree). Simulating Group 2's fix away
   (so only the `doc_health` reach remains), 19 of the 23 suites that plan
   034's F5.2 and 12.5 falsifiers protect from arc edits still fail on
   `doc_health` (`specs/034-opendox-standalone-operation/research.md` R10,
   R11; re-measured 2026-09-25 in `evidence/remeasure-2026-09-25.md` with the
   same causes, unchanged).

4. **openxFactory's governance tooling deliberately stays with openxFactory.**
   `add-neutral-product-standalone-operability`'s `design.md` (§ "the fix
   loop") is explicit: *"openxFactory's 23 governance check families stay with
   openxFactory."* So the direction fix is not "relocate `doc_health` into a
   neutral core" — that was priced and rejected for the sibling `generator.py`
   case (option (a), design.md "THE CORRECTION"). Whatever resolves this arc
   must leave `doc_health`'s governance logic inside openxFactory.

5. **Not every one of the eight imports is obviously governance logic.**
   `generator.py`'s three `doc_health` imports (design.md § "THE CORRECTION")
   are `from doc_health import corpus`, `from doc_health.corpus import
   RealGit` and `from doc_health.lines import split_keepends` — read on their
   names alone, a module of git-repository helpers and a text-splitting
   function, not a check family, a disposition reader or a classifier. This is
   an OBSERVATION, not an audited claim: it is offered as a possible seam
   (Q4 below), not a conclusion, because the other seven modules
   and the remaining reaches are not audited here.

6. **The declared exclusion has a hard deadline, not an open-ended one — and
   `doc_health` is one of the three classes it holds for this arc, not the
   only one.**
   R1Q6 (d)'s exclusion is explicitly *"an OPEN EXTRACTION"* for openXdox-code
   — `add-neutral-product-standalone-operability`'s archive act must report
   the `doc_health`-caused portion of requirement 9 as open there, and must
   not read it as closed, until this arc lands. Round 2 widened what the arc
   owns. R1Q24 (a) (`#656` comment `5850003126`, 2026-09-26, Brett Heap,
   verbatim *"go with recommendations on all the open questions"*) added two
   classes to the same declared exclusion — the test files that need
   openxFactory's status-exemption rail, and those that read openxFactory's
   contracts — each entry carrying its own reason, "as follow-on open work",
   and plan 034 T008 reads it as this arc taking them as well
   (openXdox-code's `tests/declared_exclusion.yaml` names the arc as
   `open_until` for both reasons). Neither class is `doc_health`'s cause, so
   lifting the `doc_health` entries alone does not empty the declaration, and
   the section "What the declared exclusion holds, and what R1Q24 (a) gives
   this arc" lists the files. R1Q25 (b)'s consumer-schemas class, the one
   entry for `tests/test_snapshot.py`, is NOT this arc's: plan 034 T061 (7.3)
   cleared it (openXdox-code#36 → `6a3b93b9`, which took the declaration to 65
   files). R1Q23 was answered (a), so phase 2 does not wait for this arc
   (F5.2's environment composes openxFactory's `scripts/` at a named commit)
   and the deadline stays at release 2's 12.5. Ruling and realizing this arc
   closes requirement 9's exclusion for openXdox-code only once the
   declaration holds none of its three classes.

## What the declared exclusion holds, and what R1Q24 (a) gives this arc

Added-by: Claude Sonnet 5.5 (lane openxfactory-4) · 2026-10-02 (plan 034 T008's
record, completed on round 2's answers; bookkeeping, not a ruling)

**Ruled.** R1Q24 (a), `#656` comment `5850003126` (Brett Heap, 2026-09-26): the
declared exclusion takes the status-exemption-rail and openxFactory-contracts
classes, *"add the seven openXdox-code files to the declared exclusion, each
with its reason, as follow-on open work"*. Plan 034 T008 reads that as this
arc taking them as well, and `tests/declared_exclusion.yaml` (openXdox-code)
names the arc, *"the doc_health direction arc (plan 034 T008)"*, as
`open_until` for both reasons. The same comment ruled R1Q25 (b), which kept
`tests/test_snapshot.py`'s consumer-schemas class in phase 2, and R1Q23 (a)
(Q5 below). R1Q24's own text counted seven files at T005's pin; T043's triage
at T040's pin names the files (below), and an eighth,
`tests/test_doxbench_blank_reason.py`, reads openxFactory's
`contracts/manifest.yaml` (plan 034's `evidence/analyze-round-1a.md`, C8).

**The declaration at openXdox-code `6a3b93b9`** (`main` after T061): 65 files,
three reasons. The rail and contracts lists are the same at T043's landing
`4610bca5` (openXdox-code#32), where the files were measured.

- **`doc_health`** (59 files; R1Q6 (d), `5817152735`): the files that reach
  `doc_health`. T043 measured 70 red results in 60 files, the 59 declared and
  the help-tree test that the next section names. This is the class the arc's
  eight-module surface (claim 2) causes.
- **`status-exemption-rail`** (3 files, 87 red results; R1Q24 (a),
  `5850003126`): `tests/test_doxbench_abstract_envelope.py` (1),
  `tests/test_doxbench_packet.py` (54, and 3 `doc_health` cases besides) and
  `tests/test_doxbench_turns.py` (32). Reason, as the declaration states it:
  the files need openxFactory's status-exemption rail, which only openxFactory
  registers at openDox's status-exemption seam. T027 turned the old module
  reach into that seam, which fails closed when nothing is registered, and
  T046 has openxFactory's host register the rail.
- **`openxfactory-contracts`** (5 files, 75 red results; R1Q24 (a),
  `5850003126`): `tests/test_doxbench_blank_reason.py` (1, and 1 `doc_health`
  case besides), `tests/test_project_action_contracts.py`,
  `tests/test_project_schema_election.py`,
  `tests/test_validate_ideation_dashboard_contracts.py` and
  `tests/test_wheel_action_contracts.py`. Reason, as the declaration states
  it: the files read openxFactory's contracts (the contract family's validator,
  schemas and examples, or its `contracts/manifest.yaml`) where openxFactory's
  tree keeps them, which is outside the checkout. T005 measured that
  respelling the four contract-family files' pre-carve `ROOT` and setting
  `CONTRACTS_DIR` to openXdox-spec's contracts still left them red: they read
  the family's packaged examples and three schemas openxFactory owns
  (`project-register`, `gate-intent`, `demotion-execution-receipt`), which 7.1
  and 7.1b keep in openxFactory.

Two files carry two reasons, each checked: `tests/test_doxbench_packet.py`
(`doc_health` and the rail) and `tests/test_doxbench_blank_reason.py`
(`doc_health` and the contracts). So a file leaves the declaration only when
all of its reasons are cleared, and the arc's ruling has to say, class by
class, what clears each.

**An observation, read from the reasons and not a ruling.** Installing
`doc_health` as a pinned dependency (R1Q6's option (a), Q1) supplies neither
the rail's registration nor openxFactory's contracts, so it cannot lift the
rail or contracts entries by itself. Whether option (b), option (c) or the
split (Q2–Q4) does is for the ruling to say; this topic does not decide it.

**Not this arc's.** The consumer-schemas class (`tests/test_snapshot.py`,
R1Q25 (b)) left the declaration with T061 (openXdox-code#36 → `6a3b93b9`, 66 →
65 files).

## The excluded files that validate a kind the narrowed validator gives up

Added-by: Claude Sonnet 5.5 (lane openxfactory-4) · 2026-10-02 (plan 034 T008,
second bullet: T061's list, added as bookkeeping so the arc knows which
validator each file will need once it runs)

Source: the body of openXdox-code#36 (T061, → `6a3b93b9`), § "For T008". T061
(7.3) narrowed the consumer's validator. In a lone checkout, with no
`contracts/` of its own and no `CONTRACTS_DIR`, it validates only its own three
kinds, from its installed distribution (R1Q14 (a)); the family's other seven
kinds are validated only where the running tree supplies their schemas
(R1Q27 (a), `5851950767`). These seven excluded files validate one of those
other kinds. T061's body says it measured the first two with a temporary trace
of the validator's calls, whole suite and composed (the trace was reverted),
and read the rest from content.

- `tests/test_notebook_action.py` (declared reason `doc_health`):
  `ideation-workbench`.
- `tests/test_register_edit_lane.py` (`doc_health`): `project-register`.
- `tests/test_validate_ideation_dashboard_contracts.py`
  (`openxfactory-contracts`): `workbench-model-catalog` and
  `workbench-chat-turn-v2`.
- `tests/test_project_action_contracts.py` (`openxfactory-contracts`):
  `gate-intent`.
- `tests/test_wheel_action_contracts.py` (`openxfactory-contracts`):
  `gate-intent`.
- `tests/test_project_schema_election.py` (`openxfactory-contracts`):
  `project-register`.
- `tests/test_doxbench_blank_reason.py` (`doc_health` and
  `openxfactory-contracts`): `workbench-chat-turn-v2`.

Also, from the same section of that body:

- `tests/test_aggregation_register_instance.py` is not excluded. It validates
  `project-register` and skips alone, which are the four `EXPECT_SKIPPED`
  cases.
- The other declared files that run the validator validate only its three
  kinds, so the narrowing gives up nothing there: `test_generator`,
  `test_generated_at_anchor`, `test_snapshot_determinism`,
  `test_snapshot_registry`, `test_doxbench_share`, `test_kickoff` and
  `test_session_records`.

Where those kinds' schemas live, read from plan 034 (7.1, T057, T085, R1Q27
(a)) and from the validator's own kind table
(`scripts/validate-ideation-dashboard-contracts.py` at openXdox-code
`6a3b93b9`, lines 373 and 382): `ideation-workbench`, and the validator's
`workbench-model-catalog` and `workbench-chat-turn-v2` tags (which read
`xfactory-workbench-model-catalog.schema.yaml` and
`xfactory-workbench-chat-turn.schema.yaml`), are openDox-spec's three kinds.
openDox's own validator covers `ideation-workbench` (T057, T058, landed), and
T085 (phase 3, not yet landed) gives the other two their validators over
packaged copies. `project-register` and `gate-intent` are openxFactory's kinds:
the consumer's validator keeps them wherever openxFactory's tree supplies their
schemas (R1Q27 (a)).

## What this arc's landing removes: the help-tree test's deselects, and F9.2

Added-by: Claude Sonnet 5.5 (lane openxfactory-4) · 2026-10-02 (plan 034 T008;
the rulings below are recorded in plan 034's `tasks.md` T008, T042 and T049)

**The test.** `tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records`
(openXdox-code's integration step, 9.3) fails because `cli_gate` imports
openxFactory's `doc_health` at load time, which is R1Q6 (d)'s kind of
exclusion. The declaration lists whole `tests/test_*.py` files directly in
`tests/`, so the required check carries this one test as a workflow
`--deselect` instead (openXdox-code#32).

**RULED `5859927858`** (`#656`, Brett Heap, 2026-09-27, verbatim choice *"(b)
Exclude it until T008's arc (Recommended)"*, raised by openXdox-code#31, T042):
the test leaves T042's integration step with that stated reason, and *"It runs
again once the doc_health direction arc (T008) lands. F9.2 is unchanged."*

**RULED `5870594693`** (`#656`, Brett Heap, 2026-09-28, verbatim choice *"(b)
Amend F9.1 to deselect it (Recommended)"*, raised by openXdox-code#32, T043):
F9.1's pytest line takes one `--deselect` for that test (T007 batch J,
openxFactory#1193 → `6b97c601`), citing `5859927858`, and *"T008 removes it
together with the workflow deselect."*

**So the arc's landing removes three things together**, as plan 034's T008
records them: (1) F9.1's `--deselect` for the help-tree test, which batch J
added; (2) the same `--deselect` in openXdox-code's required check (the
`LEFT_OUT` step in `.github/workflows/validate.yml`, which openXdox-code#32
folded into the whole-suite step from T042's integration step in
openXdox-code#31); and (3) the guard test beside it,
`tests/integration/test_assembled_surface.py::test_the_help_tree_is_left_out_only_while_its_stated_reason_holds`,
which passes only while the child fails exactly as the stated reason says and
fails once the arc lets the assembled command line build, so that the pull
request that clears the reason takes the exclusion and the guard out together.

**F9.2** (the falsifier #1144 attaches to 9.3's integration tests) stays red on
that one test until then. `5859927858` keeps it unchanged, and phase 1 closed
with it quoted red (plan 034 T049, `evidence/checkpoint-phase1.md` § 5, at
openXdox-code `6158151e`). Where plan 034 says F9.2 closes *"after T008"* or
stays red *"until T008"*, it means this arc's landing: the arc's landing
removes the three things above, F9.2 is re-run, and its box closes. Raising and
recording the arc (plan 034's T008, ticked) does not close it.

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

- **This topic's own subject is a currently-tolerated conflict with a
  ratified spec — one R1Q6 (d) does NOT authorize or cover.** openXdox-code's
  eight `doc_health` imports stand against `corpus-adapter-seam`'s
  Requirement 1 today. R1Q6 (d) is a separate, release-1-scoped, named,
  counted exception (`#656` comment `5817152735`) for requirement 9's own
  standalone-suite problem only; it does not authorize, preserve, or extend
  to an exception for Requirement 1, and nothing in the ruled record accepts
  or decides this conflict. That is not a new conflict this topic creates;
  it is the conflict this topic exists to EXAMINE — not necessarily to
  close. Q2 and Q3 (options (b) and (c)) can close R1Q6's requirement-9
  problem (the suite runs green alone) without touching a single production
  import, which would leave this Requirement 1 conflict standing as its
  own, separately unresolved question. Only a genuine neutral-home
  extraction (Q1's option (i) — NOT mere pinning under R1Q6's literal
  option (a), which Q1 finds does not resolve the seam by itself) closes
  the conflict for the whole eight-module surface; Q4's split closes it
  only for whatever slice it actually retargets, leaving it open for any
  module left on (b) or (c) instead. See § Exit path. No other staged topic
  or ratified spec is known to contradict the material above.
  — Added-by: Claude Sonnet 5 (lane openxfactory-4) · 2026-09-27

## Open questions

### Q1. Does openXdox-code gaining `doc_health` as an installable, pinned dependency (R1Q6's option (a)) resolve the Requirement 1 conflict on its own?

Context: R1Q6 named this as a live option: openXdox-code gains `doc_health`
as a declared, pinned, installable dependency, which needs openxFactory to
package it (a `pyproject.toml` for `scripts/doc_health/`, or a dedicated
distribution). Measured: on its own this does not resolve the seam
violation — openXdox-code would still be a neutral product importing
`openxFactory`'s own tooling, merely through a proper pin instead of an
ad-hoc `PYTHONPATH` reach, and it makes the openxFactory ↔ openXdox pin
explicitly TWO-WAY (openxFactory already pins openXdox; openXdox would then
pin openxFactory's tooling too) — the opposite of Requirement 1's one-way
rule. `corpus-adapter-seam` already requires that any two mutually importing
packages relocate their shared type into a module both depend on BEFORE
either is extracted.
Recommended answer: No, not as a standalone answer. Either (i) `doc_health`
(or the slice openXdox-code needs) first moves to a genuinely neutral,
separately-versioned home, so openXdox-code pins a THIRD PARTY rather than
"openxFactory's own tooling" — at which point this becomes a realization
detail of Q4 rather than a standalone answer — or (ii) it is adopted
explicitly as a labelled, time-boxed WORKAROUND under its own
`corpus-adapter-seam` exception, never as something that lifts R1Q6 (d)'s
exclusion by itself.
Explanation: Packaging changes the MECHANISM (an ad-hoc `PYTHONPATH` reach
becomes a declared pin) but not the DIRECTION (openXdox-code still imports
openxFactory's own tooling, and openxFactory still pins openXdox). Only
relocating the tooling itself, or explicitly accepting the residual
violation, avoids re-creating the two-way-pin shape `corpus-adapter-seam`
forbids.
Disposition status: open
Added-by: Claude Sonnet 5 (lane openxfactory-4) · 2026-09-27

### Q2. Does moving the `doc_health`-dependent tests into declared integration tests in openxFactory (R1Q6's option (b)) close the Requirement 1 conflict?

Context: Option (b) makes the `doc_health`-dependent openXdox-code tests
declared integration tests that live where the composition is declared —
openxFactory — per requirement 9's own admitted exception for tests that
need two repositories. It needs R1Q2's declared composition-test surface
widened to admit them (the same surface plan 034's T007 batch A / batch E
already grows for the `openxdox_host` composition tests).
Recommended answer: No — it closes only the `doc_health` portion of
requirement 9 (the suite no longer needs `doc_health` to run green alone). The
rail and contracts classes that R1Q24 (a) also gave this arc stand unless the
same ruling moves or composes their files too — claim 6. It moves or composes
TESTS, not production code: `DOC_HEALTH_SURFACE`'s
eight modules keep their imports exactly as measured, so the Requirement 1
conflict (claim 1) stands untouched. Chosen alone, this must not be read as
closing the conflict this topic examines, or as making openXdox-code's suite
green standalone outright.
Explanation: Requirement 9 and Requirement 1 are different rules — one about
where a test's composition is declared, the other about which direction a
production import points. Satisfying the first says nothing about the
second.
Disposition status: open
Added-by: Claude Sonnet 5 (lane openxfactory-4) · 2026-09-27

### Q3. Does composing openXdox-code's CI with a pinned openxFactory checkout and no shared package (R1Q6's option (c)) close the Requirement 1 conflict?

Context: Option (c) has openXdox-code's own CI compose an openxFactory
checkout at a declared, pinned commit (checked out beside it — the shape
`pytest-suite` already uses for the root pins), reading requirement 9's "no
sibling" as "no sibling OF ITS OWN PROJECT" rather than "no sibling
repository at all." R1Q6's own recommendation named this option, or (d), as
the two live candidates for release 1; (d) (the declared exclusion) was
ruled instead, precisely so this direction question could be taken slower
and separately.
Recommended answer: No, for the same reason as Q2 — like (b), this closes
only the `doc_health` portion of requirement 9, and not the rail and contracts
classes that R1Q24 (a) also gave this arc (claim 6) unless the ruling reaches
them too, so not the whole of requirement 9 for the repository.
It changes CI composition, not a single production import, so it leaves
Requirement 1's conflict standing too.
Explanation: (c) is a test-execution-environment change, not an
import-direction change. The eight-module surface is unaffected either way.
Disposition status: open
Added-by: Claude Sonnet 5 (lane openxfactory-4) · 2026-09-27

### Q4. Should the surface be split — extracting only the non-governance slice to a neutral home, rather than choosing one shape for all eight modules?

Context: Claim 5 observes that at least `generator.py`'s three `doc_health`
imports (`doc_health.corpus`, `doc_health.corpus.RealGit`,
`doc_health.lines.split_keepends`) read as generic git/text utilities rather
than governance-specific logic, unlike the other seven modules' unaudited
reaches (`cli_gate`, `completeness`, `corpus_root`, `gate_console`,
`gate_routes`, `round_trip`, `snapshot_registry`).
Recommended answer: Worth auditing before ruling among (a)/(b)/(c) for the
WHOLE surface. Extract a small neutral utility module (own home, own pin,
trivial distribution) for whatever slice is genuinely non-governance, while
the genuinely governance-specific reaches take (b) or (c). This closes the
Requirement 1 conflict only for whatever it actually retargets — the other
modules, left on (b)/(c), stay exactly as open as Q2/Q3 describe unless they
too are retargeted.
Explanation: A single shape for all eight modules may be wrong if the
reaches are not uniform in kind. But this is an unaudited hypothesis: the
other seven modules' imports are not examined here, only asserted as a
possibility.
Disposition status: open
Added-by: Claude Sonnet 5 (lane openxfactory-4) · 2026-09-27

### Q5. Does R1Q23's answer force this arc's decision and realization ahead of its named deadline?

Context: R1Q23 (phase 2) asked whether F5.2 (phase 2, four of 5.4a's
six generator suites, which need `doc_health` and which F5.2 does not
provide) forces this arc's decision and realization ahead of its named
deadline (release 2's 12.5).
Recommended answer: No — follows R1Q23, answered (a): the F5.2 environment
also composes openxFactory's tools at a named commit, so phase 2 does not wait
for this arc and the deadline stays at release 2's 12.5. (Option (b), "bring
the direction arc forward", was not taken.)
Explanation: This topic's own deadline was derivative of R1Q23's answer,
which belongs to plan 034's own round (T009, phase 2), not to this topic.
Disposition status: ruled 2026-09-26 — Brett Heap, `#656` comment
`5850003126` (R1Q23 (a)); recorded here 2026-10-02
Added-by: Claude Sonnet 5 (lane openxfactory-4) · 2026-09-27

### Q6. Who owns the realization work once the direction is ruled?

Context: Plan 034 names no task for the fix itself — T008 raises the arc; it
does not schedule the work of actually retargeting `DOC_HEALTH_SURFACE`.
Recommended answer: The exit proposal should either carry its own task
list, or name the plan/lane that will own it, rather than leave realization
unowned once the direction is ruled.
Explanation: An arc that is ruled but not scheduled risks sitting exactly
where R1Q6 (d)'s exclusion already sits — tolerated, not resolved — unless a
proposal and owner are named at the same time as the ruling.
Disposition status: open
Added-by: Claude Sonnet 5 (lane openxfactory-4) · 2026-09-27

## Exit path

A proposal once Q1–Q3 are ruled (which of (a)/(b)/(c), or a
split per Q4). Q5's timing is settled: R1Q23 (a) does not pull this ahead of
phase 2's close. The shape depends on which is
ruled, because R1Q6's requirement-9 problem (can the suite run green alone)
and `corpus-adapter-seam`'s Requirement 1 conflict (do the production imports
point the wrong way — claim 1) do NOT necessarily close together:

- **If (b) or (c) alone is ruled, applied to the whole eight-module
  surface:** a realization change that moves or composes TESTS/CI only, for
  all eight `DOC_HEALTH_SURFACE` modules; their production imports are
  UNTOUCHED. This lifts R1Q6 (d)'s `doc_health` entries and lets
  `add-neutral-product-standalone-operability` report the `doc_health`
  portion of requirement 9 closed (the rail and contracts entries that R1Q24
  (a) also gave this arc stand until their files are moved or composed too —
  claim 6) — but Requirement 1's conflict stands
  exactly as measured today, for the full surface. R1Q6 (d) ruled only the
  standalone-suite/requirement-9 exclusion; it does NOT waive Requirement 1,
  and nothing has accepted this violation. The proposal must say so plainly
  and bring the conflict to Brett as its own question, rather than let
  requirement 9's closure read as if it had resolved this too.
- **If Q1's genuine neutral-home extraction is realized for all eight
  modules** (NOT R1Q6's literal option (a) alone, which Q1 finds does not
  resolve the seam by itself)**:** a realization change against
  openXdox-code (and openDox-code,
  if the chosen seam borrows the registered-adapter pattern already used for
  `corpus_adapter` / `domain_profile` there) that RETARGETS all of
  `DOC_HEALTH_SURFACE`'s eight modules away from importing `openxFactory`'s
  `doc_health` by name. This closes the `doc_health` portion of requirement 9
  outright (the rail and contracts entries stand unless the realization
  covers them too — claim 6) AND the Requirement 1 conflict outright.
  A `corpus-adapter-seam` or
  `neutral-product-pin` spec delta rides along only if the ruled shape needs
  new contract text.
- **If Q4's split is taken:** the same kind of realization change retargets
  only `generator.py`'s three imports, closing the Requirement 1 conflict
  for that one module alone. This does NOT by itself close even the
  `doc_health` portion of requirement 9: the other seven `DOC_HEALTH_SURFACE`
  modules' suites still fail collection standalone until they are ALSO
  resolved — either retargeted too (extending toward the full genuine
  extraction), or given the same (b)/(c) composition/CI treatment the first
  bullet describes for
  whatever is left. Q4's own recommended answer already bundles the split
  with (b)/(c) for the remaining seven; a proposal taking the split must
  carry that bundling through, not leave it implicit or deferred, and must
  not report requirement 9 closed on the split alone.

This arc's ruling closes the `doc_health`-caused portion of requirement 9's
exclusion only once every `DOC_HEALTH_SURFACE` module has received one of
these three treatments — (b)/(c) applied whole, the full genuine extraction
applied whole, or Q4's split paired with (b)/(c) (or retargeting) for what
it does not retarget; it
does NOT close even that portion from taking the split in isolation, with
the remaining seven modules' resolution left unscheduled. And even fully
closed, that portion is not the whole of what this arc owns for
openXdox-code: R1Q24 (a) (claim 6) also gave it the status-exemption-rail
class (3 files) and the openxFactory-contracts class (5 files), neither of
which is `doc_health`'s cause. openXdox-code's suite does not run green
standalone, and requirement 9 does not close for the repository, until the
declaration holds none of the three. This proposal must say, class by class,
which treatment reaches which entries (the section "What the declared
exclusion holds" lists them), and must not read the `doc_health` closure as
reaching the other two. The consumer-schemas class (R1Q25 (b)) is not this
arc's: T061 cleared it.
Closing the Requirement 1 conflict this topic was raised to examine is a
further, separate question, decided module by module regardless of either
exclusion's status: the whole surface closes it under the full genuine
extraction; the retargeted slice alone closes it under the split; every
module left on (b)
or (c) leaves it exactly as open as before. The proposal must say, module by
module, which is which, and must not let any one class's closure — however
achieved — imply Requirement 1's, or imply another class's.

Gated on: Brett Heap's ruling of Q1–Q3 (and optionally Q4), with Q5's timing
settled (R1Q23 (a)), and Q6's owner/task-list requirement — the exit proposal
must either carry its own realization task list or name the plan/lane that
owns it; a ruling among Q1–Q3 (and Q4/Q5) without also satisfying Q6 does not
clear this gate, since it would leave the fix ruled but unowned, exactly the
tolerated-not-resolved state this arc exists to end. Deadline, as R1Q6 (d)
and T008 name it: before release 2's 12.5 needs its sixteen governed-flow
suites to run; R1Q23 (a) does not bring it forward.
