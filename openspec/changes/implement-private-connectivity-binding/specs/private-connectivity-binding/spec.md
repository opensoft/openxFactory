## ADDED Requirements

### Requirement: Optional reference-only connectivity binding

The binding SHALL identify the installation, customer, environment, operator, endpoint, network, approval, and verification references. Enrollment secrets SHALL remain in credential custody. An installation without a binding SHALL retain its existing connectivity until authorized opt-in.

#### Scenario: An existing factory upgrades

- **WHEN** the installer upgrades an installation without a binding
- **THEN** its connectivity SHALL remain unchanged until an authorized operator selects a binding

### Requirement: Installer verifies the selected connection

xFactory-Installer SHALL support local install, an existing customer-operated endpoint, and an authorized managed network. It SHALL verify endpoint, enrollment authority, and effective approved access before activation.

#### Scenario: A candidate binding fails verification

- **WHEN** endpoint, authorization, enrollment, or policy verification fails
- **THEN** the candidate SHALL remain unready and the prior authorized state SHALL be preserved
- **AND** the error SHALL identify the failed stage without disclosing a secret

### Requirement: Redacted evidence verification

The feature checker SHALL validate required cases, tested revisions, approved thresholds, and prerequisite gate results against the feature evidence contract.

#### Scenario: Evidence is missing or superseded

- **WHEN** a required case, matching prerequisite, or approved revision is missing
- **THEN** the verifier SHALL reject the record and the gate SHALL remain unsatisfied
