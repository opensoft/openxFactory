# credential-contracts Specification

## Purpose

Define the canonical shapes of the five credential contract record kinds,
domain content locality, and grant accountability requirements.

## Requirements

### Requirement: Canonical credential record shapes
Credential contract records SHALL validate against the canonical
`contracts/schemas/xfactory-credential-contracts.schema.yaml`, which owns
the five record kinds: `xfactory_credential_requirements`,
`xfactory_runtime_capability_grant_template`,
`xfactory_credential_binding_template`,
`xfactory_credential_broker_contract`, and
`xfactory_credential_audit_policy`. Domain content — credential families,
scopes, providers, workflow and action names — is domain-local; the schema
constrains shape only, and semantic invariants remain owned by the
credential access model.

#### Scenario: A domain authors a credential contract
- **WHEN** a DomainxFactory adds or edits a file under `credentials/` carrying one of the five kinds
- **THEN** it MUST validate against the pinned canonical schema

#### Scenario: A file lacks the envelope
- **WHEN** a credentials file has no `kind`
- **THEN** the validator MUST report an error

#### Scenario: A domain policy record is present
- **WHEN** a credentials file carries a kind outside the five contract kinds
- **THEN** the validator MUST skip it with notice — such kinds are candidates for future promotion, not silent failures

### Requirement: Grant shape neutrality
The runtime capability grant SHALL express scope through neutral references
(job, domain, requirement, client, customer, allowed workflows and actions,
expiry, audit) and SHALL NOT require any single domain's nouns; a grant
without issuer, approver, expiry, and audit reference is invalid.

#### Scenario: A grant omits accountability fields
- **WHEN** a grant template lacks `issued_by`, `approved_by`, `expires_at`, or `audit_ref`
- **THEN** the validator MUST report an error

#### Scenario: Another domain issues grants
- **WHEN** a non-operations domain defines grant templates for its credential families
- **THEN** the same canonical shape applies with that domain's content
