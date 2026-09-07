# Feature Specification: Factory MCP advisory conformance

Status: draft
Kind: implementation
Governed by: [add-factory-mcp-conformance](../../openspec/changes/add-factory-mcp-conformance/proposal.md), ratified 2026-09-07

Feature Branch: `030-factory-mcp-conformance`
Created: 2026-09-07
Input: Resume and finish the ratified MCP first slice.

## User Scenarios & Testing

### User Story 1 - Validate a closed declaration and pinned artifacts offline (Priority: P1)

A domain maintainer needs to validate a closed declaration and pinned artifacts offline.

Why this priority: establish the useful core contract.
Independent Test: deterministic positive and adversarial fixtures for FR-001 through FR-003.

1. Given complete authorized evidence, when evaluated, then the declared valid outcome is preserved.
2. Given inconsistent or missing required evidence, when evaluated, then a diagnostic/error is returned without a positive authority claim.

### User Story 2 - Detect contradictory authority, outcomes and repetition (Priority: P2)

A domain maintainer needs to detect contradictory authority, outcomes and repetition.

Why this priority: make the core safe to consume and review.
Independent Test: deterministic positive and adversarial fixtures for FR-004 through FR-006.

1. Given complete authorized evidence, when evaluated, then the declared valid outcome is preserved.
2. Given inconsistent or missing required evidence, when evaluated, then a diagnostic/error is returned without a positive authority claim.

### User Story 3 - Review explicit gaps and source-pinned compatibility (Priority: P2)

A domain maintainer needs to review explicit gaps and source-pinned compatibility.

Why this priority: make the core safe to consume and review.
Independent Test: deterministic positive and adversarial fixtures for FR-007 through FR-008.

1. Given complete authorized evidence, when evaluated, then the declared valid outcome is preserved.
2. Given inconsistent or missing required evidence, when evaluated, then a diagnostic/error is returned without a positive authority claim.

## Requirements

- **FR-001**: Accept only the closed versioned advisory-v1 declaration and unique tool/evidence/gap identities.
- **FR-002**: Resolve repository/revision/path/SHA256 references only within explicit offline roots; validate schemas and contained references; refuse network, traversal and symlink escapes.
- **FR-003**: Separate domain identity and deployment availability; require trusted host scope/policy mapping and explicit revocation posture.
- **FR-004**: Declare reads, execution, persistence and mutation independently; prohibit authority grants and target mutation; require bounded host execution.
- **FR-005**: Cover finite result/error inventories exhaustively and preserve domain objects with correct isError mapping; unresolved vocabulary must be a gap.
- **FR-006**: Record input/context/time/provenance and bounded disclosure; prohibit credentials/raw provider output and unsupported audit claims.
- **FR-007**: Enforce tagged reevaluate, lease_replay and fresh_observation requirements including persistence, scope, coordination and original timestamps.
- **FR-008**: Report structural, reference and semantic checks and gaps separately with deterministic diagnostics and exit codes 0/1/2; never certify runtime conformance.

Exact scenario semantics and refusal boundaries are inherited from [the ratified specification](../../openspec/changes/add-factory-mcp-conformance/specs/factory-mcp-conformance/spec.md); these requirements index that authority rather than replace it.

## Key Entities

See [data model](data-model.md) for identities, relationships and closed variants.

## Edge Cases

Unknown fields/enums; duplicate identities; unavailable or malicious dependencies; wrong provenance; timestamp/deadline boundaries; repeated calls; oversized input/output; misleading success claims. Each must retain its governed error/refusal classification. No production input is required.

## Success Criteria

- SC-001: Every ratified requirement has a deterministic positive or negative witness; no implementation claims beyond the available evidence.
- SC-002: Repeated runs of the same fixtures yield identical classifications and diagnostics.
- SC-003: Existing affected regression tests remain green; unrelated baseline validation failures are recorded separately.
- SC-004: Published schemas cover every returned variant and document exact integration limits.

## Assumptions and Clarifications

The user ratified both original proposals and their origins. No critical ambiguities require another question. Functional scope, data model, integration, failure behavior, authority and completion criteria are clear in the ratified design. Numeric bounds and file organization are implementation choices below the stated host limit. Live hosting, adoption, cancellation enforcement and release allocation are deferred by explicit scope. UI/localization does not apply to this callable/CLI slice.
