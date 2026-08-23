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
  boundary and its immutable openPractice upstream pin.

### Modified Capabilities

<!-- No existing openxFactory capability requirements change. -->

## Impact

- New private repository: `opensoft/MedxPractice`.
- xFactory aggregation submodule metadata, project register, and orientation
  documentation.
- MedxFactory orientation/composition documentation.
- No changes to the public `openPractice` repository history or runtime code.
