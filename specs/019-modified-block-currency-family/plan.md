# Implementation Plan: F1 — the modified-block-currency family module and its registrations

**Branch**: `019-modified-block-currency-family` | **Date**: 2026-08-27 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/019-modified-block-currency-family/spec.md`

**Realizes**: `openspec/changes/add-modified-block-currency-check` § 2
(tasks 2.1–2.10), the first of four Speckit features. Ratified 2026-08-27 by
Brett ("Ratify as-is").

## Summary

Build the twenty-second deterministic doc-health family: a module that reads
every ACTIVE change's `## MODIFIED Requirements` blocks against the promoted
requirement they replace, and reports what they do not carry — three arms, one
document pair, at authoring time, on the delta's own path. Register it in
`FAMILIES` and `FAMILY_IDS` in the SAME COMMIT as the `## MODIFIED
Requirements` block it owes on `doc-health`'s own "Deterministic check
families" requirement, because either half alone is a red gate — and land that
commit only AFTER `add-family-enumeration-check` has archived, because
registering while it is active reds a gate on THAT packet's path instead (see
§ Sequencing gate; measured, and it makes the packet's § 2.1 unimplementable as
written). **Phases 1–7 of `tasks.md` are unaffected and proceed now.**

Technical approach: one new module beside its twenty-one siblings, following
`promotion_fidelity.py`'s shape (module docstring that argues its own
existence, one `FAMILY` constant, named launch-severity constants, a
`fam_*(ctx)` entry point returning `list[Finding] | Skip`). Every reader that
already exists is imported rather than re-spelled — `parse_delta`, `norm`,
`load_dispositions`, `disposed`, `declared_standing`, `duplicate_packet._mention`
— and exactly one new reader is written, for the promoted side, because
`parse_promoted` returns scenario titles and this family needs bodies and
bullets. The unit derivation, the matching rule and the marker grammar are
NORMATIVE in the ratified delta and are transcribed, not designed; the
contracts in `contracts/` are that transcription at function grain. Every
behaviour ships behind a test that failed first.

## Technical Context

