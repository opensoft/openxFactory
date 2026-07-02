# Phase 2 Contract Pinning And Compatibility Evidence

Decision: READY FOR PR ADMISSION

## Install Repo PRs

| Repo | PR | Result | Commit |
|---|---|---|---|
| `opensoft/Omnigent-Install` | #3 | Merged | `53e40ab6bf3ab115a1b7b1add46879900b1ff43a` |
| `FarHeap/Hermes-Install` | #3 | Merged | `8dfbca1ed9a22fc896848ad22e7c5355a02e91eb` |

## Omnigent-Install Updates

- Added `contracts/openxfactory-contract-ref.yaml`.
- Added `scripts/validate-openxfactory-contracts.py`.
- Updated schema and policy README files with compatibility validation command.
- Validation checks referenced `openxFactory` commit `229761c`.
- Local schema and policy compatibility copies remain in place.

Validation:

- `python3 scripts/validate-openxfactory-contracts.py`
- `git diff --check`
- no-secret scan on changed files; only match was the `merge-risk-policy.yaml`
  filename

## Hermes-Install Updates

- Added `contracts/openxfactory-contract-ref.yaml`.
- Added `contracts/README.md`.
- Added `scripts/validate-openxfactory-contracts.py`.
- Uses `canonical_only` compatibility mode because Hermes-Install does not keep
  local copies of every contract.
- Validation checks referenced `openxFactory` commit `229761c`.

Validation:

- `python3 scripts/validate-openxfactory-contracts.py`
- `git diff --check`
- no-secret scan reviewed; matches were existing operational script text or
  policy filenames, not new secret material

## openxFactory Updates

- Updated `installs/omnigent-install` submodule pin to
  `53e40ab6bf3ab115a1b7b1add46879900b1ff43a`.
- Hermes-Install is not yet an `openxFactory` submodule, so no Hermes submodule
  pin changed.

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| Omnigent records which `openxFactory` commit it implements | Yes | `opensoft/Omnigent-Install#3` | `contracts/openxfactory-contract-ref.yaml` |
| Hermes records which `openxFactory` commit it implements | Yes | `FarHeap/Hermes-Install#3` | `contracts/openxfactory-contract-ref.yaml` |
| Validation checks referenced commit and required contracts | Yes | install PR evidence | Both validators passed |
| Local compatibility copies are not deleted | Yes | install PR diffs | Omnigent copies retained; Hermes uses canonical-only mode |
| Runtime adapters are not moved | Yes | install PR diffs | Only docs/contract refs/scripts changed |

## Stop Conditions Checked

- No install repo compatibility copies were deleted.
- No runtime code movement.
- No generated adapters, manifests, credentials, databases, logs, or workspaces touched.
- No Hermes dirty local working-tree changes were used; Hermes work was done in
  a clean worktree.

## Validation Plan

- `openspec validate enable-live-openxfactory-factory --strict`
- `openspec validate --all --strict`
- `git diff --check`
- `git submodule status`
