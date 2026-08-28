# Implementation Plan: the fifth finding class — unplaced-finding drift (F5)

**Branch**: `026-unplaced-finding-drift` | **Date**: 2026-08-27 |
**Spec**: [spec.md](./spec.md)

**Input**: Feature specification from
`/specs/026-unplaced-finding-drift/spec.md`

**Realizes**: `openspec/changes/add-unclassified-finding-class` — ONE ADDED
requirement in `doc-health`, "A modified-block-currency finding its own class
map cannot place is itself a finding". Ratified 2026-08-27 by Brett
("Amend now"); merged as PR #446, squash `86b7ca3f`, which is this branch's
base.

**Branch point**: `86b7ca3f4600f5771c48b2baeb2adf85f556fb82`, the packet's own
merge commit. `origin/main` advanced six commits during the feature, so the
branch took a catch-up MERGE (never a rebase) and its merge base at landing is
`22f15cdf341cac0ec89ed7e4e56f75ecaebc8585`. Both self-gate figures were re-taken
there and did not move.

## Summary

The modified-block-currency family's report block carries a fail-closed residual
row for findings its own class map cannot place. The row is prose: no severity,
no `--fail-on` reach, no ranked-plan reach. This feature makes a nonzero
residual emit work — ONE `warning` per DISTINCT unplaced rule shape per run,
naming the shape's count, quoting the first instance's rule text verbatim, and
carrying that instance's repository and delta path — and places that new finding
in a FIFTH class of the family's own registry so it is never counted by the
residual it reports. The residual row stays exactly as it is; the tally still
sums; the family stays advisory and stays out of `FAMILY_RESOLUTION`.

Predicted movement on this tree: **ZERO in every band**. The class map is
complete here, so the class reads `0` and the only visible change to a report is
one more row in the class block. That is the argument for landing it now: it
pins a state every reader currently assumes.

## Decisions taken by the orchestrator — FLAGGED FOR VETO

Each is independently reversible on a word. The three decisions of the RATIFIED
PACKET (D1 ADDED-only, D2 fifth `FindingClass` with an anchored pattern, D3 one
finding per distinct unplaced rule shape per run) are **not re-decided here** —
they are applied as ratified and remain flagged in the packet's own § 1.2. What
follows are decisions this FEATURE took, under the packet's standing patterns.

**O1 — THE PACKET'S `tasks.md` § 2 IS THE PLAN AT TASK GRAIN, AND THIS PLAN
MAPS 1:1 ONTO IT.** Every task in `tasks.md` cites the packet box it realizes
(2.1–2.15); nothing is added except what Speckit's own templates require
(setup, evidence, and the gate tasks). The packet was review-hardened before
ratification and re-deriving its shape would be re-deciding decisions Brett
already commissioned.

**O2 — RED-FIRST FOR EVERY BEHAVIOUR, AND THE LIVE-TRIGGER HONESTY NOTE GOES IN
THE TEST DOCSTRINGS AS WELL AS HERE.** No corpus-supplied title can produce an
unplaced rule text while the map is complete: every rule text this family
constructs is one of five fixed prefixes plus `{title!r}`, and `_TITLE_REPR`
admits every `repr` Python can emit. Measured at packet review (§ 3.5): 13
adversarial titles plus 4000 random ones over an alphabet of quotes,
backslashes, control characters and class phrases, times five rule shapes =
20,065 rule texts, **0 unplaceable**. So a crafted fixture title CANNOT exercise
the fifth class, and every behavioural test induces the drift the honest way —
by removing one entry from `_CLASS_PATTERNS`, which is precisely the live
condition "the map has drifted behind the arms". The family, the classifier, the
summary and the renderer all run unmodified under that seam. Stated in the
docstring of every test that uses it, so a later reader does not mistake the
monkeypatch for a convenience.

