---
code_surface: openxFactory
target_release: deferred-allocation
sequenced_after: [qualify-private-connectivity-production, register-private-connectivity-evidence-pins]
---

# Proposal: Commission private connectivity production evidence controls

Status: draft
Kind: proposal
Proposed: 2026-11-13

## Why

Feature 043 has an analyzed implementation plan but no accepted scope for its evidence verifier, shared pin registration or required CI. The feature 040 registration covers only its historical pilot; production qualification needs its own reviewed evidence boundary before T007–T010 can begin.

## What Changes

- Propose the exact coordinator E implementation/test/CI surfaces listed in [design](design.md), plus the T010 source-CI receipt. This is a partial Q0-E decision only when an actual named owner accepts that scope and its consumed custody/authentication choices at T006.
- Define closed verification for the 68 task identities, original bootstrap evidence, owner-relative scope, actual command/output/revision identity, current authority, finite approved limits and immutable dependencies.
- Preserve independent approved canary/offer/wave child DAGs without treating an incomplete aggregate task as complete, bypassing full program Q2 or inheriting another scope's acceptance.
- Register only the exact feature 043 evidence reference families and their local/foreign ownership/reachability obligations. Keep feature 040 declarations and all existing uncovered-site checks intact.
- Wire the new feature suites explicitly into required coordinator CI and retain exact-head collection proof. Do not remove required checks, change existing skip/floor obligations or widen the approval envelope.
- Keep implementation in the sole [043 task list](../../../specs/043-private-connectivity-production/tasks.md), at T006–T010. This OpenSpec packet records authority and acceptance without duplicating executable implementation tasks.

## Capabilities

### New Capabilities

- private-connectivity-production-evidence: authenticated feature-local evidence, closed bootstrap import and scoped instance/aggregate dependency verification for production qualification.

### Modified Capabilities

None. Existing production qualification, pin reachability, document lifecycle, release and managed-subject authority requirements remain in force.

## Impact

The proposed owner is opensoft/openXfactory's named neutral/evidence maintainer. The eight code/test/CI files and the initial receipt are explicit in the design; feature coordination records and this packet remain governance surfaces. Required C-08 custody, retention/access and output/approval authentication choices are review inputs, not defaults selected by Codex.

This draft grants no implementation authority, owner acceptance, provider integration, deployment credential, production-domain selection, supported contract publication or target effect. T006 stays open until actual acceptance is recorded. Q0 is unaccepted and Q1–Q5 are not entered. The neutral publication successor and every runtime owner scope remain separately governed.

Draft publication: [PR #1310](https://github.com/opensoft/openXfactory/pull/1310). Related: [ratified production policy](../qualify-private-connectivity-production/proposal.md), [evidence contract](../../../specs/043-private-connectivity-production/contracts/task-evidence.md) and [governance handoff](tasks.md).
