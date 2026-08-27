# Implementation Plan: modified-block currency — reporting and workflow (F4)

**Branch**: `022-modified-block-currency-reporting` | **Date**: 2026-08-27 |
**Spec**: [spec.md](./spec.md)

**Input**: Feature specification from
`/specs/022-modified-block-currency-reporting/spec.md`

**Packet**: `openspec/changes/add-modified-block-currency-check`, `tasks.md`
section 5 (5.1–5.3). F4 of four; F1 `19e3f6b5`, F2 `76a2ad27`, F3 `f728d57f`.

## Summary

The family already reports its four finding classes as distinct findings, with
distinct severities and (for the marker class) a distinct action. What the report
does not do is let a reader SEE that split: the section is a flat list of nine
long rows, and learning "one scenario was dropped, eight blocks diverge
editorially" means reading all nine and tallying.

F4 adds one thing — a per-class subtotal block under the family's own heading,
before its rows — through a new registry keyed exactly like the existing
per-family notes registry, and renders it from an additive branch in
`report.render` that emits nothing at all for a family with no entry. It then
PINS two boundaries that already hold by accident: that every finding carries the
family's action line (F1's `_ACTION`, verbatim section 5.2's wording), and that no
per-family workflow option or CLI option reaches this family.

No workflow change. No `openspec/` change. No rule text, severity, resolution
class, finding grammar or ranked-plan grammar change.

## Technical Context

**Language/Version**: Python 3.11+ (the suite runs on the runner's system
python3; no version pin in the repo).

**Primary Dependencies**: none new. `PyYAML` for the section 5.3 workflow read, already
a test dependency of `tests/doc-health/test_workflow_contract.py`.

**Storage**: N/A — no persisted state. The report is a rendered artifact.

**Testing**: `pytest`, `tests/doc-health/`. One new file,
`test_modified_block_currency_reporting.py`.

**Target Platform**: Linux CI runner and a developer checkout, identically.

**Project Type**: governance tooling — a single-package checker
(`scripts/doc_health/`) plus a test suite.

**Performance Goals**: the subtotal is O(findings of one family) over a list
already in memory. No corpus read, no subprocess, no I/O.

**Constraints**: additive only in `report.py`; byte-identical output for every
other family; `.github/` and `openspec/` diff empty; the family's rule texts
byte-identical so F1/F2/F3's suites stay green.

**Scale/Scope**: 22 families, 9 findings of this family over this checkout, ~50
findings of all families in a single-repo report. Three source files touched, one
test file added.

## Constitution Check

*GATE: passed before Phase 0; re-checked after Phase 1 (below).*

| principle | verdict | note |
| --- | --- | --- |
| I. Contract-first, domain-neutral core | **PASS** | doc-health tooling is neutral by construction; no domain vocabulary enters. |
| II. Governed change flow: OpenSpec before implementation | **PASS** | the change `add-modified-block-currency-check` is ratified; this is its fourth Speckit feature, realizing section 5 only. No spec delta is authored here — `openspec/` is untouched by design (section 5.3, FR-018). |
| III. Document lifecycle and status discipline | **PASS** | no governance document changes status. The feature's own artifacts are Speckit artifacts, not governed corpus documents. |
| IV. Schema and artifact discipline | **PASS** | no YAML, no credentials, no host-absolute path in a committed file. (The quickstart names the worktree path once, as a run instruction; it is a Speckit artifact, and the same shape F1–F3 used.) |
| V. Validation gates (NON-NEGOTIABLE) | **PASS** | `pytest tests/doc-health` and `openspec validate --all --strict` both recorded in `evidence/f4-gates.md`, plus a report-movement measurement and a mutation round. RED-first is a tasks-level obligation, tracked per test. **On the "affected repo-local validators" clause** (analyze finding A4): NONE is affected, and the reason is checked rather than assumed — every `scripts/validate-*.py` validates contract or governance YAML (and `validate-workflow-contracts.py` validates a DOMAIN repo's `workflows/*.yaml` contract files, not GitHub Actions). This feature adds no YAML and edits no contract, so no validator has a changed input. The gate that does own this code is `pytest-suite`, which runs `pytest tests/ -q -m "not postgres"` and is a required check on `main`. |
| VI. Versioned, content-addressed releases | **N/A** | no contract release, no manifest, no tag. |
| VII. Fail-closed authority boundaries | **PASS** | the class map is a CLOSED set with a fail-loud residual (research R6): an unrecognized finding is counted and named, never absorbed. The renderer never raises on it — loud in the artifact, not fatal to the nightly. |

**Complexity Tracking**: no violations, so the section is omitted.

## Project Structure

### Documentation (this feature)

```text
specs/022-modified-block-currency-reporting/
├── plan.md                      # this file
├── spec.md                      # the feature specification
├── research.md                  # Phase 0 — R1..R11, decisions and measurements
├── data-model.md                # Phase 1 — the four classes, the tally, invariants
├── contracts/
│   ├── report-section.md        # byte-level rendered grammar + registry contract
│   └── workflow-boundary.md     # the section 5.3 pin, W1..W6, and its mutant
├── quickstart.md                # Phase 1 — runnable validation guide
├── checklists/requirements.md   # spec quality checklist
├── evidence/f4-gates.md         # gates, mutation round, archive-readiness numbers
└── tasks.md                     # Phase 2 (/speckit-tasks)
```

### Source (repository root)

```text
scripts/doc_health/
├── report.py                    # ADDITIVE: the notes/summary render branch
├── families.py                  # ADDITIVE: FAMILY_SUMMARIES registry (+ its comment)
├── __init__.py                  # ADDITIVE: RunResult.notes docstring records the 2nd note kind
└── modified_block_currency.py   # ADDITIVE: class ids, class map, class_summary()

tests/doc-health/
└── test_modified_block_currency_reporting.py   # NEW — the whole feature's tests

.github/workflows/doc-health-reusable.yml       # READ ONLY. Never edited.
openspec/                                       # UNTOUCHED. Diff must be empty.
```

**Structure Decision**: no new module. The subtotal's knowledge is the family's
own rule texts and its own class taxonomy, so it lives in
`modified_block_currency.py` beside the arms that produce them — a second file
would split one fact across two places and make the drift argument of research R2
weaker. The registry lives with the registry it is a sibling of. The render
branch lives where family sections are rendered.

## Phase 0 — research

Complete: [research.md](./research.md). Eleven decisions, five measurements taken
before any of them. R1 (the mechanism) is FLAGGED FOR VETO. Two findings worth
carrying into review: section 5.2's action line already exists (so section 5.2 is a
pin, not an addition) and section 5.2's singular is imprecise (the family has two
action lines).