**O3 — THE FIFTH CLASS'S OPENING PHRASE IS `this family's own class map has no
pattern for `, DELIBERATELY NOT THE RESIDUAL ROW'S WORDING.** The residual line
already says "its own class map does not place". A drift rule text reusing that
phrase would make F3's fourth probe (§ 2.10) unable to tell the finding from the
row when it asserts the probe is the module's own wording — the positive control
would pass on the wrong constant. Two readings of one fact, two spellings.

**O4 — THE DRIFT FINDING QUOTES THE RULE TEXT PLAIN, NOT `repr`-WRAPPED.** The
delta says "verbatim". `{rule!r}` would escape quotes and backslashes, so the
quoted text would no longer be byte-equal to the rule it names and a test could
not assert `first.rule in drift.rule`. Plain inclusion after a colon at the end
of the rule text keeps "verbatim" literally true.

**O5 — THE NEW FIXTURE TREE IS *NOT* ADDED TO F2's `NEW_TREES`, AND CARRIES ITS
PROVENANCE README ANYWAY.** `NEW_TREES` means "the trees THIS feature (F2)
adds", and its provenance checker additionally requires each tree's README to
cite an F2 audit row (`audit row **A<n>**`) and a `add-modified-block-currency-check § 3.<n>`
section. This tree belongs to neither. Fabricating an audit row to satisfy a
checker would be exactly the false-documentation defect this family exists to
catch. The tree therefore joins `ALL_TREES` by glob (which is what makes it
behavioural), carries a README to F2's convention with `SYNTHESIZED` on line 3,
and this feature pins that README from its OWN test rather than by widening F2's
list. Recorded because the packet's § 2.8 names F2's checker as though it would
cover the tree, and it would not.

**O6 — MUTATION § 2.14(e) IS CAUGHT BY A SIMULATED-FLIP TEST OVER THE MODULE'S
OWN SOURCE, BECAUSE NO VALUE COMPARISON CAN CATCH IT TODAY.**
`_DRIFT_SEVERITY = WARNING` and `_DRIFT_SEVERITY = _LAUNCH_SEVERITY` are
value-identical until § 7.2 flips `_LAUNCH_SEVERITY` to `error`, so every
assertion about the constants' VALUES passes under both, and the existing
separately-assignable pin passes too (rebinding one module attribute never moves
another). The pin that does catch it executes the module's real source with
`_LAUNCH_SEVERITY = WARNING` textually replaced by `ERROR` and asserts the
scenario-title class moved while the drift class did not. That is the § 2.1
reasoning made falsifiable, and § 2.14(e) says the pin is owed here if it is
missing. It was.

**O7 — THE PACKET'S § 2.15 SAYS "the three `tests/doc-health/test_modified_block_currency*.py`
files"; FOUR MOVE.** `test_modified_block_currency.py` is named by § 2.12 for
its `:16` numeral, and O6's simulated-flip pin belongs beside the family's other
severity pins in that same file. Recorded as a mechanical inaccuracy in the
packet rather than a scope change: the four files are the four the packet
already names between § 2.6–2.12.

## Technical Context

**Language/Version**: Python 3 (stdlib only; the module imports `re` and
`pathlib` and nothing else).

**Primary Dependencies**: `scripts/doc_health/` — the package's own `Finding`,
`WARNING`, `INFO`, `SEVERITY_RANK`, and the family's existing readers. No new
dependency, no new import.

**Storage**: N/A — the family reads the checked-out tree and nothing else.

**Testing**: `pytest`, over `tests/doc-health/`. Baseline at the branch point:
**1215 passed** in ~27 minutes. The suite is slow, so targeted file runs carry
development and the full suite is run once at the gate.

**Target Platform**: the doc-health checker, run as `scripts/doc-health.py`
locally and by `.github/workflows/doc-health-reusable.yml` in the nightly
aggregation. **This feature edits no workflow file.**

**Project Type**: a validator/CLI library inside a governance repository.

**Performance Goals**: N/A. The emit is one grouping pass over a finding list
the family already holds in memory.

**Constraints**: additive only; the family stays advisory (`warning`/`info`,
absent from `FAMILY_RESOLUTION`); the class block stays not-a-finding; nothing
outside the named surface moves.

**Scale/Scope**: one module (~90 added lines), four test files, one new fixture
tree, one byte-level contract amended.

## Constitution Check

*GATE: passes before Phase 0, re-checked after Phase 1 design — see the
re-check at the end of this section.*

| Principle | Bearing | Verdict |
|---|---|---|
| **I. Contract-first, domain-neutral core** | `doc_health` is neutral tooling over the governance corpus; the fifth class names no domain vocabulary. | PASS |
| **II. OpenSpec before implementation** | `add-unclassified-finding-class` is RATIFIED (2026-08-27) with `code_surface: openxFactory`, and names this realization as ONE Speckit feature. This feature makes no `openspec/` edit; the packet's boxes tick at its archive act. | PASS |
| **III. Document lifecycle** | No governance document changes status. The one corpus document amended (`specs/022-…/contracts/report-section.md`) is a feature contract, amended so it stays true about the code it describes. | PASS |
| **IV. Schema and artifact discipline** | No YAML. The new fixture tree carries a README to F2's convention (O5). The action line carries a REPO-RELATIVE path (`scripts/doc_health/modified_block_currency.py`), never host-absolute. | PASS |
| **V. Validation gates (non-negotiable)** | `python3 -m pytest tests/doc-health` before/after; `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`; a single-repo doc-health run recorded as a before/after pair in `evidence/`; a mutation round over the packet's five mutants plus three reviewer-style extras. Behaviour is proved by tests, not asserted. | PASS |
| **VI. Versioned, content-addressed releases** | No contract bundle is cut: no file under `contracts/schemas/`, no manifest, no digest set, no tag. The proposal states this. | PASS — N/A |
| **VII. Fail-closed authority boundaries** | This feature IS a fail-closed strengthening: the classifier's residual, already fail-closed, gains a reachable remedy. The class registry stays closed and ordered; the new class is appended last; the pattern is anchored. | PASS |

**Constraint from § Repository Constraints**: this feature runs from its own
worktree (`../openxFactory-worktrees/026-unplaced-finding-drift`), never the
root checkout, and stages explicit pathspecs.

**Post-design re-check (after Phase 1)**: unchanged — all PASS. The design adds
no project, no pattern, and no dependency; the Complexity Tracking table below
is empty for that reason.

## Project Structure

### Documentation (this feature)

```text
specs/026-unplaced-finding-drift/
├── plan.md              # this file
├── spec.md              # the feature specification
├── research.md          # Phase 0 — the seven questions this design turned on
├── data-model.md        # Phase 1 — the class, the shape, the finding
├── quickstart.md        # Phase 1 — how to see it work, and how to see it not fire
├── contracts/
│   └── drift-finding.md # Phase 1 — byte-level: the class row, the rule text, the pattern
├── checklists/
│   └── requirements.md  # the spec-quality checklist
├── evidence/            # before/after self-gate, test counts, mutation log, scope diff
└── tasks.md             # Phase 2 — /speckit-tasks output
```

### Source (repository root)

```text
scripts/doc_health/
└── modified_block_currency.py      # the ONLY production file this feature edits

