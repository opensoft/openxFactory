# Repository Boundary Audit

This document defines the boundary between `openxFactory`, `Hermes-Install`,
and `Omnigent-Install`.

The goal is to keep the install repositories focused on subsystem install,
operations, backup, recovery, and disaster recovery, while `openxFactory`
owns the integrated factory workflow.

The pilot implementation plan for applying this boundary through the factory
workflow is [Repo Boundary Change Pilot Plan](repo-boundary-pilot-plan.md).
The next implementation phase is the
[Dogfood Content Migration Plan](dogfood-content-migration-plan.md).

## Repository Responsibilities

```text
openxFactory
  canonical factory workflow, policy, contracts, authority, traceability

Hermes-Install
  Hermes subsystem install, operations, backup, restore, upgrade, DR

Omnigent-Install
  Omnigent/Polly subsystem install, workers, operations, backup, restore, upgrade, DR
```

## Boundary Rule

Use this rule when deciding where a file or concept belongs:

```text
If it defines how the whole factory behaves:
  openxFactory

If it installs, restores, operates, or verifies Hermes:
  Hermes-Install

If it installs, restores, operates, or verifies Omnigent/Polly workers:
  Omnigent-Install

If it is a contract between subsystems:
  openxFactory owns the canonical contract
  install repos may keep pinned copies, generated adapters, or smoke-test fixtures
```

## openxFactory Scope

`openxFactory` owns:

- Hermes, Omnigent, OpenSpec, Spec Kit, GitHub, and agent boundary model
- workflow contract from epic through merge
- authority model and approval gates
- feature decomposition constitution and standards
- traceability model
- merge council policy
- merge master policy
- human escalation policy
- role model across Hermes and Omnigent
- canonical event and artifact contract definitions
- end-to-end reference examples that explain how the factory works
- release mapping that pins compatible install repo revisions

`openxFactory` should not own:

- live service manifests
- live secrets
- installed runtime state
- subsystem-specific deployment scripts
- generated databases
- CloudPC-local credential files
- provider OAuth tokens or CLI auth profiles

## Hermes-Install Scope

`Hermes-Install` should own:

- Hermes deployment manifests
- Hermes service install scripts
- Hermes namespace, service, ingress, private access, and storage setup
- Hermes auth restore from Key Vault or equivalent secret manager
- Hermes agent registry restore
- Hermes memory-provider backup and restore process
- Hermes Teams/presence bridge install when the bridge is part of Hermes runtime
- Hermes operational probes
- Hermes upgrade and rollback procedures
- Hermes DR checklist

`Hermes-Install` should not be the canonical owner of:

- cross-factory approval doctrine
- merge council policy
- portfolio-to-engineering workflow contract
- Omnigent feature decomposition policy
- Spec Kit stage ownership policy
- end-to-end factory traceability model

When Hermes-specific implementation is needed for a factory policy, the policy
belongs in `openxFactory`; the Hermes adapter, config, script, or manifest
belongs in `Hermes-Install`.

## Omnigent-Install Scope

`Omnigent-Install` should own:

- Omnigent/Polly install and configuration
- worker containers and worker host setup
- CloudPC worker packs and worker lane manifests
- Claude/Codex auth setup for Omnigent workers
- Key Vault credential materialization into worker runtimes
- worker registration with Hermes
- local Kubernetes worker deployment
- deterministic check runners
- Spec Kit runtime setup as used by Omnigent
- Omnigent operational probes
- Omnigent backup, restore, upgrade, rollback, and DR procedures

`Omnigent-Install` should not be the canonical owner of:

- Omnigent constitution text
- feature decomposition doctrine
- Hermes authority model
- merge council policy
- merge master policy
- human escalation policy
- PR admission policy as a factory gate
- end-to-end traceability model

When Omnigent implements a factory policy, the policy belongs in
`openxFactory`; the worker profile, prompt pack, harness script, smoke test, or
adapter belongs in `Omnigent-Install`.

## Current Omnigent-Install Audit

`Omnigent-Install` currently includes useful proof-lab material that crosses
the final repo boundary. It should be classified before any moves are made.

### Keep In Omnigent-Install

These are install or operations artifacts and should remain:

