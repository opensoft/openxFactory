## ADDED Requirements

### Requirement: Approved repository casing preserves disposition scope

The disposition reader SHALL recognize only the approved compatibility pairs
`codexFactory` / `codeXfactory` and `openxFactory` / `openXfactory` when matching
repository scope. It MUST preserve original record bytes and the observed
identity in reports, exact finding matching, duplicate refusal and whole-corpus
staleness detection. Other names MUST retain their existing exact-match behavior.

#### Scenario: Approved current spelling reads legacy scope
- **WHEN** a current approved spelling validates a finding covered by the legacy spelling's disposition
- **THEN** the existing exception applies with its original authority and citation, without rewriting it

#### Scenario: Current and legacy entries duplicate one finding
- **WHEN** both approved spellings declare a disposition for the same item, path and finding
- **THEN** the reader refuses the duplicate rather than retaining an invisible extra exception

#### Scenario: Missing finding remains stale through a casing alias
- **WHEN** a whole-corpus scan uses an approved spelling and its in-scope exception no longer matches a finding
- **THEN** the reader reports that exception as stale

#### Scenario: Unapproved name remains a distinct scope
- **WHEN** a different, suffix-expanded, unlisted case variant or Unicode lookalike names the repository
- **THEN** it gains no compatibility alias and cannot consume the approved pair's exception
