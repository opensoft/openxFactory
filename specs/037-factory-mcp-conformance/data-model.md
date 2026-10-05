# Data model

Status: draft
Kind: implementation

- FR-001: Accept only the closed versioned advisory-v1 declaration and unique tool/evidence/gap identities.
- FR-002: Resolve repository/revision/path/SHA256 references only within explicit offline roots; validate schemas and contained references; refuse network, traversal and symlink escapes.
- FR-003: Separate domain identity and deployment availability; require trusted host scope/policy mapping and explicit revocation posture.
- FR-004: Declare reads, execution, persistence and mutation independently; prohibit authority grants and target mutation; require bounded host execution.
- FR-005: Cover finite result/error inventories exhaustively and preserve domain objects with correct isError mapping; unresolved vocabulary must be a gap.
- FR-006: Record input/context/time/provenance and bounded disclosure; prohibit credentials/raw provider output and unsupported audit claims.
- FR-007: Enforce tagged reevaluate, lease_replay and fresh_observation requirements including persistence, scope, coordination and original timestamps.
- FR-008: Report structural, reference and semantic checks and gaps separately with deterministic diagnostics and exit codes 0/1/2; never certify runtime conformance.

Exact entities and variants follow [ratified design](../../openspec/changes/add-factory-mcp-conformance/design.md). Immutable source/context identities differ from trace IDs. Original observation timestamps survive reuse. Results confer no authority. Unknown fields/enums fail closed.