- `containers/omnigent-worker/`
- `compose/phase1-worker/`
- `compose/phase8-worker-stack/`
- `k8s/local/worker-lanes.yaml`
- `workers/`
- `speckit/`
- `scripts/claude-subscription-auth.sh`
- `scripts/create-dev-auth-profile.sh`
- `scripts/plan-a-login-tui.py`
- `scripts/prepare-local-omnigent-tool.sh`
- `scripts/preseed-speckit-scaffold.sh`
- `scripts/prewarm-omnigent-runtime.sh`
- `scripts/register-worker.sh`
- `scripts/validate-worker-auth.sh`
- CloudPC worker runbooks
- LLM credential onboarding and restore runbooks
- worker deployment, scale-out, and operations runbooks

### Move Canonical Policy To openxFactory

The canonical versions of these concepts should live in `openxFactory`:

- `docs/project-master-plan.md`
- `docs/omnigent-implementation-plan.md`, for workflow doctrine sections
- `docs/project-lead-agents.md`, for cross-factory role definitions
- `docs/hermes-governance-agents.md`, for authority model and agent group meaning
- `docs/hermes-profiles-and-groups.md`, for governance group semantics
- `docs/clarification-routing.md`, for stage ownership and routing policy
- `docs/clarification-router-implementation-plan.md`, for contract-level routing behavior
- `docs/runbooks/phase3-feature-decomposition.md`, for decomposition policy
- `docs/runbooks/phase4-speckit-control.md`, for Spec Kit ownership contract
- `docs/runbooks/phase6-pr-admission.md`, for PR admission policy
- `docs/runbooks/phase7-merge-council.md`, for merge council policy
- `docs/runbooks/merge-master-implementation-plan.md`, for merge master policy
- `policies/hermes-governance-agents.yaml`, for canonical group/authority meaning
- `policies/merge-risk-policy.yaml`, for canonical risk policy

After canonical policy is moved or copied to `openxFactory`, the install repo
may keep implementation-oriented copies that point back to `openxFactory`.

### Candidate For Hermes-Install

These look Hermes-runtime-specific and should be reviewed for movement into
`Hermes-Install`:

- `hermes_service/`
- `compose/hermes-postgres-test/`
- `containers/hermes-test/`
- `docs/hermes-job-status-schema.md`
- `docs/hermes-structured-event-contract.md`, if treated as Hermes API implementation
- `docs/runbooks/hermes-api.md`
- `docs/runbooks/hermes-postgres-test-container.md`
- `docs/runbooks/hermes-profiles-groups-implementation-plan.md`
- `schemas/hermes-operational-postgres.sql`
- Hermes API smoke tests
- Hermes Postgres smoke tests
- Hermes group and authority enforcement smoke tests

If these are only a local integration proof for Omnigent, keep them temporarily
in `Omnigent-Install` and mark them as proof-lab artifacts. If they are becoming
the actual Hermes service implementation, move them to `Hermes-Install`.

### Candidate For openxFactory Integration Tests

These are end-to-end factory proofs. They may eventually belong in
`openxFactory` under an integration-test or reference-pilot area:

- `examples/project-alfa-*`
- `examples/live-pilot/`
- `examples/merge-master/`
- `pilot-flows/`
- `live-pilot/`
- `scripts/pilot-flow.sh`
- `scripts/run-alfa-*.sh`
- `scripts/live-pilot-*.sh`
- `scripts/smoke-live-pilot.sh`
- `scripts/smoke-live-factory-*.sh`
- `scripts/smoke-non-doc-*.sh`

Until the repo split is complete, these may remain in `Omnigent-Install` as
the working proof harness.

## Current Hermes-Install Audit

`Hermes-Install` currently appears closer to the desired scope.

### Keep In Hermes-Install

- `scripts/deploy-hermes-nextest.sh`
- `scripts/restore-hermes-auth-from-keyvault.sh`
- `scripts/create-teams-user-token.py`
- `k8s/hermes-angels-presence-scheduler.yaml`
- `k8s/hermes-angels-teams-user-bridge.yaml`
- Hermes AKS install and restore instructions
- company agent registry restore instructions
- Hermes runtime backup and recovery instructions

### Move Or Summarize In openxFactory

The following concepts should be summarized in `openxFactory` if they define
factory behavior rather than install procedure:

