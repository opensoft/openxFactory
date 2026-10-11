# Security Requirements Quality Checklist: Factory MCP authorization profile

Status: record
Kind: report

**Purpose**: test whether the token-profile requirements (issuer, algorithms,
audience, metadata and secret handling) are complete, exact and fail closed, at
release-gate rigor.
**Created**: 2026-10-09
**Feature**: [`spec.md`](../spec.md)

## Requirement Completeness

- [x] CHK001 Is the required algorithm named, and are the only admissible algorithms enumerated? [Completeness, Spec §FR-008, §FR-010; OQ-2]
- [x] CHK002 Is the forbidden set (`none` and every HMAC name) enumerated exhaustively? [Completeness, Spec §FR-009; D2]
- [x] CHK003 Are the issuer's required form and each refused component (query, fragment, userinfo, non-https, missing host) listed? [Completeness, Spec §FR-004; research R-8]
- [x] CHK004 Are all three audience refusals (another resource, wildcard, equal to the issuer) specified for both bindings where they apply? [Completeness, Spec §FR-011, §FR-013]
- [x] CHK005 Is it specified that an `issuer_assigned` binding is never certified and rests on cited support? [Completeness, Spec §FR-012; OQ-1]
- [x] CHK006 Is it stated that a shared audience across declarations cannot be detected offline, and what bounds that risk? [Completeness, Spec §Edge Cases] (Gap found and fixed in this pass.)
- [x] CHK007 Are runtime token checks (signature, key discovery, expiry) explicitly placed outside the profile, with validity certifying none of them? [Completeness, Spec §Assumptions; §FR-016] (Gap found and fixed in this pass.)

## Requirement Clarity

- [x] CHK008 Is letter-case handling defined for both the admitted names (exact) and the forbidden names (without case)? [Clarity, Spec §FR-009, §FR-010, §Edge Cases; research R-7]
- [x] CHK009 Is the handling of a non-ASCII lookalike of a forbidden name defined? [Clarity, research R-7]
- [x] CHK010 Is "equals the issuer" defined as an exact string comparison? [Clarity, Spec §FR-013] (Gap found and fixed in this pass.)
- [x] CHK011 Is "wildcard" defined (the literal `*` anywhere in the value)? [Clarity, Spec §FR-013; research R-9]
- [x] CHK012 Is "absolute https issuer identifier" tied to the same character rules as the resource URI, so that one rule governs both? [Clarity, research R-8]

## Fail-Closed Coverage

- [x] CHK013 Is every algorithm not named in the profile refused rather than tolerated? [Coverage, Spec §FR-010; constitution VII]
- [x] CHK014 Is an unknown `binding` value refused? [Coverage, Spec §FR-003]
- [x] CHK015 Is a missing block on a deployed service refused rather than defaulted? [Coverage, Spec §FR-001]
- [x] CHK016 Is it specified that a valid declaration still reports `verified_conformance: false`? [Coverage, Spec §FR-016]
- [x] CHK017 Is a block with no `auth` support refused, so that no authorization claim stands uncited? [Coverage, Spec §FR-007; OQ-4]

## Dependencies and Assumptions

- [x] CHK018 Is the reason RS256 is the baseline (the estate's only live issuer signs it) traceable to the ruling? [Traceability, Spec §User Story 2; proposal ruling 1]
- [x] CHK019 Are the synthetic-only and offline-only constraints stated, so that no real issuer, tenant or host enters a test? [Assumption, Spec §Assumptions]

## Notes

- 19 items; all pass after the three fixes recorded at CHK006, CHK007 and CHK010.
