# FEAT-MIG-001 Roles And Authority Evidence

Decision: READY FOR PR ADMISSION

## Sources Reviewed

- `/home/brett/projects/Agents/Omnigent-Install/docs/project-lead-agents.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/hermes-governance-agents.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/hermes-profiles-and-groups.md`
- `/home/brett/projects/Agents/Hermes-Install/README.md`

## Target Artifact

- `docs/roles-and-authority.md`
- `README.md`

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| Defines PO, PM, CA, PA, LA, LE, LC, LQ, LI, LS, Merge Master, and Merge Council | Yes | `docs/roles-and-authority.md` | Includes ownership, decision scope, and escalation boundaries |
| Separates Hermes governance roles from Omnigent execution roles | Yes | `docs/roles-and-authority.md` | Hermes owns governance and approval; Omnigent owns repo execution |
| Preserves source provenance | Yes | `docs/roles-and-authority.md` | Source files are listed explicitly |
| Leaves install repo source docs in place | Yes | Git diff | This slice changes `openxFactory` only |
| Updates openxFactory documentation index | Yes | `README.md` | Adds the canonical role doc |

## Stop Conditions Checked

- No install repo deletions.
- No runtime code movement.
- No generated state, credentials, databases, logs, or workspaces touched.
- No submodule pointer changes.
- No agent roster mutation.

## Validation Plan

- `openspec validate migrate-canonical-policy-to-openxfactory --strict`
- `openspec validate --all --strict`
- `git diff --check`
- `git submodule status`

## PR Admission

This feature is documentation-only, below the PR size limit, and preserves
copy-first migration boundaries. It is ready to open a PR after validation.
