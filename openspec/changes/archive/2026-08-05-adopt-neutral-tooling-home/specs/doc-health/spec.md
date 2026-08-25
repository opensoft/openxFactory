# doc-health Delta: Implementation Comes Home

## MODIFIED Requirements

### Requirement: Ownership and hosting split
The doc-health contract, report schema, and implementation SHALL all be owned by openxFactory
(checker scripts, report generator, and the reusable workflow move home
with the contract they follow); the nightly runner SHALL be hosted by the xFactory
aggregation repo as the only repo pinning every submodule; and content
authority SHALL stay with each owning factory — health tooling reports
and stages, it never approves or merges another factory's content.

#### Scenario: The pipeline changes shape

- **WHEN** a check family, report schema element, severity rule, or threshold default changes
- **THEN** the change MUST be an OpenSpec delta to this capability in openxFactory, and the in-repo implementation follows in the same change or a named successor

#### Scenario: A finding concerns a domain factory's content

- **WHEN** the ranked plan proposes work on a DomainxFactory's documents
- **THEN** the item enters that work as a staged proposal; approval remains with the owning factory's authority, and the health pipeline MUST NOT auto-apply content changes

#### Scenario: A neutral artifact cites the implementation

- **WHEN** a neutral schema, validator, or doc references a checker implementation file
- **THEN** the reference resolves inside openxFactory itself — a neutral artifact citing a domain-repo implementation path is a conformance defect of this capability
