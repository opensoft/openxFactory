Status: ratified
Ratified: 2026-06-26 — record: the archive act, commit `7c4dacb` "Archive repo boundary OpenSpec change", which applied this change's spec delta into `openspec/specs/repo-boundary-governance/spec.md`, `openspec/specs/shared-contract-ownership/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. This is the repository's first OpenSpec change. The `.openspec.yaml` origin pair (`approved_by: Brett`, `approved_on: 2026-06-26`) is permission to author and is NOT cited as the ratification, per the register's C2 ruling. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The factory documentation has grown across `openxFactory`, `Hermes-Install`,
and `Omnigent-Install`, which makes it unclear which repo owns workflow policy
versus subsystem installation and recovery. We need a governed repo-boundary
change now so Hermes, Omnigent/Polly, OpenSpec, Spec Kit, GitHub, and the
merge council can evolve without duplicating policy or breaking working
install proofs.

## What Changes

- Establish `openxFactory` as the canonical authority for factory workflow
  policy, cross-system roles, traceability, merge policy, and shared
  contracts.
- Narrow `Hermes-Install` to Hermes installation, operations, backup, restore,
  upgrade, and DR.
- Narrow `Omnigent-Install` to Omnigent/Polly installation, worker runtime,
  credential setup, operations, backup, restore, upgrade, and DR.
- Use copy-first migration for canonical policy so current install repo proofs
  remain stable while policy moves into `openxFactory`.
- Add a canonical contract home in `openxFactory` before moving schema files or
  generating adapters.
- Defer submodule creation until policy, contract ownership, and install repo
  scope links are approved.
- Defer runtime code moves, file deletions, and Hermes remote changes to later
  approved features.

## Capabilities

### New Capabilities

- `repo-boundary-governance`: Defines how the factory assigns canonical
  ownership between `openxFactory`, `Hermes-Install`, and `Omnigent-Install`,
  including migration phases, allowed changes, and stop conditions.
- `shared-contract-ownership`: Defines how cross-system workflow contracts,
  schemas, version pins, and install-repo adapters are governed from
  `openxFactory`.

### Modified Capabilities

- None.

## Impact

- Affected repositories:
  - `opensoft/openxFactory`
  - `opensoft/Omnigent-Install`
  - `FarHeap/Hermes-Install`, or a future `opensoft/Hermes-Install` mirror
- Initial implementation is documentation-only and starts in `openxFactory`.
- Later features may update install repo READMEs, add `openxFactory/contracts/`,
  and add install repos as submodules after explicit approval.
- No secrets, credential profiles, generated databases, runtime workspaces, or
  live service manifests are moved by the initial proposal.
- Source documents:
  - `docs/repo-boundary-audit.md`
  - `docs/repo-boundary-pilot-plan.md`
