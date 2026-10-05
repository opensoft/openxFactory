# Tasks: Factory MCP advisory conformance

Status: draft
Kind: implementation

## Setup and foundation

- [x] T001 Publish closed bounded schemas and fixtures in contracts/factory-mcp/ (FR-001).
- [x] T002 Add failing adversarial contract tests in tests/factory-mcp before behavior (SC-001).

## User Story 1

Independent test: valid synthetic inputs pass; malformed or untrusted references refuse.

- [x] T003 [US1] Implement structural validation and trusted reference/context resolution in scripts/validate-factory-mcp.py (FR-001–003).

## User Story 2

Independent test: authority/evidence/timing contradictions yield governed safe failures.

- [x] T004 [US2] Implement semantic evaluation and safe diagnostics in scripts/validate-factory-mcp.py (FR-004–006).

## User Story 3

Independent test: public mappings preserve complete outcomes and schemas cover all variants.

- [x] T005 [US3] Implement repetition/descriptor/mapping integration in scripts/validate-factory-mcp.py (FR-007–008).
- [x] T006 [P] [US3] Document exact compatibility and limits in docs/factory-mcp-conformance.md and README.md (FR-008).

## Verification

- [x] T007 Run focused tests and affected regressions; record specs/037-factory-mcp-conformance/verification.md.
- [x] T008 Inspect final diff and repository/OpenSpec validators; record baseline findings in specs/037-factory-mcp-conformance/verification.md.

## Dependencies

T001 → T002 → T003 → T004 → T005 → T007 → T008. T006 may run after T001 in parallel. US1 is the core increment; all stories are required.

## Repair round 2026-10-05 (opensoft/openxFactory#1242, pull request #1243)

- [x] T009 Renumber the feature 030 to 037 and update every reference; keep AGENTS.md at main's bytes.
- [x] T010 Rename the test module to a unique import name; seed the sweep-ledger row.
- [x] T011 Write failing tests that assert diagnostic codes and locations, and the H2, H3, M1, M7 and L1-L5 behaviours (at d8b2e0cb: 96 failed, 23 passed).
- [x] T012 [US1] Embedded `$id` resources with resource-relative fragment resolution in scripts/validate-factory-mcp.py (FR-002).
- [x] T013 [US2] Discriminated union inventories, strict JSON Pointer indices and union-member coverage (FR-005).
- [x] T014 [US3] Located, de-duplicated diagnostics with distinct input codes and exit 2 for usage errors; an https resource URI, a tool id token, tool schemas tied to source, and `contentSchema` and `dependencies` walked (FR-001 to FR-003, FR-008).
- [x] T015 Run the full CI command on the branch and on main in the same clone kind, plus the pinned OpenSpec validation, doc-health and the sequenced-after validators; record an addendum in verification.md.
- [x] T016 Answer every Copilot review finding red first (five rounds, `94ca87e1` to `a12c7027`; table in verification.md).
