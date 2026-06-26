# FEAT-MIG-005 Shared Contract Migration Evidence

Decision: READY FOR PR ADMISSION

## Sources Reviewed

- `/home/brett/projects/Agents/Omnigent-Install/schemas/`
- `/home/brett/projects/Agents/Omnigent-Install/policies/hermes-governance-agents.yaml`
- `/home/brett/projects/Agents/Omnigent-Install/policies/merge-risk-policy.yaml`
- `contracts/README.md`
- `openspec/changes/migrate-canonical-policy-to-openworkflow/specs/canonical-contract-migration/spec.md`
- `openspec/changes/migrate-canonical-policy-to-openworkflow/specs/shared-contract-ownership/spec.md`

## Target Artifacts

- `contracts/schemas/`
- `contracts/policies/`
- `contracts/manifest.yaml`
- `contracts/README.md`

## Copied Contracts

- `contracts/schemas/clarification-answer-packet.schema.yaml`
- `contracts/schemas/clarification-answer.schema.yaml`
- `contracts/schemas/clarification-questions.schema.yaml`
- `contracts/schemas/hermes-job-envelope.schema.yaml`
- `contracts/schemas/hermes-job-event.schema.yaml`
- `contracts/schemas/hermes-job-run.schema.yaml`
- `contracts/schemas/hermes-operational-postgres.sql`
- `contracts/policies/hermes-governance-agents.yaml`
- `contracts/policies/merge-risk-policy.yaml`

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| Canonical contract files exist in `openWorkflow/contracts` | Yes | `contracts/schemas/`, `contracts/policies/` | Copy-first migration from Omnigent install sources |
| Each contract has source, version, compatibility, and adapter ownership notes | Yes | `contracts/manifest.yaml` | Manifest records source path, source commit, schema version, consumers, and adapter owner |
| Install repo schema copies are not deleted in the same PR | Yes | Git diff | No install repo edits in this slice |
| Contract syntax is validated where applicable | Yes | validation output | YAML parse and SQL statement scan in validation |

## Stop Conditions Checked

- No install repo deletions.
- No runtime code movement.
- No generated adapters, smoke fixtures, runtime configs, credentials, databases, logs, or workspaces touched.
- No submodule pointer changes.

## Validation Plan

- `openspec validate migrate-canonical-policy-to-openworkflow --strict`
- `openspec validate --all --strict`
- YAML parse for `contracts/**/*.yaml`
- SQL statement scan for `contracts/schemas/hermes-operational-postgres.sql`
- `git diff --check`
- `git submodule status`

## PR Admission

This feature is contract-copy-only, below the PR size limit, and preserves
copy-first migration boundaries. It is ready to open a PR after validation.
