# ideation-dashboard

## ADDED Requirements

### Requirement: Convergent lens regions draft candidate-register seeds
The dashboard SHALL draft a domain-neutralization candidate-register seed from a repository-lens region carrying two or more repositories, because such a region is the promotion process's first candidate rule — two or more domain repositories carrying the same structure — computed rather than eyeballed. A region with a single carrier SHALL NOT be draftable and SHALL say why. The draft SHALL be produced in the register's own format: a Candidate List row and a `### DTN-NNN:` detail section, numbered past every identifier the register mentions so a drafted-but-unmerged seed never collides, quoting the rule it satisfies and listing each identity with its carriers as the evidence — the carrier set IS the evidence for this rule, so the draft SHALL be deterministic and involve no model judgment.

The drafting SHALL write nothing. The register is never opened for writing and a candidate enters the register lifecycle only when a human merges the seed, which is the same seed-first discipline the machine-drafted intake path already records; because nothing is written, the affordance SHALL remain available on a composed read-only view and SHALL NOT claim a gate capability. The evidence SHALL be recomputed by the serving side from its own composed view — the client names the project, the visible member set, and the region's carrier combination, never the identities — and a seed SHALL cover exactly the region it was drafted from rather than everything the wider visible set happens to share.

#### Scenario: A convergent region drafts a seed
- WHEN a human drafts from a lens region whose identities two or more repositories carry
- THEN the response is a register-format row and detail section naming those identities and their carriers, numbered from the register's own numbering
- AND the register file is unchanged

#### Scenario: A seed covers exactly its region
- WHEN the region is a sector naming an exact repository combination
- THEN the drafted seed covers the identities whose carriers are exactly that combination, and no others

#### Scenario: A single-carrier region cannot be drafted
- WHEN a region's identities are carried by only one repository
- THEN the draft affordance is unavailable and states that a candidate needs two or more carriers

#### Scenario: A plane that cannot compose has no candidates
- WHEN the drafting route is asked about a project with no composed view
- THEN it refuses and names the project, rather than drafting from a single repository's documents
