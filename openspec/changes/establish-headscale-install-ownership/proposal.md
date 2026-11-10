---
code_surface: none
target_release: implemented
sequenced_after: [add-private-connectivity]
---

# Proposal: Establish Headscale install ownership

Status: ratified
Ratified: 2026-11-10 by Brett Heap. [Ratification record](review/ratification-2026-11-10.md)
Kind: proposal
Proposed: 2026-11-10

## Why

The [ratified private connectivity policy](../add-private-connectivity/proposal.md) assigns operating procedures to OpsxFactory and leaves the install repository subject to separate review. T001 needs an approved repository boundary and implementation scope for each owner.

## What Changes

- Propose private `opensoft/Headscale-Install` as the independently released install repository for customer-operated and managed Headscale.
- Retain OpsxFactory as the operational workflow owner. Keep entitlement and factory onboarding with the hosted product owner.
- Require a reviewed bootstrap and repository inventory admission before naming the proposed repository as an executable code surface. Aggregation admission, where sought, is a separate reviewed decision.
- Define the proposed bootstrap, install, operations, and qualification scopes for review.

## Capabilities

### New Capabilities

- `headscale-install-ownership` governs install custody, release qualification, and the OpsxFactory boundary.

### Modified Capabilities

None.

## Impact

This is the ownership decision packet. Repository bootstrap and runtime work require their own approved realization records. T001 records those approvals and executable scopes when they exist.
