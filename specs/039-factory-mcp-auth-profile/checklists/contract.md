# Contract Requirements Quality Checklist: Factory MCP authorization profile

Status: record
Kind: report

**Purpose**: test whether the requirements for the declaration's shape (the
block, its fields, its bounds and the concern vocabulary) are complete,
unambiguous and consistent, at release-gate rigor.
**Created**: 2026-10-09
**Feature**: [`spec.md`](../spec.md)

Run with no focus argument, so at maximum coverage: one checklist per
requirement-quality domain the feature touches (contract, security,
diagnostics, outcomes, compatibility, governance, acceptance). Each item was
evaluated against `spec.md`, `research.md`, `data-model.md` and
`contracts/interface.md` on 2026-10-09.

## Requirement Completeness

- [x] CHK001 Is every field of the block named, with its type and whether it is required? [Completeness, Spec §FR-003; data-model `service.auth`]
- [x] CHK002 Is the block's placement specified: the `deployed` branch only, and nowhere else? [Completeness, Spec §FR-001, §FR-002; D1]
- [x] CHK003 Is it specified that the block carries no second resource field, so that the resource it protects is `canonical_resource_uri`? [Completeness, Spec §Key Entities; data-model]
- [x] CHK004 Are length and count bounds specified for every new string and list? [Completeness, research R-12]
- [x] CHK005 Is the concern-vocabulary extension specified for both the evidence and the gap records? [Completeness, Spec §FR-007; data-model "Concern vocabulary"]
- [x] CHK006 Is the deployed synthetic example's content specified (identifiers, algorithms, binding, metadata path, support)? [Completeness, Spec §FR-017; research R-16]
- [x] CHK007 Are the constants that must NOT change (`schema_version`, `kind`, `profile`) named? [Completeness, interface "Declaration"; OQ-5]
- [x] CHK008 Is the text that calls the declaration unreleased, and when it changes, specified? [Completeness, Spec §FR-019] (Gap found and fixed in this pass: FR-019 now moves the schema title and the runbook paragraph at the cut.)

## Requirement Clarity

- [x] CHK009 Is "closed" defined as any field beyond the six being refused? [Clarity, Spec §FR-003]
- [x] CHK010 Is the closed set of `audience.binding` values enumerated? [Clarity, Spec §FR-003]
- [x] CHK011 Is "exactly one issuer" (OQ-6) stated in a way a test can falsify (a list, or a second issuer field)? [Clarity, Spec §Edge Cases, §FR-003]
- [x] CHK012 Is it unambiguous that the block is optional in shape but required in meaning on a deployed service? [Clarity, research R-2; Spec §FR-001]

## Requirement Consistency

- [x] CHK013 Do the block's `evidence_ids` and `gap_ids` bounds match a tool's? [Consistency, research R-12, R-10]
- [x] CHK014 Does the issuer's length bound match the existing resource URI's? [Consistency, research R-12]
- [x] CHK015 Do the spec, the data model and the interface name the same nine codes and the same locations? [Consistency, data-model; interface "Diagnostics"]

## Scenario and Edge Case Coverage

- [x] CHK016 Are empty, repeated and wrongly typed algorithm lists all addressed? [Coverage, Spec §FR-003, §Edge Cases]
- [x] CHK017 Is a block on a not-deployed service addressed, and is its code consistent with the closed branch's behavior on `main`? [Coverage, Spec §FR-002]
- [x] CHK018 Is the `auth` concern on a not-deployed declaration addressed (admitted, no rule)? [Edge Case, Spec §Edge Cases]
- [x] CHK019 Is it specified that no field can hold key material, a secret or a token, and how that is enforced? [Coverage, Spec §FR-003; research R-13]

## Notes

- 19 items; all pass after the one fix recorded at CHK008.
