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
   are `doc_health.corpus.RealGit` and `doc_health.lines.split_keepends` —
   read on their names alone, a git-repository wrapper and a text-splitting
   helper, not a check family, a disposition reader or a classifier. This is
   an OBSERVATION, not an audited claim: it is offered as a possible seam
   (open question 4 below), not a conclusion, because the other seven modules
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

This topic's own subject is a currently-tolerated conflict with a ratified
spec: openXdox-code's eight `doc_health` imports stand against
`corpus-adapter-seam`'s Requirement 1 today, held open only by R1Q6 (d)'s
named, counted, release-1-scoped exception (`#656` comment `5817152735`). That
is not a new conflict this topic creates; it is the conflict this topic exists
to close. No other staged topic or ratified spec is known to contradict the
material above.

## Open questions

1. **(R1Q6's option (a)) Pinned dependency — does NOT by itself conform.**
   openXdox-code gains `doc_health` as a declared, pinned, installable
   dependency (needs openxFactory to package it: a `pyproject.toml` for
   `scripts/doc_health/`, or a dedicated distribution). On its own this does
   NOT resolve the stated seam violation: openXdox-code would still be a
   neutral product importing `openxFactory`'s own tooling, merely through a
   proper pin instead of an ad-hoc `PYTHONPATH` reach, and it makes the
   openxFactory ↔ openXdox pin explicitly TWO-WAY (openxFactory already pins
   openXdox; openXdox would then pin openxFactory's tooling too) — the
   opposite of Requirement 1's one-way rule. As stated, this cannot be the
   exit option by itself; either (i) `doc_health` (or the slice openXdox-code
   needs) first moves to a genuinely neutral, separately-versioned home, so
   openXdox-code pins a THIRD PARTY rather than "openxFactory's own tooling"
   — at which point this option becomes a realization detail of open
   question 4, not a standalone answer — or (ii) it is adopted explicitly as
   a labelled, time-boxed WORKAROUND under its own `corpus-adapter-seam`
   exception, rather than as something that lifts R1Q6 (d)'s exclusion by
   itself. `corpus-adapter-seam` already requires that any two mutually
   importing packages relocate their shared type into a module both depend
   on BEFORE either is extracted — the same discipline (i) would need,
   applied to whatever `doc_health` surface openXdox-code actually needs.
2. **(R1Q6's option (b)) Declared integration tests.** The `doc_health`-dependent
   openXdox-code tests become declared integration tests that live where the
   composition is declared — openxFactory — per requirement 9's own admitted
   exception for tests that need two repositories. Needs R1Q2's declared
   composition-test surface widened to admit them (the same surface plan 034's
   T007 batch A / batch E already grows for the `openxdox_host` composition
   tests).
3. **(R1Q6's option (c)) Composed CI, no shared package.** openXdox-code's own
   CI composes an openxFactory checkout at a declared, pinned commit (checked
   out beside it — the shape `pytest-suite` already uses for the root
   pins), reading requirement 9's "no sibling" as "no sibling OF ITS OWN
   PROJECT" rather than "no sibling repository at all." R1Q6's own
   recommendation named this option, or (d), as the two live candidates for
   release 1; (d) (the declared exclusion) was ruled instead, precisely so
   this direction question could be taken slower and separately.
4. **A narrower seam: split the surface instead of choosing one shape for all
   eight modules.** Claim 5 above observes that at least `generator.py`'s
   three `doc_health` imports read as generic git/text utilities rather than
   governance logic. Is part of `DOC_HEALTH_SURFACE` better served by
   extracting a small neutral utility module (own home, own pin, trivial
   distribution) while the genuinely governance-specific reaches (in
   `cli_gate`, `completeness`, `corpus_root`, `gate_console`, `gate_routes`,
   `round_trip`, `snapshot_registry`) take option (b) or (c) instead? This
   needs the other seven modules' imports audited the way claim 5 only
   sketches for `generator.py`.
5. **Timing: does this arc have to move into release 1?** R1Q23 (open, phase
   2) asks whether F5.2 (phase 2, four of 5.4a's six generator suites) forces
   this arc's decision and realization ahead of its named deadline (12.5,
   release 2). If R1Q23 is answered (b) ("bring the direction arc forward"),
   this topic's exit gate tightens to phase 2's close rather than 12.5.
6. **Who owns realization once the direction is ruled?** Plan 034 names no
   task for the fix itself — T008 raises the arc; it does not schedule the
   work. The exit proposal below should either carry its own task list or
   name the plan/lane that will.

## Exit path

A proposal once open questions 1–3 are ruled (which of (a)/(b)/(c), or a
split per open question 4) and open question 5's timing is settled (does
R1Q23 pull this ahead of phase 2's close). Most likely shape: a realization-only
change against openXdox-code (and openDox-code, if the chosen seam borrows the
registered-adapter pattern already used for `corpus_adapter` /
`domain_profile` there) that retargets `DOC_HEALTH_SURFACE`'s eight modules,
with a `corpus-adapter-seam` or `neutral-product-pin` spec delta only if the
ruled option needs new contract text. Closing this arc lifts R1Q6 (d)'s
declared exclusion and lets `add-neutral-product-standalone-operability`
report requirement 9 closed for openXdox-code rather than as an open
extraction.

Gated on: Brett Heap's ruling of open questions 1–3 (and optionally 4), and
R1Q23's answer for timing. Deadline, as R1Q6 (d) and T008 name it: before
release 2's 12.5 needs its sixteen governed-flow suites to run, or sooner if
R1Q23 is answered (b).
