# FEAT-MIG-007 Mark Install Repo Policy Copies Evidence

Decision: READY FOR PR ADMISSION

## Install Repo PRs

| Repo | PR | Result | Commit |
|---|---|---|---|
| `opensoft/Omnigent-Install` | #2 | Merged | `f805d473f710dbbd247e17385e65f8ed50a6ece5` |
| `FarHeap/Hermes-Install` | #2 | Merged | `705e258262e655fcba48f15774436c2fefa2a0fb` |

## Omnigent-Install Updates

Marked migrated policy/schema/example copies as install implementation or
compatibility copies:

- `docs/project-lead-agents.md`
- `docs/hermes-governance-agents.md`
- `docs/hermes-profiles-and-groups.md`
- `docs/hermes-integration-plan.md`
- `docs/runbooks/phase3-feature-decomposition.md`
- `docs/runbooks/phase6-pr-admission.md`
- `docs/runbooks/merge-master-implementation-plan.md`
- `schemas/README.md`
- `policies/README.md`
- `examples/README.md`

Validation:

- `git diff --check`
- no-secret scan on changed docs/README files

## Hermes-Install Updates

Marked `openWorkflow` as canonical factory workflow policy home in:

- `README.md`

Validation:

- `git diff --check`
- no-secret scan reviewed; matches were existing operational references in the
  README, not new content

## openWorkflow Updates

- Updated `installs/omnigent-install` submodule pin from `e254c22` to
  `f805d47`.
- Recorded install repo evidence in this file.

Hermes-Install is not yet an `openWorkflow` submodule, so no Hermes submodule
pin was changed.

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| Migrated `Omnigent-Install` source docs link to canonical policy or are labeled implementation copies | Yes | `opensoft/Omnigent-Install#2` | Docs, schema copies, policy copies, and example copies marked |
| Migrated `Hermes-Install` source docs link to canonical policy or are labeled operational install docs | Yes | `FarHeap/Hermes-Install#2` | README marker added |
| Install repo validation and no-secret checks run | Yes | PR evidence above | No runtime files changed |
| Install repo PR evidence is recorded in OpenSpec | Yes | This file | Includes PRs and commits |

## Stop Conditions Checked

- No install repo deletions.
- No runtime code movement.
- No generated adapters, manifests, credentials, databases, logs, or workspaces touched.
- No Hermes dirty local working-tree changes were used; Hermes PR was created
  from a clean temporary clone.
- Only the Omnigent submodule pointer changed in `openWorkflow`.

## Validation Plan

- `openspec validate migrate-canonical-policy-to-openworkflow --strict`
- `openspec validate --all --strict`
- `git diff --check`
- `git submodule status`

## PR Admission

This feature is documentation/linking plus a submodule pin update to the merged
Omnigent marker commit. It is ready to open a PR after validation.
