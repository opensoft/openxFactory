# runtime-foundation Specification Delta

## ADDED Requirements

### Requirement: Probe endpoint
The runtime SHALL expose a probe endpoint.

#### Scenario: The probe answers
- **WHEN** the probe endpoint is called
- **THEN** it MUST answer with the runtime's readiness
