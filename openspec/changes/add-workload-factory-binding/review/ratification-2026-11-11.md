# Source-only ratification of factory/workload binding

Status: ratified
Kind: report
Decision date: 2026-11-11
Ratifier: Brett Heap, repository owner
Scope: source acceptance only

Brett Heap gave this instruction in the current Codex chat:

> I ratify #1304 at 102d5f906cc4 with #48 at 9e0b60e89bb3 for source acceptance only. Go ahead and land both through the governed process when green. Keep feedback deferred and don’t replay either blocked write.

## Exact accepted snapshots

- Factory PR [#1304](https://github.com/opensoft/openxFactory/pull/1304):
  102d5f906cc4e3525c56af6608f58b26a4fd5e7c.
- Paired adapter PR [#48](https://github.com/opensoft/openXwallet/pull/48):
  9e0b60e89bb39c13a30635d8c9defd7334466ed8.

The ratification accepts the factory proposal/design/capability/profile and the
paired reviewed source implementation at those snapshots. These snapshots
remain immutable in Git history. The following candidate commits add acceptance
metadata only; they do not revise the accepted technical requirements, code or
tests. Fresh exact-head checks and Codex review are required before landing.

## Accepted factory file SHA-256 values

- proposal.md: 2bf3fb69588255fd456f34c916122f0033395496a0828c3bbfa861cffa57edf7
- design.md: e758780a43c1380e745a3b383cc06e216ce10dcad1795a83fbc593d02d378650
- specs/workload-factory-binding/spec.md: 2488022afdba7c497fbd5a246c1d347c29b6663617b9467d54c041e38ab62184
- supporting-docs/profile.md: 50188da10e8c711ed37502b2fd78f9d92f0fb0511af827c7110823b13f342f83

## Scope boundaries

This is source acceptance, not live workload/supervisor/custody qualification,
hostile-OS isolation, a human approval grant, a published contract/release,
consumer-pin adoption or attended pilot acceptance. CodeXfactory T002 remains
blocked. Feedback remains deferred and neither historically denied write is
replayed. The accepted trusted-storage boundary and review-class refusal remain
unchanged.

## Landing authority

The owner authorizes landing both PRs when green, factory first and adapter
second, through repository governance. No auto-approval envelope, required
check, protection rule, floor, disposition or policy is changed by this record.
