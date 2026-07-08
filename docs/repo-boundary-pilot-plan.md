# Repo Boundary Change Pilot Plan

This plan uses the factory workflow itself to implement the repo-boundary
restructure described in [Repository Boundary Audit](repo-boundary-audit.md).

Status: retired
Kind: plan
Retired: pilot completed; outcome archived in the restructure-factory-repo-boundaries change

The next phase is the copy-first content migration described in
[Dogfood Content Migration Plan](dogfood-content-migration-plan.md). That phase
must use the full factory stack on the factory itself.

The pilot is intentionally constrained: doc-only first, `openxFactory` first,
no deletions, and no submodules until the policy and contracts are approved.

## Goal

Prove that Hermes, Omnigent/Polly, Spec Kit, GitHub, and merge council can
manage a real governance change with low blast radius.

The change being piloted:

```text
openxFactory becomes the canonical factory workflow repo
Hermes-Install narrows to Hermes install, operations, and DR
Omnigent-Install narrows to Omnigent install, operations, and DR
openxFactory later pins install repos as submodules
```

## Guardrails

The pilot must follow these restrictions:

- doc-only changes first
- touch `openxFactory` only in the first feature
- do not delete or move working install repo files in the first feature
- do not add submodules in the first feature
- do not move Hermes runtime code in the first feature
- do not move Omnigent worker runtime code in the first feature
- do not alter secrets, credentials, generated state, databases, or runtime workspaces
- keep all install repo smoke tests green before any later install-repo change

## Proposed OpenSpec Change

```yaml
change_id: restructure-factory-repo-boundaries
owner: Hermes
implementation_orchestrator: Omnigent/Polly
initial_scope: doc-only
source_document: docs/repo-boundary-audit.md
primary_repo: opensoft/openxFactory
related_repos:
  - opensoft/Omnigent-Install
  - FarHeap/Hermes-Install
```

## Pilot Workflow

```text
Hermes opens OpenSpec proposal
  -> Hermes approves decomposition request
  -> Omnigent/Polly decomposes into small features
  -> Hermes approves Feature 1 for Spec Kit
  -> Omnigent runs Spec Kit for Feature 1
  -> coder implements doc-only change
  -> Omnigent runs local checks
  -> Omnigent runs local branch review
  -> Hermes admits branch to PR
  -> GitHub PR opens
  -> Hermes merge council reviews
  -> GitHub enforces final merge
```

## Feature Slices

### FEAT-RB-001: Canonical Boundary Policy

Repo touched: `openxFactory`

Purpose: make `openxFactory` the explicit authority for repo boundaries.

Allowed changes:

- add or update repo-boundary policy docs
- add migration checklist
- add release/submodule intent
- add OpenSpec proposal artifacts if OpenSpec is enabled in this repo

Not allowed:

- no install repo edits
- no file moves
- no submodules
- no runtime code

Acceptance criteria:

- `openxFactory` clearly states canonical ownership of factory workflow policy
- `Hermes-Install` and `Omnigent-Install` responsibilities are defined
- migration phases are documented
- open decisions are listed
- branch review confirms doc-only scope

### FEAT-RB-002: Contract Home Placeholder

Repo touched: `openxFactory`

Purpose: define where canonical shared schemas and contracts will live.

Allowed changes:

- create `contracts/README.md`
- list planned contract schemas
- define versioning and install-repo pinning rule

Not allowed:

- no schema migration yet unless copied as draft/reference
- no install repo edits
- no generated clients

Acceptance criteria:

- `openxFactory/contracts/` exists
- contract source-of-truth rule is documented
- install repo adapter rule is documented

### FEAT-RB-003: Omnigent-Install Scope Link

Repo touched: `Omnigent-Install`

Purpose: narrow `Omnigent-Install` README to install, operations, worker
runtime, auth, backup, restore, upgrade, and DR.

Allowed changes:

- README scope clarification
- links to canonical `openxFactory` docs
- mark policy docs as implementation notes where appropriate

Not allowed:

- no file deletions
- no runtime code moves
- no submodule edits

Acceptance criteria:

- README points to `openxFactory` as workflow authority
- Omnigent-specific install scope is clear
- existing Omnigent smoke tests still pass

### FEAT-RB-004: Hermes-Install Scope Link

