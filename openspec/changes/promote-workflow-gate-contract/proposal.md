# Promote Workflow Gate Contract

## Why

All five DomainxFactories independently converged on the same workflow
contract shape — envelope, workflow object, gate records, policy, audit —
but openxFactory publishes no neutral schema for it (DTN-001), and the gate
record vocabulary is drifting: codexFactory gates use `produces`/`blocks_when`
while the other domains use `blocks_on_failure`, and codexFactory omits the
`schema_version`/`kind` envelope entirely (DTN-002 evidence). This is the
`shared-contract-ownership` rule's textbook case: a shape governing behavior
across multiple factories MUST be canonically defined in
`openxFactory/contracts/`. Executing now exercises the freshly ratified
promotion rules (drafting/provenance/mid-promotion authority) on the two P0
register candidates.

## What Changes

- Add `contracts/schemas/xfactory-workflow.schema.yaml`: the neutral
  workflow contract envelope and workflow object (DTN-001).
- Define the gate record and outcome vocabulary inside it: `id`,
  `owner_layer`, `requires[]`, blocking via `blocks_on_failure` or
  `blocks_when[]`, optional `produces[]` (DTN-002) — admitting both observed
  styles rather than forcing a migration.
- Constrain `owner_layer` to canonical roles or layer ids declared in the
  domain's stack; unknown layers become validator warnings.
- Add `scripts/validate-workflow-contracts.py` validating any domain repo's
  `workflows/*.yaml` against the schema.
- Adoption (per the promotion process): each domain validates its workflows
  unchanged (except codexFactory adding the missing envelope), declares
  `promoted_from` provenance, and the register entries reach `adopted`.

## Capabilities

### New Capabilities

- `workflow-gate-contract`: neutral workflow contract schema, gate record
  and blocking vocabulary, owner-layer constraint, and adoption rules.

### Modified Capabilities

- None. (`shared-contract-ownership` placement rules already require this
  home; this change executes them.)

## Impact

- openxFactory: new schema, new validator, contract CHANGELOG v1.4 entry,
  register updates (DTN-001/002 `seed -> openspec -> adopted`).
- Domain repos (adoption phase, cross-repo tasks): codexFactory adds
  envelopes to its six workflow YAMLs; all five domains gain a
  `promoted_from` declaration; no domain content changes — the neutrality
  test is that all evidence workflows validate as-is.
- Doc-only-plus-schema change (no runtime); archives on artifact landing —
  the adoption tasks are completion criteria for `adopted` register status,
  not for archival, per the mid-promotion authority rule.
