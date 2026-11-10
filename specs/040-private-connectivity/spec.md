# Feature Specification: Private connectivity for DomainxFactory

**Feature Branch**: `040-private-connectivity`

**Created**: 2026-11-10

**Status**: Draft

**Input**: Specify local Headscale, standalone Hosted Headscale, and hosted DomainxFactories on openXsoft.com.

**Governed by**: [Ratified add-private-connectivity proposal](../../openspec/changes/add-private-connectivity/proposal.md) and [requirements](../../openspec/changes/add-private-connectivity/specs/private-connectivity/spec.md), landed in [PR #1300](https://github.com/opensoft/openxFactory/pull/1300).

## User Scenarios & Testing

### User Story 1 - Connect a self-hosted factory (Priority: P1)

A customer operator installs Headscale locally, connects to an existing customer-operated server, or selects an authorized openXsoft.com network. The operator gets a verified connection to the service the factory needs.

**Independent test**: Run all three choices at a synthetic customer site and verify the approved connection. Test an invalid endpoint, an interrupted setup, and a factory with no binding. [Local Headscale acceptance scenarios](local-headscale.md)

### User Story 2 - Operate a managed network independently (Priority: P1)

An openXsoft.com customer provisions Hosted Headscale, enrolls and revokes devices, and can later authorize a factory to join the same network.

**Independent test**: Use two synthetic customers without factory subscriptions. Provision and operate a network for each, verify isolation, and attach and detach a factory from one network. [Standalone Hosted Headscale acceptance scenarios](standalone-hosted-headscale.md)

### User Story 3 - Use a hosted factory with private access (Priority: P2)

A customer deploys a DomainxFactory on openXsoft.com and authorizes the factory to use a managed network when private access is required.

**Independent test**: Onboard a hosted domain with a new network and with an existing network. Verify approved access, denial of public ingress, and application authorization. [Hosted DomainxFactory acceptance scenarios](hosted-domainxfactories.md)

### Edge Cases

- A retry after a partial provision or enrollment must reconcile the same authorized operation.
- Expired credentials, replay, and ineffective policy must leave the affected binding unready.
- Recovery and rollback must honor current revocations.
- Installations without a connectivity binding retain their current behavior until an operator opts in.

## Requirements

### Functional Requirements

- **FR-001**: Record factory hosting mode separately from the optional connectivity binding. A binding MUST identify the installation, environment, operator mode, approved control endpoint, and stable network or binding reference.
- **FR-002**: A factory MUST declare the source identities, destinations, and ports it requires. Approval, enrollment, and effective policy verification MUST each succeed before a binding becomes ready. Subnet route approval MUST be separate and scoped to required destinations.
- **FR-003**: Resolve enrollment secrets through the existing credential path. Keep secret values out of bindings, logs, and support artifacts. Managed workload enrollment MUST use short-lived, single-use credentials scoped to the approved attachment.
- **FR-004**: Identify the operator responsible for policy, revocation, and recovery. Associate approval and verification evidence with the installation and network.
- **FR-005**: Each offering MUST meet its track specification and the ratified requirements. Private connectivity MUST preserve application-level authorization.

### Key Entities

- **Factory installation**. A deployed instance with a client, domain, environment, and hosting mode.
- **Connectivity binding**. An approved association between an installation and a network, with a verification status.
- **Managed network and entitlement**. A customer trust boundary and the independent right to operate its network.
- **Factory attachment**. An authorization for one installation to join a managed network, with the access and enrolled nodes subject to revocation.

## Success Criteria

- **SC-001**: All four offering paths pass the pilot acceptance tests. The paths are a local factory with customer-operated Headscale, a local factory with Hosted Headscale, standalone Hosted Headscale, and a hosted DomainxFactory.
- **SC-002**: Across two synthetic customers, all tested unapproved enrollment, administrative action, route, and private traffic attempts are denied.
- **SC-003**: The pilot records verified detachment, recovery, and endpoint migration with rollback. Operators measure the outcomes against approved windows before launch.

## Assumptions and ownership

openxFactory owns the neutral runtime binding and verification. DomainxFactory owners declare access and qualify their hosted profiles. OpsxFactory owns operating procedures. The proposed `Headscale-Install` repository requires its own repository decision. openXsoft.com owns entitlement, managed provisioning, and hosted factory delivery.

These specifications share one Speckit feature. Each runtime successor retains its own authorization, implementation plan, and release evidence. Planning will select the pilot domains, infrastructure, identity and relay arrangements, operating windows, and capacity targets before the relevant pilot or launch.
