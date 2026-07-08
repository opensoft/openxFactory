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
