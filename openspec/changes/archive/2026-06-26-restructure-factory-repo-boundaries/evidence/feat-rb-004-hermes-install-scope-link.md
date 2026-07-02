# FEAT-RB-004 Hermes-Install Scope Link Evidence

Feature: FEAT-RB-004 Hermes-Install Scope Link
OpenSpec Change: `restructure-factory-repo-boundaries`
Implementation Repo: `FarHeap/Hermes-Install`
Implementation PR: https://github.com/FarHeap/Hermes-Install/pull/1
Decision: READY FOR PR ADMISSION

## Scope

Allowed scope:

- `Hermes-Install` README scope clarification
- links from `Hermes-Install` to canonical `openxFactory` docs
- explicit note that the `Hermes-Install` remote ownership decision is unresolved
- statement that duplicate policy docs are implementation notes or legacy
  working copies unless `openxFactory` delegates ownership

Confirmed exclusions:

- no deployment script changes
- no manifest changes
- no runtime code
- no submodules
- no file moves
- no secrets, credentials, generated databases, or runtime state

## Inputs Reviewed

- `openxFactory/docs/repo-boundary-audit.md`
- `openxFactory/contracts/README.md`
- `openxFactory/openspec/changes/restructure-factory-repo-boundaries/proposal.md`
- `Hermes-Install/README.md`
- `Hermes-Install` PR #1 diff

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| `Hermes-Install` README states Hermes install, operations, backup, restore, upgrade, and DR scope | Yes | `Hermes-Install` PR #1 | Scope section added |
| README links to canonical `openxFactory` boundary and workflow policy | Yes | `Hermes-Install` PR #1 | Links to boundary audit, pilot plan, contracts, OpenSpec change |
| unresolved `Hermes-Install` remote ownership decision is documented | Yes | `Hermes-Install` PR #1 | FarHeap vs Opensoft decision stated |
| no deployment scripts or manifests changed | Yes | `git diff --name-status` | Only `README.md` changed in clean PR branch |

## Local Checks

Checks run in clean `Hermes-Install` clone:

```bash
git diff --check
git diff --name-status
```

Result:

- Diff has no whitespace errors.
- Only `README.md` changed.
- No deployment scripts or manifests changed.

## Branch Review

Review result: PASS

Review notes:

- The implementation PR changes only `Hermes-Install/README.md`.
- The README now treats `openxFactory` as canonical workflow and contract
  authority.
- The README keeps Hermes-specific install, runtime, bridge, memory, auth, and
  recovery scope in `Hermes-Install`.
- The Hermes submodule remains blocked until remote ownership is approved.

## PR Admission

Decision: ADMIT

Reason:

FEAT-RB-004 satisfies the Hermes install repo scope-link requirement without
moving files, changing runtime behavior, altering manifests, or creating
submodules.

Conditions:

- Do not merge FEAT-RB-005 or later feature work into the same PR.
- Merge council must review Hermes PR #1 before merge.
