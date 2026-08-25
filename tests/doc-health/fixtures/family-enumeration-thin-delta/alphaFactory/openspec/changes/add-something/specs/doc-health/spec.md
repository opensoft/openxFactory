# doc-health Specification Delta

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twenty-one check families over
the whole factory family's governance corpus: status validity, and family
enumeration.
Every check in this pass MUST be deterministic. Four of the twenty-one —
alpha check, beta check, gamma check, and delta check — SHALL additionally read
the lifecycle scan set this capability declares; the other seventeen families
SHALL be computed from the governed corpus alone.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run
