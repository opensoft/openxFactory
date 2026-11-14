# Design: Supported neutral binding publication

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [publish-private-connectivity-production-contract](proposal.md).

## Context

See [proposal](proposal.md). The existing reader resolves specs/040-private-connectivity/contracts/private-connectivity/binding.schema.json. That pilot candidate is explicitly outside the bundle. Its schema/readiness semantics are useful neutral inputs, while supported publication and exact consumer compatibility remain missing.

Feature 043 T016 must accept this scope independently of T006's evidence scope. T018–T019 own realization/readback; all implementation remains in the [single task list](../../../specs/043-private-connectivity-production/tasks.md).

## Goals / Non-Goals

**Goals:** Publish an independently usable neutral binding and conformance artifact through the normal release process; preserve optional/unbound compatibility and verify exact released content before consumer adoption.

**Non-Goals:** Change binding or deployment semantics, edit 040 history, reserve a version, publish a tag during drafting, grant cross-repository pin changes, introduce provider/domain vocabulary or bypass source/staging/canary/commercial gates.

## Decisions

### Exact proposed publication surfaces

All paths are relative to opensoft/openXfactory and require actual T016 scope/release-owner acceptance before changes.

| Surface | Proposed change |
| --- | --- |
| contracts/private-connectivity/binding.schema.json | Supported neutral schema with its declared contract-schema version; preserve the ratified optional binding shape and closed semantics |
| contracts/private-connectivity/README.md | Supported contract, conformance and compatibility/migration documentation backed by accepted governance |
| contracts/private-connectivity/conformance.json | Secret-free deterministic positive/refusal cases for the published contract; no live provider/customer evidence |
| scripts/validate-private-connectivity.py | Resolve the supported schema and retain existing read-only conformance, endpoint/context/scope and safe-input behavior |
| tests/private_connectivity/test_binding.py | Preserve the existing conformance regressions and update only directly required supported-schema expectations |
| tests/private_connectivity/test_published_contract.py | Publication/content/compatibility and independent neutral-consumer regressions |
| contracts/manifest.yaml | Schema/bundle identity and actual per-file content digests in the approved atomic cut |
| contracts/CHANGELOG.md | Matching actual release entry and compatibility notes in the same cut |
| contracts/releases/ | Only the one builder-generated inventory whose exact filename is fixed at the actual allocated cut; never a hand-edited inventory or broad directory grant |
| specs/043-private-connectivity-production/evidence/T018.json | Scoped neutral publication/source/release receipt |
| specs/043-private-connectivity-production/evidence/T019.json | Independent tag/commit/content and compatibility readback receipt |

The exact generated inventory filename and version are closed into the accepted realization file list at the approved cut before writing, never reserved by this proposal. Normal reader/test discovery already runs tests/private_connectivity under required pytest tests/; retain actual collection proof. This grants no workflow, release-builder or additional validator edit. If publication needs such a change, stop for the owning scope/task refinement first.

### Conformance and historical compatibility

Use the current ratified neutral semantics as the comparison baseline: absent optional binding preserves existing behavior; an included binding matches installation/customer/environment; the endpoint has HTTPS syntax and endpoint-bound approval scopes; minimum access, current approval, enrollment, effective policy and separately approved routes remain distinct; state vocabulary stays closed. Actual TLS identity and reachability observations remain in owner qualification, outside the offline conformance reader.

The reader remains offline and reports redacted conformance codes. Preserve current ordinary-input/path/symlink and duplicate-field refusals. A ready-shaped declaration is not proof of real reachability, actual approval or supported provider behavior. Test the published schema/reader and corpus independently of feature 040 imports and hosted product code; retain equivalent historical fixtures as regressions. Do not rewrite the 040 schema or lab approvals.

An additive cut preserves accepted consumers. If implementation discovers a breaking change, it must return for explicit schema-major/migration decisions under the existing policy rather than hiding a behavior change in a publication task.

### Normal atomic cut and readback

Use the existing [versioning policy](../../../docs/contract-versioning-policy.md) and release CLI. Allocate the actual bundle/schema version only at an authorized cut, generate the inventory from the actual tree and commit contract files, manifest, changelog and inventory atomically. Preserve every existing member's required digest and normal release/tag gates. Verify the realized commit, reviewed landing, remote promotion and annotated tag/readback with the existing build, verify-commit, verify-promotion and verify-tag commands as applicable to that release.

Never manufacture digests, retag an immutable published release, reserve a future version or treat the builder's output as publication. Actual tag publication requires current release authority at realization. This draft requests no tag or release operation now.

### Consumer boundary and Q1

T019 independently verifies the actual tag, exact release commit and every consumed content digest, supported validator/corpus identity and declared compatibility. Only then may separately accepted owners adopt those pins. No branch name, mutable tag, old lab schema or test literal is a compatibility proof.

Consumer implementation and pin changes remain in their owners. T049 later closes the exact final consumer/service/profile/harness matrix before T050/Q1. A supported neutral release alone passes no live qualification or product eligibility gate.

### Acceptance inputs

Proposed neutral/release maintainer: Brett Heap, subject to explicit role and exact-scope acceptance. T016 must record the actual owner, accepted source/CI/schema/test files, source revision and commands, release custody/process/authority, compatibility obligations and validity. The approved cut later supplies its actual version/inventory filename. T006's E approval cannot fill these fields.

## Risks / Trade-offs

- Copying draft bytes without a real release can look supported → require atomic member registration, generated inventory, realized commit and remote annotated-tag readback.
- Publication can accidentally change behavior → preserve old conformance cases and optional/unbound semantics; separate breaking decisions before changes.
- Generated inventory or tag drift can invalidate identity → use the existing release verifier and immutable-tag rules, with independent T019 verification.
- Neutral publication can be mistaken for deployment eligibility → retain every owner handoff and Q0–Q5 decision; no provider/domain runtime code enters this tree.

## Migration Plan

Before T016, draft artifacts only. After accepted scope, T018 publishes through the existing release sequence and T019 verifies the supported content. Owners then propose/adopt compatible pins within their own decisions. Preserve feature 040. If a release fails validation or readback, block adoption and complete a reviewed corrective release; do not rewrite a published tag or revive a revoked runtime binding. Archive only after merged, green scoped realization and required publication/promotion evidence.
