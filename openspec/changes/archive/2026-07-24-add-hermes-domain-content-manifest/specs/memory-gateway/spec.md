# memory-gateway — Spec Delta (memory-binding record schema)

## ADDED Requirements

### Requirement: Derived memory bindings validate against the neutral schema
A `hermes_memory_binding` record — the normalized, gateway-vocabulary-expressed projection of a layer's seeded memory boundary that the gateway's rails consume — SHALL validate against the neutral memory-binding schema: `layer_role`, `scopes[]` with per-scope `subject_scope` and an optional promotion block whose `gateway` MUST be `customer_memory_gateway` and whose `accepted_authority_level` MUST be drawn from the ratified `authority_levels` vocabulary, `denied_scopes[]`, `invariants[]`, `derived_from: memory_boundary`, and `vocabulary_bundle_tag` provenance — and a binding declaring a provider endpoint, credential, or any raw secret SHALL fail validation (a binding is rails input, never a provider binding and never a store).

#### Scenario: A live-derived domain binding validates
- **WHEN** the binding derived from the domain's memory boundary (cross-tenant learning scope with the `reviewed` cap, `client_private` denied) is validated
- **THEN** it passes the canonical validator

#### Scenario: A foreign authority level fails validation
- **WHEN** a binding's promotion block carries an `accepted_authority_level` outside the ratified `authority_levels` vocabulary
- **THEN** the canonical validator rejects it naming the level

#### Scenario: A provider or secret surface fails validation
- **WHEN** a binding declares a provider endpoint or credential-bearing field
- **THEN** the canonical validator rejects it — provider bindings and grants live in the gateway's own binding layer, never in a derived boundary record
