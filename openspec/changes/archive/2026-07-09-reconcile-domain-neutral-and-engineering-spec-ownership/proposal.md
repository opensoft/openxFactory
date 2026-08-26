Status: ratified
Ratified: 2026-07-09 — record: the promoting act, commit `d5ada44` (2026-07-08, "Reconcile domain-neutral spec ownership"), which proposed this change and applied its spec delta into `openspec/specs/canonical-policy-migration/spec.md`, `openspec/specs/repo-boundary-governance/spec.md`, `openspec/specs/shared-contract-ownership/spec.md` in that same commit; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. STATED PRECISELY, because this record's shape is unusual: the archive act itself, commit `a195244` (2026-07-09, "Archive five implemented OpenSpec changes and promote capabilities"), moved the folder to archive ONE DAY LATER and promoted nothing further — its own body says so, "reconcile deltas were already synced". The by-construction reasoning still holds; only the promoting act and the archive act are one day apart, and the date recorded here is the archive act's, consistent with this backfill's dating convention. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

Current `openxFactory` documentation says engineering-specific Spec Kit and PR
admission policy moved to `codexFactory`, but promoted OpenSpec specs still say
`openxFactory` owns canonical Spec Kit stage ownership and PR admission policy.
That mismatch makes the hard spec contradict the intended domain-neutral split.

This change makes OpenSpec, prose docs, and domain conformance checks agree:
`openxFactory` owns the neutral workflow rail, while DomainxFactories own their
domain-specific execution mechanics.

## What Changes

- Clarify in hard specs that `openxFactory` owns domain-neutral gates,
  traceability, authority boundaries, admission concepts, and cross-factory
  contracts.
- Clarify that DomainxFactories own domain-specific execution policy and
  artifacts, including `codexFactory` owning software engineering Spec Kit flow,
  branch review, PR admission packet implementation, and merge readiness packet
  implementation.
- Narrow `openxFactory` prose docs that currently embed software-specific
  mechanics into neutral contracts or pointers.
- Add machine-readable `codexFactory` workflow gate YAML so engineering workflow
  contracts are not prose-only.
- Add the missing `codexFactory` tenant example and memory gateway scaffold
  required by strict domain validation.
- Promote and archive the completed memory-gateway OpenSpec change so its hard
  requirements live under canonical specs rather than an active change folder.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `canonical-policy-migration`: Replace the obsolete requirement that
  `openxFactory` owns software-specific Spec Kit and PR admission policy with a
  domain-neutral ownership rule and explicit DomainxFactory specialization rule.
- `repo-boundary-governance`: Clarify that new policy affecting multiple systems
  belongs in `openxFactory` only when the policy is domain-neutral or
  cross-factory; domain execution details belong in the owning DomainxFactory.
- `shared-contract-ownership`: Clarify that `openxFactory` owns shared contract
  homes and compatibility rules, while domain-specific packet formats and
  workflow gate implementations can live in the owning DomainxFactory when they
  preserve upstream references.

## Impact

- Updates OpenSpec requirements under `openspec/specs/`.
- Updates domain-neutral docs under `docs/`.
- Updates `codexFactory` workflow and stack metadata under the top-level
  aggregation checkout.
- Archives/promotes the completed `add-customer-memory-gateway-architecture`
  change.
- No runtime code, credentials, generated workspaces, or submodule pointer
  changes are in scope.
