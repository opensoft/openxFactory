# Merge Readiness Report

Feature: FEAT-MIG-006 Reference Pilot And Example Placement
PR: opensoft/openxFactory#15
Decision: READY

## Inputs Reviewed

- `openspec/changes/migrate-canonical-policy-to-openxfactory/proposal.md`
- `openspec/changes/migrate-canonical-policy-to-openxfactory/design.md`
- `openspec/changes/migrate-canonical-policy-to-openxfactory/tasks.md`
- `openspec/changes/migrate-canonical-policy-to-openxfactory/specs/reference-proof-placement/spec.md`
- `examples/README.md`
- `examples/project-alfa/`
- `examples/merge-master/`
- `openspec/changes/migrate-canonical-policy-to-openxfactory/evidence/feat-mig-006-reference-examples.md`
- GitHub PR metadata for `opensoft/openxFactory#15`

## PR Metadata

| Field | Value |
|---|---|
| Title | Add canonical reference examples |
| Base | `main` |
| Head | `feat/mig-006-reference-examples` |
| Changed files | 51 |
| Additions | 2252 |
| Deletions | 4 |
| Mergeable | Yes |
| Review decision | None recorded |
| Status checks | None configured |

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| Placement decision is documented | Yes | `examples/README.md` | Defines openxFactory, Omnigent-Install, and future factory-lab homes |
| No proof harness is moved before replacement validation | Yes | `examples/README.md`, Git diff | Live pilot and pilot-flow harnesses remain in `Omnigent-Install` |
| Canonical reference examples live in `openxFactory` | Yes | `examples/project-alfa/`, `examples/merge-master/` | Static examples copied |
| Generated state, credentials, databases, logs, and local workspaces are excluded | Yes | File inventory | No secrets, databases, logs, or local workspaces copied |
| Copy-first boundary is preserved | Yes | Git diff | No install repo edits, deletions, runtime moves, or submodule pointer changes |

## Local Checks

| Check | Result |
|---|---|
| `openspec validate migrate-canonical-policy-to-openxfactory --strict` | Pass |
| `openspec validate --all --strict` | Pass |
| YAML parse for copied `examples/**/*.yaml` | Pass |
| `git diff --check` | Pass |
| `git submodule status` | Pass; `installs/omnigent-install` remains pinned to `e254c22` |

## Council Results

| Reviewer | Decision | Blocking |
|---|---|---:|
| Spec Traceability | Pass | No |
| Security | Pass | No |
| Tests | Pass | No |
| Architecture | Pass | No |
| Maintainability | Pass | No |

## Required Fixes

None.

## Merge Master Recommendation

Approve as low-risk static reference-example migration. No live harness,
credentials, runtime generated state, database, or submodule pointer changed.
No human review escalation is required by the current risk policy.
