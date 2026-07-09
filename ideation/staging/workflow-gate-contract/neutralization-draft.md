# Staged: Workflow And Gate Contract Neutralization (DTN-001 + DTN-002)

Status: staged
Kind: architecture
Repository context: openxFactory
Source: [Domain Neutralization Candidate Register](../../../docs/domain-neutralization-candidate-register.md)
entries DTN-001 (neutral workflow contract schema) and DTN-002 (gate record
and outcome vocabulary) — promoted together because gate records exist only
inside workflow contracts; separate schemas would share every consumer.
Target capability: new `workflow-gate-contract` (delta: ADDED).
Evidence base: `AdxFactory/workflows/campaign-intake.yaml`,
`LedgerxFactory/workflows/client-intake.yaml`,
`MedxFactory/workflows/decision-foundation-loop.yaml`,
`codexFactory/workflows/branch-review.yaml`, plus the four domain gate docs.

## Claims (the neutral shape, extracted from convergent evidence)

1. Envelope: `schema_version` (int) + `kind` matching
   `<domain>_workflow_contract`. codexFactory's workflows currently omit the
   envelope — adoption includes adding it there.
2. `workflow` object: `id`, `display_name`, `owner_layer`, `purpose`,
   `triggers[]`, `inputs[]`, `outputs[]`, `gates[]`, `policy`, `audit`;
   optional `state_store` (Medx precedent).
3. Gate record (DTN-002): `id`, `owner_layer`, `requires[]`, and blocking
   declared through EITHER `blocks_on_failure: true` (Adx/Ledgerx/Medx
   style) OR `blocks_when[]` conditions (codex style) — the neutral schema
   admits both, requires at least one, and `produces[]` is optional.
4. `owner_layer` values: canonical roles (`customer`, `client`, `domain`,
   `xfactory`, `<domain>_omnigent`) or a layer id declared in the domain's
   `stack.yaml` hermes layers; free-invented layer names are a validator
   warning.
5. `policy` carries `agents_cannot[]` plus domain-named human-approval
   flags; `audit` carries `required` + `records[]`.
6. Domain-local exclusions (per the register): workflow names, domain
   triggers, evidence types, reviewer roles, action policies, gate names,
   professional thresholds, escalation roles — all stay in domain files;
   the neutral schema constrains shape only.

## Neutrality test plan

All four evidence workflows must validate against the neutral schema with
zero content changes beyond codexFactory's missing envelope — the origin
domains become consumers #1–#4 simultaneously.

## Exit

One OpenSpec change: `promote-workflow-gate-contract` (openxFactory) —
schema + vocabulary + validator + adoption tasks. Register entries DTN-001
and DTN-002 move `seed -> openspec` at proposal, `adopted` after domain
re-validation completes.