Repo touched: `Hermes-Install`

Purpose: narrow `Hermes-Install` README to Hermes install, operations, backup,
restore, upgrade, and DR.

Allowed changes:

- README scope clarification
- links to canonical `openxFactory` docs
- note remote ownership decision for future submodule use

Not allowed:

- no deployment script changes
- no manifest changes
- no submodule edits

Acceptance criteria:

- README points to `openxFactory` as workflow authority
- Hermes-specific install scope is clear
- existing Hermes install files are unchanged

### FEAT-RB-005: Submodule Decision Record

Repo touched: `openxFactory`

Purpose: document, but not yet implement, the submodule layout.

Allowed changes:

- add submodule decision record
- document `installs/hermes-install`
- document `installs/omnigent-install`
- record decision needed for `Hermes-Install` remote

Not allowed:

- do not run `git submodule add`
- do not move install repos

Acceptance criteria:

- decision record exists
- open remote decision is explicit
- rollback and update procedure are documented

### FEAT-RB-006: First Actual Submodule Add

Repo touched: `openxFactory`

Purpose: add the first install repo as a submodule after policy approval.

Prerequisites:

- FEAT-RB-001 through FEAT-RB-005 merged
- install repo scope docs updated
- submodule remote decision approved
- human or merge master approves risk level

Allowed changes:

- add `.gitmodules`
- add `installs/omnigent-install` submodule first
- document clone/update procedure

Not allowed:

- do not add Hermes submodule until remote ownership is resolved
- do not move files across repos in same PR

Acceptance criteria:

- fresh clone with submodules succeeds
- submodule points to approved commit
- README explains how to update pinned install repo revision

## Pilot Roles

```yaml
PO:
  responsibility: approve business value and repo ownership intent
PM:
  responsibility: sequence the pilot and track readiness
CA:
  responsibility: approve factory architecture boundary
PA:
  responsibility: verify repo-level structure and contract placement
LA:
  responsibility: lead Omnigent/Spec Kit execution for approved features
LC:
  responsibility: manage doc/coder implementation agents
LQ:
  responsibility: verify acceptance criteria and checks
LS:
  responsibility: verify no secrets or unsafe runtime changes
LI:
  responsibility: verify install repo integration and submodule sequencing
Merge Master:
  responsibility: judge final merge risk and route human review only when needed
Merge Council:
  responsibility: approve readiness before merge
```

## Pilot Risk Controls

| Risk | Control |
|---|---|
| Repo split breaks working proof harness | copy-first migration, no deletions in first pass |
| Policy duplicated across repos | `openxFactory` becomes canonical, install repos link back |
| Submodules create operational confusion | decision record before any submodule add |
| Hermes runtime code moves too early | runtime moves deferred until separate feature |
| Install repo tests fail | each install-repo feature must run existing smoke tests |
| Secret material accidentally moves | doc-only first, no `.local`, `.claude`, `.codex`, DB, or token files |

## Evidence Required

Each feature should produce:

- source OpenSpec proposal or change record
- feature decomposition entry
- acceptance criteria table
- implementation diff
- local check output
- branch review result
- PR admission packet
- merge readiness report

## Initial Checklist

- [x] Create repo boundary audit.
- [x] Create OpenSpec proposal for `restructure-factory-repo-boundaries`.
- [x] Decompose change into the feature slices above.
- [x] Run FEAT-RB-001 as the first doc-only pilot.
- [x] Review branch locally before PR admission.
- [x] Open GitHub PR after Hermes approval.
- [x] Run merge council on the PR.
- [x] Merge only after GitHub checks and merge council approval.

## Stop Conditions

Stop the pilot if any of the following occur:

- a feature proposes deleting install repo files before canonical replacements exist
- a feature touches secrets, credentials, runtime state, or generated databases
- a feature combines submodule creation with file moves
- install repo smoke tests fail after an install repo change
- Hermes cannot record approval, PR admission, or merge readiness artifacts

## Success Criteria

The pilot is successful when:

- `openxFactory` owns the canonical repo-boundary policy
- the first PR is doc-only and low risk
- Hermes records the approval path
- Omnigent/Polly produces traceability artifacts
- local review and PR admission are recorded
- merge council produces a readiness report
- GitHub merge enforcement remains the final gate