tests/doc-health/
├── test_modified_block_currency.py            # § 2.12 numeral; O6's simulated-flip pin
├── test_modified_block_currency_reporting.py  # the delta's six scenarios; six pins move
├── test_modified_block_currency_self_gate.py  # § 2.10 fourth probe + positive control
├── test_modified_block_currency_fixtures.py   # § 2.11 FR-023 snapshot; § 2.12 numeral
└── fixtures/modified-block-currency-unplaced/ # NEW — the behavioural tree (§ 2.8)

specs/022-modified-block-currency-reporting/
└── contracts/report-section.md     # AMENDED at its four enumeration sites (§ 2.9)
```

**Structure Decision**: no new module, no new package, no new test file. The
fifth class lives beside the four in the module that owns them, and its tests
live beside the tests of the report block they extend — which is the only place
the six standing pins that move can be moved by name.

## Phase 0 — research

`research.md` records the seven questions this design turned on and what settled
each: the rule-text grammar and why it must not reuse the residual's wording
(R1); why the anchor is load-bearing when `re.match` already anchors (R2); the
shape mask and its ordering (R3); where the emit sits in the family and why it
sorts twice (R4); why the monkeypatched pass cannot index `by_id` with
`UNCLASSIFIED` (R5); why the new tree is not an F2 tree (R6); and how the
reserved severity flip is made falsifiable (R7).

## Phase 1 — design and contracts

- `data-model.md` — the fifth `FindingClass`, the two new module constants, the
  shape function, and the drift `Finding`'s five fields, each with the FR it
  answers.
- `contracts/drift-finding.md` — byte-level, in F4's own idiom: the class-block
  row, the rule-text template, the anchored pattern, the action line, and the
  state table (placed / drifted / two shapes / quiet / skipped).
- `quickstart.md` — the two runs a reviewer takes: the family over this tree
  (the class reads 0, no residual row) and the family under an induced drift
  (one `warning` in the ranked plan, the residual counting the arms' unplaced
  findings only).

## Implementation order (and why it is forced)

1. **The fixture tree first.** It is inert until the class exists — over the
   unmodified map it contributes only PLACED findings — so it can land before
   any RED test and it makes the RED tests possible to write against measured
   findings rather than constructed ones.
2. **The RED tests next, all of them, before the module moves.** The delta's six
   scenarios plus the anchor's red case plus the double-match pin. Each is run
   and seen to fail for the stated reason; the reasons are recorded in
   `evidence/red-log.md`.
3. **Then the module**, in the order the constants require: `_DRIFT_SEVERITY`
   and `_DRIFT_ACTION` → the fifth `FindingClass` → the anchored pattern → the
   shape function → the emit in `fam_modified_block_currency`. The class cannot
   be constructed before its constants and cannot be placed before its pattern.
4. **Then the six standing pins that red**, moved BY NAME (§ 2.7) rather than by
   re-running until green — a pin moved by iteration is a pin nobody read.
5. **Then the self-gate probe, the FR-023 snapshot and the numeral sweep**,
   which are corrections rather than behaviour and must not be mixed into the
   RED/GREEN cycle above.
6. **Then the contract amendment**, last of the writing, because it describes
   what the code now does and copying a prediction into a byte-level contract is
   how a contract becomes false.
7. **Then the gates and the mutation round.**

## Risks, and what each one is caught by

| Risk | Caught by |
|---|---|
| The drift finding is itself unplaced, so the count names itself | `test_the_drift_finding_is_placed_in_the_fifth_class_and_not_by_the_residual`; mutation (a) |
| The emit fires on a clean run | The delta's scenario-1 test over every fixture tree and the real tree; mutation (b) |
| Two shapes collapse to one finding, or one shape splits into two | The scenario-3 test in both directions; mutation (c) |
| A quoted arm-shaped rule text misfiles the drift finding | The anchor's red case; mutation (d) |
| A corpus title embedding the drift phrase double-matches | `test_a_title_that_embeds_the_drift_phrase_still_matches_exactly_one_pattern` — the same construction F4 used for the arms |
| The reserved § 7.2 flip silently drags the new class | O6's simulated-flip pin; mutation (e) |
| The class label reddens the standing `unclassified`-absence pin | The label carries no such substring; the reviewer-style mutation that inserts it must red |
| The new fixture tree breaks F2's unanchored `CLASSIFIERS` partition | Plain requirement titles, and F2's own `test_every_finding_falls_into_exactly_one_class` over `ALL_TREES` |
| The block stops being not-a-finding | The existing `parse_previous` equality pin, whose SUBJECT must not weaken by one assertion |
| Something outside the surface moves | The scope diff (§ 2.15), run mechanically and recorded |

## What this feature must NOT do

- Touch `.github/` or `openspec/`. `git diff --stat <merge-base> -- .github/ openspec/` MUST be empty.
- Touch any other family, `report.py`, `families.py`, `Finding`, `FAMILY_RESOLUTION`, `FAMILY_SUMMARIES`, or any threshold.
- Reword, move or condition the residual row.
- Add a public callable to the module.
- Advance, block, or fold itself into the reserved § 7.2 flip.
- Re-decide D1, D2 or D3.

## Complexity Tracking

No Constitution Check violation. The table is deliberately empty.

## Clarify gate — assessed, not opened

No clarification round was run and no questions file was written. Every question
this feature could have asked at Brett grain is answered by the ratified
packet's § 2, and the three design decisions that remain genuinely open are
flagged in the PACKET's § 1.2, not here. The four decisions this feature took on
its own (O3–O6, plus the O5/O7 packet corrections) are recorded above for veto
rather than asked, because each is a one-file change if reversed and none
changes what ships.

## O8 — the six-rule-shapes rename (added by the analyze pass)

`test_each_of_the_five_rule_shapes_classifies_into_its_own_class` is renamed to
`test_each_of_the_six_rule_shapes_classifies_into_its_own_class`. The packet's
§ 2.7 cites the `def` line and says "five shapes and four classes become six and
five"; leaving the count in the FUNCTION NAME would be a numeral stating a count
the code contradicts, which is exactly what § 2.12 sweeps out of the prose. The
drift emit really is a SIXTH constructed rule text: the arms build five fixed
prefixes and this builds a sixth. Flagged for veto like the rest.

## Analyze residue

`/speckit-analyze` ran after tasks generation. **No CRITICAL findings.** Six
findings, all dispositioned in place rather than deferred:

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| C1 | MEDIUM | FR-018 ("adds no deterministic check family") was covered only by an existing untouched pin and the scope diff, and named by no task | T044 now names `test_the_reporting_list_mirrors_the_registry`'s `len(FAMILY_IDS) == 22` in its evidence |
| C2 | MEDIUM | The new fixture tree sits outside F2's only band sweep, which iterates `NEW_TREES` — and it deliberately does not join `NEW_TREES` (§ O5) | T037 now also sweeps the new tree's bands, non-empty first |
| F1 | MEDIUM | Phase 7 is numbered before Phase 8 but runs after it | Kept the story-priority numbering (Speckit's own rule) and added an ordering note at Phase 7's head; the Dependencies block already carried the real order |
| F2 | MEDIUM | The brief says "seven named F4 pins"; the packet's § 2.7 roster is SIX (all in `..._reporting.py`) and § 3.6 adds two more sites for EIGHT | Reported, no artifact change. All eight are tasked: T029–T034 (§ 2.7's six), T035 (self-gate), T036 (FR-023 snapshot) |
| U1 | MEDIUM | The packet moves the five-rule-shapes pin to six without saying the function NAME must move | Recorded as O8 above and written into T030 |
| D1 | LOW | Constitution Principle V names `scripts/validate-*.py`; this repository has none (its validators are `check-*.py` and `doc-health.py`) | N/A — the affected validator IS `scripts/doc-health.py` and its suite, run by T038 and T039. Recorded so a later reader does not read the absence as a skipped gate |

**Coverage**: 24/24 functional requirements and 7/7 success criteria have at
least one task. No unmapped task: every one cites a packet box or a constitution
gate.

## RULED AND IMPLEMENTED — OPEN-1, closed 2026-08-28

### OPEN-1 — shape identity is the ARM TEMPLATE, all interpolations masked

**Status: RULED by Brett 2026-08-28, verbatim: "Amend: shape = arm template,
all interpolations masked". Implemented in this feature on top of `8841a8ab`.**
The delta amendment itself is a parallel branch,
`change/amend-unplaced-shape-rule`; this feature's spec cites the amended text,
so the PR waits on that landing.

**What was found.** The delta as first ratified defined shape identity as "rule
texts equal after every single-quoted span, every double-quoted span and every
run of digits has been replaced by a fixed placeholder". A rule text's UNQUOTED
parts were therefore shape-bearing, and this family's arms interpolate several:
the promoted spec's repo-relative path, the `[body]`/`[bullet]` unit-kind list,
a change-id list, an unresolved block's `why` clause.

**Measured, before and after, with the pattern dropped named for each row** (a
drop of a DIFFERENT pattern exercises a different arm, so the figures are not
comparable without it):

| tree | pattern dropped | unplaced | shapes — was | now |
|---|---|---|---|---|
| this repository | `carriage-ledger` | 7 | **6** | **1** |
| `-two-writers` | `title-resolution` | 9 | 4 | **1** |
| `-markers` | `carriage-ledger` | 3 | 3 | **1** |
| `-unplaced` (this feature's) | `carriage-ledger` | 3 | 1 | **1** |

SIX findings on the real tree where ONE new map entry would place all seven —
now one. The fixture rows read 1 both before and after where their findings
happened to share every unquoted field, which is precisely why the grain had to
be measured against the REAL tree and not against a fixture built for it.

**The amended rule.** Two rule texts are ONE SHAPE where they come from the SAME
ARM TEMPLATE, whatever their interpolated values. One shape is one template, one
template is one map entry to write, and the count of drift findings is the count
of REMEDIES.

**THE MECHANISM — derived from the templates, never guessed lexically.** Each
arm's rule text now renders through one registered `_ArmTemplate`, so the fixed
prose has exactly one definition and the arm that prints it cannot drift from
the mask that reads it. `_shape` then works in two steps whose ORDER is
load-bearing: first every `repr`-emitted span is masked by a left-to-right
consumer (a quote opens a span only at the start or after a non-alphanumeric,
which is what keeps the prose apostrophe in `sibling's` from being an opener and
what keeps a corpus-supplied title from carrying another arm's phrase into the
match); then the masked text is matched against the registered templates, first
match wins, and the shape IS the template's id. A text no template claims falls
back to the old lexical mask rather than being merged into a neighbouring
template — fail-closed, constitution VII.

