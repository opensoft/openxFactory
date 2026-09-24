# Clarify questions — 034-opendox-standalone-operation (round 1)

**Feature**: `034-opendox-standalone-operation` — release 1 ("standalone
operation", phases 1–3) of the ratified OpenSpec change
`add-neutral-product-standalone-operability` (#1144).
**Lane**: `openxfactory-4`. **Raised**: 2026-09-24, while planning, before any
code.

**Status: 11 ANSWERED, 12 OPEN.**

- **ANSWERED** (R1Q1–R1Q9, R1Q20, R1Q22: every question phase 1 needed).
  RULED 2026-09-24T15:31:46Z by Brett Heap, interactive in the lane session,
  on `#656`, comment `5817152735`, verbatim: *"(a) on all eleven, (d) on
  R1Q6"*. So each of the eleven is answered (a), except R1Q6, which is
  answered (d). Every one of them is the option this file recommended. Each is
  encoded in [`spec.md`](./spec.md) § Clarifications and in
  [`tasks.md`](./tasks.md), where it shows as a `Ruled:` line.
- **OPEN** (R1Q10–R1Q19 and R1Q21, which bear on phases 2–3 and on process).
  Also **R1Q23**, which R1Q6's answer raises for phase 2. Where one of these
  carries a recommendation, it is a recommendation only. Every task it blocks
  names it on a `Blocked by:` line. Until they are answered, phases 2 and 3 are
  PROVISIONAL in the plan and authorize no implementation.

**Naming.** These are `R1Q1`…`R1Q23`. A bare `Q<n>` in this estate already names
one of #1144's own rulings (RULING Q1, RULING Q2, Q-R4, DIRECTION Q5), so this
round never uses one.

**Measured at**: openDox-code `1e4a57fb`, openXdox-code `626f2c8d`, openDox-spec
`8fe8c4c7`, openXdox-spec `f088b097`, openxFactory `dd2466ad`. Every figure is
re-runnable from [`research.md`](./research.md), which gives the command beside
it. Task ids (`T0nn`) are [`tasks.md`](./tasks.md)'s.

**How to answer.** One line per question is enough, e.g. `R1Q15 b`. An answer is
written inline under its question and encoded into `spec.md` in the same commit.
T004 did that for round 1a. T009 does it for phase 2's questions, and T069 for
phase 3's.
- An answer that changes a falsifier or a task line of #1144's `tasks.md` is
  recorded there by T007, on your word, under a Rule 6 window.
- An answer that would change a requirement's text or a scenario is put to
  you as RULING NEEDED first, and is not applied here. RN-1 is the one so far
  (plan.md § "Ruling needed").

**What each phase waits on.**

| phase | cannot start or close without |
|---|---|
| 1, it runs | no open question: R1Q1–R1Q9 and R1Q22 are answered (`5817152735`). T006's round-1a analyze and each slice's claim gate its start, and RN-1 gates its close |
| 2, useful alone | R1Q11, R1Q12, R1Q13 (the projection and the validator); R1Q10 (serving it); R1Q14 (7.3); R1Q23 (F5.2's four `doc_health` suites). T009 encodes them and re-plans the phase |
| 3, it installs | R1Q15, R1Q16 (the install); R1Q10, R1Q12 (chat standalone); R1Q17, R1Q18 (16.3); R1Q19 (the lens in the acceptance). T069 encodes them and re-plans the phase |
| every landing | nothing open. R1Q20 and R1Q22 are answered |
| process only | R1Q21 |

**What can start now**: the holder tasks T002, T003, T005 and T008, and T007's
batches A and C. T006 follows T003 and T005, and T007's batch B follows T041.
Every phase-1 task follows T006 and its slice's claim (T002). See `tasks.md`
§ "What can start".

---

## R1Q1 — Dropping the lanes mixin needs a mechanism #1144 says it will not design *(governs T007, T010, T011, T045, T084, T086; phases 1 and 3)* — **ANSWERED (a)**

**Measured.** `DashboardHandler` takes `serve_openxfactory_lanes.LaneRoutes` as a
BASE CLASS (`src/opendox/serve.py:734`), beside `consumer_reach.LateGateRoutes`
and `LateProjectionRoutes` (`:732-733`). A contributed `RouteBinding` names its
handler METHOD by string, and `route_extension.resolve_handlers` refuses at
wiring time any binding whose method the handler class lacks
(`src/route_extension.py:481-543`); the module says so in terms: *"A binding
therefore cannot introduce a handler the server does not already have"* (`:60`).
`build_server` builds the handler as
`type("BoundDashboardHandler", (DashboardHandler,), {...})` (`serve.py:1809`), so
no contributed base is possible. openxFactory's `LaneRoutesExtension.routes()`
names `_serve_committed_intents`, `_handle_refresh_action`, `_handle_dtn_seed`,
`_handle_staging_seed` and `_handle_apply_register_edits`
(`scripts/ideation_dashboard/serve_openxfactory_lanes.py:464-477`) — methods that
exist only on that mixin (`:110-400`).

**What #1144 says.** 2.2: *"openxFactory's half already exists … What remains is
openDox-code's half: 2.1's removal."* design.md § D4: *"No new mechanism is
designed by this packet for G1."*

**The collision.** Removing the base makes openxFactory's `build_server` refuse
with `RouteBindingError` on the five bindings. The same holds for openXdox's gate
and projection columns when 4.3 retires `consumer_reach.py` (phase 3).

**Options.**
- (a) **A handler-contribution facet.** A profile or extension declares the mixin
  classes holding the methods its bindings name; `build_server` composes them
  into `BoundDashboardHandler`'s bases. `resolve_handlers` is unchanged (every
  binding is still checked against the class that will dispatch it), and no core
  module names a contributor. openxFactory declares `LaneRoutes` in
  `scripts/profile_openxfactory.py`, an 11.1 surface. New mechanism, small.
- (b) `RouteBinding` may carry a callable. Reverses the seam's documented rule,
  *"never a callable the binding carries"* (`route_extension.py:43`).
- (c) openDox keeps a name-forwarding stand-in for the lanes column — the
  `consumer_reach` pattern 4.3 exists to retire.

**Recommendation.** (a). **ANSWER: (a)**, RULED in `5817152735`. T010 declares the facet. T007 batch A records the addenda to 2.2 and design.md § D4, since D4 said no new mechanism would be designed.

---

## R1Q2 — 11.1's allow-list forbids editing the openxFactory tests that pin openDox's internals *(governs T007, T034, T035, T045, T046, T093, T094; phases 1–3)* — **ANSWERED (a)**

**Measured.** openxFactory's
`test_the_mixins_precede_simplehttprequesthandler_in_the_mro`
(`tests/ideation-dashboard/test_extension_point_parity.py:380`) asserts, at
`:404-425`, that `DashboardHandler.__mro__[:8]` is exactly `(DashboardHandler,
WorkbenchRoutes, ProjectRoutes, LateGateRoutes, LateProjectionRoutes,
_LateConsumerColumn, LaneRoutes, SimpleHTTPRequestHandler)`, and imports
`opendox.consumer_reach` (`:406`). `pytest-suite`, a required check on
openxFactory `main`, runs all of `tests/`.

**What #1144 says.** 11.1: openxFactory's arc edits are *"exactly three kinds"* —
manifest notes; the host wiring in `scripts/opendox_host.py` and
`scripts/profile_openxfactory.py` *"with its tests under `tests/domain_profile/`"*;
and the two pin pairs. The guard refuses any other path an `Arc:`-trailered
landing touches.

**The collision.** The openDox pin advance that carries R1Q1's change (9.5), and
the one that deletes `consumer_reach.py` (4.3), make that test fail; repairing it
is a path outside the three surfaces. Without the pin advance the host wiring
cannot call the new seams. T035 has the same shape: relocating
`tests/test_session_harness.py` (it execs a script only openxFactory has) into
openxFactory is also a path outside the surfaces.

**Options.**
- (a) Widen 11.1's declared surfaces to NAMED openxFactory composition tests
  (edited, never removed), e.g. `tests/ideation-dashboard/test_extension_point_parity.py`.
- (b) Land those test edits as NON-arc acts (no `Arc:` trailer, like F3's
  overlays), in a form that passes at both the old and the new pin, before the
  pin advance.
- (c) Hold openxFactory's openDox pin until release 1 ends and do the host wiring
  in one landing.

**Recommendation.** (a); (b) works without amending the guard.
**ANSWER: (a)**, RULED in `5817152735`. T007 batch A widens 11.1 and F11.1 to NAMED composition tests, starting with `tests/ideation-dashboard/test_extension_point_parity.py`. Any further path (T034, T035) joins the named set in a later batch, before the landing that adds it.

---

## R1Q3 — Is the default profile registered by the entry point, or a fallback inside `current()`? *(governs T007, T016, T022; phase 1)* — **ANSWERED (a)**

**Measured.** Group 3's falsifier line 2 runs
`python -c "from opendox import domain_profile as d; print('OK', d.name_of(d.current()))"`
in a bare process and expects the default's name — only a fallback INSIDE
`current()` passes it. 3.2 puts the fallback in `build_parser()` and
`build_server()`, and 4.1a ties the adapter to it: *"exactly as Group 3's
default profile stands in for an unregistered host … so the default is a
registration the entry point makes and never a fallback inside the seam"*, with a
falsifier that needs a bare process to refuse. `register()` refuses a second,
different profile (`AlreadyRegistered`, `src/opendox/domain_profile.py:133`,
raised at `:180-181`), and openXdox's `_upstream()` reads `is_registered()` before
`current()` (openXdox-code `src/openxdox/domain_profile.py:1135-1156`).

**What the requirements say.** Requirement 3, scenario 1: *"WHEN the product's
parser or server is built in a process where no host has registered a domain
profile — THEN it builds on the product's OWN default profile and starts"*;
scenario 4: *"the default is a fallback and never a privileged path"*.
Requirement 5, scenario 3: *"WHEN a verb's seam has no registered implementation
in the running process — THEN the verb refuses"*. So for the ADAPTER a fallback
inside the seam is refused by the requirement itself; for the PROFILE either form
meets it, and F3.1 and 4.1a disagree about which was meant.

**Options.**
- (a) **Both defaults are registrations an entry point makes.** Amend F3.1 line 2
  to ask after `build_parser()`; `ProfileNotRegistered` stays for library
  callers; `is_registered()` answers True once an entry point registered the
  default.
- (b) **The profile default is a fallback inside `current()`** (F3.1 as written),
  the adapter keeps 4.1a/4.2 as written, and 4.1a's "exactly as" is corrected;
  `ProfileNotRegistered` becomes unreachable from `current()` and
  `profile_proxy`'s nothing-registered arm retires.

**Sub-questions, whichever option.** (i) 3.2 says `profile_proxy.py`'s refusal
*"is kept for the case it was written for — an ambiguous registration"*; the
file's own docstring says it was written for NOTHING REGISTERED
(`src/opendox/profile_proxy.py:42-46`), and an ambiguous second registration is
`AlreadyRegistered`. Proposed: correct 3.2's wording. (ii) A host that registers
AFTER an entry point registered the default: replace it (requirement 3,
scenario 4), or refuse as `AlreadyRegistered` because a parser was already built
from the default (RULED ASK-4 Q5's reason)? Recommended: replace while nothing
has been built; refuse once a parser or server was built from the default.

**Recommendation.** (a), with (i) as proposed and (ii) as recommended.
**ANSWER: (a)**, with (i) and (ii), RULED in `5817152735`. T007 batch A amends F3.1 line 2 and 3.2's wording. (ii) conflicts with the TEXT of requirement 3's fourth scenario, which replaces the default unconditionally. That text change is **RULING NEEDED RN-1** (plan.md § "Ruling needed"). It holds phase 1's close (T049), not T016's landing, because the after-build refusal is today's `AlreadyRegistered`.

---

## R1Q4 — What does the default profile contribute, given that an EMPTY default stays refused? *(governs T015, T038, T046; phase 1)* — **ANSWERED (a)**

**Measured.** A profile's facets are `SUBCOMMAND_EXTENSIONS`, `ROUTE_EXTENSIONS`,
`cli_gate` and `DISPLAY` (`scripts/opendox_host.py:113`). design.md § D5: *"an
EMPTY default is still refused"*, because *"a parser whose contributed verbs are
silently absent is indistinguishable from a working one"* (RULED ASK-2). Once a
default exists, a governed host that FORGETS to register gets a working-looking
parser without its gate verbs — the same failure mode, moved to hosts. With an
empty stand-in profile, today's core parser offers five verbs: `create`, `edit`,
`generate`, `generate-and-open`, `model-binding` (research R8).

**Options.**
- (a) The default contributes openDox's OWN verbs and routes — the runtime verbs
  now (R1Q5), release 2's `submit`/`land`/`health` later — with `DISPLAY` =
  `NEUTRAL_DISPLAY`; a governed host's own start asserts that its profile is the
  registered one (a host-side check in `scripts/opendox_host.py`).
- (b) Empty extension tuples plus `DISPLAY`; the forgotten-registration case is
  accepted.
- (c) Something else you name.

**Recommendation.** (a). **ANSWER: (a)**, RULED in `5817152735`. The default profile contributes openDox's own verbs, the runtime verbs now (T015, T038). The host's own start asserts its registration (T046). No #1144 line changes.

---

## R1Q5 — RULED Q-R4 wires the runtime verbs into `opendox.cli`; where do they register without breaking the 31-entry golden? *(governs T007, T015, T038, T042; phase 1)* — **ANSWERED (a)**

**Measured.** `src/opendox/runtime/cli.py:39-42` records RULED Q-R4 (`#656`
comment `5701772032`): *"the verbs are wired into `opendox.cli` in the BUILD-arc
act that repairs `opendox.serve`, and `opendox-runtime` is the spelling until
then"* (#1144 cites it at `:40-46`). The same file already ships
`RuntimeSubcommand` (`:1088`), structurally a
`subcommand_extension.SubcommandExtension`, written to be *"one line at the
assembly point"*. 10.1 says it *"discharges Q-R4's condition"* but adds only
`opendox = "opendox.cli:main"`, and the Group 13 and 14 falsifiers still call
`opendox-runtime`. openxFactory's `test_extension_point_parity.py` pins
`build_parser()`'s 31-entry `--help` tree (*"Regenerate the golden ONLY with a
ruling"*, `:205`), and 9.3 asserts the same tree in openXdox-code.

**Options.**
- (a) The runtime verbs arrive through the default profile's
  `SUBCOMMAND_EXTENSIONS` (R1Q4 (a)): `opendox runtime …` works standalone, a host
  that registers its own profile keeps its 31-entry tree, and `opendox-runtime`
  stays as an alias.
- (b) Wire them into `build_parser()` itself and regenerate both goldens on your
  word.
- (c) Keep `opendox-runtime` only, and record that 10.1 does not discharge Q-R4.

**Recommendation.** (a). **ANSWER: (a)**, RULED in `5817152735`. The verbs arrive through `RuntimeSubcommand` in the default profile's `SUBCOMMAND_EXTENSIONS`, and `opendox-runtime` stays as an alias (T038). Both 31-entry goldens stand (T042). T007 batch A adds 10.1's addendum.

---

## R1Q6 — openXdox-code cannot run its whole suite green alone while its own modules import openxFactory's `doc_health` *(governs T007, T008, T035, T041, T042, T043, T044, T059; phases 1–2)* — **ANSWERED (d)**

**Measured.** Eight openXdox-code modules import `doc_health` (`cli_gate`,
`completeness`, `corpus_root`, `gate_console`, `gate_routes`, `generator`,
`round_trip`, `snapshot_registry`), declared *"lawful HERE and nowhere else in
the estate"* (`tests/test_dependency_direction.py:290-315`, `DOC_HEALTH_SURFACE`).
openxFactory packages nothing (no `pyproject.toml`), so `doc_health` is not an
installable distribution. In a fresh venv (openXdox-code `626f2c8d`, openDox at
its pinned `5c137a90`), 57 of 85 test files fail collection: **26 on
`doc_health`**, 28 on `ideation_dashboard` (Group 2 fixes those), 3 on a missing
`test_gate_routes` helper. With Group 2 simulated, 19 of the 22 suites that 5.4a
and 12.5 protect still fail on `doc_health` (research R11). The six skips defer
*"`doc_health` reachability"* to *"BUILD-arc work (§ 3.5/3.6)"*, as does RULED
Q-L8 (b′), which narrowed `validate.yml` — the runtime arc, finished, which
design.md § D2 says is a different arc of the same name.

**What the requirement says.** Requirement 9: each repository runs its suite to
green *"in its own checkout with no sibling repository present"*, and a test
needing two repositories is an integration test living *"where the composition is
declared"*. Its first scenario also admits a DECLARED exclusion *"with its count
and its reason"*, reported as an open extraction.

**Options.**
- (a) openXdox-code gains `doc_health` as a declared, pinned dependency. Needs
  openxFactory to package it, and makes the pins two-way (openxFactory already
  pins openXdox).
- (b) The `doc_health`-dependent openXdox tests become declared integration tests
  where openXdox + openxFactory are composed — openxFactory — which needs R1Q2's
  surfaces widened to admit them.
- (c) openXdox-code's CI composes openxFactory at a declared commit (checked out
  beside it, the shape `pytest-suite` uses for the roots), and 9.2's "no sibling"
  is read as "no sibling of its own project".
- (d) For release 1, F9.1 is amended for openXdox-code to accept a DECLARED
  exclusion list with its count and reason — requirement 9's first scenario — and
  the direction question becomes its own arc, decided before 12.5 (release 2)
  needs the 16 governed suites to run.

**Recommendation.** (d) for release 1, or (c) now; (a) creates a pin cycle.
**ANSWER: (d)**, RULED in `5817152735`. The exclusion is declared with its count and its reason (T041), and T007 batch B amends F9.1 for openXdox-code. T008 raises the direction arc. Two consequences follow. Requirement 9 stays an OPEN EXTRACTION for openXdox-code until that arc lands, and the archive must report it so. Four of 5.4a's six suites also need `doc_health`, which F5.2 does not provide; that raises **R1Q23** (phase 2).

---

## R1Q7 — The suites 5.4a and 12.5 forbid the arc to edit already fail, and one of them introspects a method release 1 moves *(governs T007, T043, T059, T086; phases 1–3)* — **ANSWERED (a)**

**Measured.** 5.4a's falsifier refuses any arc edit to openXdox's six generator
suites, and 12.5's to the 16 governed-flow suites, counted over EVERY `Arc:`
landing since `ARC_BASE` — release 1's included. All 22 error today, 12 on
`ideation_dashboard` and 10 on `doc_health`. With Group 2 simulated (research
R11): 19 fail on `doc_health`; `test_gate_loop_views.py` passes 74;
`test_snapshot.py` fails 3, all in the validator lookup and schema path 7.3 and
C3 fix; `test_snapshot_validation_launch.py` fails 9 on a missing
`tests/fixtures/base-repo`, an openxFactory fixture the carve did not bring.
`tests/test_branch_session.py:1145-1154` reads
`inspect.getsource(serve_mod.DashboardHandler._handle_gate_action)` and asserts on
its text; since BUILD slice 2b that attribute is `consumer_reach`'s forwarder —
qualname `LateGateRoutes._handle_gate_action`, source `def forward(...)` — and the
asserted text is ABSENT, so the suite fails on that assertion even once it
imports. Release 1 then removes the base altogether (R1Q1).

**Options.**
- (a) Admit a reviewed allow-list of edits to protected suites that only RESPELL
  a reference to a moved seam (no assertion weakened), recorded per edit.
- (b) Keep a named `_handle_gate_action` forwarder on `DashboardHandler` so the
  suite needs no edit — a late forwarder 4.3 otherwise retires, and the stale
  assertion still fails.
- (c) Fixture and dependency fixes only (added files, no suite edit), and
  `test_branch_session.py` put to you as the one named exception.

**Recommendation.** (a). **ANSWER: (a)**, RULED in `5817152735`. T007 batch C records the reviewed allow-list in F5.2 and 12.5's falsifier. In release 1, `test_branch_session.py` sits in R1Q6 (d)'s exclusion, because it needs `doc_health`. So its respelling is due when it becomes runnable (T043).

---

## R1Q8 — Does openDox-code's "whole suite" include `tests_runtime/`? *(governs T036; phase 1)* — **ANSWERED (a)**

**Measured.** `pyproject.toml:228` sets `testpaths = ["tests"]`, so the Group 9
falsifier's plain `python -m pytest -q` never collects `tests_runtime/` (10
modules). A separate `runtime` job runs `pytest -q tests_runtime/` against a
Postgres service; the only check required on a PR is `validate`, so it is not
one. 22 modules are run by no CI step at all (research R4; the packet said 26).

**Options.**
- (a) Yes: widen `testpaths` to both roots and give the required job a database
  (a Postgres service now, Group 13's bundled server later); F9.1 unchanged.
- (b) No: `tests_runtime/` stays in the `runtime` job, which becomes a second
  required check; F9.1 is read as `tests/` only.
- (c) Widen `testpaths`, and database-backed tests skip without a DSN — a skip
  9.4 wants to stop.

**Recommendation.** (a). **ANSWER: (a)**, RULED in `5817152735`. T036 widens `testpaths` and gives the required `validate` job a PostgreSQL service. F9.1 is unchanged, and its runs export the job's DSN.

---

## R1Q9 — `session_documents` is a notebook membership rule, not part of `run_scoped_doc_health` *(governs T007, T025, T046; phase 1)* — **ANSWERED (a)**

**Measured.** 4.3: *"`workbench.py`'s four are the reaches `run_scoped_doc_health`
makes (6.2). Once routed here, they refuse until Group 6 registers openDox's own
check."* Only three are (`workbench.py:1407-1409`). The fourth, `:746`, is inside
`session_documents` — the source set of a session's NotebookLM notebook, whose
membership rule is openxFactory's governed roots plus a `Status:` header —
called from `branch_session.py:3293`. Routing it to "refuse until Group 6"
removes the session notebook from the standalone product until release 2.

**Options.** (a) It resolves through the registered corpus adapter's
`list_documents` in phase 1 — openDox's `LocalGitCorpus` standalone,
openxFactory's adapter hosted — and the hosted membership rule is proved
unchanged (openxFactory's adapter or host wiring supplies the governed-roots +
`Status:` rule). (b) As written: it refuses until Group 6.

**Recommendation.** (a). **ANSWER: (a)**, RULED in `5817152735`. T025 does this in phase 1, and T046 keeps the hosted membership rule. T007 batch A corrects 4.3's "four".

---

## R1Q10 — Which consumer mechanisms get an openDox-owned default, so the wheel, lens and chat work with nothing else installed? *(blocks T009, T055, T069, T081, T082, T084, T085, T095; phases 2–3)* — **OPEN**

**Measured.** Beyond 4.3's 27 literal reaches, openDox reads 11 `consumer_reach`
names at **65 use sites**, and 4.3's falsifier deletes `consumer_reach.py`
(research R6). Every mechanism on release 1's path:

| mechanism (openXdox unless noted) | `consumer_reach` uses | 4.3 reaches | what needs it standalone |
|---|---|---|---|
| `snapshot_registry` (1,318 lines) | 22 (serve 18, serve_workbench 4) | 5 (branch_session 4, cli 1) | `build_server` itself (`serve.py:1647`), `/snapshot.json`, `/source/`, sessions |
| `serve_projection` column (`LateProjectionRoutes`, `hosted_ref_refused`) | 1 base + 2 | — | the core `/snapshot.json` arm (`_serve_snapshot`) |
| `serve_gate` column (`LateGateRoutes`) | 1 base | — | the gate route |
| `corpus_root` (101 lines) | 2 (cli) | 2 (`serve.py:629`, `:1993`) | every `build_server` (`_checkout_real`, `:1687`); `generate` on a plain repo |
| `snapshot` (223 lines; writer, validator lookup) | 7 (cli 6, workbench 1) | — | every generate verb |
| `generator` (974 lines) | 3 (cli) | 1 (branch_session) | every generate verb (5.4's seam) |
| `doxbench_scope` (769 lines) | — | 4 (serve_workbench) | workbench thread, chat turn, abstract pane, session refs |
| `gate_console` (2,380 lines), `gate_routes` (3,553 lines) | 27 (branch_session 20, cli 7) | 4 (serve_workbench 3, serve_project 1) | chat Save (the first-edit gate), model approval, sessions, project register |
| `kickoff`, `register` | — | 3 | sessions, project register |
| openxFactory `ideation_dashboard.doxbench_contracts` (`serve_wire.py:1369`) | — | 1 | the model-catalog and chat-turn routes (`serve_workbench.py:759`, `:1515`), which fail closed without it |
| openxFactory status-exemption rail (`doxbench_packet.py:177`) | — | 1 | chat packet assembly |

Measured with the imports fixed and a stand-in profile registered: a standalone
`build_server(...)` is REFUSED at `serve.py:1647` —
`ConsumerReachUnavailable: 'openxdox.snapshot_registry' belongs to openXdox…`
(research R7). And F16.1 checks "no model configured" IN PROCESS
(`declared_model_port_factory(...)().catalog()`), while the SERVED catalog route
validates its answer with openxFactory's `doxbench_contracts` — so F16.1 can pass
while the page cannot reach that state. AT-R1 would catch it; F16.1 would not.

**What #1144 says.** It rules an openDox-owned implementation for the generator
(R-G3) and the corpus adapter (4.1a) only. For the rest, 4.3: *"resolves through
an existing seam … or through one declared for it … With nothing registered, a
verb refuses."* The release map: *"Group 16's chat must answer with no consumer
installed"*; 16.5: sessions and saving *"answer exactly as they do with a model
configured"*.

**Options.**
- (a) R-G3's pattern for each: openDox grows a small neutral default, openXdox
  keeps its governed one and contributes it through the seam. For the two
  openxFactory rows: openDox's own doxBench validators over its spec leg's two
  chat schemas (R1Q12), and no status exemption by default.
- (b) Relocate the mechanisms that carry no governance vocabulary (measured per
  module) from openXdox-code into openDox-code; openXdox keeps thin governed
  wrappers.
- (c) Narrow release 1: chat turns, the no-model state and the views work
  standalone; Save, model approval and sessions stay consumer-backed until
  release 2 (amends 16.5).

**Recommendation.** (a). **ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q11 — The snapshot contract requires the very words Group 5's falsifier forbids *(blocks T009, T050, T052, T053, T054, T058; phase 2)* — **OPEN**

**Measured.** openXdox-spec `contracts/schemas/ideation-dashboard-snapshot.schema.yaml`
REQUIRES `documents[].stage` (`required: [id, path, stage]`) and restricts it to
`lifecycle_status` = `brainstorm, staged, draft, ratified, standard, superseded,
retired, record, projection`; `possibles[].state` is `latent, picked, rejected,
superseded`; `changes`, `possibles` and `staged_topics` are required top-level
keys. openDox's own `display_profile.SNAPSHOT_VALUES` (`:227-231`) makes its
views match `documents[].stage` on `brainstorm`/`staged` and `possibles[].state`
on `latent … superseded`.

**What #1144 says.** 5.0 and F5.3 forbid `brainstorm, staged, draft, ratified,
standard, superseded, retired, record` in ANY string value of the neutral
snapshot; requirement 4, scenario 2: *"a snapshot is generated and it names no
publisher noun"*; 5.3: *"`display_profile.py` is unchanged by this group"*; F7.2
validates the generated snapshot under `--strict`.

**The collision.** A schema-valid snapshot with one document fails F5.3; one that
passes F5.3 fails F7.2. As written, neither can pass beside the other.

**Options.**
- (a) openDox owns a NEUTRAL snapshot contract — a new schema in openDox-spec
  whose stage values are the six role keys; its generator writes it and its views
  read it; openXdox's governed generator keeps `ideation-dashboard-snapshot`, and
  its facet maps roles to governed values. Cost: `SNAPSHOT_VALUES`' neutral
  defaults move (contra 5.3, unless the governed values move to openXdox's facet),
  and an openDox-spec contract is added — likely a `dox-v1.1` bundle minor at the
  openDox root, which 9.5's *"none cuts a contract bundle"* did not foresee.
  Largest; the only option that meets scenario 2 as ratified.
- (b) Keep `ideation-dashboard-snapshot`; narrow F5.3 to exclude
  schema-enumerated machine values (`documents[].stage`, `possibles[].state`) and
  assert instead that no governance word is RENDERED. Smallest; reads "names" in
  scenario 2 as "renders", which is an amendment.
- (c) Widen the schema's enums (an openXdox-spec change) to admit neutral values,
  and change `SNAPSHOT_VALUES`' defaults (edits `display_profile.py`, contra 5.3).

**Recommendation.** (a). **ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q12 — Which snapshot schema does openDox's validator own, and how does a spec-leg schema reach the code leg's package? *(blocks T009, T051, T053, T057, T058, T069, T081, T085, T095; phases 2–3)* — **OPEN**

**Measured.** The post-render validator's subject is the rendered snapshot
(`ideation-dashboard-snapshot`), whose schema lives in openXdox-spec. openDox-spec's
three schemas are `ideation-workbench`, `xfactory-workbench-chat-turn` and
`xfactory-workbench-model-catalog` — the workbench manifest and the doxBench chat
wire, not the snapshot. `neutral-product-pin` admits a vendored copy of a
PUBLISHER's schema; openXdox is the consumer, and RULING OQ-2's pin chain forbids
openDox pinning it. 7.1 ships the schemas as package data *"so `pip install
openDox-code` puts them on disk"*, but they live in another repository.

**What #1144 says.** 7.1: openDox validates *"its spec leg's three"*; *"The
openXdox-spec three belong to the CONSUMER's validator and openDox never needs
them."* F7.2 validates a snapshot and asserts the malformed fixture's
`EXPECTED_RULE`.

**Options.**
- (a) Follows R1Q11 (a): openDox-spec owns the neutral snapshot schema; the code
  leg carries digest-checked copies of its spec leg's schemas, held by a test to
  the spec-leg commit the openDox root pins; the malformed fixture breaks one of
  that schema's rules. The same copies serve T085's chat validators.
- (b) Re-home `ideation-dashboard-snapshot` (and `-index`) from openXdox-spec to
  openDox-spec; openXdox then consumes it from openDox, the lawful direction.
- (c) Drop post-render snapshot validation from openDox's generate verbs; openDox
  validates only its own three kinds, and F7.2 is amended to validate a workbench
  manifest.

**Recommendation.** (a) if R1Q11 is (a); otherwise (b).
**ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q13 — How does a plain document land in one of the six stations, and what front matter is neutral? *(blocks T009, T050, T054, T096; phase 2 and the acceptance)* — **OPEN**

**Measured.** The six stations read six different snapshot sections, declared in
`web/views/display.js:139-144`: sources ← `documents`, groups ← `clusters`,
candidates ← `possibles`, selections ← `staged_topics`, submissions ← active
`changes`, completed ← archived `changes`. `NEUTRAL_DISPLAY`'s areas all carry
`prefix: null`. openDox's default adapter, `LocalGitCorpus()`, defaults
`required_fields=()` (`runtime/local_git_adapter.py:1544-1547`), so with 4.1a in
place `required_header_fields()` answers an empty tuple. And the chat pane is
reachable ONLY through the wheel's `workbench` verb on a grouping, candidate or
selection tile (`web/views/wheel.js:278-282`; `app.js:1544` is its one caller) —
so AT-R1 needs the plain repository to yield at least one such tile.

**What #1144 says.** 5.0: plain documents *"spread across the six neutral
stages"*; design.md § D10.5 names *"a declared stage that disagrees with where the
document sits"* and *"missing neutral front matter from the adapter's fields"*.
Nothing defines either.

**Options.**
- (a) A neutral front-matter key names the stage role (e.g. `stage: grouping`),
  and the default adapter declares a small neutral field set (e.g. title, summary).
- (b) A folder convention per role, declared by the default profile's areas.
- (c) A plain repository's documents are all sources, groups derive from shared
  topics, and later stations fill only through the product's own acts.

**Recommendation.** (a), with (c) for documents that declare nothing — and the
fixture yields at least one group, so AT-R1 can open the chat pane.
**ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q14 — 7.3's falsifier and lane 4's ruled C3 act disagree about `find_validator` *(blocks T009, T061; phase 2)* — **OPEN**

**Measured.** C3 (claimed on `#656` `5815613524`, ruled (a) in `5815412869`) makes
openXdox's `find_validator` answer `None` from a start outside the product
(`test_a_start_outside_the_product_is_refused_not_walked`), and the claim says
realizing 7.3 *"will revisit that confinement and that test"*. 7.3's falsifier
requires `snapshot.find_validator(planted / "work")` to return the INSTALLED
consumer's own validator. It also names
`tests/test_snapshot.py::test_the_validator_is_the_installed_consumers_own`,
which does not exist yet. T061 must add it to one of 5.4a's six protected
suites, and F5.2 refuses that edit, because R1Q7 (a)'s allow-list admits only
respellings. So an answer here must also say how F5.2 admits it.

**Options.** (a) 7.3 governs: the lookup ignores its start and resolves the
installed distribution's validator, and C3's test is revised in 7.3's landing.
(b) C3 governs: 7.3's falsifier is amended to expect `None` outside the product.

**Recommendation.** (a). **ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q15 — With nothing configured, does `opendox generate-and-open` serve (Group 10) or refuse (Group 13)? *(blocks T069, T070, T074, T076, T077, T095; phase 3 and the acceptance)* — **OPEN**

**Measured.** F10.1 runs
`opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8080`
with NO setting and requires the bundle to be served. 13.4: the selector
*"defaulting to `hosted`"*, *"It is UNSET, not `local`, that must be safe"*;
F13.1's last probe runs the same command with the selector unset and requires a
refusal naming `OPENDOX_OIDC_ISSUER`. Both close in phase 3.

**What the requirements say.** Requirement 13: *"The local mode SHALL BE SELECTED
EXPLICITLY and SHALL NOT BE REACHABLE BY OMISSION"*; its scenario 1: a student
*"selects the local mode"*. Requirement 10, scenario 2: the user *"runs the single
command its README documents"*.

**The collision.** After Group 13 lands, F10.1 fails; and the one documented
command must carry the mode.

**Options.**
- (a) The install mode governs only the runtime's datastore and identity; the
  loopback document surface needs neither, so F10.1 stands and F13.1's hosted
  probes move to the runtime's own entry. Conflicts with 13.4a's "one served
  product".
- (b) The documented command selects local explicitly (a `--local` flag or
  `OPENDOX_INSTALL_MODE=local`); F10.1 is amended to pass it, and 10.3's README
  documents it.
- (c) Default to local when bound to loopback, hosted otherwise. Conflicts with
  requirement 13's *"SHALL NOT BE REACHABLE BY OMISSION"*, so it amends a
  requirement.

**Recommendation.** (b), with a `--local` flag. **ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q16 — "One served product": process shape, what the document surface needs the datastore for, and what `pip install` brings *(blocks T069, T070, T072, T073, T074, T077, T095; phase 3)* — **OPEN**

**Measured.** The document surface never imports the runtime: outside
`src/opendox/runtime/`, only `conformance_corpus.py` touches it, and only
`local_git_adapter` (research R9). The runtime is a separate FastAPI app
(`/livez`, `/readyz`, `/api/v1`). `pyproject.toml` keeps FastAPI, uvicorn,
psycopg, PyJWT and httpx in a SEPARATE `runtime` extra on purpose (*"WHY A
SEPARATE EXTRA AND NOT `dependencies`"*, `:96`). F13.1 installs plain `.` and
then needs a bundled PostgreSQL server and `opendox-runtime runtime status`,
which needs psycopg.

**What #1144 says.** 13.4a: *"the document surface and the runtime are one served
product, so the process a user reaches is the process whose configuration is
reported."* 13.1: *"its packaging is the realization's choice."*

**Sub-questions.** (i) Topology: the document server loads the runtime settings
and owns the bundled server as a child; or the entry point supervises the runtime
as a second process; or the runtime mounts in-process. (ii) In release 1 the
document surface reads nothing from the store — is starting and migrating it all
13.1 asks? (iii) Does the base install gain the runtime dependencies and a bundled
PostgreSQL, or is the standalone install `pip install "opendox[local]"` with F13.1
amended? (iv) Does the bundled server stop with the entry point?

**Recommendation.** (i) the document server owns the bundled server as a child and
reports it; (ii) yes; (iii) an `opendox[local]` extra; (iv) yes.
**ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q17 — What resolves a credential reference in a standalone install? *(blocks T069, T080; phase 3 — #1144 leaves this to the realization)* — **OPEN**

**Measured.** Every binding record names a broker program (`broker_argv`,
required, `src/opendox/doxbench_binding.py:138`); the one broker that exists is
openProfiler's `openprofiler-broker`, a separate product. design.md § D14: *"Both
are realization decisions … task 16.3 names them rather than making them."*

**Options.** (a) Require `openprofiler-broker` for hosted APIs. (b) A minimal
built-in resolver for a reference such as `env:NAME` or the OS keyring, resolved
at call time inside `doxbench_provider.py` only. (c) Release 1 ships
credential-free local endpoints only; hosted APIs need the broker.

**Recommendation.** (b). "The realization's choice" is a valid answer.
**ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q18 — How does an endpoint that takes no credential say so? *(blocks T069, T080; phase 3 — also left to the realization)* — **OPEN**

**Measured.** `AUTH_KINDS` is `(api_key, oauth)` (`doxbench_binding.py:93`) and
`broker_argv` is a required field (`:129-139`). Requirement 17 says only that the
absence is declared explicitly, never by a field left out.

**Options.** (a) A third auth kind, `none`, under which `broker_argv` and
`credential_ref` are forbidden. (b) A sentinel `credential_ref` value.

**Recommendation.** (a). **ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q19 — The lens's two openxFactory seed actions, in a standalone install *(blocks T069, T088, T096; the acceptance)* — **OPEN**

**Measured.** `web/views/lens.js:57,61` post to `/actions/dtn-seed` and
`/actions/staging-seed`, which only openxFactory's lanes answer. The web census
keeps `lens.js` as its one declared `?` row, *"until: a future ruling on
views/lens.js's two openxFactory-lane routes"*
(`tests/fixtures/web_boundary_census.yaml:429`).

**Options.** (a) Offer the two actions only where a binding answers them
(capability-gated); `lens.js` stays `?`. (b) Move the two controls into a view
extension openxFactory contributes; the `?` row retires. (c) Leave them; they fail
standalone.

**Recommendation.** (a) now, (b) later. **ANSWER:** OPEN (phases 2–3); awaiting Brett Heap.

---

## R1Q20 — Do the arc's own bookkeeping commits carry the `Arc:` trailer? *(governs T003, T007, T091, T093, T096, T097)* — **ANSWERED (a)**

**Measured.** 11.0: *"Every commit this arc lands, in EVERY repository it touches —
openxFactory, … — carries the trailer"*. 11.1's guard refuses any trailered
openxFactory landing that touches a path outside its three surfaces, and
*"Nothing is exempt"* (its own example is a ledger edit). This feature's
directory, the ticks and evidence notes in #1144's `tasks.md`, and any interim
guard output are openxFactory paths outside those surfaces. F3's overlays are the
precedent for a non-arc act.

**Options.** (a) Bookkeeping (Speckit feature files, #1144 ticks and evidence)
carries NO `Arc:` trailer; only realization landings do. (b) Bookkeeping carries
it, and 11.1's surfaces are widened to this feature's directory and the packet's
`tasks.md`.

**Recommendation.** (a). This planning PR follows (a) already.
**ANSWER: (a)**, RULED in `5817152735`. Bookkeeping carries no `Arc:` trailer (T091). T007 batch A adds 11.0's addendum. This PR, T003, T007, T093, T096 and T097 follow it.

---

## R1Q21 — Release 2: a second Speckit feature, or phases 4–5 appended here? *(process; no release-1 task waits on it)* — **OPEN**

**Measured.** The global protocol says a change hands off to *"exactly one
Speckit feature"*; openxFactory's constitution (Principle II) allows *"one or
more"*; this repository has done it both ways — `split-openxwallet-repo` by five
features (016, 017, 018, 023, 024) and `add-modified-block-currency-check` by four
(019–022).

**Options.** (a) Release 2 is its own feature, planned after release 1 lands.
(b) 034 grows phases 4–5.

**Recommendation.** (a). **ANSWER:** OPEN (process; no release-1 task waits on it); awaiting Brett Heap.

---

## R1Q22 — Does the carve's declared-edit discipline govern the arc's edits to carved files? *(governs T007 and every task that edits a carved file: T010–T012, T016, T021, T022, T025–T027, T034, T035, T038, T055, T057, T073, T078–T081, T084, T088; in openXdox-code, T061 and T086; and T092)* — **ANSWERED (a)**

**Measured.** `src/opendox/runtime/cli.py:17-19`: *"`src/opendox/cli.py` is a
CARVED file with a row in openxFactory's `docs/opendox-carve-manifest.yaml`, so a
line added to it is a DECLARED EDIT that has to land as a row annotation at
openxFactory first"*. The manifest records declared-edit windows that added
`edits[]` entries BEFORE the destination edit (the ASK-7 window,
`docs/opendox-carve-manifest.yaml:504-521`), and lane 4's C3 does the same today
for openXdox's `snapshot.py` (`moved_verbatim` → `moved_with_declared_edit`, the
openxFactory annotation first, RULED Q-XDV3). Release 1 edits at least 12 carved
openDox-code SOURCE files, and also eight of R3's nine red tests and six of the
seven `collect_ignore` modules, all of them carved rows (research R12). In
openXdox-code, T061 and T086 edit carved rows too. Two of the
source files are `moved_verbatim` rows with no `edits[]` entry: `doxbench_binding.py` (16.1–16.3) and, likely,
`web/views/doxbench-chat.js` (16.4). 11.1's guard lets an arc landing change the
manifest only by adding or extending an existing `edits[].note` — it refuses
any other change (*"a row, a field, a digest"*) and any disposition move.

**Options.**
- (a) No: the manifest records the carve as it ARRIVED; post-arrival development
  is ordinary work, and 11.1's notes record only each closed reach. C3's
  re-disposition is different because it discharges the carve's own archived
  residue.
- (b) Yes: every arc edit to a carved file first needs a declared-edit landing in
  openxFactory, as a NON-arc act (like C3's PR 1), one per slice.
- (c) Yes, and 11.1's guard is widened so trailered landings may add `edits[]`
  entries.

**Recommendation.** (a). **ANSWER: (a)**, RULED in `5817152735`. No arc edit to a carved file needs a declared-edit act. T038 corrects `runtime/cli.py:17-19`, which said otherwise, and T007 batch A adds 11.1's addendum.

---

## R1Q23 — R1Q6 (d) leaves four of 5.4a's six generator suites unable to run where F5.2 runs them *(blocks T009, T059, T063; phase 2)* — **OPEN**

**Raised by** the answer to R1Q6 (`5817152735`), on 2026-09-24, and asked here
rather than assumed.

**Measured.** F5.2 runs 5.4a's six generator suites in an openXdox-code
checkout. It installs `.[test]` and then the realized openDox, and nothing
else. With Group 2 simulated, four of the six fail on `doc_health`:
`test_generator`, `test_snapshot_determinism`, `test_snapshot_registry` and
`test_session_snapshot` (research R11). openXdox's `generator.py` and
`snapshot_registry.py` import it at module level (`DOC_HEALTH_SURFACE`,
research R10). R1Q6 (d) makes that reach a DECLARED EXCLUSION for F9.1 and
moves the direction question into its own arc (T008). It sets that arc's
deadline at release 2's 12.5. It says nothing of F5.2, which closes in phase
2, in release 1.

**What #1144 says.** 5.4a: the consumer *"loses no capability — requirement
4's third scenario is the check"*. F5.2: *"the governed projection's own suites
pass, and the arc did not edit them."* Requirement 4, third scenario: *"WHEN
the consumer layer IS installed and points the product at the publisher's
governed corpus — THEN the projection is unchanged."*

**Options.**
- (a) F5.2's environment also composes openxFactory at a NAMED commit: its
  `scripts/` directory, where `doc_health` lives, goes on `PYTHONPATH`, and
  the run quotes that commit. Only F5.2's environment line is amended. This is
  the declared-composition pattern of requirement 9's second scenario, and it
  is the setting requirement 4's third scenario names.
- (b) Bring T008's direction arc forward. It is decided and realized before
  phase 2 closes, so `doc_health` reaches openXdox-code however that arc
  decides, and F5.2 runs as written. That puts a new arc on release 1's
  critical path.
- (c) 5.4a and F5.2 stay open at release-1 close and move to the arc's close,
  like 9.5. Release 1 then records the four suites as the same open
  extraction.

**Recommendation.** (a). **ANSWER:** OPEN (phase 2); awaiting Brett Heap.
