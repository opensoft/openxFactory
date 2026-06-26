# FEAT-RB-003 Omnigent-Install Scope Link Evidence

Feature: FEAT-RB-003 Omnigent-Install Scope Link
OpenSpec Change: `restructure-factory-repo-boundaries`
Implementation Repo: `opensoft/Omnigent-Install`
Implementation PR: https://github.com/opensoft/Omnigent-Install/pull/1
Decision: READY FOR PR ADMISSION

## Scope

Allowed scope:

- `Omnigent-Install` README scope clarification
- links from `Omnigent-Install` to canonical `openWorkflow` docs
- statement that duplicate policy docs are implementation notes or legacy
  working copies unless `openWorkflow` delegates ownership

Confirmed exclusions:

- no runtime code changes
- no deployment script changes
- no manifest changes
- no submodules
- no schema migration
- no file moves
- no secrets, credentials, generated databases, or runtime state

## Inputs Reviewed

- `openWorkflow/docs/repo-boundary-audit.md`
- `openWorkflow/contracts/README.md`
- `openWorkflow/openspec/changes/restructure-factory-repo-boundaries/proposal.md`
- `Omnigent-Install/README.md`
- `Omnigent-Install` PR #1 diff

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| `Omnigent-Install` README states install, worker runtime, operations, and DR scope | Yes | `Omnigent-Install` PR #1 | README scope narrowed |
| README links to canonical `openWorkflow` boundary and workflow policy | Yes | `Omnigent-Install` PR #1 | Links to boundary audit, pilot plan, contracts, OpenSpec change |
| duplicate policy material marked as implementation notes or legacy copies | Yes | `Omnigent-Install` PR #1 | Added Policy Copies section |
| existing Omnigent smoke checks pass | Yes | validation output | See Local Checks |
| no runtime code or install artifacts changed | Yes | PR diff | README only |

## Local Checks

Checks run in `Omnigent-Install`:

```bash
git diff --check
./scripts/smoke-no-committed-secrets.sh
./scripts/smoke-plan-a-credential-install.sh
./scripts/smoke-cloudpc-deployment-plan.sh
```

Result:

- `OK no committed secrets smoke`
- `OK Plan A credential install smoke`
- `OK CloudPC deployment plan smoke`

## Branch Review

Review result: PASS

Review notes:

- The implementation PR changes only `Omnigent-Install/README.md`.
- The README now treats `openWorkflow` as canonical workflow and contract
  authority.
- The README keeps Omnigent-specific implementation, runtime, worker, adapter,
  and verification scope in `Omnigent-Install`.

## PR Admission

Decision: ADMIT

Reason:

FEAT-RB-003 satisfies the install repo scope-link requirement without moving
files, changing runtime behavior, or creating submodules.

Conditions:

- Do not merge FEAT-RB-004 or later feature work into the same PR.
- Merge council must review Omnigent PR #1 before merge.
