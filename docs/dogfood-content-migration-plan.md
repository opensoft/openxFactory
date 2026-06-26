# Dogfood Content Migration Plan

This plan defines how the factory should use its own workflow stack to migrate
canonical policy, contracts, and reference examples into their final repo
homes.

The repo-boundary pilot proved the governance path. This plan is the next
phase: use the same stack to perform the actual copy-first content migration.

## Principle

We will dogfood the factory on itself.

```text
OpenSpec owns the change proposal
Hermes approves scope, sequencing, PR admission, and merge readiness
Omnigent/Polly decomposes and orchestrates implementation
Spec Kit runs only for approved feature slices
GitHub PRs carry the implementation
Merge council records readiness before merge
GitHub branch protection remains the final enforcement layer
```

Do not perform the migration as a direct bulk file shuffle outside this
workflow.

## Scope

The migration will move or summarize canonical material from install and proof
repos into `openWorkflow`, then point the install repos back to the canonical
copies.

Initial source repos:

- `opensoft/Omnigent-Install`
- `FarHeap/Hermes-Install`

Initial target repo:

- `opensoft/openWorkflow`

## Required OpenSpec Change

Create a new OpenSpec change:

```yaml
change_id: migrate-canonical-policy-to-openworkflow
owner: Hermes
implementation_orchestrator: Omnigent/Polly
primary_repo: opensoft/openWorkflow
related_repos:
  - opensoft/Omnigent-Install
  - FarHeap/Hermes-Install
source_specs:
  - openspec/specs/repo-boundary-governance/spec.md
  - openspec/specs/shared-contract-ownership/spec.md
```

The OpenSpec proposal must link to:

- [Repository Boundary Audit](repo-boundary-audit.md)
- [Repo Boundary Change Pilot Plan](repo-boundary-pilot-plan.md)
- [Decision 0001: Install Repo Submodules](decisions/0001-install-repo-submodules.md)
- [Factory Contracts](../contracts/README.md)

## Dogfood Workflow

```text
Hermes opens OpenSpec proposal
  -> Hermes approves decomposition
  -> Omnigent/Polly decomposes migration into small features
  -> Hermes approves one feature slice at a time
  -> Omnigent runs Spec Kit for the approved slice
  -> implementation agent makes copy-first doc/contract changes
  -> Omnigent runs local checks
  -> Omnigent runs branch review
  -> Hermes admits branch to PR
  -> GitHub PR opens
  -> merge council records readiness
  -> GitHub merge enforcement completes merge
  -> OpenSpec evidence is updated
```

## Migration Rules

- Use copy-first migration.
- Do not delete source docs in the same PR that creates canonical docs.
- Do not move runtime code while migrating policy.
- Do not combine schema migration with generated adapter changes.
- Do not combine submodule pointer changes with content moves.
- Do not move or copy `.local`, `.claude`, `.codex/auth`, databases, token
  files, credential profiles, or generated runtime state.
- Every feature slice must have evidence: source references, acceptance
  criteria, checks, branch review, PR admission, and merge readiness.
- Install repo copies become implementation notes or legacy working copies
  before they are removed.

## Feature Slices

### FEAT-MIG-001: Roles And Authority

Purpose: create the canonical cross-factory role and authority model.

Primary target:

- `openWorkflow/docs/roles-and-authority.md`

Initial sources:

- `Omnigent-Install/docs/project-lead-agents.md`
- `Omnigent-Install/docs/hermes-governance-agents.md`
- `Omnigent-Install/docs/hermes-profiles-and-groups.md`
- relevant Hermes group notes from `Hermes-Install/README.md`

Allowed:

- copy or summarize canonical role policy into `openWorkflow`
- preserve source links and provenance
- update `openWorkflow` README

Not allowed:

- no install repo deletion
- no runtime config changes
- no agent roster mutation
- no submodule pointer changes

Acceptance criteria:

- `openWorkflow` defines PO, PM, CA, PA, LA, LE, LC, LQ, LI, LS, Merge Master,
  and Merge Council responsibilities.
- Hermes-level roles are clearly separated from Omnigent execution roles.
- Install repo source docs remain in place.

### FEAT-MIG-002: Spec Kit Stage Ownership And Clarification Routing

Purpose: make Spec Kit stage ownership and clarification routing canonical in
`openWorkflow`.

Primary target:

- `openWorkflow/docs/spec-kit-stage-ownership.md`

Initial sources:

- `Omnigent-Install/docs/clarification-routing.md`
- `Omnigent-Install/docs/clarification-router-implementation-plan.md`
- `Omnigent-Install/docs/runbooks/phase4-speckit-control.md`

Acceptance criteria:

- `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`,
  `/speckit.tasks`, `/speckit.analyze`, and `/speckit.implement` ownership is
  canonical.
- Clarification routing from LE to PO/PM/PA/LS/LQ/LI/LC is canonical.
- Omnigent implementation docs link back to the canonical policy.

### FEAT-MIG-003: PR Admission, Merge Council, And Merge Master

Purpose: consolidate branch admission and merge authority policy.

Primary targets:

