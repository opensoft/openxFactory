# Hosted DomainxFactories on openXsoft.com

**Status**: Draft

**Delivery owners**: openXsoft.com for catalog, hosting and onboarding. Each DomainxFactory owner for its access declaration and hosted profile qualification.

**Authority**: [Feature specification](spec.md) and [ratified delta](../../openspec/changes/add-private-connectivity/specs/private-connectivity/spec.md), especially Hosted DomainxFactory availability and Approved connectivity and independent revocation.

## User Scenarios & Testing

1. **Given** an entitled customer selecting a hosted domain that requires private connectivity, **when** onboarding reaches network setup, **then** it provisions a managed network or binds to an authorized existing one and verifies the approved private endpoints before reporting readiness.
2. **Given** a customer with an existing standalone managed network, **when** the customer authorizes a hosted factory to use it, **then** the factory joins that same eligible network. Access requires both a network grant and the private application's own authorization.
3. **Given** a deployment that requires private access, **when** its policy, enrollment, or connectivity test fails, **then** onboarding reports the failed step and keeps private endpoints outside public ingress. A retry reconciles the same approved deployment and attachment.
4. **Given** a new domain candidate or an existing hosted profile with material changes, **when** the domain owner requests customer release, **then** the catalog requires that domain's deployment, tenant scoping, connectivity where needed, and lifecycle evidence.

## Requirements

- **HD-01**: Every DomainxFactory MUST have a hosted offering through the common openXsoft.com onboarding path. Publish each domain for customer use after its own hosted profile qualifies.
- **HD-02**: A hosted installation that requires private access MUST use the managed connectivity binding. Verify entitlement and customer approval for either a new or an existing network. A hosted installation with no private access requirement can complete onboarding without a connectivity binding.
- **HD-03**: Domain owners MUST declare the minimum source identities, destinations, and ports required. The onboarding flow MUST verify effective access, cross-customer denial, and absence of public ingress for private endpoints before release.
- **HD-04**: Hosted profile qualification MUST verify installation, tenant scoping, applicable connectivity, and lifecycle operations. Hosted factory detachment MUST revoke its access independently of the underlying managed network entitlement.
- **HD-05**: The customer MUST be able to identify the failed step if onboarding stalls. Repeated requests MUST preserve the approved installation and attachment identity and avoid duplicate network provisioning.

## Success Criteria

- **HD-SC-01**: A pilot domain qualifies both new-network and existing-network onboarding. Approved services are reachable privately and public access to those endpoints is denied.
- **HD-SC-02**: Every pilot request from the wrong customer is denied. A permitted network path with missing application authorization is denied by the application.
- **HD-SC-03**: The hosted catalog can distinguish qualified domains from domains pending evidence. A factory retirement test revokes its access and preserves independent network use.
