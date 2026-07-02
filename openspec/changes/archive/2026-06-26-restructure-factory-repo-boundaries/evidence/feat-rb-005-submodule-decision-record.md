# FEAT-RB-005 Submodule Decision Record Evidence

Feature: FEAT-RB-005 Submodule Decision Record
OpenSpec Change: `restructure-factory-repo-boundaries`
Repo: `opensoft/openxFactory`
Decision: READY FOR PR ADMISSION

## Scope

Allowed scope:

- `openxFactory` decision record
- OpenSpec task and evidence updates
- no actual submodule creation

Confirmed exclusions:

- no `.gitmodules`
- no `installs/` submodule pointer
- no install repo edits
- no runtime code
- no schema migration
- no secrets, credentials, generated databases, or runtime state

## Inputs Reviewed

- `docs/repo-boundary-audit.md`
- `docs/repo-boundary-pilot-plan.md`
- `contracts/README.md`
- `openspec/changes/restructure-factory-repo-boundaries/design.md`
- merged `Omnigent-Install` scope-link PR
- merged `Hermes-Install` scope-link PR

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| decision record exists | Yes | `docs/decisions/0001-install-repo-submodules.md` | New decision record |
| proposed submodule paths are documented | Yes | decision record | `installs/omnigent-install`, `installs/hermes-install` |
| update procedure is documented | Yes | decision record | Includes approved-commit pin flow |
| rollback procedure is documented | Yes | decision record | Includes previous-pin rollback |
| Hermes submodule waits for remote ownership decision | Yes | decision record | FarHeap vs Opensoft decision is explicit |
| no actual submodule add happened | Yes | git diff | No `.gitmodules`, no submodule pointer |

## Local Checks

Required checks:

```bash
OPENSPEC_TELEMETRY=0 openspec validate restructure-factory-repo-boundaries --strict
git diff --check
git diff --name-status
```

Expected result:

- OpenSpec validates.
- Diff has no whitespace errors.
- Diff is limited to docs and OpenSpec evidence/tasks.

## Branch Review

Review result: PASS

Review notes:

- The change documents submodule behavior without creating submodules.
- The first allowed submodule is `installs/omnigent-install`.
- Hermes submodule remains blocked until remote ownership is approved.

## PR Admission

Decision: ADMIT

Reason:

FEAT-RB-005 satisfies the submodule decision-record requirement without
combining it with submodule creation.

Conditions:

- Do not include FEAT-RB-006 in the same PR.
- Merge council must review before merge.
