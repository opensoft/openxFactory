# doc-health — add-client-identity-roster deltas

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement sixteen check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, and client
identity roster composition. Every check in this pass MUST be
deterministic — identical inputs produce identical findings, with no model
calls; semantic analysis belongs to the agentic semantic sweep and the separate
document-cataloger and ideation-organizer lanes their owning capabilities
define. Check families SHALL implement promoted spec wording; staged ideation
fragments are inputs to contracts, never check definitions. The client
identity roster composition family SHALL cover only the CROSS-DOMAIN
concerns — assembling per-client fragments published by each domain and
reporting shared identity material or undeclared cross-domain reach —
because intra-repo roster conformance is a blocking domain gate rather than
an advisory report.

#### Scenario: A run executes the check families

- **WHEN** the deterministic pass runs over the family corpus
- **THEN** every implemented family reports findings or an explicit skip with a reason

#### Scenario: Roster composition is checked across domains

- **WHEN** two or more pinned domain repositories publish client identity roster fragments for the same client
- **THEN** the roster composition family assembles them and reports shared identity material or undeclared cross-domain reach
- **AND** intra-repo entry conformance is NOT reported here, because it fails the owning domain's gate instead
