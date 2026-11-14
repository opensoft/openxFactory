# Commission actual software-factory hosted connectivity profiles

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-hosted-domain-production](../../proposal.md).

## Purpose

Provide codeXfactory/codeXfactory's production behavior and verifiable source, release and qualification boundary while retaining neutral private-connectivity and rollout authority requirements.

## ADDED Requirements

### Requirement: Actual separate private and unbound profiles

The domain SHALL qualify its real MCP workload through distinct exact private and explicitly unbound profiles. Application authorization MUST remain independent of network membership and private application public ingress MUST be absent.

#### Scenario: Actual separate private and unbound profiles succeeds within scope
- **WHEN** an exact supported profile is selected under current authority
- **THEN** its own application/network path is tested

#### Scenario: Actual separate private and unbound profiles refuses invalid scope or proof
- **WHEN** a caller changes privacy or substitutes the synthetic pilot profile
- **THEN** production eligibility and binding are refused

### Requirement: Strict required production validation

Every production definition SHALL pass its closed schema and semantic/application-authority checks in required validation. Unknown kinds/fields, wrong scope and missing schema dependencies MUST fail.

#### Scenario: Strict required production validation succeeds within scope
- **WHEN** a complete supported definition is checked
- **THEN** actual schema/semantic collection is proven

#### Scenario: Strict required production validation refuses invalid scope or proof
- **WHEN** a dependency is absent or a kind would otherwise warn/skip
- **THEN** required validation fails

### Requirement: Exact protection and measured witnesses

Both exact production definitions SHALL receive definition-time protection, with only coupled witnesses/admissions derived by established producers. Broader exceptions, removed unrelated predicates and fabricated digest/count changes are prohibited.

#### Scenario: Exact protection and measured witnesses succeeds within scope
- **WHEN** the two reviewed paths are added
- **THEN** actual differential/witness tests prove them and preserve unrelated behavior

#### Scenario: Exact protection and measured witnesses refuses invalid scope or proof
- **WHEN** a broad prefix or unrelated predicate change appears
- **THEN** the protected-surface regression refuses it

### Requirement: Supported compatible profile release

The domain SHALL retain exact released workload/profile/schema and supported neutral/service/SDK identity with required atomic pin/vendor/lineage coupling. Actual application qualification remains required.

#### Scenario: Supported compatible profile release succeeds within scope
- **WHEN** the compatible candidate is published/read back
- **THEN** its content and required-CI/protection proof are independently verifiable

#### Scenario: Supported compatible profile release refuses invalid scope or proof
- **WHEN** a stale/unsupported pin or source-only result is offered as live proof
- **THEN** candidate closure or rollout acceptance remains blocked
