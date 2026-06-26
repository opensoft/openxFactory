## Why

The factory documentation has grown across `openWorkflow`, `Hermes-Install`,
and `Omnigent-Install`, which makes it unclear which repo owns workflow policy
versus subsystem installation and recovery. We need a governed repo-boundary
change now so Hermes, Omnigent/Polly, OpenSpec, Spec Kit, GitHub, and the
merge council can evolve without duplicating policy or breaking working
install proofs.

## What Changes

- Establish `openWorkflow` as the canonical authority for factory workflow
  policy, cross-system roles, traceability, merge policy, and shared
  contracts.
- Narrow `Hermes-Install` to Hermes installation, operations, backup, restore,
  upgrade, and DR.
- Narrow `Omnigent-Install` to Omnigent/Polly installation, worker runtime,
  credential setup, operations, backup, restore, upgrade, and DR.
- Use copy-first migration for canonical policy so current install repo proofs
  remain stable while policy moves into `openWorkflow`.
- Add a canonical contract home in `openWorkflow` before moving schema files or
  generating adapters.
- Defer submodule creation until policy, contract ownership, and install repo
  scope links are approved.
- Defer runtime code moves, file deletions, and Hermes remote changes to later
  approved features.

## Capabilities

### New Capabilities

- `repo-boundary-governance`: Defines how the factory assigns canonical
  ownership between `openWorkflow`, `Hermes-Install`, and `Omnigent-Install`,
  including migration phases, allowed changes, and stop conditions.
- `shared-contract-ownership`: Defines how cross-system workflow contracts,
  schemas, version pins, and install-repo adapters are governed from
  `openWorkflow`.

### Modified Capabilities

- None.

## Impact

- Affected repositories:
  - `opensoft/openWorkflow`
  - `opensoft/Omnigent-Install`
  - `FarHeap/Hermes-Install`, or a future `opensoft/Hermes-Install` mirror
- Initial implementation is documentation-only and starts in `openWorkflow`.
- Later features may update install repo READMEs, add `openWorkflow/contracts/`,
  and add install repos as submodules after explicit approval.
- No secrets, credential profiles, generated databases, runtime workspaces, or
  live service manifests are moved by the initial proposal.
- Source documents:
  - `docs/repo-boundary-audit.md`
  - `docs/repo-boundary-pilot-plan.md`
