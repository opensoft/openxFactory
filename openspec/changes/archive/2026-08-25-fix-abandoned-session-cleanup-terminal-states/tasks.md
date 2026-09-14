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

## 6. Review-driven evidence hardening

- [x] 6.1 Bind abandonment records to the exact branch head and require machine retention evidence to be durably recorded no earlier than the abandonment.
- [x] 6.2 Distinguish absent origin metadata from ad-hoc or malformed origins, scope ambiguous possibles-pick fallback failures to the requested tile, and remove duplicate change scans.
- [x] 6.3 Require executed demotion receipts to prove every planned move, exact contained destinations, source removal, and exact transition-manifest correspondence.
- [x] 6.4 Add semantic cleanup-record validation for exact target/scope identity, nonempty machine references, required change ids and recording times, and explicit-release reasons.

## 7. Review-driven transaction and release hardening

- [x] 7.1 Make cleanup a repository-locked, ref-keyed, exclusive `prepared`/`completed` transaction and refuse mismatched gate/Git roots.
- [x] 7.2 Delete local refs atomically with the expected abandoned head and restore the ref when record finalization fails safely.
- [x] 7.3 Align CLI and HTTP validation/error handling, reject blank superseding references, and report post-mutation receipt failures as partial execution.
- [x] 7.4 Add regression tests for historical evidence, moved refs, incomplete demotion, unsafe paths, record collisions, atomic deletion, malformed origins, and command-surface parity.
- [x] 7.5 Update operator guidance, realize the next contract bundle, run focused/full validation, and resolve every remaining review or CI failure.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas associated with the `ideation-dashboard` capability — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and are slated for removal from the bundle at `contract-v4.0` (§ 5.7; cut PR #983). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
