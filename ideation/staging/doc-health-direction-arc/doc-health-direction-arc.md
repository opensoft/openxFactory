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
reprieve deferred: how the dependency should actually run, so requirement 9
stops being an open extraction for openXdox-code.
Topics: doc_health, direction-arc, corpus-adapter-seam, dependency-direction, openxdox-code, neutral-tooling-home, R1Q6, opendox-standalone-operation, plan-034
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
governed-flow suites to run — or sooner, if R1Q23 (open, phase 2) is answered
(b).

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

6. **The declared exclusion has a hard deadline, not an open-ended one.**
   R1Q6 (d)'s exclusion is explicitly *"an OPEN EXTRACTION"* for openXdox-code
   — `add-neutral-product-standalone-operability`'s archive act must report
   requirement 9 as open there, and must not read it as closed, until this arc
   lands. R1Q23 (open, phase 2, `specs/034-opendox-standalone-operation/clarify-questions.md`)
   already asks whether this arc must be brought forward INTO release 1's
   critical path, because four of 5.4a's six generator suites need
   `doc_health` in phase 2's F5.2 falsifier too and F5.2 does not provide it.

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

- **This topic's own subject is a currently-tolerated conflict with a
  ratified spec.** openXdox-code's eight `doc_health` imports stand against
  `corpus-adapter-seam`'s Requirement 1 today, held open only by R1Q6 (d)'s
  named, counted, release-1-scoped exception (`#656` comment `5817152735`).
  That is not a new conflict this topic creates; it is the conflict this
  topic exists to EXAMINE — not necessarily to close, and NOT waived by
  R1Q6 (d): that ruling covers only the standalone-suite/requirement-9
  problem, and nothing in the ruled record accepts or decides this conflict.
  Q2 and Q3 (options (b) and (c)) can close R1Q6's requirement-9 problem (the
  suite runs green alone) without touching a single production import,
  which would leave this Requirement 1 conflict standing as its own,
  separately unresolved question. Only option (a) done as a genuine
  extraction closes the conflict for the whole eight-module surface; Q4's
  split closes it only for whatever slice it actually retargets, leaving it
  open for any module left on (b) or (c) instead. See § Exit path. No other
  staged topic or ratified spec is known to contradict the material above.
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
Recommended answer: No — it closes requirement 9 only (the suite runs green
alone, because the moved tests no longer need to). It moves or composes
TESTS, not production code: `DOC_HEALTH_SURFACE`'s eight modules keep their
imports exactly as measured, so the Requirement 1 conflict (claim 1) stands
untouched. Chosen alone, this must not be read as closing the conflict this
topic examines.
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
requirement 9 only. It changes CI composition, not a single production
import, so it leaves Requirement 1's conflict standing too.
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

Context: R1Q23 (open, phase 2) asks whether F5.2 (phase 2, four of 5.4a's
six generator suites, which need `doc_health` and which F5.2 does not
provide) forces this arc's decision and realization ahead of its named
deadline (release 2's 12.5).
Recommended answer: Follows R1Q23; not decided here. If R1Q23 is answered
(b) ("bring the direction arc forward"), this topic's exit gate tightens to
phase 2's close rather than 12.5.
Explanation: This topic's own deadline is derivative of R1Q23's answer,
which belongs to plan 034's own round (T009, phase 2), not to this topic.
Disposition status: open
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
split per Q4) and Q5's timing is settled (does
R1Q23 pull this ahead of phase 2's close). The shape depends on which is
ruled, because R1Q6's requirement-9 problem (can the suite run green alone)
and `corpus-adapter-seam`'s Requirement 1 conflict (do the production imports
point the wrong way — claim 1) do NOT necessarily close together:

- **If (b) or (c) alone is ruled, applied to the whole eight-module
  surface:** a realization change that moves or composes TESTS/CI only, for
  all eight `DOC_HEALTH_SURFACE` modules; their production imports are
  UNTOUCHED. This lifts R1Q6 (d)'s declared exclusion and lets
  `add-neutral-product-standalone-operability` report requirement 9 closed —
  but Requirement 1's conflict stands exactly as measured today, for the
  full surface. R1Q6 (d) ruled only the standalone-suite/requirement-9
  exclusion; it does NOT waive Requirement 1, and nothing has accepted this
  violation. The proposal must say so plainly and bring the conflict to
  Brett as its own question, rather than let requirement 9's closure read as
  if it had resolved this too.
- **If (a) is ruled and realized as a genuine extraction of all eight
  modules:** a realization change against openXdox-code (and openDox-code,
  if the chosen seam borrows the registered-adapter pattern already used for
  `corpus_adapter` / `domain_profile` there) that RETARGETS all of
  `DOC_HEALTH_SURFACE`'s eight modules away from importing `openxFactory`'s
  `doc_health` by name. This closes requirement 9 for the repository AND the
  Requirement 1 conflict outright. A `corpus-adapter-seam` or
  `neutral-product-pin` spec delta rides along only if the ruled shape needs
  new contract text.
- **If Q4's split is taken:** the same kind of realization change retargets
  only `generator.py`'s three imports, closing the Requirement 1 conflict
  for that one module alone. This does NOT by itself close requirement 9 for
  the repository: the other seven `DOC_HEALTH_SURFACE` modules' suites still
  fail collection standalone until they are ALSO resolved — either
  retargeted too (extending toward full (a)), or given the same (b)/(c)
  composition/CI treatment the first bullet describes for whatever is left.
  Q4's own recommended answer already bundles the split with (b)/(c) for the
  remaining seven; a proposal taking the split must carry that bundling
  through, not leave it implicit or deferred, and must not report
  requirement 9 closed on the split alone.

Requirement 9 closes for the repository only once every `DOC_HEALTH_SURFACE`
module has received one of these three treatments — (b)/(c) applied whole,
(a) applied whole, or Q4's split paired with (b)/(c) (or retargeting) for
what it does not retarget; it does NOT close from taking the split in
isolation, with the remaining seven modules' resolution left unscheduled.
Closing the Requirement 1 conflict this topic was raised to examine is a
separate question, decided module by module regardless of requirement 9's
status: the whole surface closes it under full (a); the retargeted slice
alone closes it under the split; every module left on (b) or (c) leaves it
exactly as open as before. The proposal must say, module by module, which is
which, and must not let requirement 9's closure — however it is achieved —
imply Requirement 1's.

Gated on: Brett Heap's ruling of Q1–Q3 (and optionally Q4), and
R1Q23's answer for timing. Deadline, as R1Q6 (d) and T008 name it: before
release 2's 12.5 needs its sixteen governed-flow suites to run, or sooner if
R1Q23 is answered (b).
