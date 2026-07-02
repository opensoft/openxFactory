## Why

The repo-boundary work established that `openxFactory` owns canonical factory
policy and contracts, but much of that material still lives in install and
proof repositories. We need a governed, dogfooded migration so canonical policy
and contracts move into `openxFactory` without breaking install repos,
runtime proof harnesses, or traceability.

## What Changes

- Create a new OpenSpec-governed migration that uses the factory stack on
  itself: OpenSpec proposal, Hermes approval, Omnigent/Polly decomposition,
  approved feature slices, PR admission, merge council, and GitHub PRs.
- Copy or summarize canonical policy from `Omnigent-Install` and
  `Hermes-Install` into `openxFactory`.
- Add canonical docs for roles/authority, Spec Kit stage ownership, PR
  admission, merge master, and migrated policy surfaces.
- Copy shared contracts into `openxFactory/contracts/` with provenance and
  compatibility rules.
- Decide where reference pilots and proof examples belong before moving them.
- Mark install repo policy copies as implementation notes, legacy copies, or
  operational runbooks after canonical replacements exist.
- Defer deletions and runtime code moves to later approved cleanup features.

## Capabilities

### New Capabilities

- `canonical-policy-migration`: Governs copy-first migration of canonical
  workflow policy, roles, authority, stage ownership, PR admission, merge
  authority, feature decomposition, and traceability into `openxFactory`.
- `canonical-contract-migration`: Governs copy-first migration of shared
  contracts, schemas, and policy YAML into `openxFactory/contracts/` with
  source provenance and compatibility metadata.
- `reference-proof-placement`: Governs placement of end-to-end examples,
  pilot flows, and proof harnesses without breaking existing validation.

### Modified Capabilities

- `repo-boundary-governance`: Adds dogfood migration requirements after the
  repo-boundary pilot.
- `shared-contract-ownership`: Adds contract migration and provenance
  requirements for copied schemas and policies.

## Impact

- Primary target repo:
  - `opensoft/openxFactory`
- Related source repos:
  - `opensoft/Omnigent-Install`
  - `FarHeap/Hermes-Install`
- Initial work is copy-first and documentation/contract focused.
- Source docs remain in place until canonical copies are merged and install
  repo links are updated.
- No secrets, credential profiles, generated databases, runtime workspaces,
  installed service state, or provider auth material are moved.
- Submodule pointers are not changed by content migration PRs.
