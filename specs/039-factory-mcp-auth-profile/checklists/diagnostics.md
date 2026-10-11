# Diagnostics Requirements Quality Checklist: Factory MCP authorization profile

Status: record
Kind: report

**Purpose**: test whether the requirements for what the validator reports
(codes, dimensions, locations, combination and ordering) are complete and
unambiguous, at release-gate rigor.
**Created**: 2026-10-09
**Feature**: [`spec.md`](../spec.md)

## Requirement Completeness

- [x] CHK001 Does every new refusal name a stable code, a dimension and a JSON Pointer location? [Completeness, interface "Diagnostics"; D7]
- [x] CHK002 Are the two existing codes at new locations listed with their exact locations? [Completeness, Spec §FR-007; interface]
- [x] CHK003 Is the dimension of a closed-shape fault (`structure`) distinguished from the semantic codes? [Completeness, interface; data-model "Report"]
- [x] CHK004 Is it specified where the checks run (the semantic pass, after structure and references), so that a reference failure suppresses them as it suppresses every semantic check? [Completeness, Spec §FR-016]

## Requirement Clarity

- [x] CHK005 Is it specified that a structural fault inside the block cannot name its field, and why? [Clarity, Spec §Edge Cases; research R-3]
- [x] CHK006 Is the location of `unsupported_auth` fixed (`/service/auth/evidence_ids`) even when the block cites only gaps? [Clarity, Spec §FR-007; D7]
- [x] CHK007 Is the list-versus-entry location rule for duplicate and missing ids stated? [Clarity, Spec §FR-007]

## Requirement Consistency

- [x] CHK008 Are combination rules stated where two codes can share a location (`invalid_resource_uri` with `auth_resource_query`)? [Consistency, Spec §Edge Cases; research R-5]
- [x] CHK009 Is it stated whether `auth_metadata_path_mismatch` is reported when the resource URI is itself invalid? [Consistency, Spec §Edge Cases; research R-6]
- [x] CHK010 Is it stated that a forbidden algorithm entry is reported once (as forbidden), not also as unadmitted? [Consistency, research R-7]
- [x] CHK011 Are de-duplication, sort order and exit codes stated as unchanged? [Consistency, Spec §FR-016; interface "Compatibility"]

## Scenario Coverage

- [x] CHK012 Is `auth_resource_query` specified for a deployed service with no block, alongside `hosted_auth_missing`? [Coverage, research R-5]
- [x] CHK013 Is `auth_rs256_missing` specified beside an unadmitted entry such as `rs256`? [Coverage, Spec §Edge Cases]
- [x] CHK014 Is determinism (identical reports on repeated runs) a stated success criterion? [Measurability, Spec §SC-007]

## Notes

- 14 items; all pass.
