# FEAT-MIG-008 Removal Or Cleanup Decision Evidence

Decision: READY FOR PR ADMISSION

## Sources Reviewed

- `docs/dogfood-content-migration-plan.md`
- `docs/repo-boundary-audit.md`
- `contracts/README.md`
- `examples/README.md`
- `openspec/changes/migrate-canonical-policy-to-openworkflow/evidence/feat-mig-007-install-repo-markers.md`
- `opensoft/Omnigent-Install#2`
- `FarHeap/Hermes-Install#2`

## Target Artifacts

- `docs/content-cleanup-decision.md`
- `README.md`

## Decision Summary

Keep migrated install repo copies for now as marked implementation,
compatibility, or operational copies. Do not remove install repo docs, schemas,
policies, examples, runtime files, generated adapters, manifests, logs,
databases, or workspaces in this migration.

Future removals require separate approved PRs with replacement validation and a
rollback path.

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| Decide whether legacy policy copies should be removed, archived, or kept | Yes | `docs/content-cleanup-decision.md` | Keep marked copies for now |
| If removals are approved, isolate them in dedicated PRs | Yes | `docs/content-cleanup-decision.md` | No removals approved in this slice |
| Confirm no runtime files, scripts, manifests, or generated adapters are removed | Yes | Git diff | This slice adds docs only |
| Document rollback path | Yes | `docs/content-cleanup-decision.md` | Revert cleanup PR, restore pins, rerun checks, record failure |

## Stop Conditions Checked

- No install repo deletions.
- No runtime code movement.
- No generated adapters, manifests, credentials, databases, logs, or workspaces touched.
- No submodule pointer changes.

## Validation Plan

- `openspec validate migrate-canonical-policy-to-openworkflow --strict`
- `openspec validate --all --strict`
- `git diff --check`
- `git submodule status`

## PR Admission

This feature is documentation-only, below the PR size limit, and preserves
copy-first migration boundaries. It is ready to open a PR after validation.
