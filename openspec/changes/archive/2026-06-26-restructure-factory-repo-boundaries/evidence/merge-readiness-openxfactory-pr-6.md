# Merge Readiness Report

Feature: FEAT-RB-006 First Actual Submodule Add
OpenSpec Change: `restructure-factory-repo-boundaries`
PR: `opensoft/openxFactory#6`
Decision: READY

## Inputs Reviewed

- `.gitmodules`
- `installs/omnigent-install` submodule pointer
- `README.md`
- `evidence/feat-rb-006-omnigent-submodule-add.md`
- `tasks.md`
- fresh clone validation result
- OpenSpec validation result

## Scope Reviewed

Allowed scope:

- add the first approved install repo submodule
- add `installs/omnigent-install`
- update README install repo pin docs
- OpenSpec task and evidence updates

Confirmed exclusions:

- no `installs/hermes-install`
- no Hermes submodule
- no install repo content edits
- no file moves across repositories
- no runtime code
- no schema migration
- no secrets, credentials, generated databases, or runtime state

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| FEAT-RB-001 through FEAT-RB-005 are merged | Yes | PR history | Prior slices merged |
| install repo scope docs are updated and approved | Yes | Omnigent and Hermes PRs | Both scope links merged |
| only approved first install repo submodule added | Yes | `.gitmodules` | Omnigent only |
| fresh clone and submodule initialization validates | Yes | FEAT-RB-006 evidence | Checked out `e254c22` |
| merge council readiness evidence exists | Yes | this report | Decision READY |

## Council Results

| Reviewer | Decision | Blocking |
|---|---|---:|
| Spec Traceability | Pass | No |
| Submodule Safety | Pass | No |
| Scope Control | Pass | No |
| Install Repo Boundary | Pass | No |
| Security / Secret Safety | Pass | No |
| Maintainability | Pass | No |

## Validation

Local validation:

```bash
OPENSPEC_TELEMETRY=0 openspec validate restructure-factory-repo-boundaries --strict
git submodule status
git diff --check
```

Fresh clone validation:

```text
Submodule path 'installs/omnigent-install': checked out 'e254c22ce14e585e909b05c44aed21fd07beba84'
```

Result:

- OpenSpec change is valid.
- Submodule pointer resolves.
- Fresh clone with recursive submodules works.
- Diff has no whitespace errors.

## Required Fixes

None.

## Merge Conditions

- Merge PR #6 only.
- Do not add Hermes submodule in this PR.
- Do not archive the OpenSpec change until final validation passes on `main`.
