# memory-gateway — add-ontology-stewardship-hardening deltas

## MODIFIED Requirements

### Requirement: Gateway Conformance Is Testable

The system SHALL provide conformance fixtures or checks for provider profiles,
rail denials, caller identity, credential custody, fail modes, break-glass,
context-packet metadata, packet leash behavior, expert context-packet
metadata, consent contract behavior, promotion review, revocation, erasure,
migration, and audit, mapped to the conformance tiers. Semantic-context
conformance fixtures SHALL be EXECUTED, never merely declared: each fixture
either carries a probe — a recorded mutation of the canonical example packet
that the canonical gateway validator applies and runs through its own
preflight, asserting the expected rejection — or names the exact existing
artifact or suite that executes the behavior, whose resolution the validator
verifies. A fixture that neither executes nor resolves its delegate SHALL
fail validation.

#### Scenario: Domain stack declares xFactory memory gateway provider

- **WHEN** a DomainxFactory declares an xFactory Memory Gateway provider profile
  or an Omnigent expert memory provider profile
- **THEN** validation MUST verify required ports, subject-safety rails,
  source-authority rails, prohibited content, companion stores, erasure
  capability, migration behavior, and example customer or expert
  context-packet behavior

#### Scenario: Domain stack declares gateway configuration

- **WHEN** a DomainxFactory stack.yaml declares a `memory_gateway` block
  (providers, per-layer-scope bindings, declared break-glass workflows,
  conformance tier)
- **THEN** the canonical conformance validator
  (`openxFactory/scripts/validate-domain-factory.py`) MUST validate the block
  against the gateway contract schemas, and MUST flag provider endpoints or
  connection references found inside Hermes overlay files as direct-binding
  violations

#### Scenario: A semantic-context fixture executes its promise

- **WHEN** a semantic-context conformance fixture carries a probe
- **THEN** the gateway validator applies the probe to the canonical example packet, runs the result through the same preflight it applies to examples, and fails unless the packet is rejected as the fixture promises

#### Scenario: A fixture delegates to an executed proof

- **WHEN** a fixture's behavior is executed elsewhere (a canonical negative fixture or a named test suite) rather than by an inline probe
- **THEN** the fixture names the executing artifact and the validator verifies it exists — a dangling delegate fails validation