**Language/Version**: Python 3.11 (the package's floor: `from __future__ import
annotations`, `X | None` annotations, `frozenset`/dataclass idioms already in
use)

**Primary Dependencies**: standard library only (`re`, `pathlib`,
`dataclasses`) plus the package's own siblings; `PyYAML` is reached ONLY through
`promotion_fidelity.load_dispositions`, which already imports it defensively

**Storage**: none. Two documents are read per comparison; nothing is written

**Testing**: `pytest`, via `tests/doc-health/conftest.py` (`make_ctx`,
`FakeGit`, `FIXTURES`, `REPO_ROOT`) and fixture repo trees under
`tests/doc-health/fixtures/modified-block-currency*/`

**Target Platform**: the doc-health deterministic pass — a CLI
(`scripts/doc-health.py`) run locally, in the PR gate, and in the nightly
aggregation sweep

**Project Type**: single project; a check family inside an existing Python
package with a closed registry

**Performance Goals**: none stated and none needed. This repository has 26
active change directories; the family reads their `specs/*/spec.md` files and
one promoted spec per referenced capability, cached, with no subprocess at all —
strictly cheaper than `promotion-fidelity`'s 89-packet archive walk

**Constraints**: deterministic (identical inputs → identical findings, ordering
included); no model calls; no network; the CHECKED-OUT tree as the only
measurement basis; advisory in both halves (`warning`/`info` severities AND
absence from `FAMILY_RESOLUTION`); no edit to any other family's behaviour

**Scale/Scope**: one module (~500–650 lines with the docstring the house style
requires), one test file, three registration edits, one owed spec-delta block;
23 MODIFIED requirements in scope on this repository today

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md` v1.0.0 before Phase
0 and re-evaluated after Phase 1. Both passes below are the post-design state.*

| principle | verdict | basis |
| --- | --- | --- |
| **I. Contract-First, Domain-Neutral Core** | PASS | The family reads OpenSpec governance documents in neutral vocabulary — capability, requirement, scenario, change — and carries no domain term. "Runtime code is out of scope except governed reference implementations and validators explicitly ratified by an OpenSpec change" (Repository Constraints) is satisfied by name: this validator is the code surface a ratified change declares. |
| **II. Governed Change Flow: OpenSpec Before Implementation** | PASS | The change was ratified 2026-08-27 before any code. It declares `code_surface:` and `target_release:`. This feature is the Speckit decomposition the principle describes, and it does NOT duplicate the OpenSpec task list: `tasks.md` here references § 2's boxes rather than restating them, and § 3/§ 4/§ 5 stay with F2/F3/F4. |
| **III. Document Lifecycle and Status Discipline** | PASS | No governance document changes status here. The one governance edit is the owed `## MODIFIED Requirements` block inside an already-`ratified` packet, which is an amendment to a ratified change rather than a status transition, and it is exactly what `tasks.md` § 2.1 commissions. Speckit artefacts under `specs/` are outside `GOVERNED_ROOTS` (`corpus.py`:39) and carry no controlled `Status:` header. |
| **IV. Schema and Artifact Discipline** | PASS | No YAML added, so no `schema_version`/`kind` obligation. No credentials. No host-absolute path in any committed file — checked, and the one that existed in an early `quickstart.md` draft was removed rather than justified, even though `specs/` carries the practice elsewhere in this repository. |
| **V. Validation Gates (NON-NEGOTIABLE)** | PASS | `tasks.md` carries `pytest tests/doc-health`, the whole-tree `pytest tests`, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` as gate tasks, plus the RED-first discipline the principle's "deterministic, reviewable evidence rather than assertion" clause asks for. The auto-fixable/contested discipline is respected by ABSENCE from `FAMILY_RESOLUTION`: this family's findings are not `contested` at launch, so no finding of it can be resolved by a silent edit that the uncited-resolution rule would then convert into an `error`. |
| **VI. Versioned, Content-Addressed Releases** | N/A, declared | The proposal's `target_release:` states it: no schema under `contracts/schemas/` changes, no digest set moves, no `contract-v*` tag is owed. The archive gate is merge-plus-green. Nothing in F1 touches `contracts/manifest.yaml` or `contracts/CHANGELOG.md`. |
| **VII. Fail-Closed Authority Boundaries** | PASS | The marker registry is CLOSED — exactly two forms, and a paragraph that does not match one is not a marker, so it suppresses nothing (fail closed, never "degrade open"). A marker name that resolves to no canon unit likewise buys no silence. The family is deterministic with no model call, so "model output is non-authoritative" is satisfied structurally. No credentials, no tenant data, no high-cardinality identifiers enter a finding; a finding names governance text only. |

**Repository Constraints**: shared-tree discipline is followed literally —
explicit pathspecs on every `git add` and `git commit`, `git status -sb` before
each, no `git add -A`, no stash, no force-push. This feature runs from its own
sibling worktree, as the constraint requires. The aggregation pin update in
`opensoft/xFactory` is a SEPARATE later commit and is out of scope here (this
branch is not merged).

**Development Workflow deviations, named**: the lifecycle the constitution
lists is specify → clarify → plan → checklist → tasks → analyze → implement.
`clarify` was a no-op by design (zero `[NEEDS CLARIFICATION]` markers — the
ratified delta is normative down to the derivation) and is recorded as such in
`spec.md` § Clarifications. `checklist` produced
`checklists/requirements.md` at specify time; no domain checklist was
generated, the launching brief not asking for one and the requirement-quality
domain being the only one this feature touches. `analyze` runs before
implementation and its residue is recorded below.

**Post-design re-evaluation**: no new violation. The one design decision that
could have become a violation — reaching into `promotion_fidelity` and editing
it to share a helper — was measured and found unnecessary (research R12), so
Principle V's "generated evidence lands with the change that produced it" holds
for that module too: it produces no evidence here because it does not change.

## Project Structure

### Documentation (this feature)

```text
specs/019-modified-block-currency-family/
├── spec.md                        # 5 user stories, FR-001..FR-031, SC-001..SC-010
├── plan.md                        # this file
├── research.md                    # Phase 0 — R1..R15
├── data-model.md                  # Phase 1 — Unit, Marker, ActiveBlock, PromotedRequirement, WriterSet, Finding
├── contracts/
│   ├── unit-derivation.md         # normalize, mask_code_spans, split_sentences, is_dated_bold_note, derive_units, carried
│   ├── marker-parser.md           # extract_code_spans, parse_marker, suppression, marker_defects
│   └── family-entrypoint.md       # constants, discovery, resolution, the three arms, dispositions, registration surface
├── quickstart.md                  # Phase 1 — how to run it, the RED gate, the mutation table
├── checklists/
│   └── requirements.md            # spec-quality checklist (all items pass)
├── tasks.md                       # Phase 2 (/speckit-tasks) — 64 tasks, RED-first paired
└── pr-body.md                     # written by T063, at the END of implementation
```

### Source Code (repository root)

```text
scripts/doc_health/
├── modified_block_currency.py     # NEW — the whole family
├── families.py                    # +1 import name, +1 FAMILIES entry, +1 FAMILY_RESOLUTION-absence comment, docstring owner list
├── __init__.py                    # +1 FAMILY_IDS entry
├── promotion_fidelity.py          # IMPORTED, NOT MODIFIED (parse_delta, norm, load_dispositions, disposed, declared_standing)
└── duplicate_packet.py            # IMPORTED, NOT MODIFIED (_mention — the whole-token matcher the delta names)

tests/doc-health/
├── test_modified_block_currency.py            # NEW — F1's RED-first behavioural pins
├── test_lifecycle_scan_set.py                 # PHASE 8 — +1 NON_READERS member, the 17 -> 18 literal, +1 named assertion
├── test_family_enumeration.py                 # PHASE 8 — enumeration collateral (B2): numerals/names at :65,67,75,78,79,81,118,128,136,164,178
├── fixtures/family-enumeration-*/  (7 dirs)   # PHASE 8 — the same collateral in fixture spec text
└── fixtures/modified-block-currency*/         # NEW — the minimum fixture trees F1's own tests need

openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md
                                   # +the owed ## MODIFIED Requirements block (SAME COMMIT as the registration)
```

**Structure Decision**: the single-project layout the repository already has.
No new directory, no new package, no new entry point. The family is reachable
only through `families.FAMILIES`, which is what buys it the report section, the
ranked-plan line, the disposition keying and inclusion in the suite that gates
every PR — the four things `design.md`'s "What was considered and not done"
gives as the reason not to write a standalone `scripts/validate-*.py`.

## The sequencing gate (B1 — RULED 2026-08-27, option (a))

**`add-family-enumeration-check` archives FIRST, as a separate PR. F1's
registration cannot land until it has.**

`fam_family_enumeration` checks EVERY active delta that restates "Deterministic
check families" against the LIVE registry, independently
(`family_enumeration.py`:412-437, and its docstring says so in as many words).
So registering a twenty-second family makes that OTHER packet's still-active
restatement stale, and a block inside THIS change's delta cannot clear it.
Measured on this branch, by monkeypatching `_registry` and running the family
against this tree — no registration performed, nothing committed:

```text
21 registered: 0 findings
22 registered: 3 findings, ALL on
  openspec/changes/add-family-enumeration-check/specs/doc-health/spec.md
    omits 1 of the 22 registered check families: 'modified-block-currency'
    says 'twenty-one' check families, but 22 are registered
    says 'Four' of 'twenty-one', but 22 families are registered
```

**The packet's § 2.1 is therefore unimplementable as written** in a tree where
that change is active. D5 proved half the problem (a proposal-only tree reds the
gate) and did not measure the other half (a registering tree reds it on the
SIBLING's path). Recorded as a defect in the packet, not worked around.

**Consequences for this feature, both directions:**

- Phases 1–7 are unaffected and proceed now. They touch no registry: F1's
  behavioural tests call `fam_modified_block_currency` directly, and only the
  registration tests route through `families.FAMILIES`.
- Phase 8 waits. When the archive lands on `main`, this branch merges it and the
  registration commit lands with the block written relative to CANON — which by
  then IS that change's promoted outcome, so the second authority disappears and
  the two-writers instance § 2.1 was going to create never exists.
- **If the archive is delayed, F1 STOPS at the end of phase 7 and waits.** A
  complete, tested, unregistered module is a coherent reviewable state; a
  half-landed registration is not.

## Predicted movement — the ONE figure, and F3 asserts it

**Every other artefact points here. Two copies of a prediction is how a
prediction becomes two predictions.**

The packet measured at `9be81a40` over 23 MODIFIED requirements
(+1 `warning`, +10 `info` baseline; +1/+11 with § 2.1's block). This branch is
not that tree: `add-hermes-customer-subject-runtime-contract` and
`add-shared-identity-seeds` have archived since.

**Measured at this branch point** (after `git merge origin/main`, upstream
`501a3ae0`): 24 active changes, **22** MODIFIED requirement blocks across 17
delta files.

| | baseline (no § 2.1 block) | with § 2.1's block |
| --- | --- | --- |
| scenario-title arm | 1 `warning` | 1 `warning` |
| carriage ledger | 9 `info` / 12 units | 10 `info` / 14 units |
| resolution arm | 0 | 0 |
| marker defects | 0 | 0 |
| `error` / `critical` | 0 | 0 |

Those figures are the reviewer's, taken with the spike method at this branch
point; **they are re-measured through the real module at the end of phase 7 and
this table is then the measured truth rather than a forecast.** F3 (§ 4.1/§ 4.5)
asserts the right-hand column and nothing else asserts it.

Also corrected here: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`
reads **76 passed** on this branch (24 active + 52 specs), not the 77 recorded in
this feature's first two commits.

## Module design: the function inventory

`scripts/doc_health/modified_block_currency.py`, in file order. Contracts for
the first two groups are in `contracts/`.

**Constants** — `FAMILY`, `_LAUNCH_SEVERITY` (WARNING, the scenario-title arm,
the one § 7.2's flip moves), `_RESOLUTION_SEVERITY` (WARNING),
`_LEDGER_SEVERITY` (INFO), `DELTA_GLOB`, `CANON_TEMPLATE`, `_ACTION`.

**Normalization and units** — `normalize(text)`; `mask_code_spans(text)`;
`split_sentences(paragraph)`; `is_dated_bold_note(paragraph)`;
`derive_units(lines) -> (units, markers)`; `carried(canon_units, block_units)`.

**The marker** — `extract_code_spans(text)`; `parse_marker(paragraph)`;
`suppression(markers, canon_units, block_units)`; `marker_defects(...)`.

**Documents** — `active_blocks(root)`; `parse_spec_requirements(text)`;
`promoted(root, capability)` (cached).

**Resolution and ordering** — `resolve(block, canon, sibling_titles)`;
`declares(root, change_a, change_b)`; `writer_sets(blocks)`;
`order(writer_set)`.

**The arms and the fourth class** — `_arm_titles(...)`; `_arm_ledger(...)`;
`_arm_resolution(...)`; `_arm_marker_defects(...)` — three arms, FOUR finding
classes, the fourth being a defect in a declaration rather than a comparison
between documents (ruled 2026-08-27, B6: the first cut of this plan gave
`marker_defects` a producer and no emitter, which is how `dh:153-156`'s "SHALL
itself be reported" ends up realized in a docstring).

**Entry point** — `fam_modified_block_currency(ctx) -> list[Finding] | Skip`.

Two shapes are deliberately NOT built: no tree abstraction (one basis by
contract — R1) and no second disposition reader (R12).

## Decisions taken by the orchestrator — FLAGGED FOR VETO

Five decisions were taken for this feature by the orchestrating session, on
standing patterns rather than on a ruling. **None is backed by a ruling from
Brett**, and reverting any one of them is an edit to this plan rather than a new
feature. They are listed so they can be reversed on a word.

**O1 — F1 carries its own RED-first behavioural tests for everything it
builds.** The packet's § 3 is the exhaustive regression-fixture catalogue and
stays F2; this decision adds that no F1 behaviour ships without a test that
FAILED first — unit derivation including backtick masking and dated-note units,
same-kind exact matching with the containment negative, the three arms, the
marker parser in both forms including longer-fence code spans, the
destination-not-a-unit and present-unit-reported cases, title-carries-bullets
only in a genuine removal, the marker-form anchor, own-RENAMED-first
resolution, and the by-declaration two-writers cases including neither and both
declaring. Behavioural pins over text greps, and a mutation round before the
PR. *Cost of a veto*: F1 lands with no tests of its own and F2 becomes the only
gate, which is how a module arrives already-passing.

**O2 — § 2.1's MODIFIED block lands in the SAME COMMIT as the registration**,
with the per-requirement count (8 → 8) in the commit message and
`fam_family_enumeration` reading 0 against the tree. The one carriage-ledger
finding that block draws against itself is EXPECTED and ADVISORY — the packet
predicted it (§ 6.6) and the self-gate must treat it as evidence that the
family reads its own packet, never as a regression, and never dispositioned
away. *Cost of a veto*: two commits, one of which reds a standing gate on
`main`; or waiting for `add-family-enumeration-check` to archive, which this
feature cannot schedule.

**O3 — Launch severities exactly as the delta says**, and the family is ABSENT
from `FAMILY_RESOLUTION`. No flip in F1, in either half. *Cost of a veto*:
nothing in F1 changes; a flip is a later ruling by construction.

**O4 — No new disposition reader.** `promotion_fidelity.load_dispositions` /
`disposed` are imported. The contingency the brief allowed — a small refactor
to a shared helper, with its own test — does NOT trigger: the reader is already
parameterized by family and `duplicate_packet` already consumes it in this
shape, so `promotion_fidelity.py` is not edited at all and its tests stay
byte-green. *Cost of a veto*: a second reader of one file, which is the defect
three families' proposals argue against.

**O5 — Scope guard.** F1 does not touch `.github/workflows/`, `report.py`'s
grammars, any threshold, or any other family's behaviour. F4 owns workflow
wiring and the report section. *Cost of a veto*: F1 grows into F4 and the
feature boundary the packet drew stops meaning anything.

Three further decisions belong to this plan rather than to the brief, and are
flagged the same way because each is a reading the delta does not spell out:

**O6 — The "dated bold note" predicate** (research R6): a paragraph opening a
`**` bold run whose bold run contains an ISO date, tested only after the marker
test returns None. One of exactly TWO rules F1 supplies that the delta does not
write (the other is O9). A veto moves unit counts and therefore the predicted
ledger figure.

**O7 — "A resolvable change-id" in the marker anchor means "matches the
change-id token grammar", not "names an existing change"** (research R7). The
delta requires a marker to keep parsing after the change that wrote it archives,
which the existence reading would break. A veto makes markers rot on archive.

**O8 — Three severity constants, not one** (research R11), so § 7.2's flip
moves the scenario-title arm alone. A veto (one constant) drags the
title-resolution arm to `error` on a flip nobody asked for.

**O9 — Prose under a scenario heading is a `body` unit** (research R5). The
delta defines a scenario region's heading and its bullets and is silent on a
non-bullet paragraph inside one. Deriving it as a body unit keeps it under both
carriage arms; dropping it would let a block move an obligation into scenario
prose and have neither arm see it. A veto makes that text uncheckable.

**O10 — What "the declared sibling's OUTCOME" is computed as.** `dh:74-76`
requires a declaring block to be "measured against the declared sibling's
outcome rather than against canon", and the packet measured its own ledger
prediction on that basis (§ 6.6) without ever writing how the outcome is
derived. F1 computes it as: **canon's units for that requirement, REPLACED by
the sibling's MODIFIED block for the same requirement — and nothing else.** One
archive act simulated: no other active change applied, and the sibling's own
markers honoured as the sibling wrote them.

The clause this decision used to carry — "plus the sibling's units where the
sibling ADDS or RENAMES it" — is **DELETED by ruling of 2026-08-27 (B4)**. It
would have synthesized a basis for every MODIFIED-over-a-sibling's-ADDED pair,
of which this corpus has seven, and measured blocks the delta says must not be
measured: `dh:278-280` calls such a title "pending rather than absent", and
pending means nothing is compared. The deleted clause would have invented
roughly six `info` findings against text no promoted requirement carries.

**One consequence of reusing `duplicate_packet._mention`, noted rather than
hidden (N8)**: its boundaries are `[\w-]`, so a change id appearing inside a
PATH in the declaring proposal — `openspec/changes/<sibling>/tasks.md` — counts
as a declaration, because `/` is a boundary. That is accepted: a proposal citing
a sibling's path IS referencing that change in the ordinary reading of
`release-realization`, and the alternative is a second, stricter matcher for a
question one function already owns. A veto here needs a new matcher and a reason
the duplicate-packet family should not share it.

## Complexity Tracking

*No Constitution Check violation requires justification.* One complexity is
recorded because a reviewer will ask about it.

| item | why needed | simpler alternative rejected because |
| --- | --- | --- |
| Two normalizations in one module (`normalize`, whitespace-only; `promotion_fidelity.norm`, whitespace + casefold) | The delta forbids normalization beyond whitespace for UNIT comparison (`dh:84-90`) while the disposition mechanism and requirement-title lookup key on the casefolded spelling every other family uses | One normalization either violates the delta (casefolding units) or splits the shared disposition file into two key spellings. The two are named apart and pinned by a test that asserts they differ |
| Importing private helpers from sibling families — `duplicate_packet._mention`, and `promotion_fidelity._REQUIREMENT` / `_SCENARIO` / `_SECTION` | The delta names the matcher by reference: "the whole-token match the duplicate packet family already uses" (`dh:71-74`); and the three heading regexes are the ONE grammar four readers of these documents already share | Re-spelling either is a second grammar for one rule, which is the defect this corpus keeps paying for (`align-status-reader-to-real-lines`); `duplicate_packet.py`:142-144 already imports private names from `promotion_fidelity`, so the direction and the underscore are both precedented |

## Analyze residue

`/speckit-analyze` ran 2026-08-27 over `spec.md`, `plan.md` and `tasks.md`
against the ratified packet and this constitution. **No CRITICAL finding.**
Twelve findings; eleven were FIXED in the artefacts and one is carried
deliberately. Metrics: 31 functional requirements, 10 success criteria, 64
tasks, requirement coverage 31/31 after the fixes (30/31 before), zero
unresolved placeholders, zero duplicate requirements.

| # | severity | finding | disposition |
| --- | --- | --- | --- |
| A1 | HIGH | SC-001 and SC-002 asserted the #351 and #329 reconstructions as F1 outcomes, which § Out of Scope assigns to F2 — the spec contradicted its own boundary | FIXED in `spec.md`: both criteria now read at F1 grain ("the SHAPE of…"), and each names the F2 box that owns the byte-faithful fixture |
| A2 | HIGH | FR-002's second half — "MUST NOT offer or consume a live-`main` basis" — had no task and no test; the intent was recorded nowhere a build could fail | FIXED: FR-002 now says it is asserted rather than intended, and T020 gains `test_the_family_declares_no_measurement_basis_option` (no basis field read, absent from `FAMILY_NOTES`, no git-ref call in the module) |
| A3 | MEDIUM | O6 claimed the dated-note predicate was "the ONE rule F1 supplies that the delta does not write", but `contracts/unit-derivation.md` also rules that prose under a scenario heading is a `body` unit — a second such rule, unrecorded and unflagged | FIXED: O6 reworded to "one of exactly TWO"; the second is now **O9**, flagged for veto with its reason; `research.md` R5 records it beside the note predicate; T016 gains `test_prose_under_a_scenario_heading_is_a_body_unit` |
| A4 | MEDIUM | The "a capability with no promoted spec at all" edge case in `spec.md` had no task; it is a distinct code path (`promoted()` returns `None`, not a dict missing the title) | FIXED: T039 gains `test_a_capability_with_no_promoted_spec_at_all_resolves_to_nothing` |
| A5 | MEDIUM | Assumption A4 (groups of more than two active MODIFIED writers evaluated over the group) had no test; the population is zero today, so no natural fixture would ever produce one | FIXED: T042 gains `test_a_group_of_three_writers_with_one_declaration_is_evaluated_over_the_group`, with the note that the fixture has to be built because the corpus supplies none |
| A6 | MEDIUM | FR-010's punctuation half was untested — the exact normalization `promotion_fidelity.norm`'s own docstring names as the one it refuses (trailing periods) | FIXED: T018 gains `test_a_trailing_period_difference_is_not_forgiven`, and `quickstart.md`'s mutation table gains the matching mutant |
| A7 | MEDIUM | The single-repo disposition caveat was documented in three places and asserted in none, so the self-gate's silence about dispositions would be discovered rather than understood | FIXED: T045 gains `test_a_single_repo_run_has_no_aggregation_root_and_applies_no_disposition` |
| A8 | MEDIUM | Task-to-requirement traceability was inferable but not written: only FR-020, FR-030 and SC-007 were named in `tasks.md` | FIXED: `tasks.md` gains a full traceability table, every FR and SC to its tasks |
| A9 | LOW | `tasks.md` § Path Conventions carried a malformed backtick run in the fixtures line | FIXED |
| A10 | LOW | "Nothing in Phase 2 is parallel: it is a dependency chain by construction" was overstated — the two chains inside Phase 2 are independent of each other and serialize only because they write one file | FIXED: both reasons now stated apart |
| A11 | LOW | `pr-body.md` (written by T063) was absent from the plan's documentation tree | FIXED |
| A12 | LOW | **CARRIED, not fixed.** T055 asks for a text-level confirmation that the module contains no `_lifecycle_scope(` call, which sits oddly beside FR-031's "no behaviour ships on a text-grep assertion" | Deliberate. That grep is not F1's evidence for a behaviour — it is the pre-condition of an EXISTING package-wide test (`test_the_reader_list_is_structural_not_incidental`), which greps the package by design and for a reason its own docstring argues (a mutation survived without it). F1 inherits that test's shape rather than inventing one |

**One thing the analyze pass looked for and did not find**: a requirement with
no task, a task with no requirement, a vague adjective standing in for a
measurable criterion, or a placeholder. The three the pass would have flagged as
vague — "advisory", "editorial", "genuine removal" — are each defined
normatively in the ratified delta and cited to it.

## Adversarial plan review residue

An adversarial review of this plan ran 2026-08-27 and returned **6 blockers and
13 nits, with rulings**. All nineteen are applied. Four of the blockers changed
what this feature will BUILD, not merely how it is described, and two of them
found the ratified packet wrong.

| # | severity | finding | disposition |
| --- | --- | --- | --- |
| B1 | BLOCKER | `fam_family_enumeration` checks every ACTIVE delta's restatement against the live registry, so registering the 22nd family while `add-family-enumeration-check` is active emits 3 findings on THAT packet's path — which § 2.1's block in our delta cannot clear. The packet's § 2.1 is unimplementable as written | FIXED by RULING (option (a)): that change archives FIRST, as a separate parallel PR. § Sequencing gate added with the measurement (0 at 21, 3 at 22, reproduced here); FR-028 split into 028/028a/028b; SC-006, US5's story and its first two acceptance scenarios rewritten; research R13 replaced; T052–T056 rewritten and gated; contingency stated both ways (N2) |
| B2 | BLOCKER | The registration collateral omitted `tests/doc-health/test_family_enumeration.py` (11 assertion sites) and 7 `fixtures/family-enumeration-*` specs, all declared as `add-family-enumeration-check`'s own surface (`proposal.md`:2) | FIXED: new task T055a; the scope allowlist in research R15 and T059 now names exactly those paths, with the citation |
| B3 | BLOCKER | FR-014 emitted a second `warning` for units the ledger already reports at `info` | FIXED by RULING: a declaration is BASIS SUBSTITUTION ONLY. The resolution arm reports exactly two things — an unresolved title, and an undeclared or mutual ordering. FR-014, `contracts/family-entrypoint.md` (new "Arm 3, exhaustively"), `data-model.md`'s WriterSet table, T042 and T044 all rewritten |
| B4 | BLOCKER | O10's "plus the sibling's units where the sibling ADDS or RENAMES" would have measured all 7 MODIFIED-over-a-sibling's-ADDED pairs (~+6 `info`) where `dh:278-280` says "pending rather than absent" | FIXED by RULING: clause DELETED. A pending title is compared against NOTHING, pinned at T042 |
| B5 | BLOCKER | The prediction was measured at `9be81a40` (23 MODIFIED blocks); this branch has 22, and the artefacts restated the figure in three places | FIXED: `origin/main` fetched (the worktree's ref was stale) and merged; § Predicted movement is now the ONE home and every other artefact points at it; `openspec --all --strict` corrected 77 → 76 (24 active + 52 specs); re-measured through the real module at the end of phase 7 |
| B6 | BLOCKER | FR-018's "a marker naming a present unit is itself reported" had a producer (`marker_defects`) and no emitter | FIXED by RULING: a FOURTH finding class, "marker defects", at `_LEDGER_SEVERITY` (`info`, never `error`), with rule text, an emitter `_arm_marker_defects`, a flow entry, a traceability row and a `[TEST]` |
| N1 | nit | § 2.1's task did not name the eight scenario titles or the three dated notes | Applied: T052 lists all eight titles and the three notes at `add-family-enumeration-check/specs/doc-health/spec.md`:48, :71, :86, to be carried VERBATIM |
| N2 | nit | No contingency if the archive is delayed | Applied: § Sequencing gate and T052's preamble both state it — F1 stops at the end of phase 7 and waits |
| N3 | nit | T020's no-basis assertion was structural | Applied, and made BEHAVIOURAL: the family is called with a ctx carrying `promotion_fidelity_basis="live-main"` and the findings must be identical |
| N4 | nit | T025 asserted `--fail-on` was unaffected without first asserting findings exist | Applied: the test asserts a non-empty finding list before asserting no severity is in `{critical, error}` |
| N5 | nit | Four mutants missing | Applied to `quickstart.md`: per-unit vs per-requirement granularity; the ledger hedge; a `_RESOLUTION_SEVERITY` half-flip to `error`; a canon-side marker becoming a unit |
| N6 | nit | Complexity Tracking did not name the `_REQUIREMENT`/`_SCENARIO` imports | Applied |
| N7 | nit | Fenced code blocks | Applied by RULING: fenced lines are neither units nor markers, in canon or block. `fenced_regions` added to `contracts/unit-derivation.md` as step 0 of the derivation, with a T012 case using this change's OWN written-out example at `dh:187-190` — which would otherwise parse as two real markers on the requirement that defines them |
| N8 | nit | `_mention`'s `[\w-]` boundary makes a bare path citation count as a declaration | Accepted and noted in O10, with the reason it is accepted |
| N9 | nit | O9 accepted; record its population | Applied: population 2 measured, recorded in research R5 |
| N10 | nit | The `## ` section-stop invariant was unstated | Applied to `contracts/family-entrypoint.md`, citing `family_enumeration.py`:226-229, with the failure it prevents (the last requirement swallowing trailing sections) |
| N11 | nit | A traceability row asserted a requirement with no code surface | Applied: FR-031's row is marked "no code surface — process requirement, discharged by the `[TEST]` pairing and T061" |
| N12 | nit | T058 counted the whole-tree run as evidence | Applied by RULING: the count-delta evidence is `python3 -m pytest tests/doc-health -q` ONLY. The whole-tree run is out-of-band and **never run from a worktree** — it drives live Postgres containers. Removed from T058 and from `quickstart.md` |
| N13 | nit | `SPECIFY_FEATURE` is not the variable the scripts read | Applied: `quickstart.md` now exports `SPECIFY_FEATURE_DIRECTORY` |

**What the review did not change**: the three arms' severities, the advisory
launch in both halves, the same-kind exact matching rule, the marker grammar's
anchor, and the decision to import rather than re-spell every reader that
already exists. O1–O9 stand as written; O10 is amended by B4 and annotated by
N8.

