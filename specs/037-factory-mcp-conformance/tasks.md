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
