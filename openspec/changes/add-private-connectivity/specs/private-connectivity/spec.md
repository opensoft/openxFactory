## ADDED Requirements

### Requirement: Local DomainxFactory connectivity choice

A self-hosted DomainxFactory installation SHALL support a customer-operated Headscale instance, including installing a new local instance or connecting to an existing one. It SHALL also support binding to a Hosted Headscale network authorized by the customer. Existing installations SHALL retain their current connectivity until an authorized operator selects a binding.

#### Scenario: Customer installs Headscale locally

- **WHEN** an authorized operator chooses local Headscale during a self-hosted factory installation
- **THEN** the installation SHALL support deploying Headscale in the customer environment and verifying enrollment and approved connectivity against that instance
- **AND** it SHALL complete without an openXsoft.com Headscale subscription or credentials

#### Scenario: Customer brings an existing network

- **WHEN** the operator supplies an existing customer-operated Headscale endpoint or selects an entitled Hosted Headscale network
- **THEN** the installation SHALL verify the selected endpoint and authorization before binding and enrolling
- **AND** an invalid endpoint or unauthorized selection SHALL leave private connectivity unavailable

### Requirement: Standalone Hosted Headscale

openXsoft.com SHALL offer Hosted Headscale independently of DomainxFactory subscriptions. An authorized customer SHALL be able to provision and operate an entitled network and later authorize a factory attachment to that same network.

#### Scenario: Customer uses Headscale without a factory

- **WHEN** an entitled customer requests a managed network without a DomainxFactory subscription
- **THEN** the service SHALL provision the network and support authorized node enrollment and revocation
- **AND** retrying the same provisioning operation SHALL resolve the same network

#### Scenario: Customer later attaches a factory

- **WHEN** the customer authorizes an eligible factory installation to join its existing managed network
- **THEN** the service SHALL bind that installation to the existing network and verify its approved access
- **AND** existing authorized devices SHALL retain their bindings

### Requirement: Hosted DomainxFactory availability

Every DomainxFactory SHALL have a hosted offering on openXsoft.com. A hosted installation that requires private connectivity SHALL use the common managed connectivity binding. Each domain SHALL qualify its hosted profile before customer release.

#### Scenario: Hosted factory needs private access

- **WHEN** an authorized customer requests a hosted DomainxFactory whose deployment requires private connectivity
- **THEN** onboarding SHALL provision or bind an authorized managed network and verify that the required private endpoints are reachable within the approved policy
- **AND** private endpoints SHALL remain outside public ingress

#### Scenario: New domain joins the hosted catalog

- **WHEN** a DomainxFactory is prepared for hosted availability
- **THEN** its hosted profile SHALL verify deployment, customer scoping, approved connectivity where needed, and lifecycle operations before customer release

### Requirement: Managed customer network isolation

Hosted Headscale SHALL allocate a dedicated Headscale instance, endpoint, durable state, keys, and policy to each customer trust boundary. It SHALL separate production and non-production by default. Sharing a network among factory installations SHALL require explicit approval by the customer with authority over that network.

#### Scenario: A customer attempts to cross a network boundary

- **WHEN** a customer or workload attempts enrollment, administrative action, or private traffic from one managed customer network into another customer's managed network
- **THEN** the service SHALL deny the action and prevent cross-boundary changes and private traffic

#### Scenario: Customer authorizes two factories on one network

- **WHEN** the customer explicitly approves two factory installations in the same trust boundary to use its managed network
- **THEN** both installations SHALL be bound to that network with only their individually approved access

### Requirement: Approved connectivity and independent revocation

The connectivity binding SHALL identify the installation, environment, operator mode, endpoint, and network reference without storing enrollment secrets. The operator SHALL authorize node enrollment and the allowed sources, destinations, and ports before activation. Managed networks SHALL apply explicit deny-by-default policy before enrolling workloads. Advertised subnet routes SHALL require separate approval scoped to the required destinations. The responsible operator SHALL be identifiable for policy, revocation, and recovery.

#### Scenario: Factory requests a private service

- **WHEN** an approved factory workload enrolls and the required connectivity is checked
- **THEN** it SHALL reach only the approved service and port under the managed policy
- **AND** failure to verify the approved policy SHALL leave the binding unready

#### Scenario: Factory attachment ends

- **WHEN** the customer removes a factory attachment or a factory subscription ends
- **THEN** the service SHALL revoke that installation's enrollment and access within the approved operating window
- **AND** other authorized bindings and any independently entitled Hosted Headscale network SHALL remain usable

#### Scenario: A managed instance needs recovery

- **WHEN** the operator restores a managed network from backup
- **THEN** the operator SHALL verify the recovered network identity, approved grants, and current revocations before returning it to service
- **AND** recovery SHALL preserve the isolation of other networks
