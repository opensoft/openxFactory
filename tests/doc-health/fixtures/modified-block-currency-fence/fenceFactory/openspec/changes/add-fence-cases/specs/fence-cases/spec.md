# fence-cases Specification Delta

## MODIFIED Requirements

### Requirement: A longer fence names the whole unit
The fence rule holds here.

**Removed from canon by add-fence-cases (2026-08-27):** ``An adapter that reaches a hosted provider SHALL obtain its credential through the `openxFactory` broker lane.`` — the credential clause moved to its own requirement

#### Scenario: The adapter runs
- **WHEN** the adapter reaches a hosted provider
- **THEN** it MUST use the broker lane

### Requirement: A single backtick names a fragment
The fence rule holds here too.

**Removed from canon by add-fence-cases (2026-08-27):** `An adapter that reaches a hosted provider SHALL obtain its credential through the `openxFactory` broker lane.` — the same clause, named with a single-backtick span that ends at its first inner backtick

#### Scenario: The other adapter runs
- **WHEN** the other adapter reaches a hosted provider
- **THEN** it MUST use the broker lane
