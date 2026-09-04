---
code_surface: opensoft/xFactory (the aggregation — the `.gitmodules` entry and the gitlink at `xFactories/MedxChart`), opensoft/MedxChart (the new descendant repository — `contracts/openchart-pin.yaml`, the nested `openChart` gitlink, its own `.gitmodules`, `README.md`, `AGENTS.md`), and MedxFactory (ONE documentation line, commit `933c5025`). openxFactory itself carries NO runtime artifact here: this packet, its two spec deltas, and one README "OpenSpec Records" row — no contract, no schema, no manifest row, no release surface, no validator. THE DESCENDANT PIN VALIDATOR AND ITS REQUIRED CHECK DO NOT YET EXIST in `opensoft/MedxChart`; they are commissioned as the bound follow-on at `tasks.md` § 5, which gates ARCHIVE and not this ratification.
target_release: implemented — each affected repository's own main line, and the topology is already on them. `opensoft/MedxChart` exists and is published; its `main` is `68d2f1f5db932cb5099ceac75dab66316ef22579`, exactly the commit the aggregation's gitlink names. The aggregation landed the boundary at `bed2a69` ("Replace openChart aggregate with MedxChart", 2026-08-23) and CORRECTED the submodule URL this proposal originally chose at `386e7ee2` (2026-08-25) — see § Impact and `design.md` Decision 2. No contract bundle is cut and no release tag is owed. This field read `implementation_pending` until 2026-09-03; that is not a legal value of the field under `release-realization`, and it was also false.
Status: ratified
Proposed: 2026-08-23
Ratified: 2026-09-03 by Brett Heap (openxFactory operator authority) — "ratify both, 1 and 1"; record at review/ratification-2026-09-03.md
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

- `domain-descendant-boundary`: the promoted requirement **A descendant is
  placed at a ratified placement** records the aggregation's `xFactories/`
  placement as REALIZED BUT NOT YET RATIFIED, names THIS change as the
  establishing act, and states in its own scenario that when this change
  archives the requirement "is amended by an explicit delta to say so rather
  than by re-reading". This change carries that explicit delta
  (`specs/domain-descendant-boundary/spec.md`): the placement is RATIFIED as of
  2026-09-03 and its realized placements are BOTH `xFactories/MedxChart` and
  `xFactories/MedxPractice`. **This change owns the placement delta and the
  sibling `create-medxpractice-overlay-boundary` carries none**, so one
  requirement has one writer and the ordering question the
  `release-realization` sequencing rule exists for never arises between them.
- No runtime clinical behavior is modified. The topology and provenance
  statement above is the whole of the modification.

## Impact

- A new local Git repository and nested submodule are added.
- The xFactory superproject's `.gitmodules`, gitlink, project register, README,
  and MedxFactory documentation links change.
- Existing vendored SHA-256 evidence remains immutable; the MedxChart pin must
  identify the current openChart commit without rewriting the upstream history.
- **CORRECTED 2026-09-03 — the remote EXISTS.** As authored this bullet read
  "The change intentionally does not create or push a GitHub remote
  repository." That was true of the local act of 2026-08-23 and is no longer
  true of the world: `opensoft/MedxChart` is a PRIVATE repository at
  https://github.com/opensoft/MedxChart, last pushed 2026-08-23T20:23:45Z, and
  the aggregation resolves `xFactories/MedxChart` against it. The remote was
  published outside this packet's task list; the packet is corrected to
  acknowledge it rather than left asserting an absence a reader can disprove
  with one API call. `opensoft/MedxPractice` was published the same way.
  `adopt-medxsoft-repository-identity` moves `opensoft/MedxFactory` and
  `opensoft/MedxEHR` to the `MedxSoft` organization and names no other
  repository; MedxChart's `opensoft/` home is not moved by this act or by that
  one, and the aggregation's live `.gitmodules` still reads
  `git@github.com:opensoft/MedxChart.git`.
