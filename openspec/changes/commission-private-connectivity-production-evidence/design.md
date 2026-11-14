# Design: Coordinator E evidence commissioning

Status: ratified
Ratified: 2026-11-13 by Brett Heap. [Ratification record](review/ratification.md)

## Context

See [proposal](proposal.md). The production policy and the exact E scope/source-only C-08 choices are ratified. Feature 043's component runtime scopes and live evidence custody remain unaccepted. Its [task evidence contract](../../../specs/043-private-connectivity-production/contracts/task-evidence.md) resolves bootstrap and per-instance dependencies. The existing 040 reader/registration is preserved.

## Goals / Non-Goals

**Goals:** Make T006 review concrete, then permit only T007–T010 if the named owner accepts the listed surfaces and consumed evidence decisions. Preserve authenticated, reviewable outputs, closed required cases and fail-closed source/CI verification.

**Non-Goals:** Execute an owner command, collect target state, approve a provider/domain, publish the neutral binding contract, alter release policy, provision a target, accept another owner or pass a live rollout gate.

## Decisions

### Exact proposed surfaces

All paths below are relative to opensoft/openXfactory. T006 acceptance must identify the exact accepted subset, source revision, commands, approver, validity and exclusions; a proposed path is not a grant.

| Surface | Proposed responsibility | Speckit task |
| --- | --- | --- |
| specs/043-private-connectivity-production/verify-evidence.py | Read-only closed task/bootstrap/instance/evidence checks | T007 |
| specs/043-private-connectivity-production/tests/test_evidence.py | Positive and rejection cases, authenticated bootstrap, scope/authority/limits and child/aggregate dependency regressions | T007 |
| specs/043-private-connectivity-production/register-evidence-pins.py | Exact 043 reference inventory, distinct write/check modes | T008 |
| specs/043-private-connectivity-production/tests/test_evidence_pins.py | Exact inventory, owner reachability and no-write check regressions | T008 |
| scripts/doc_health/pin_class.py | Only local/foreign 043 evidence declarations; retain existing reachability and uncovered-site behavior | T009 |
| tests/doc-health/test_pin_reachability.py | Directly affected 043 declaration and reachability regressions | T009 |
| tests/doc-health/test_sentinel_vocabulary.py | Only census deltas actually measured from the accepted declarations | T009 |
| .github/workflows/pytest-suite.yml | Explicit collection of the new feature suites; preserve existing required jobs, counts, floors and skip obligations | T010 |
| specs/043-private-connectivity-production/evidence/T010.json | First coordinator source-CI receipt with immutable actual output references | T010 |

The 043 task/evidence/validation/policy documents, README and generated corpus ledger are coordination inputs/handoff records. This proposal does not grant all files beneath a directory. Future task/instance receipts need their own exact accepted C-01 file lists before writes. If implementation needs another source/test/CI path, return to owner review before editing.

### Closed evidence and bootstrap

Required task/owner/class/dependency/case identities come from the reviewed 68-row registry, then are frozen in the accepted verifier and command definitions. Reject caller-selected cases, unknown/duplicate/missing cases, forged pass text, non-finite or invalid measurements, wrong candidate/profile/target/customer/environment and current-authority failures. Actual outputs and expected results must match their command and source identity.

T001–T009 retain their original governance/source outputs instead of inventing new task receipts. T006 accepts the consumed custody/authentication choices; an authenticated immutable import of those original artifacts feeds the closed T007 bootstrap adapter. T010 requires the actual tests, diffs and exact-head collected CI. Later custody cannot retroactively authorize an earlier action. Self-verification does not establish a human approval.

### Instance and aggregate decisions

Freeze approved opaque instance identities, exact scopes/candidates and required child predecessors before use. The planned instance command is verify-evidence.py --task TNNN --instance INSTANCE_ID CHILD_RECORD; the default task command verifies aggregate completion. A same-scope accepted child can progress without an unrelated aggregate; aggregate checkboxes stay open until all commissioned children pass. Full program Q2 remains required before any canary. Offer admission precedes its wave, and each wave needs its own decision. Changed manifests or evidence need reviewed updates and renewed authority.

### Narrow pin registration and CI

Register the closed 043 top-level receipt names and the approved T057–T064 instance-reference areas, with explicit local/foreign repository ownership. No prefix exception, arbitrary owner reference or extension of the 040 registration is allowed. Generated inventory/write mode can write only an already accepted receipt/output scope; check mode is read-only. Retain local reachability and foreign-owner proof instead of treating an unavailable tree as verified.

Explicitly invoke both new feature suites in required coordinator CI. Capture the exact head and actual collection/results. Only directly affected new-suite counts and measured census additions can change; existing required floors and skipped counts stay intact. Missing collection, dependencies or output fails source readiness.

### Acceptance at T006

The [owner approval and custody note](review/owner-scope-approval-and-custody.md) and [ratification record](review/ratification.md) record Brett Heap's E owner-scope approval and his subsequent selection of the prepared source-only Git custody policy.

Accountable neutral/evidence maintainer and evidence custodian: Brett Heap. The combined T006 decision accepts:

- The exact nine E surfaces above, the reviewed source revision and T007–T010 verification commands.
- Reviewed redacted E bootstrap/source/CI exports and approval references in opensoft/openXfactory Git history, with exact commit/content identities and the existing reviewed publication process.
- Project-lifetime retention and existing repository access permissions; Brett is accountable for actual output/human-decision review, source/receipt commits, SHA-256 and GitHub repository/run/job/output provenance.
- The reviewed task/case/instance contract and feature-bounded E authority; changed scope needs renewed owner review and later operating choices stay due at their consumers.

The source-only storage/retention/authentication values were explicitly selected by the owner; they are recorded in review/ratification.md and origin approval metadata. Actual bootstrap ingestion/authentication still occurs at its consuming tasks. Customer/provider/staging/production evidence requires a separate protected-custody decision before consumption. No credential or private storage material belongs in the packet.

## Risks / Trade-offs

- Structural evidence may look authentic while describing no actual run → require protected actual output and independent owner confirmation.
- Self-approval or missing bootstrap receipts can create a cycle → import only the original closed bootstrap evidence under actual accepted custody.
- Parallel canaries can blur scope → freeze child identities and same-scope dependencies; keep aggregate completion distinct.
- A broad registration could conceal unrelated pins → exact 043 declarations, reachability checks and uncovered-path regression remain required.
- Source CI can be mistaken for live acceptance → evidence classes remain separate; no verifier invocation runs a target or grants authority.

## Migration Plan

Before acceptance, draft artifacts and local bootstrap validation only. After T006, use T007–T010 in the sole coordinating task list. Preserve feature 040 and existing required checks. A failed E validation blocks its consumers; a rollback restores the prior source/configuration through reviewed changes and withdraws affected evidence readiness rather than disabling a gate. Archive follows merged, green scoped realization and the existing promotion process.