## Phase 1 — design and contracts

Complete: [data-model.md](./data-model.md),
[contracts/report-section.md](./contracts/report-section.md),
[contracts/workflow-boundary.md](./contracts/workflow-boundary.md),
[quickstart.md](./quickstart.md).

**Post-design Constitution re-check**: unchanged, all PASS. The design added no
dependency, no persisted artifact, no authority claim, and no new option; the
fail-closed obligation (VII) is discharged by the closed class set plus the
residual line rather than asserted.

## Implementation order (and why it is forced)

1. **The class map and the tally**, in `modified_block_currency.py`, with its
   RED tests first. Nothing can be rendered before a finding can be classified,
   and the classification is the only part with a correctness question in it.
2. **The registry** in `families.py`. One line plus the comment that says why the
   registry exists and why it is a sibling of `FAMILY_NOTES` rather than a
   widening of it.
3. **The render branch** in `report.py`. Last of the three, because its
   byte-identity test needs a populated registry to be non-vacuous — a render
   test over an empty registry passes on a no-op.
4. **The section 5.2 pins** — independent of 1–3; they assert F1's landed constants
   and can be written at any point. Sequenced here so an early green does not
   hide that they were never RED.
5. **The section 5.3 pins** — fully independent (a different file, no shared code).
   `[P]`-able against everything above.
6. **Gates, mutation round, evidence.** After 1–5, never interleaved: a mutation
   round over a partially built feature kills mutants for the wrong reason.

## Risks, and what each one is caught by

| risk | caught by |
| --- | --- |
| the render generalisation perturbs another family | the in-process byte-identity test (research R8 proof 1) AND F3's subprocess movement gate (proof 2) |
| a rule text drifts and a class silently empties | `test_every_finding_classifies_into_exactly_one_class` over fixtures and the real tree, plus the `unclassified` row on the artifact |
| the subtotal is read back as a finding | the `PLAN_RE` pin, following `test_promotion_fidelity.py::test_the_basis_lines_can_never_be_read_back_as_findings` |
| a zeros line beside a skip claims a measurement | the two skip-shape tests (FR-004) |
| F1/F2/F3 reds because a rule text moved | rule texts are not edited at all; the three suites are re-run as gate evidence to prove it rather than assumed |
| the section 5.3 pin passes vacuously | W2 and W6 of `contracts/workflow-boundary.md`, and the scratch-workflow mutant |

## What F4 must NOT do

- Tick or perform the packet's section 8. F4 leaves the tree archive-ready and
  records the three numbers; the archive act is a separate later commit.
- Decide F3's open question on the blast radius of an exact-set corpus gate in a
  required check. Carried forward verbatim into the hand-off and the PR body.
- "Fix" a corpus-driven red in F3's self-gate by loosening it. F3's hand-off
  names the two movements already known to be coming.
- Touch `.github/` or `openspec/`.