- `openWorkflow/docs/pr-admission.md`
- `openWorkflow/docs/merge-master.md`
- updates to `openWorkflow/docs/merge-council.md`

Initial sources:

- `Omnigent-Install/docs/runbooks/phase6-pr-admission.md`
- `Omnigent-Install/docs/runbooks/phase7-merge-council.md`
- `Omnigent-Install/docs/runbooks/merge-master-implementation-plan.md`
- `Omnigent-Install/policies/merge-risk-policy.yaml`

Acceptance criteria:

- PR admission policy is canonical in `openWorkflow`.
- Merge council readiness inputs and outputs are canonical.
- Merge Master risk and human escalation rules are canonical.
- Install repo runbooks are marked as implementation guidance.

### FEAT-MIG-004: Feature Decomposition And Traceability

Purpose: consolidate decomposition doctrine and traceability artifacts.

Primary targets:

- updates to `openWorkflow/docs/feature-decomposition.md`
- updates to `openWorkflow/docs/traceability-model.md`

Initial sources:

- `Omnigent-Install/docs/runbooks/phase3-feature-decomposition.md`
- `Omnigent-Install/docs/project-master-plan.md`
- `Omnigent-Install/examples/project-alfa-decomposition/`

Acceptance criteria:

- orthogonal, user-perceivable, encapsulated feature slicing is canonical.
- bug-to-feature mapping requirements are canonical.
- traceability from OpenSpec to Spec Kit to branch review to PR to merge is
  canonical.

### FEAT-MIG-005: Shared Contract Migration

Purpose: copy canonical shared schemas/contracts into `openWorkflow/contracts`.

Primary target:

- `openWorkflow/contracts/`

Initial sources:

- `Omnigent-Install/schemas/`
- `Omnigent-Install/policies/hermes-governance-agents.yaml`
- `Omnigent-Install/policies/merge-risk-policy.yaml`

Acceptance criteria:

- canonical contract files exist in `openWorkflow/contracts`.
- each contract has a source, version, compatibility note, and install-repo
  adapter rule.
- install repo schema copies are not deleted in the same PR.

### FEAT-MIG-006: Reference Pilot And Example Placement

Purpose: decide where end-to-end proof examples live.

Primary target options:

- `openWorkflow/examples/`
- future `factory-lab` repo
- temporary status quo in `Omnigent-Install`

Initial sources:

- `Omnigent-Install/examples/project-alfa-*`
- `Omnigent-Install/examples/live-pilot/`
- `Omnigent-Install/pilot-flows/`
- `Omnigent-Install/live-pilot/`

Acceptance criteria:

- Hermes approves the placement decision.
- no proof harness is moved until replacement validation exists.
- examples that become canonical reference examples live in `openWorkflow`.

### FEAT-MIG-007: Mark Install Repo Policy Copies

Purpose: update install repo docs to clearly distinguish canonical policy from
implementation notes.

Affected repos:

- `Omnigent-Install`
- `Hermes-Install`

Acceptance criteria:

- migrated source docs link to canonical `openWorkflow` docs.
- source docs are marked implementation notes, legacy copies, or operational
  runbooks.
- existing install repo smoke tests still pass.

### FEAT-MIG-008: Removal Or Cleanup Decision

Purpose: decide whether legacy policy copies should be removed, archived, or
kept as implementation notes.

Prerequisites:

- FEAT-MIG-001 through FEAT-MIG-007 merged
- canonical docs validated
- install repo links updated
- proof harnesses still pass

Acceptance criteria:

- removals, if any, are isolated to a dedicated PR.
- no runtime files, scripts, manifests, or generated adapters are removed by
  policy cleanup.
- rollback path is documented.

## Required Evidence Per Feature

Each feature must produce:

- OpenSpec feature record
- source inventory
- acceptance criteria table
- implementation diff
- local validation output
- branch review
- PR admission packet
- merge readiness report
- post-merge OpenSpec task update

## Validation Matrix

| Feature Type | Required Validation |
|---|---|
| `openWorkflow` docs only | `openspec validate --all --strict`, `git diff --check` |
| `openWorkflow/contracts` | schema/file lint where applicable, contract source/provenance check |
| `Omnigent-Install` docs | existing Omnigent smoke checks plus no-committed-secrets check |
| `Hermes-Install` docs | README-only or file-scope diff check; no manifest/script changes unless explicitly approved |
| examples/proof harness | fresh clone, referenced file existence, and no generated state |

## Stop Conditions

Stop and return to Hermes approval if any feature:

- proposes deleting source docs before canonical copies are merged
- touches secrets, credentials, generated runtime state, or databases
- moves runtime code while migrating policy
- changes submodule pointers during a content migration PR
- changes install repo scripts/manifests without explicit feature approval
- cannot produce PR admission or merge readiness evidence

## Success Criteria

The dogfood migration is complete when:

- canonical policy docs live in `openWorkflow`
- canonical shared contracts live in `openWorkflow/contracts`
- install repos link to canonical policy instead of owning it
- proof/reference examples have an approved home
- duplicate install repo policy copies are marked or cleaned up by approved PRs
- OpenSpec archives the migration with evidence for every feature slice
