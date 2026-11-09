# Design: Add private connectivity

Status: ratified
Ratified: 2026-11-09 by Brett Heap. [Ratification record](review/ratification-2026-11-09.md)

## Context

The [runtime binding plan](../../../docs/self-hosted-runtime-binding-plan.md) already distinguishes where the application runs and gives self-hosted installations a guided binding flow. Extend that flow with a separate connectivity choice. Follow the [install repository boundary](../../specs/repo-boundary-governance/spec.md) for runtime ownership and reviewed aggregation admission.

## Goals / Non-Goals

**Goals.** Give local installations a customer-operated or managed Headscale choice, sell managed networks independently, and give every hosted DomainxFactory a common way to request private connectivity.

**Non-goals.** This packet leaves pricing, infrastructure placement, repository creation, and commercial service commitments to their own decisions. The initial integration uses Headscale and a qualified set of clients. Compatibility with other control servers is outside this proposal.

## Decisions

### Bind the network separately from the factory deployment

A factory installation records its deployment environment and an optional connectivity binding. The binding identifies the operator mode, approved control endpoint, installation and environment, and a stable network or binding reference. Local enrollment uses authorization supplied by the local operator. Managed enrollment uses a customer-authorized reference to a provisioned network. Resolve short-lived enrollment credentials through the existing credential path and keep them out of the binding, logs, and support artifacts.

A local deployment offers install-new and connect-existing paths for customer-operated Headscale. A hosted factory provisions or selects an authorized managed network when private access is required. Each factory declares source identities, destinations, and ports. Approval, node enrollment, and effective policy verification are separate steps. Retrying setup resolves the same approved network and operation instead of provisioning another instance.

### Separate managed provisioning from each customer's network

Headscale serves a single tailnet per instance. The proposed openXsoft.com provisioning service uses one Headscale instance per customer trust boundary, with a dedicated endpoint, isolated durable state, keys, policy, and recovery scope. Production and non-production use separate networks by default. One customer can deliberately share a network across its factories if the approval identifies those installations and their allowed traffic. A common administrative service can manage the fleet with authorization checked against the customer and network on each operation. [Headscale design goals](https://headscale.net/stable/about/faq/)

Start each network with explicit deny-by-default grants before enrollment. Use narrowly scoped, short-lived, single-use credentials for managed workload enrollment. Gate subnet routes separately from node access. Keep Headscale service administration with the instance operator and expose customer actions through scoped authorization. Verify granted access and denied access with real clients. [Headscale policy](https://headscale.net/stable/ref/policy/) · [Headscale registration](https://headscale.net/stable/ref/registration/) · [Headscale routes](https://headscale.net/stable/ref/routes/)

### Keep the managed network subscription independent

Represent the managed network separately from factory installations. A factory attachment records which installation may use which approved network. The same network can outlive a factory attachment. Removing an attachment revokes the factory's nodes and grants while preserving other authorized nodes and bindings. Service termination follows a separate customer-authorized process, with recovery and data disposition handled by the service operator.

## Risks / Trade-offs

- Each managed instance adds operating work. Qualify repeatable provisioning, upgrade, backup, restore, and recovery before commercial rollout. Test recovery of one network without affecting another.
- Endpoint changes may require node re-enrollment. Treat a change of control server as a planned cutover with verified client behavior, source revocation, and rollback steps. Keep migration credentials scoped to the approved cutover.
- Factory software, client software, and site networking may fail independently. Qualify the supported client platforms, DNS, direct and relayed connectivity, and upstream upgrades. Preserve existing tenant application authorization when network access succeeds.

## Migration Plan

Existing factory installations adopt the binding by explicit opt-in. Start with a pilot that provisions Hosted Headscale for a customer without a factory subscription, attaches a local factory to that network, then qualifies customer-operated Headscale and a hosted factory deployment. Use a second managed customer to test enrollment, route, administration, and traffic isolation. Demonstrate credential expiry, detachment, recovery, and a control endpoint change with rollback. Onboard additional domains using the same hosting flow and their own readiness evidence.

## Open Questions

Successor changes will select the hosted runtime platform and regions, relay ownership and placement, identity integration, fleet capacity and recovery targets, and the first pilot domains. Launch decisions will set service commitments after those choices are qualified.
