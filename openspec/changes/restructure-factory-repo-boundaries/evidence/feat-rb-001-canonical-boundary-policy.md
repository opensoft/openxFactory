# FEAT-RB-001 Canonical Boundary Policy Evidence

Feature: FEAT-RB-001 Canonical Boundary Policy
Change: `restructure-factory-repo-boundaries`
Repo: `opensoft/openWorkflow`
Decision: READY FOR PR ADMISSION

## Scope

This feature is the first low-risk pilot slice for the repo-boundary change.

Allowed scope:

- `openWorkflow` only
- documentation and OpenSpec artifacts only
- no install repo edits
- no file moves
- no submodules
- no runtime code
- no secrets, credential profiles, generated databases, or runtime state

## Approval Record

Hermes/operator approval to proceed was represented by the operator request:

```text
implement
```

The implementation interprets that approval as permission to complete the
proposal review tasks and execute FEAT-RB-001 only. Later feature slices still
require separate approval.

## Inputs Reviewed

- `openspec/changes/restructure-factory-repo-boundaries/proposal.md`
- `openspec/changes/restructure-factory-repo-boundaries/design.md`
- `openspec/changes/restructure-factory-repo-boundaries/specs/repo-boundary-governance/spec.md`
- `openspec/changes/restructure-factory-repo-boundaries/specs/shared-contract-ownership/spec.md`
- `docs/repo-boundary-audit.md`
- `docs/repo-boundary-pilot-plan.md`
- `README.md`

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| `openWorkflow` clearly states canonical workflow policy ownership | Yes | `docs/repo-boundary-audit.md` | Defines `openWorkflow` as policy, contract, authority, and traceability owner |
| `Hermes-Install` responsibility is defined | Yes | `docs/repo-boundary-audit.md` | Scoped to Hermes install, operations, backup, restore, upgrade, and DR |
| `Omnigent-Install` responsibility is defined | Yes | `docs/repo-boundary-audit.md` | Scoped to Omnigent/Polly install, workers, operations, backup, restore, upgrade, and DR |
| migration phases are documented | Yes | `docs/repo-boundary-audit.md` and `docs/repo-boundary-pilot-plan.md` | Includes classify, copy policy, link install repos, defer runtime moves, submodule plan |
| open decisions are listed | Yes | `docs/repo-boundary-audit.md` and `design.md` | Includes Hermes remote ownership and proof-harness location |
| first feature is doc-only and `openWorkflow` only | Yes | this evidence file and git diff | No install repo edits, no runtime code, no submodules |
| README links to boundary docs and OpenSpec change | Yes | `README.md` | Boundary audit, pilot plan, and active OpenSpec change are linked |

## Local Checks

Required checks for this feature:

```bash
OPENSPEC_TELEMETRY=0 openspec validate restructure-factory-repo-boundaries --strict
git diff --check
git status --short
```

Expected result:

- OpenSpec change validates
- markdown diff has no whitespace errors
- changed files are limited to `openWorkflow` documentation/OpenSpec artifacts

## Branch Review

Review result: PASS

Review notes:

- The change is documentation/OpenSpec-only.
- It does not alter `Hermes-Install` or `Omnigent-Install`.
- It does not add submodules.
- It does not move runtime code.
- It does not include secret, credential, database, or runtime workspace files.

## PR Admission

Decision: ADMIT

Reason:

FEAT-RB-001 satisfies the pilot guardrails and creates the canonical boundary
policy evidence needed before later install repo scope changes.

Conditions:

- Do not include FEAT-RB-002 or later feature work in the same PR.
- Do not archive the OpenSpec change until all approved feature slices are
  complete.
