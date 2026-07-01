# Domain Repo Review Improvements

Status: shared xFactory template review
Repository context: openxFactory
Purpose: capture what the sibling domain repos teach the openxFactory starter
template.

## Reviewed Repos

- `AdxFactory`
- `LedgerxFactory`
- `MedxFactory`
- `OpsxFactory`
- `openCodexFactory`

## What The Repos Show

`AdxFactory` and `LedgerxFactory` are strong concept stacks. They show that a
new domain factory needs narrative docs that explain the domain boundary,
Hermes model, workflow gates, and Omnigent behavior before implementation
details are complete.

`MedxFactory` is a deeper domain implementation. It shows that profiles,
schemas, templates, and a local validation command should appear early because
they turn a concept repo into an implementation target.

`openCodexFactory` is the clearest executable example. It shows that workflows
become understandable when backed by example artifacts, golden-path flows,
schema files, and validation scripts.

`OpsxFactory` is the credential-heavy test stack. It shows that the starter
must generate credential requirements, a broker contract, binding templates,
runtime grant templates, policy files, and a rerun report without ever creating
raw credentials.

## Template Improvements

The starter template now creates:

- a `Makefile` with a `validate` target
- narrative docs for domain overview, customer Hermes model, workflow gates,
  and Omnigent constitution
- example read-only and privileged workflows
- credential broker, binding, grant, audit, approval, rotation, and revocation
  surfaces
- schema descriptors for stack, workflow, and credential requirements
- an `examples/` area with a golden-path folder
- a pre-run questionnaire, setup runbook, and example answers file
- simulated pre-run answer records for the existing domain repos
- a validation script that checks required files, parses YAML, checks basic
  cross-file references, and scans for common secret patterns
- an idempotent starter rerun report

## Template Rules

The starter should:

- create missing generic surfaces
- preserve existing domain-owned files
- add missing README implementation links without replacing the README
- validate what it can safely validate
- require pre-run answers before implementation or instantiation proceeds
- label inferred answers and implementation gaps before any real instantiation
- report missing domain work instead of guessing it

The starter should not:

- infer real provider scopes
- create live tenant bindings
- create OAuth consent records
- write raw credentials
- make domain-specific legal, clinical, financial, marketing, or operational
  authority decisions
