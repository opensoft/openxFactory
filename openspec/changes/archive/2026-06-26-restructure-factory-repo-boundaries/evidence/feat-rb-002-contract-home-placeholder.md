# FEAT-RB-002 Contract Home Placeholder Evidence

Feature: FEAT-RB-002 Contract Home Placeholder
OpenSpec Change: `restructure-factory-repo-boundaries`
Repo: `opensoft/openWorkflow`
Decision: READY FOR PR ADMISSION

## Scope

Allowed scope:

- `openWorkflow` only
- contract placeholder documentation only
- OpenSpec task and evidence updates

Confirmed exclusions:

- no `Hermes-Install` edits
- no `Omnigent-Install` edits
- no schema file migration
- no generated clients
- no runtime adapters
- no submodules
- no runtime code
- no secrets, credentials, generated databases, or runtime state

## Inputs Reviewed

- `openspec/changes/restructure-factory-repo-boundaries/proposal.md`
- `openspec/changes/restructure-factory-repo-boundaries/design.md`
- `openspec/changes/restructure-factory-repo-boundaries/specs/shared-contract-ownership/spec.md`
- `docs/repo-boundary-audit.md`
- `docs/repo-boundary-pilot-plan.md`

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| `openWorkflow/contracts/` exists | Yes | `contracts/README.md` | Placeholder only |
| planned shared contracts and schema names are listed | Yes | `contracts/README.md` | Includes Hermes job, clarification, PR admission, merge readiness, risk, release map |
| source-of-truth rule is documented | Yes | `contracts/README.md` | `openWorkflow/contracts/` owns canonical contract meaning |
| version pinning rule is documented | Yes | `contracts/README.md` | Commit/tag pin examples included |
| adapter/generated-copy rule is documented | Yes | `contracts/README.md` | Install repo copies are implementation artifacts |
| no install repo files changed | Yes | git diff | Only `openWorkflow` files changed |

## Local Checks

Required checks:

```bash
OPENSPEC_TELEMETRY=0 openspec validate restructure-factory-repo-boundaries --strict
git diff --check
git diff --name-only main...HEAD
find . -maxdepth 5 -type f | rg '(\.local/|\.claude/|\.codex/auth|credentials|token|secret|\.db$|\.sqlite)' || true
```

Expected result:

- OpenSpec validates.
- Diff has no whitespace errors.
- Diff is limited to `openWorkflow`.
- No secret, credential, database, or runtime-state files are present.

## Branch Review

Review result: PASS

Review notes:

- The change creates only a contract placeholder and governance rules.
- It does not migrate schema files yet.
- It does not touch install repos.
- It preserves copy-first migration.

## PR Admission

Decision: ADMIT

Reason:

FEAT-RB-002 satisfies the shared-contract ownership requirement without
combining it with adapter migration, install repo edits, or submodule changes.

Conditions:

- Do not include FEAT-RB-003 or later feature work in the same PR.
- Do not move schemas into `contracts/` until a separate approved feature.
