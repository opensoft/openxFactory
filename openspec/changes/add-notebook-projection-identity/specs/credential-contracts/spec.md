# credential-contracts (delta) — add-notebook-projection-identity

## MODIFIED Requirements

### Requirement: The credential vault operator is an execution binding, never contract content

Who operates the worker-credential vault SHALL be a per-install execution binding following the client-infrastructure operating models — the operations factory where one is licensed, the client's own authorized IT channel where not — and the consuming lane SHALL be identical in both cases, receiving only bindings: an opaque secret reference and a fetch-identity identifier. Contract artifacts, lane definitions, and domain repositories SHALL NOT hard-code a vault operator, a vault product, or any secret value, and the bootstrap material for this pattern SHALL be reachable by a client licensing a single domain factory without the operations factory.

The same rule SHALL govern any OPERATED IDENTITY the family stands up on a third-party platform, not the credential vault alone. Who operates such an identity — an account, a tenant principal, or a hosted workspace the family's own tooling acts through — SHALL be a per-install execution binding following the same two operating models, and the consuming implementation SHALL be identical in both cases, receiving only a declared identifier for the identity it is to act as. Contract artifacts SHALL NOT hard-code the identity itself, its operator, or any credential for it. Custody is the general rule; the vault is its first instance.

Where the platform constrains what KIND of identity can be operated, that constraint SHALL be stated as part of the binding rather than left to the operator to rediscover. An operator-hosted binding SHALL name an identity the operating party administers under organizational policy, and SHALL NOT accept a personal identity merely designated as the organization's — a personal identity retains an individual recovery path, which is the failure both operating models exist to bound.

Both cases SHALL remain legitimate. Self-hosted operation by an individual or a client is not a degraded form of operator-hosted operation, and SHALL carry no obligation to stand up an organizational identity it has no operator for; the governance obligations that attach to the operator-hosted case attach because an operator exists to bear them.

#### Scenario: An operations-factory-operated install

- **WHEN** the install's execution binding is operations-factory-executed
- **THEN** that factory operates the vault, mints and rotates the token, and grants the fetch identity read on exactly the lane's secret — and the lane consumes bindings only

#### Scenario: A client-operated install

- **WHEN** the client licenses the domain factory without an operations factory
- **THEN** the client's authorized IT channel operates a vault of its choice under the same contract, no licensor identity performs the privileged acts, and the identical lane consumes the client's bindings

#### Scenario: An operated platform account is bound the same way

- **WHEN** an install must act on a third-party platform through an account the family stands up rather than through a vaulted credential
- **THEN** who operates that account is a per-install execution binding under this same rule, declared as an identifier the implementation consumes
- **AND** no contract artifact hard-codes the account, its operator, or any credential for it

#### Scenario: A personal identity is offered for the operator-hosted case

- **WHEN** an operator-hosted binding names a personal identity designated as the organization's rather than one the organization administers
- **THEN** the binding is refused, because the individual recovery path it retains is exactly what the operator-hosted case exists to remove

#### Scenario: A self-hosted install carries no organizational-identity obligation

- **WHEN** an individual operates their own install under the self-hosted model
- **THEN** their own identity is a complete and legitimate binding, and the operator-hosted case's governance obligations do not attach
