---
code_surface: xFactory aggregation and Medx clinical repository topology
target_release: implementation_pending
Status: draft
---
# Proposal: create-medxchart-overlay-boundary

## Why

`openChart` is an independent public clinical-chart repository, but the xFactory
aggregation currently presents it as the Medx clinical program's submodule. A
dedicated `MedxChart` repository is needed to own the Medx-specific composition
boundary while keeping the upstream `openChart` revision independently movable
and explicitly pinned.

## What Changes

- Create a local Git repository named `MedxChart` under the projects workspace.
- Make `MedxChart` pin the current `openChart` commit as a nested submodule and
  record the upstream revision in a committed pin manifest.
- Replace the xFactory aggregate's `xFactories/openChart` submodule with
  `xFactories/MedxChart`.
- Move the canonical standalone `openChart` checkout to the projects workspace
  root and update documentation and worktree references that assume the old
  sibling path.
- Update the Medx program register and cross-repository references so MedxChart
  is the Medx clinical component while the upstream provenance remains clear.

## Capabilities

### New Capabilities

- `medxchart-overlay-boundary`: Defines the repository and submodule contract
  for a Medx-specific chart composition pinned to an independent openChart
  revision.

### Modified Capabilities

- None. This change modifies repository topology and provenance, not runtime
  clinical behavior.

## Impact

- A new local Git repository and nested submodule are added.
- The xFactory superproject's `.gitmodules`, gitlink, project register, README,
  and MedxFactory documentation links change.
- Existing vendored SHA-256 evidence remains immutable; the MedxChart pin must
  identify the current openChart commit without rewriting the upstream history.
- The change intentionally does not create or push a GitHub remote repository.
