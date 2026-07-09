# workflow-gate-contract Specification

## Purpose

Define the neutral workflow contract schema, the gate record and blocking
vocabulary, the owner-layer constraint, and the adoption rules promoted from
convergent domain evidence (DTN-001, DTN-002).

## Requirements

### Requirement: Neutral workflow contract schema
Domain workflow contracts SHALL validate against the canonical
`contracts/schemas/xfactory-workflow.schema.yaml`: an envelope of
`schema_version` and `kind` matching `<domain>_workflow_contract`, and a
`workflow` object carrying `id`, `display_name`, `owner_layer`, `purpose`,
`triggers`, `inputs`, `outputs`, `gates`, `policy`, and `audit`, with
`state_store` optional. Domain nouns — workflow names, triggers, evidence
types, reviewer roles, thresholds — remain domain-local content the schema
constrains only in shape.

#### Scenario: A domain authors a workflow contract
- **WHEN** a DomainxFactory adds or edits a `workflows/*.yaml` contract
- **THEN** it MUST validate against the pinned neutral schema
- **AND** validation failures block the change in that domain's review flow

#### Scenario: A workflow omits the envelope
- **WHEN** a workflow file lacks `schema_version` or a `kind` matching the domain pattern
- **THEN** the validator MUST report an error

#### Scenario: Domain content stays local
- **WHEN** the neutral schema is revised
- **THEN** revisions MAY constrain structure and vocabulary but MUST NOT enumerate domain-specific workflow names, triggers, evidence types, or reviewer roles

### Requirement: Gate record and blocking vocabulary
Every gate record SHALL carry `id`, `owner_layer`, and `requires[]`, and
SHALL declare blocking behavior through `blocks_on_failure: true` or one or
more `blocks_when[]` conditions; `produces[]` is optional. A gate with no
blocking declaration is a validator error.

#### Scenario: Both observed styles validate
- **WHEN** a gate declares `blocks_on_failure: true` (Adx/Ledgerx/Medx style) or `blocks_when[]` conditions (codexFactory style)
- **THEN** both forms MUST validate without content migration

#### Scenario: A gate declares no blocking behavior
- **WHEN** a gate carries neither `blocks_on_failure` nor `blocks_when`
- **THEN** the validator MUST report an error naming the gate id

### Requirement: Owner layer constraint
Gate and workflow `owner_layer` values SHALL be canonical role names
(`customer`, `client`, `domain`, `xfactory`, or the domain's Omnigent
layer) or a layer id declared in that domain's `stack.yaml` Hermes layers;
any other value SHALL be reported as a validator warning.

#### Scenario: A gate names an undeclared layer
- **WHEN** a gate's `owner_layer` matches neither a canonical role nor a declared stack layer id
- **THEN** the validator MUST report a warning identifying the gate and the unknown layer

### Requirement: Adoption completion
The DTN-001/DTN-002 promotion SHALL be complete only when every domain's
workflow contracts validate against the pinned neutral schema, each
consuming domain declares `promoted_from` provenance for the schema, and
the register entries reach `adopted`; a domain-local competing workflow
schema surviving adoption SHALL be reported as a health finding.

#### Scenario: The neutrality test runs
- **WHEN** the neutral schema is implemented
- **THEN** the four evidence workflows (Adx campaign-intake, Ledgerx client-intake, Medx decision-foundation-loop, codex branch-review) MUST validate with no content changes other than codexFactory's added envelope

#### Scenario: Adoption stalls mid-promotion
- **WHEN** the schema is promoted but a domain has not completed re-validation
- **THEN** that domain's local workflow shape remains authoritative for it and the register entry status is the tiebreaker, per the promotion process
