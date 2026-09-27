# Analyze, round 3 (T067)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../spec.md) · **Task**: T067
([`tasks.md`](../tasks.md)) · **Run**: 2026-09-27, over T067's encoding on
`main` at `468863d1` (#1176) · **Lane**: `openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`).

## Verdict

**CRITICAL: 0.** No finding breaks a MUST of the constitution or leaves a
requirement without a task.

Brett Heap answered round 2's two new questions on `#656`, comment
`5851950767` (2026-09-27T02:25:29Z), verbatim *"(a) Admit the two edits
(Recommended)"* for R1Q26 and *"(a) Own three, others by tree
(Recommended)"* for R1Q27. Round 2's second analyze pass then found a route
R1Q26 had not listed (W2-10, in `evidence/analyze-round-2.md`). It was put to
him, and he kept (a), on comment `5852513402` (2026-09-27T04:08:46Z),
verbatim *"Keep (a) as ruled (Recommended)"*. T067 encodes the answers. With
them, all 27 questions are answered, no task carries a `Blocked by:` line,
and the constitution's workflow gate, *"material ambiguities MUST be resolved
before planning"*, holds for the whole plan without a deviation. The held
tasks' row leaves plan.md § Complexity Tracking.

The author's pass found 1 HIGH, 2 MEDIUM and 6 LOW (U3-1 to U3-9). An
independent verifier then ran the analysis again over the encoding commit,
`a28e6af9`. It found CRITICAL 0, HIGH 0, MEDIUM 0 and LOW 1 (W3-1): one of the
author's dispositions was carried only in part. Copilot's review of the same
commit raised one more (CP3-1), about this note's own state. This PR
dispositions all eleven, in § "Findings, and what this revision does with
each" and § "The verifier's pass".

## What T067 encodes

- **R1Q26 (a).** T007's batch I amends 5.3a to admit the facet's `values`
  block, and 12.5's falsifier to admit two edits to
  `tests/test_gate_loop_views.py`, each entered in the reviewed allow-list with
  its reason. T060 makes the first, to the facet-declaration test, and T059
  the second, to the overlay test at the phase-2 pin. T066 composes `values`
  into openxFactory's profile and updates its facet test, in its both-pins
  form.
- **R1Q27 (a).** The consumer's validator validates its own three kinds from
  its installed distribution wherever it runs, and the other kinds only where
  the tree it runs from supplies their schemas, its own `contracts/schemas/`
  read first. openxFactory's farm supplies the whole family, so it keeps
  validating all ten, and no contract row changes. F7.1's second test reads
  *"every schema this install validates is on disk"* (batch I; T061, T063).
- **T066**, re-planned. It moves none of openxFactory's validator callers,
  because under R1Q27 (a) nothing they validate is given up in openxFactory's
  farm. Round 2's question of how each kind would be dispatched (V2-12) no
  longer arises. T066 keeps the seal test's revision under R1Q14 (a), and it
  gains the facet composition under R1Q26 (a).
- **The holds lift.** T059, T060, T061, T066, T067 and T007's batch I lose
  their `Blocked by:` lines. T059, T060, T061, T063, T064 and T066 gain
  `Ruled:` lines, and the two question headers list them (`qcheck.py`).
- **Batch I** has three rows in tasks.md § "Ruled amendments": 5.3a, 12.5's
  falsifier, and 7.3 with F7.1. It lands before T059, T060, T061 and T063.
- **T091's trailer finding.** F5.2, F11.1 and 12.5's falsifier select the
  arc's landings with `git log --first-parent
  --grep='^Arc: neutral-product-standalone-operability$'`, which matches that
  line anywhere in a message. So the seven openDox-code landings whose squash
  body carries it count as written. openDox-code#37 (`e295b1a9`, T020) and
  #44 (`9d13bd16`, T021) carry none, and T091's record at the arc's close
  names both. No falsifier changes, and no `main` is rewritten. This is the
  disposition of the finding the holder raised about how F11.1 and T091 find
  the arc's landings.

## How it was run

**What was analyzed.** T067's encoding commit, on `main` at `468863d1`, which
is #1176 squash-merged. The analysis read `spec.md`, `plan.md` and
`tasks.md`, with `clarify-questions.md`, `quickstart.md`, `research.md`, the
checklist and the round-2 record as context. The authority is #1144 at
`468863d1`, with batches A (#1171) and D (#1170) landed. The constitution is
`.specify/memory/constitution.md`, version 1.0.0.

**The feature context.** The check was run in the lane's clone, with the
feature named in the environment. `<clone>` stands for the clone's root:

    $ SPECIFY_FEATURE_DIRECTORY=specs/034-opendox-standalone-operation bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
    {"FEATURE_DIR":"<clone>/specs/034-opendox-standalone-operation","AVAILABLE_DOCS":["research.md","quickstart.md","tasks.md"]}
    (exit 0)

It writes `.specify/feature.json`, which is gitignored (`.gitignore:17`). The
optional `before_analyze` and `after_analyze` hooks offer an automatic git
commit, and they were not run, because this feature commits by hand, with
pathspecs.

**How the encoding was made.** Scripted edits, each refusing unless its old
text occurs exactly once, were applied to #1176's head `d4a314f1` and then
carried onto `468863d1`, whose feature files are the same. They are
persisted beside the lane's plan tools in `opensoft/brett-wip`, so neither
this PR nor batch I's depends on scratch space.

**Measurements made for this round.** Each was run in a scratch clone or a
measurement tree, and none touches a shared tree.
- **The arc's openDox-code landings.** Since `ARC_BASE` (`1e4a57fb`), on
  openDox-code's `main`, `git log --first-parent
  --grep='^Arc: neutral-product-standalone-operability$'` selects eight of ten
  first-parent landings: #38, #39, #40, #41, #42, #43, #46 and #47.
  `git interpret-trailers --parse` finds the line in the trailer block of #42
  alone (`19370adc`, landed 03:20:45Z, after the kit's fix). #37 and #44 carry
  no `Arc:` line in the message, and their PR bodies have none either
  (`gh pr view … --json body`).
- **The grep reads the body.** With git 2.43, in a scratch repository, a
  commit whose `Arc:` line sits in the body, above a non-trailer paragraph, is
  selected by that grep, and `git interpret-trailers --parse` does not list
  the line.
- **#1144's boxes.** `box_census.py` over #1144's `tasks.md` at `468863d1`
  prints `total 124`: 104 `[ ]`, 11 `[x]` and 9 `[~]`, as at round 2.

## Findings, and what this revision does with each

Severity follows the skill: CRITICAL breaks a constitution MUST or leaves a
requirement uncovered. HIGH is a conflict with the authority or inside the
plan, or an acceptance criterion that cannot be tested. MEDIUM is drift, a
missing step or an underspecified case. LOW is wording.

### The author's pass

| ID | sev | finding | disposition |
|---|---|---|---|
| U3-9 | HIGH | Three lines still had T066 send openDox's kinds to openDox's validator, though T066 now moves no caller: T061's list of where the other seven kinds are validated, R1Q14's answer in spec.md § Clarifications, and R1Q14's ANSWER line in `clarify-questions.md`. A writer reading T061 would have moved callers that T066 leaves alone. | All three now say that openxFactory's callers run the validator in openxFactory's farm, which supplies the whole family, and that T066 moves neither (R1Q27 (a)). R1Q14's ANSWER line says that T067 re-planned it, so the change to what Brett ruled is nil: 7.3 still governs. |
| U3-4 | MEDIUM | Under R1Q26 (a), two slices edit `tests/test_gate_loop_views.py`, P2-X (T060) and P2-K (T059), but plan.md's single-writer table did not list it. | Added, T060 → T059. The persisted `chaincheck.py` and `chaindirect.py` carry the fourteenth chain, and its one pair is DIRECT: T059's `After:` line names T060. |
| U3-6 | MEDIUM | T019's rule for who creates the reviewed allow-list named T043, or else T061. Under R1Q26 (a), T060's entered edit lands before T061's. | T019's bullet now says that T060 creates the file if T043 has not. T060 already said so. |
| U3-1 | LOW | T061's R1Q27 (a) paragraph had a line broken mid-sentence. | Reflowed. |
| U3-2 | LOW | § Dependencies' batch bullet had a line broken mid-sentence. | Reflowed. |
| U3-3 | LOW | quickstart.md's answers sentence had a line broken mid-sentence. | Reflowed. |
| U3-5 | LOW | Batch G's bullet and R1Q11's ANSWER line said that R1Q26 *"decides"* how the block lands, though it is answered. | *"R1Q26 (a) decided"*. |
| U3-7 | LOW | `clarify-questions.md`'s phase table said that batch I lands before T059, T060 and T061. tasks.md also names T063. | T063 is added. |
| U3-8 | LOW | T091's account of the kit's fix gave no landing made since it. | It names openDox-code#42 (`19370adc`, T016), which carries its `Arc:` line in the trailer block. |

## The verifier's pass

**How it was run.** An independent Sonnet verifier ran `/speckit-analyze`
again, read-only, over a clone of `a28e6af9`, with #1144, the constitution,
the measurement trees and a clone of openDox-code as this note names them. It
read the two ruling comments verbatim through the API and re-ran the plan
tools from the feature directory. It ran the full prerequisite check in a
scratch clone of its own, where it exited 0 with the JSON above, and it did
not run the optional hooks. Its trees showed no change afterwards (`git status
--porcelain --ignored`).

**What it found.** CRITICAL 0, HIGH 0, MEDIUM 0 and LOW 1. Of the author's
nine dispositions, eight were carried in full, and U3-3 only in part (W3-1).

| ID | sev | finding | disposition |
|---|---|---|---|
| W3-1 | LOW | U3-3's reflow of quickstart.md's answers paragraph left one line of 94 characters, *"datastore's stop, … Use whatever the openDox"*, in a paragraph of 64 to 78. The meaning was unaffected. | The paragraph is rewrapped. |
| CP3-1 | — | Copilot's review of `a28e6af9` (thread `4114067826`): this note carried `Status: record` while its verifier's pass was still to come. | This section records the pass, and the verdict counts it. |

**What it confirmed**, each with its command:
- The ANSWER lines of R1Q26 and R1Q27 match comments `5851950767` and
  `5852513402` word for word. Batch I's three rows and plan.md's round-3 rows
  state only option (a)'s consequences. U3-9's change to R1Q14's ANSWER line
  leaves what Brett ruled as it was, (a) on `5850003126`, and corrects only
  the plan's own account of T066.
- No task carries a `Blocked by:` line. The one left is the field's
  definition in § Format. Every `(governs …)` header matches the `Ruled:`
  lines (`qcheck.py`).
- T066's re-plan holds against the sources, and no other line of the
  feature says that T066 moves a caller:
  - `delegated_semantic_validation` calls `_composed_validator` for every
    kind, and that links the whole family's schemas into its farm;
  - `find_openxfactory_validator` returns one script, run in the same farm;
  - the consumer's validator reads *"this tree's own `contracts/`"* first
    (`:119-121`, at `e28930bf`), and `SCHEMA_FILENAMES` still lists the ten
    there.
- The two entered edits are to `tests/test_gate_loop_views.py:1644`, which
  asserts `DISPLAY == {"stages": …}`, and `:1723`, which asserts exactly five
  changed leaves. 12.5's ratified falsifier refuses any arc edit, and batches
  C and I amend it. T019, T043, T060 and T061 state the allow-list's owner
  the same way.
- T091's trailer account matches openDox-code's history landing by landing,
  and #42's landing time, 03:20:45Z. F5.2 and 12.5 run their grep in
  openXdox-code, and F11.1 runs it in openxFactory, so no falsifier reads
  openDox-code's landings.
- The tools give the figures in § "The checks after the dispositions", and
  this note's counts, metrics and coverage table hold: 90 tasks, eight ids
  unused, nine done, 19 requirements, and `total 124` from `box_census.py`.

## Coverage

| key | tasks | note |
|---|---|---|
| FR-001 | T010, T011, T030, T031, T032, T036, T045, T049 | |
| FR-002 | T001, T015, T016, T017, T049 | requirement 3 as #1170 amended it |
| FR-003 | T012, T020–T022, T025–T027, T046, T055, T084–T086, T089 | |
| FR-004 | T050, T052–T056, T059, T060, T061, T063 | T060 and T059 make R1Q26 (a)'s two entered edits |
| FR-005 | T051, T053, T057, T058, T061, T063 | T061 reads R1Q27 (a); T066 keeps openxFactory at both pins |
| FR-006 | T034–T037, T040–T044, T049, T061, T086, T090 | T061 clears `tests/test_snapshot.py`'s entry |
| FR-007 | T038, T075–T077 | |
| FR-008 | T070–T074 | |
| FR-009 | T034, T078–T083, T085 | |
| FR-010 | T017, T018, T045, T065, T091–T093, T098 | |
| FR-011 | T095, T096 (T088 is its precondition) | |
| FR-012 | T002, T009, T019, T067, T069 | no task carries a `Blocked by:` line |
| SC-001–SC-007 | T049, T063, T089, T095 and T096, T018, T065 and T098, T097, T047, T064, T066 and T094 | |

All 69 release-1 boxes still map to a task. T067 closes none of the boxes: it
is a process task, as T009, T019 and T069 are.

## Constitution alignment

No finding breaks a MUST at this revision.
- **The workflow gate** holds for the whole plan. All 27 questions are
  answered, and no task is planned before the answer it turns on. The
  Complexity Tracking row that kept four held tasks in the plan is gone.
- **Principle II.** R1Q27 (a) changes no contract row, so nothing here needs
  an OpenSpec change. Batch I's three lines are #1144 amendments made on
  Brett's word, as bookkeeping under a Rule 6 window (T007).
- **I, III–VII.** No committed host-absolute path, and no credential. This
  note carries `Status: record` and is linked from the README entry (IV). The
  PR adds no `openspec/` path, so `openspec validate --all --strict` is
  `main`'s. The plan readings of T070 and T080 still fail closed (VII), as
  round 2 recorded.

## Metrics

| metric | value |
|---|---|
| requirements | 19 (12 FR, 7 SC) |
| tasks | 90, T001–T098 with eight ids unused; nine done (T001, T003–T006, T009, T019, T067, T069) |
| coverage | 19 of 19 |
| questions | 27, all answered: 11 on `5817152735`, 14 on `5850003126` and 2 on `5851950767`, with R1Q26 (a) kept on `5852513402`; RN-1 ruled (a) and landed |
| held tasks | none |
| findings, author's pass | CRITICAL 0, HIGH 1, MEDIUM 2, LOW 6 (U3-1 to U3-9) |
| findings, verifier's pass | CRITICAL 0, HIGH 0, MEDIUM 0, LOW 1 (W3-1) |
| findings, Copilot's review of `a28e6af9` | 1 (CP3-1) |

## The checks after the dispositions

Run from `specs/034-opendox-standalone-operation/` with the persisted tools,
twice, with the same output:

| check | result |
|---|---|
| `qcheck.py` over `qmap.py` (R1Q1–R1Q27) | `headers checked: 27 of 27; mismatches: 0`. R1Q26 and R1Q27 are `ANSWERED (a)`, and their headers name T007, T059, T060, T064, T066 and T067, and T007, T061, T063, T064, T066 and T067 |
| `depcheck.py` | `tasks: 90 nodes: 99`, `edges: 217`; `cycles: none`, and `none` with the Lands-with groups merged |
| `arrowcheck.py` | `arrow mismatches: 0`, `arrows checked: 67`. The held arrow line left plan.md's graph |
| `phasecover.py` | phase 1 32 tasks, phase 2 17 and phase 3 23, each before its checkpoint; T048 after T049, by design |
| `chaincheck.py` | `single-writer chain gaps: 0`, over fourteen chains |
| `chaindirect.py` | 42 pairs, 26 DIRECT and 16 transitive, each through a printed path |
| `sharedfiles.py` | 54 shared pairs, 4 NOT ORDERED: the same four phase-1 pairs as round 2. P2-X and P2-K share `tests/test_gate_loop_views.py`, ordered |

## Next

- **This PR** lands on Brett Heap's word as the holder relays it, *"Yes, land
  when green"*.
- **T007's batch I** follows it, in its own bookkeeping PR under a Rule 6
  window: the three rows above, written into #1144's `tasks.md`. Batch F's
  PR goes in beside it.
