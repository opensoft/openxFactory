---
code_surface: opensoft/MedxPractice (the new descendant repository, CREATED by this change — its single commit `d8d73195` carrying `.gitmodules`, `AGENTS.md`, `README.md`, `contracts/openpractice-pin.yaml` and the nested `openPractice` gitlink), opensoft/xFactory (the aggregation — the `.gitmodules` entry, the `xFactories/MedxPractice` gitlink, `README.md`, `CLAUDE.md` and `project-register.yaml`, all at `3a365206`), and MedxFactory (`README.md` ONLY, five added lines at `ccd40789`). openxFactory itself carries NO runtime artifact here: this packet, ONE spec delta, and one README "OpenSpec Records" row — no contract, no schema, no manifest row, no release surface, no validator. THE DESCENDANT PIN VALIDATOR AND ITS REQUIRED CHECK DO NOT YET EXIST in `opensoft/MedxPractice` — `gh api repos/opensoft/MedxPractice/actions/workflows` returns `{"total_count":0,"workflows":[]}` and its only two rulesets are ORGANIZATION-sourced ("Copilot Auto-Review All PRs", "Require Code Owner Review"), neither a status check. They are commissioned as the bound follow-on at `tasks.md` § 5, which gates ARCHIVE and not this ratification.
target_release: implemented — each affected repository's own main line, and the topology is already on them. `opensoft/MedxPractice` exists (PRIVATE, created 2026-08-23T20:44:44Z); its `main` is `d8d73195609df3b567643a7bf1252eac352d9996`, exactly the commit the aggregation's gitlink names. The aggregation landed the boundary at `3a365206` ("Add MedxPractice composition boundary", 2026-08-23T20:46:44Z) and NORMALIZED the submodule URL from the relative `../MedxPractice` this packet chose to the absolute `git@github.com:opensoft/MedxPractice.git` at `386e7ee2` (2026-08-25) — the same commit that corrected its MedxChart sibling; see `design.md` Risk 3. No contract bundle is cut and no release tag is owed. The proposal carried NO front-matter block at all until 2026-09-03 — a bare `Status: draft` on line one — so both declarations `release-realization` requires are stated here for the first time rather than corrected.
Status: ratified
Proposed: 2026-08-23
Ratified: 2026-09-03 by Brett Heap (openxFactory operator authority) — "ratify both, 1 and 1"; record at review/ratification-2026-09-03.md
---
# Proposal: create-medxpractice-overlay-boundary

## Why

The public `openPractice` checkout currently exists as an untracked workspace
copy rather than a governed composition boundary. Medx needs a private branded
practice-operations overlay that can pin a known public upstream revision while
keeping the upstream repository independently usable and replaceable.

## What Changes

- Create a private `MedxPractice` repository in the `opensoft` organization.
- Make `MedxPractice` compose a pinned `openPractice` git submodule and a
  machine-readable upstream pin manifest.
- Move the standalone `openPractice` checkout to the shared projects area and
  remove the untracked copy from the xFactory aggregation workspace.
- Add `MedxPractice` to the xFactory aggregation in the role previously
  occupied by any direct public practice-operations checkout.
- Update MedxFactory documentation and composition references to use
  `MedxPractice` as the branded practice-operations boundary.
- Publish the private repository and all reachable aggregate pins.

## Capabilities

### New Capabilities

- `medxpractice-overlay-boundary`: Govern the private MedxPractice composition
  boundary and its immutable openPractice upstream pin. **NARROWED 2026-09-03**
  under decision 2 option 1 to what is MedxPractice-SPECIFIC — the identity of
  this pin, the aggregation's single route to `openPractice` that the relocation
  left behind, and this descendant's placement CITED rather than restated. The
  three requirements as authored restated promoted `domain-descendant-boundary`
  in differing words, which the Explicit delta rule
  (`openspec/specs/document-lifecycle/spec.md:149-161`) calls a defect. It was
  narrowed AGAIN in the pre-capture fix round on pull request #609: the
  placement requirement states none of the path, remote or gitlink in its body
  (they are evidence in its scenarios), the relocation requirement keeps only
  the half a remote reading can settle with the workspace-root layout recorded
  as a local convention at `design.md` Decision 4, and the pin manifest is
  described in the NESTED shape the descendant actually carries. The narrowing,
  both rounds of it, and the mapping of each old requirement to the promoted one
  it restated are stated at the head of
  `specs/medxpractice-overlay-boundary/spec.md`.

### Modified Capabilities

- **NONE, AND THE NONE IS DELIBERATE.** As authored this section read
  "`<!-- No existing openxFactory capability requirements change. -->`", and that
  was WRONG in a way worth correcting rather than deleting: the promoted
  `domain-descendant-boundary` requirement **A descendant is placed at a
  ratified placement** DOES change, because it carried the aggregation's
  `xFactories/` placement as "REALIZED BUT NOT YET RATIFIED" and this ruling
  ratifies it. **That modification is carried by the sibling change**
  `create-medxchart-overlay-boundary`, at
  `openspec/changes/create-medxchart-overlay-boundary/specs/domain-descendant-boundary/spec.md`,
  whose delta names BOTH `xFactories/MedxChart` and `xFactories/MedxPractice`
  (gitlink `d8d73195609df3b567643a7bf1252eac352d9996`) as the ratified
  placement's realized placements. **This change CITES that delta and carries no
  `## MODIFIED Requirements` block of its own** — one requirement, one writer,
  so the ordering hazard `release-realization`'s sequencing rule exists for
  never arises between the two Medx packets, and neither can drift from the
  other's statement of a rule they share.
- **What this change RELIES ON WITHOUT MODIFYING**, named under the Explicit
  delta rule rather than restated — ALL FIVE promoted
  `domain-descendant-boundary` requirements:
  **A domain consumes a neutral product through a descendant repository**
  (`openspec/specs/domain-descendant-boundary/spec.md:6-16`),
  **A descendant pins the product by commit, twice** (`:30-41`),
  **A descendant carries profile, never fork** (`:55-62`),
  **A descendant is placed at a ratified placement** (`:76-85`) — relied on
  here, MODIFIED by the sibling's delta cited above, and not written twice —
  and **A descendant is created on its first profile, not before** (`:103-120`),
  under which MedxPractice is a REPORTED EMPTY BOUNDARY (`tasks.md` § 6 and
  `review/ratification-2026-09-03.md` § 4) rather than precedent for creating
  more.
- No runtime practice-operations behavior is modified. The topology and
  provenance statement above is the whole of the modification.

## Impact

- New private repository: `opensoft/MedxPractice` — PRIVATE over a PUBLIC
  upstream, which is the boundary's reason for existing.
- xFactory aggregation submodule metadata, project register, and orientation
  documentation.
- MedxFactory orientation/composition documentation — **measured 2026-09-03 as
  ONE FILE**: `README.md`, five insertions and no deletions, at `ccd40789`
  ("Use MedxPractice branded practice overlay", 2026-08-23T20:45:44Z).
- No changes to the public `openPractice` repository history or runtime code.
  Its `main` has since moved two commits ahead of the pinned revision
  (`0ec9fca7` vs `9526bd9e`, read 2026-09-03) and the composition has not
  followed it, which is the pin working rather than the pin ageing.
