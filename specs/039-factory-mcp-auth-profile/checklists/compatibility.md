# Compatibility Requirements Quality Checklist: Factory MCP authorization profile

Status: record
Kind: report

**Purpose**: test whether the requirements state precisely what changes for
existing declarations, existing tests, the real domains and the contract
bundle, at release-gate rigor.
**Created**: 2026-10-09
**Feature**: [`spec.md`](../spec.md)

## Existing Declarations

- [x] CHK001 Is it stated that a not-deployed declaration validates exactly as before? [Completeness, Spec §FR-002; interface "Compatibility"]
- [x] CHK002 Is the intended break stated: a deployed declaration without a block, or with a query in its resource URI, becomes invalid? [Clarity, interface "Compatibility"; design *Compatibility*]
- [x] CHK003 Is the reason no pinned consumer breaks (the declaration is unreleased) stated? [Assumption, interface; D10]

## Existing Tests

- [x] CHK004 Is the rule for existing tests stated: all keep passing except those whose premise the ratified *Compatibility* section reverses? [Completeness, Spec §SC-005]
- [x] CHK005 Are the amended tests named, with the reason and the alternative rejected? [Traceability, research R-15]

## Real Domains

- [x] CHK006 Are the engineering domain's expected signals stated (`hosted_auth_missing` before its slice, `auth_rs256_missing` for an EdDSA-only block, stdio unaffected)? [Completeness, Spec §SC-008] (Gap found and fixed in this pass.)
- [x] CHK007 Is the out-of-tree check's method limited to `--snapshot`, with no vendored bytes, and is "owed" defined if it cannot run? [Clarity, Spec §SC-008, §Assumptions]
- [x] CHK008 Is the operations domain's position stated (callable-only, nothing changes)? [Completeness, Spec §Assumptions] (Gap found and fixed in this pass.)
- [x] CHK009 Are the downstream acts this feature does not perform listed? [Completeness, Spec §Assumptions; change `tasks.md` § 5]

## Contract Bundle

- [x] CHK010 Is the change class stated (additive minor: a new contract in the bundle)? [Clarity, Spec §FR-019; D10]
- [x] CHK011 Is it stated that the version is allocated at the cut and never reserved, and who claims it? [Completeness, Spec §FR-019, §Assumptions; research R-17]
- [x] CHK012 Are the cut's release surfaces enumerated (manifest row with digest, changelog entry, release inventory) as one candidate commit? [Completeness, Spec §FR-019]

## Notes

- 12 items; all pass after the two fixes recorded at CHK006 and CHK008.
