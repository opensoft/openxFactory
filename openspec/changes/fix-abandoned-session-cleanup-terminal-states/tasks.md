## 1. Cleanup evidence contracts

- [x] 1.1 Introduce a cleanup-specific retention-release evidence model instead of reusing live `ProposalState`, and share exact staged-origin identity resolution across active and historical change records.
- [x] 1.2 Extend the gate-action contract and validators with a `cleanup-abandoned-branch` record that captures the branch, pre-delete head SHA, exact tile or staged origin, abandonment evidence, disposition evidence, actor, and reason.
- [x] 1.3 Add a durable demotion-execution receipt written only after the proposal has been returned successfully, including the exact source change and returned staged destination.

## 2. Retention-release evidence resolution

- [x] 2.1 Resolve active-proposal evidence from exact `.openspec.yaml` staged origins, retaining the current possibles-pick mapping only as a compatibility fallback and making ambiguous matches fail closed.
- [x] 2.2 Resolve archived-proposal evidence from exact archived `.openspec.yaml` staged origins even when the current dashboard tile is absent.
- [x] 2.3 Resolve executed demotion from the new execution receipt, and support legacy demotions only when an exact transition manifest is corroborated by the exact returned staged artifact.
- [x] 2.4 Reject transition plans or manifests by themselves, mismatched origins or destinations, ambiguous evidence, and mere absence of a current tile.
- [x] 2.5 Add an explicit human retention-release path for true orphan, duplicate, superseded, cluster, possible, or missing-tile branches, requiring a nonblank reason and any supplied superseding references to be recorded rather than treated as machine proof.

## 3. Governed cleanup transaction

- [x] 3.1 Preserve the existing exact branch-family, live-session, worktree, and successful-abandonment checks for every cleanup path.
- [x] 3.2 Write and validate the main-resident cleanup record before deleting the local branch, then remove or invalidate that record if branch deletion fails.
- [x] 3.3 Update CLI and HTTP request parsing, console-only enforcement, result payloads, and refusal hints to report the selected evidence path and the corrective action when cleanup remains blocked.
- [x] 3.4 Keep the operation local-only: do not delete remote branches, infer disposition from age or absence, or enable unattended cleanup.

## 4. Verification

- [x] 4.1 Add tests for active proposal evidence through both authoritative origin metadata and the compatibility possibles-pick mapping.
- [x] 4.2 Add tests for exact archived-origin evidence, including cleanup after the current tile has disappeared.
- [x] 4.3 Add tests for new demotion execution receipts, legacy manifest-plus-returned-artifact corroboration, and refusal of plan-only, manifest-only, mismatched, or ambiguous evidence.
- [x] 4.4 Add tests for explicit human release of orphaned and non-staged tile branches, including refusal when the reason, abandonment proof, exact branch identity, or other safety preconditions are missing.
- [x] 4.5 Add tests for cleanup-record schema validation, evidence reporting, record unwind on deletion failure, CLI/HTTP parity, and console-only enforcement.
- [x] 4.6 Run the focused ideation dashboard test suites and confirm existing propose, demote, abandon, and cleanup behavior remains compatible.

## 5. Operator guidance and validation

- [x] 5.1 Update the ideation dashboard runbook to explain active, archived, demoted, and explicit human retention-release paths and the evidence each path requires.
- [x] 5.2 Validate all new schemas, fixtures, and gate-action examples with the repository validators.
- [x] 5.3 Run strict OpenSpec validation for this change and resolve every reported issue before implementation is considered complete.
