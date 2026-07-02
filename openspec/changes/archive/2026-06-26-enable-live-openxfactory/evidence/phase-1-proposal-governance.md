# Phase 1 Proposal And Governance Evidence

Decision: READY FOR PR ADMISSION

## Sources Reviewed

- `README.md`
- `docs/workflow-contract.md`
- `docs/deployment-worker-model.md`
- `contracts/manifest.yaml`
- `openspec/specs/canonical-contract-migration/spec.md`
- `openspec/specs/canonical-policy-migration/spec.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/omnigent-implementation-plan.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/runbooks/live-factory-six-workstream-plan.md`

## Target Artifacts

- `openspec/changes/enable-live-openxfactory-factory/proposal.md`
- `openspec/changes/enable-live-openxfactory-factory/design.md`
- `openspec/changes/enable-live-openxfactory-factory/tasks.md`
- `openspec/changes/enable-live-openxfactory-factory/specs/live-factory-runtime/spec.md`
- `openspec/changes/enable-live-openxfactory-factory/specs/hermes-omnigent-integration/spec.md`
- `openspec/changes/enable-live-openxfactory-factory/specs/worker-runtime-admission/spec.md`
- `openspec/changes/enable-live-openxfactory-factory/specs/github-merge-enforcement/spec.md`

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| Proposal, design, tasks, and runtime capability specs exist | Yes | OpenSpec change files | Four new runtime capability specs added |
| OpenSpec strict validation passes | Yes | validation output | `enable-live-openxfactory-factory` and `--all` passed |
| Hermes approval to proceed is recorded | Yes | user request and this evidence | User explicitly requested implementation of the plan |

## Stop Conditions Checked

- No install repo changes in this proposal slice.
- No runtime code movement.
- No generated adapters, manifests, credentials, databases, logs, or workspaces touched.
- No submodule pointer changes.

## Validation

- `openspec validate enable-live-openxfactory-factory --strict`
- `openspec validate --all --strict`
- `git diff --check`