**NO FIELD WAS ADDED TO `Finding`.** The report grammar is shared by
twenty-two families and the semantic lanes; a field added for one family's local
identity would be a change to that grammar for a local need, which is the same
argument `classify` already makes for reading off the rule text.

**What holds it.** `test_the_drift_grain_is_one_finding_per_arm_template`
(the four figures, measured against an independently written mask and an
independently typed set of template probes);
`test_every_finding_matches_exactly_one_arm_template` (the templates are
mutually exclusive over masked text, over every fixture tree and the real
corpus, asserted at TEMPLATE level rather than through `_shape`'s single
return); `test_the_arm_templates_are_the_only_place_the_prose_lives` (no arm
builds a rule text inline again);
`test_two_findings_of_one_template_differing_in_an_unquoted_field_are_one_shape`
and `test_two_findings_of_different_templates_are_two_shapes` (the amended
scenario 3, both halves);
`test_a_rule_text_no_template_claims_falls_back_and_is_never_merged` (the
fail-closed fallback); and mutant `T1`, which reverts `_shape` to the
quoted-spans-only mask and must red the grain test.

**Predicted movement, unchanged: ZERO.** The amendment changes how unplaced
findings GROUP, and there are none on any tree where the map is complete — which
is every run today. The self-gate diff is still exactly one line.
