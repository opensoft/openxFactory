# doc-health Specification

## Purpose
Fixture canon for the family enumeration check.

## Requirements
### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twenty-one check families over
the whole factory family's governance corpus: status validity, staged-topic template, standard backing, ratified provenance, succession integrity, location conformance, record immutability, staged/candidate aging, register-lifecycle consistency, tag hygiene, submodule pin drift, contract-copy drift, notebook projection drift, document catalog, ideation routing, proposal origin, client identity roster composition, promotion fidelity, release-inventory drift, duplicate packet, and family enumeration.
Every check in this pass MUST be deterministic. Four of the twenty-one —
alpha check, beta check, gamma check, and delta check — SHALL additionally read
the lifecycle scan set this capability declares; the other seventeen families
SHALL be computed from the governed corpus alone.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run
- **AND** every family MUST run as its owning requirement defines

#### Scenario: A second scenario nobody may destroy
- **WHEN** a delta restates this requirement
- **THEN** it MUST restate this scenario too
