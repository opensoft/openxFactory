---
code_surface: openxFactory, xFactory-Installer
target_release: deferred-allocation
sequenced_after: [add-private-connectivity]
---

# Proposal: Implement the private connectivity binding

Status: draft
Kind: proposal
Proposed: 2026-11-10

## Why

The ratified [private connectivity policy](../add-private-connectivity/proposal.md) assigns the neutral binding to openxFactory. The operator selected `opensoft/xFactory-Installer` to realize the installer flow on 2026-11-10. This proposal gives those responsibilities explicit implementation and release boundaries.

## What Changes

- Publish an optional, versioned binding and conformance cases in openxFactory. Keep approval, enrollment, and verification distinct and use credential references for enrollment.
- Implement local install, existing customer-operated instance, and managed network selection in xFactory-Installer. Preserve unbound installations and require explicit opt-in.
- Scope the feature-local evidence checker and self-tests to redacted gate records for feature 040.
- Capture approval, file scope, release target, and verification for T001 before implementation.

## Capabilities

### New Capabilities

- `private-connectivity-binding` defines the neutral binding, installer behavior, and evidence validation boundary.

### Modified Capabilities

None.

## Impact

openxFactory publishes the additive contract at the next applicable bundle cut, with the exact version assigned at realization. xFactory-Installer consumes an approved pilot pin and then the published bundle before customer release. Headscale packaging, managed service operations, and hosted product delivery follow the sibling proposals.
