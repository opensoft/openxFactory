# Outcomes Requirements Quality Checklist: Factory MCP authorization profile

Status: record
Kind: report

**Purpose**: test whether the requirements for M5's narrowing (*Lossless results
and explicit failures*) and for per-domain error vocabularies are complete and
measurable, at release-gate rigor.
**Created**: 2026-10-09
**Feature**: [`spec.md`](../spec.md)

## Requirement Completeness

- [x] CHK001 Are both halves of the classification rule stated: error-inventory codes are execution failures, result-schema statuses are completed evaluations? [Completeness, Spec §FR-014; MODIFIED body]
- [x] CHK002 Is the narrowed *Unavailable dependency* scenario quoted with its WHEN as ratified, without restating it differently? [Completeness, Spec §User Story 4, scenario 1]
- [x] CHK003 Is it stated which MODIFIED scenario is outside the feature (*Existing digested result*), and why? [Completeness, Spec §User Story 4]
- [x] CHK004 Is it stated that no validator change is required for M5 or for the vocabularies? [Completeness, Spec §FR-014, §FR-015; D8, D9]

## Measurability

- [x] CHK005 Is the mutant defined precisely enough to be reproduced (which comparison is removed, from which tree)? [Measurability, Spec §FR-014; research R-14]
- [x] CHK006 Is it specified that both runs (mutant red, `main` green) are kept in the verification record? [Measurability, Spec §SC-004]
- [x] CHK007 Can "never compared across declarations" be witnessed by a test (two declarations sharing a code name, validated independently)? [Measurability, Spec §FR-015, §User Story 4, scenario 3]

## Requirement Clarity

- [x] CHK008 Is "result status" tied to the inventory's `kind`, not to what a status's name suggests? [Clarity, data-model "Outcome mapping"; D8]
- [x] CHK009 Is it clear that what a result status MEANS stays the domain's? [Clarity, data-model; D8]

## Scenario Coverage

- [x] CHK010 Is a result status mapped as an execution failure addressed as well as an error code mapped as a completed evaluation? [Coverage, Spec §FR-014]
- [x] CHK011 Is the positive case (a dependency status in a result inventory mapped as a completed evaluation is accepted) addressed, so that the narrowing is not read as forbidding such a status? [Coverage, Spec §FR-014; D8 probe]
- [x] CHK012 Is a code that no other domain uses addressed? [Coverage, Spec §User Story 4, scenario 4]

## Notes

- 12 items; all pass.
