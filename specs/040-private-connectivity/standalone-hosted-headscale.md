# Standalone Hosted Headscale on openXsoft.com

**Status**: Draft

**Delivery owners**: openXsoft.com for entitlement and customer operations. OpsxFactory and the approved install owner for operational procedures and managed instance lifecycle.

**Authority**: [Feature specification](spec.md) and [ratified delta](../../openspec/changes/add-private-connectivity/specs/private-connectivity/spec.md), especially Standalone Hosted Headscale, Managed customer network isolation, and Approved connectivity and independent revocation.

## User Scenarios & Testing

1. **Given** an entitled customer with no factory subscription, **when** they request a network, **then** they receive a usable managed network and can authorize and revoke devices. Retrying a request with an uncertain outcome returns the original network.
2. **Given** two customer networks, **when** a customer or workload attempts cross-network enrollment, administration, a route change, or private traffic, **then** each attempt is denied. Production and non-production are separate by default.
3. **Given** an existing standalone network, **when** the customer authorizes a factory, **then** the factory uses that network and its individually approved access. When the attachment ends, its nodes and grants are revoked and other authorized devices retain access.
4. **Given** a failed instance, **when** the operator restores from backup, **then** the operator verifies network identity, approved grants, and current revocations before returning it to service. The other pilot customer's network remains available.

## Requirements

- **HS-01**: Customers MUST be able to acquire Hosted Headscale, provision and operate an entitled network, and manage authorized devices independently of factory enrollment or subscriptions.
- **HS-02**: Each customer trust boundary MUST have a dedicated Headscale instance, endpoint, durable state, keys, and policy. Sharing within an eligible boundary MUST identify the approving customer, participating installations, and each installation's access.
- **HS-03**: Before enrollment, apply explicit deny-by-default grants. Scope all managed actions to the authorized customer and network. Require separate approval for advertised subnet routes and reject expired or replayed enrollment credentials.
- **HS-04**: Track managed network entitlement separately from factory attachments. Removing an attachment or ending a factory subscription MUST revoke only its authorized access within the approved operating window. Terminating a managed network requires a separate authorized action and follows the approved recovery and data disposition policy.
- **HS-05**: The operator MUST be able to upgrade, back up, and recover one network in isolation. Recovery MUST reconcile current revocations before any recovered policy becomes effective.

## Success Criteria

- **HS-SC-01**: Two pilot customers each operate a standalone network without factory subscriptions. Repeated provisioning for the same operation creates no additional network.
- **HS-SC-02**: Every cross-customer access test is denied. An expired credential and a replay are denied. Authorized devices retain connectivity after a factory is detached.
- **HS-SC-03**: A managed recovery and upgrade qualification show that the recovered network honors prior grants and current revocations within the agreed operating window. The second customer's network remains available.
