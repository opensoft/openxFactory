# roles-authority-model Specification

## Purpose

Define neutral ownership of the cross-factory authority model and the
requirement that each DomainxFactory instantiate its execution lead roles
as a declared specialization.

## Requirements

### Requirement: Neutral authority model ownership
`openxFactory` SHALL own the cross-factory authority model: the authority
layers, Hermes-level governance roles (project ownership, sequencing,
system and project architecture, merge readiness and merge authority),
escalation principles, and external enforcement concepts — expressed
without any single domain's execution roles, group names, or tooling.

#### Scenario: The neutral roles doc is revised
- **WHEN** `docs/roles-and-authority.md` changes
- **THEN** it MUST NOT define domain execution lead roles, domain-specific escalation routes, or deployment group names — those belong to the owning DomainxFactory

### Requirement: Domain execution role instantiation
Each DomainxFactory SHALL instantiate its execution lead roles — the
domain-side counterparts that decompose, implement, verify, integrate, and
secure approved work — in its own documentation, declared as a
specialization of the neutral model.

#### Scenario: Engineering roles are defined
- **WHEN** software engineering execution roles are defined or revised
- **THEN** the canonical text lives in `codexFactory/docs/engineering-roles-and-authority.md`
- **AND** codexFactory's stack.yaml declares `specializes` for the roles model

#### Scenario: Another domain instantiates roles
- **WHEN** a non-engineering DomainxFactory defines its execution roles
- **THEN** it follows the same pattern in its own repository and MUST NOT edit the neutral model to add its roles
