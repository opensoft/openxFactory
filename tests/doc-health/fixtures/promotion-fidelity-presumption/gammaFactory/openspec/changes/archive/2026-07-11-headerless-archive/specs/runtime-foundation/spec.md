# runtime-foundation Specification Delta

## ADDED Requirements

### Requirement: Tiered ingestion
The runtime SHALL ingest sources in declared tiers.

#### Scenario: A tier is ingested
- **WHEN** a tier becomes ready
- **THEN** its sources MUST be ingested in order
