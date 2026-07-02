# FEAT-RB-006 First Actual Submodule Add Evidence

Feature: FEAT-RB-006 First Actual Submodule Add
OpenSpec Change: `restructure-factory-repo-boundaries`
Repo: `opensoft/openxFactory`
Decision: READY FOR PR ADMISSION

## Scope

Allowed scope:

- add `.gitmodules`
- add `installs/omnigent-install` submodule
- document the install repo pin in `README.md`
- OpenSpec task and evidence updates

Confirmed exclusions:

- no `installs/hermes-install`
- no Hermes submodule
- no file moves across repositories
- no install repo content edits
- no runtime code
- no schema migration
- no secrets, credentials, generated databases, or runtime state

## Prerequisites

| Prerequisite | Status | Evidence |
|---|---|---|
| FEAT-RB-001 merged | Complete | `openxFactory#1` |
| FEAT-RB-002 merged | Complete | `openxFactory#2` |
| FEAT-RB-003 merged | Complete | `Omnigent-Install#1`, `openxFactory#3` |
| FEAT-RB-004 merged | Complete | `Hermes-Install#1`, `openxFactory#4` |
| FEAT-RB-005 merged | Complete | `openxFactory#5` |
| Omnigent install scope docs approved | Complete | `Omnigent-Install#1` |
| Hermes remote decision resolved | Deferred | Decision 0001 blocks Hermes submodule only |

## Submodule Pin

```text
path: installs/omnigent-install
url: git@github.com:opensoft/Omnigent-Install.git
commit: e254c22ce14e585e909b05c44aed21fd07beba84
```

The pinned commit is the merged FEAT-RB-003 Omnigent scope-link commit.

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| FEAT-RB-001 through FEAT-RB-005 merged | Yes | PR history | All prior slices merged |
| install repo scope docs updated and approved | Yes | Omnigent and Hermes merged PRs | Hermes submodule still deferred |
| only approved first install repo submodule added | Yes | `.gitmodules` | Omnigent only |
| fresh clone and submodule init validates | Yes | fresh clone check | Checked out `e254c22` |
| merge council readiness evidence recorded | Pending | PR readiness report | To be added before merge |

## Local Checks

Required checks:

```bash
OPENSPEC_TELEMETRY=0 openspec validate restructure-factory-repo-boundaries --strict
git submodule status
git diff --check
```

Fresh clone validation:

```bash
git clone --branch feat/repo-boundary-omnigent-submodule --recurse-submodules \
  git@github.com:opensoft/openxFactory.git /tmp/openxfactory-submodule-smoke
git -C /tmp/openxfactory-submodule-smoke submodule status
test -f /tmp/openxfactory-submodule-smoke/installs/omnigent-install/README.md
```

Result:

```text
Submodule path 'installs/omnigent-install': checked out 'e254c22ce14e585e909b05c44aed21fd07beba84'
e254c22
```

## Branch Review

Review result: PASS

Review notes:

- The change adds only the approved Omnigent install submodule.
- Hermes install is not added.
- No install repo files are edited through the submodule.
- No file moves are combined with the submodule add.

## PR Admission

Decision: ADMIT

Conditions:

- Merge council must review before merge.
