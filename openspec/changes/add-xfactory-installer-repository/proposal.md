code_surface: openxFactory, xFactory, xFactory-Installer, OpsxFactory, cloudpc-install
target_release: repository-bootstrap

## Why

The branded xFactory workstation-intake application needs an independent
security, build, Store-certification, and release lifecycle, while the xFactory
aggregation repository must remain a pin-only workspace assembler. Establishing
the repository boundary now prevents the public installer implementation from
being mixed into canonical contracts, a domain factory, or Cloud PC host
requirements.

## What Changes

- Create private repository `opensoft/xFactory-Installer` as the implementation
  home for xFactory intake and installer applications.
- Bootstrap the repository with ownership, architecture, contract-consumption,
  security, validation, and release documentation without claiming that the
  WinUI application is already implemented.
- Define `xFactory Workstation Intake` as the first product surface, with future
  website, CLI/TUI, or cross-platform surfaces required to share the same
  neutral intake contract.
- Add the repository to the top-level xFactory aggregation repo at
  `installs/xfactory-installer` and pin an exact initial release commit.
- Keep canonical intake and enrollment evidence contracts in openxFactory;
  keep Intune/Graph administration and tenant credentials in OpsxFactory; and
  keep workstation end-state requirements in CloudPC-Install.
- Record the repository remote, visibility, update process, compatibility
  declaration, and rollback procedure before treating the pin as supported.

## Capabilities

### New Capabilities

- `workstation-intake`: Defines the neutral product and authority boundary for
  device eligibility, consent, Microsoft enrollment handoff, verification, and
  installer release evidence.

### Modified Capabilities

- `repo-boundary-governance`: Adds the independently released xFactory installer
  repository and its aggregation pin, compatibility, update, and rollback
  requirements.

## Impact

- **openxFactory:** Owns the proposal and canonical workstation-intake contract.
- **xFactory-Installer:** New private product repository for application code,
  packaging, Store metadata, tests, and release evidence.
- **xFactory aggregation:** Adds one exact submodule pin and documents it in the
  workspace topology.
- **OpsxFactory:** Remains the authority for tenant Intune policy, Graph grants,
  deployment, compliance, and remediation; no credentials move into the app.
- **CloudPC-Install:** Continues to own host eligibility and required end state,
  and may reference the installer without owning its implementation.
- **Compatibility:** Initial repository bootstrap is tagged independently and
  consumes openxFactory by explicit compatibility declaration rather than
  copying canonical policy.
