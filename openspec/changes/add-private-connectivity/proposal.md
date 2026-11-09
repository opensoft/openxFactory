---
code_surface: none (This packet establishes the product and repository boundaries. Runtime changes are realized under separately governed successor changes.)
target_release: implemented (The policy is realized when the approved requirements are promoted. Each runtime successor owns its own release.)
sequenced_after: []
---

# Proposal: Add private connectivity

Status: ratified
Ratified: 2026-11-09 by Brett Heap. [Ratification record](review/ratification-2026-11-09.md)
Kind: proposal
Proposed: 2026-11-09

## Why

Every DomainxFactory will be available as a hosted offering on openXsoft.com. Customers installing a factory on their own infrastructure need the choice of running Headscale locally or using openXsoft.com Hosted Headscale, which must also be available to customers who buy it on its own.

## What Changes

- Add an optional private connectivity binding per DomainxFactory installation. Customers running a factory locally can install Headscale locally, connect to an existing customer-operated instance, or bind to an authorized Hosted Headscale network.
- Offer Hosted Headscale on openXsoft.com independently of any DomainxFactory subscription. Allow an authorized customer to attach a factory to an existing managed network later.
- Make every DomainxFactory available as a hosted offering on openXsoft.com, with managed private connectivity available when needed. Introduce domains through a shared hosting and onboarding model, with separate readiness evidence for each domain.
- Establish a managed network boundary per customer trust boundary. Separate production and non-production by default. Require explicit approval before installations share a network.
- Set ownership and acceptance criteria for factory integration, Headscale installation and operations, and openXsoft.com product delivery.

## Capabilities

### New Capabilities

- `private-connectivity` covers local and managed Headscale, independent hosted service entitlement, DomainxFactory runtime bindings, and network isolation and lifecycle.

### Modified Capabilities

None.

## Impact

- **openxFactory** owns the neutral rules for connectivity requests, binding, enrollment, verification, revocation, and the hosted DomainxFactory integration. The existing runtime binding flow is the integration point. A successor will define any released schema or installer changes.
- **DomainxFactory repositories** declare the access their workloads require and qualify their own hosted profiles.
- **OpsxFactory** owns the operations workflow. A separately approved install surface, proposed as `Headscale-Install`, would own repeatable local deployment and managed Headscale installation, upgrades, recovery, and verification.
- **openXsoft.com** owns the service catalog, customer entitlement, onboarding, managed network provisioning, and hosted DomainxFactory delivery. Deployment repository placement and any aggregation admission are successor decisions.
- This packet proposes requirements and acceptance criteria. The implementation releases, service pricing, and launch commitments each have their own decision path.
