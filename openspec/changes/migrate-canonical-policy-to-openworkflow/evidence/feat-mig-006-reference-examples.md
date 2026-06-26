# FEAT-MIG-006 Reference Pilot And Example Placement Evidence

Decision: READY FOR PR ADMISSION

## Sources Reviewed

- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-decomposition/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-speckit/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-pr-admission/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-merge-council/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-next-non-doc/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/merge-master/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/live-pilot/`
- `/home/brett/projects/Agents/Omnigent-Install/pilot-flows/`

## Target Artifacts

- `examples/README.md`
- `examples/project-alfa/`
- `examples/merge-master/`
- `README.md`

## Placement Decision

| Example Type | Home |
|---|---|
| Canonical static workflow examples | `openWorkflow/examples` |
| Executable install proofs and harness fixtures | `Omnigent-Install` |
| Future executable factory lab | future `factory-lab` repo |

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| Hermes approves the placement decision | Yes | `examples/README.md` | Placement is documented for canonical examples, install proofs, and future lab |
| No proof harness is moved until replacement validation exists | Yes | Git diff | Live pilot and pilot-flow materials remain in `Omnigent-Install` |
| Canonical reference examples live in `openWorkflow` | Yes | `examples/project-alfa/`, `examples/merge-master/` | Static examples copied only |
| Generated state, credentials, databases, logs, and local workspaces are excluded | Yes | `examples/README.md` and file inventory | Only `.example.yaml` and `.example.md` style references copied |

## Stop Conditions Checked

- No install repo deletions.
- No runtime code movement.
- No generated state, credentials, databases, logs, or workspaces touched.
- No submodule pointer changes.
- No live pilot harness moved.

## Validation Plan

- `openspec validate migrate-canonical-policy-to-openworkflow --strict`
- `openspec validate --all --strict`
- YAML parse for copied `examples/**/*.yaml`
- `git diff --check`
- `git submodule status`

## PR Admission

This feature is static-example-copy-only, below the PR size limit, and preserves
copy-first migration boundaries. It is ready to open a PR after validation.
