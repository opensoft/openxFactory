# Local Headscale and self-hosted DomainxFactory

**Status**: Draft

**Delivery owners**: openxFactory runtime binding, the local Headscale install owner, and the customer operator.

**Authority**: [Feature specification](spec.md) and [ratified delta](../../openspec/changes/add-private-connectivity/specs/private-connectivity/spec.md), especially Local DomainxFactory connectivity choice and Approved connectivity and independent revocation.

## User Scenarios & Testing

1. **Given** a local factory and no existing network, **when** the operator chooses local Headscale, **then** setup supports installing it in the customer environment and verifies the approved service connection without an openXsoft.com subscription or credentials.
2. **Given** an existing customer-operated instance, **when** the operator supplies its endpoint and authorized enrollment, **then** setup verifies both and enrolls the installation. An invalid endpoint or authorization leaves the binding unready.
3. **Given** a local factory and an entitled managed network, **when** the customer approves the attachment, **then** setup binds to the selected network and verifies the requested access. [Standalone service](standalone-hosted-headscale.md)
4. **Given** an interrupted setup after enrollment, **when** the operator retries, **then** setup reconciles the existing enrollment and reports any remaining operator action.
5. **Given** a working binding, **when** the operator changes the control endpoint, **then** setup verifies the replacement and revokes obsolete access at cutover. A failed cutover can restore the last binding if it remains authorized and removes any partial replacement access.

## Requirements

- **LC-01**: Offer install-new, connect-existing, and managed network selection. Preserve unbound installations across upgrades and reruns.
- **LC-02**: Verify the selected endpoint and enrollment authorization before enrolling. The customer operator controls local policy, routes, credentials, and recovery.
- **LC-03**: Before activation, verify the approved service and port and test denial of at least one unapproved destination or port. Report the failed step without exposing secrets.
- **LC-04**: Treat endpoint changes, retry, rollback, and detachment as authorized operations. Keep the old binding until the replacement is verified and the cutover commits or an authorized operator revokes it.

## Success Criteria

- **LC-SC-01**: Each of the three local setup paths passes. Both customer-operated paths succeed without a hosted entitlement.
- **LC-SC-02**: All negative cases leave the attempted binding unready. A retry produces one effective attachment for the operation.
- **LC-SC-03**: Demonstrate a successful endpoint change and a failed change with verified rollback and revocation of partial access.