- company and cross-company Hermes group meaning
- xForge management boundary meaning
- Hermes approval authority model
- Hermes relationship to OpenSpec
- Hermes relationship to Omnigent
- Hermes relationship to merge council and merge master

The Hermes install repo may keep operational details for how those concepts are
deployed.

## Shared Contract Ownership

Canonical contracts belong in `openxFactory`.

Install repos may keep generated or pinned copies, but the source of truth
should be here:

```text
openxFactory/contracts/
  hermes-job-envelope.schema.yaml
  hermes-job-event.schema.yaml
  hermes-job-run.schema.yaml
  clarification-questions.schema.yaml
  clarification-answer.schema.yaml
  clarification-answer-packet.schema.yaml
  merge-readiness-report.schema.yaml
  pr-admission-packet.schema.yaml
```

Version rule:

```text
openxFactory contract version
  -> install repo pins compatible version
  -> smoke tests prove adapter compatibility
```

## Proposed Submodule Layout

`openxFactory` should become the umbrella repo for the factory:

```text
openxFactory/
  docs/
  contracts/
  examples/
  installs/
    hermes-install/      # submodule
    omnigent-install/    # submodule
```

Recommended remotes:

```text
github.com/opensoft/openxFactory
github.com/opensoft/Hermes-Install
github.com/opensoft/Omnigent-Install
```

Current note: local `Hermes-Install` points to `github.com:FarHeap/Hermes-Install`.
Before adding it as an `openxFactory` submodule, decide whether to move, fork,
or mirror it into the `opensoft` organization.

## Migration Plan

Status: record
Kind: report

The initial repo-boundary pilot is complete. The remaining migration work must
be performed through the dogfood workflow described in
[Dogfood Content Migration Plan](dogfood-content-migration-plan.md).

### Phase 1: Classify

- [x] Mark each `Omnigent-Install` doc as keep, move canonical policy, move to Hermes, or proof-lab.
- [x] Mark each `Hermes-Install` doc/script as keep or summarize into `openxFactory`.
- [x] Identify canonical contracts and create `openxFactory/contracts/`.
- [ ] Identify examples that should become reference workflow examples.

### Phase 2: Copy Canonical Policy

- [ ] Copy canonical role and authority docs into `openxFactory`.
- [ ] Copy canonical merge council and merge master policy into `openxFactory`.
- [ ] Copy canonical PR admission and human escalation policy into `openxFactory`.
- [ ] Copy canonical Spec Kit stage ownership and clarification routing into `openxFactory`.
- [ ] Copy canonical traceability and artifact contract docs into `openxFactory`.

Use copy-first migration. Do not delete working install repo files in this
phase.

### Phase 3: Point Install Repos Back To openxFactory

- [x] Update `Omnigent-Install` README with reduced scope.
- [x] Update `Hermes-Install` README with reduced scope.
- [x] Add links from install repo docs to canonical `openxFactory` policy.
- [ ] Mark duplicate policy docs as implementation notes or legacy copies.

### Phase 4: Move Runtime-Specific Pieces

- [ ] Decide whether `hermes_service/` belongs in `Hermes-Install`.
- [ ] Move Hermes runtime code and Hermes operational tests if appropriate.
- [ ] Keep Omnigent worker runtime code in `Omnigent-Install`.
- [ ] Keep end-to-end proof harness temporarily stable until replacement tests exist.

### Phase 5: Add Submodules

- [ ] Resolve `Hermes-Install` canonical remote decision.
- [ ] Add `installs/hermes-install` submodule.
- [x] Add `installs/omnigent-install` submodule.
- [x] Document submodule update and release pin process.

### Phase 6: Enforce Boundary

- [ ] Add a repo-boundary checklist to PR templates.
- [ ] Add smoke checks that install repos do not become canonical policy owners.
- [ ] Add release notes mapping `openxFactory` versions to install repo commits.

## Decision Log

| Decision | Status |
|---|---|
| `openxFactory` is the canonical factory workflow repo | accepted |
| `Hermes-Install` is scoped to Hermes install, operations, and DR | accepted |
| `Omnigent-Install` is scoped to Omnigent install, workers, operations, and DR | accepted |
| `openxFactory` may submodule both install repos | proposed |
| `Hermes-Install` should move or mirror to `opensoft` before submodule use | open |
| Proof-lab artifacts remain in place until replacement location exists | accepted |
