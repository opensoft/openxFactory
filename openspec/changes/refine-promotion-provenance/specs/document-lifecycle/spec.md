## MODIFIED Requirements

### Requirement: Promotion process binding
Domain-to-neutral concept promotion and neutral-to-domain devolution SHALL
follow the documented promotion process, including candidate registration
with evidence, classification and scoring, OpenSpec ratification, and the
adoption steps (consumer re-pin, overlay replacement, local-copy retirement).
Register statuses SHALL be defined in terms of the canonical lifecycle
states. Neutralization drafts SHALL be produced by codexFactory
doc-engineering execution and approved by the originating domain's Hermes;
promotion provenance SHALL be machine-readable via optional `promoted_from`
and `specializes` declarations on the domain stack contract; and until a
promotion's re-pin gate completes, the domain-local copy SHALL remain
authoritative, with the register entry's status as the tiebreaker.

#### Scenario: A promotion is implemented
- **WHEN** a promoted neutral artifact merges into `openxFactory`
- **THEN** the promotion is not complete until each consuming DomainxFactory re-pins, replaces its local copy with a reference plus thin overlay, and the register entry reaches `adopted`
- **AND** a surviving domain-local near-duplicate MUST be reported as a health finding

#### Scenario: A neutral artifact proves domain-specific
- **WHEN** a neutral artifact is found to encode single-domain authority or vocabulary
- **THEN** a devolution MUST run the same lifecycle in reverse through an OpenSpec change, with the owning DomainxFactory adopting the content

#### Scenario: A neutralization draft is produced
- **WHEN** a promotion candidate is selected for drafting
- **THEN** codexFactory doc-engineering workers MAY produce the neutralization draft in openxFactory staging
- **AND** the originating domain's Hermes MUST review and approve the surrendered meaning before the OpenSpec change ratifies

#### Scenario: A promoted contract declares provenance
- **WHEN** a neutral artifact originates from a domain repo, or a domain overlay refines a neutral artifact
- **THEN** the consuming `stack.yaml` MAY declare `promoted_from` (origin repo and artifact) or `specializes` (refined neutral artifact)
- **AND** health tooling MUST verify that register entries at `adopted` status have resolvable provenance declarations where present

#### Scenario: A concept exists in both tiers mid-promotion
- **WHEN** a concept exists simultaneously in a domain repo and in openxFactory staging or an active change
- **THEN** consumers MUST treat the domain-local copy as authoritative until the re-pin gate completes
- **AND** the candidate register entry's status is the authoritative statement of promotion progress
