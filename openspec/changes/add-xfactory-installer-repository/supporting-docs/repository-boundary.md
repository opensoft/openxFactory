# xFactory Installer Repository Boundary

Status: record
Kind: decision-input
Proposal origin: ad hoc
Authorized by: explicit user direction in the xFactory Cloud PC intake task
Captured: 2026-07-09

## Decision Input

Create one private neutral product repository named
`opensoft/xFactory-Installer` and pin it in the top-level xFactory aggregation
repository at `installs/xfactory-installer`.

The repository owns implementation and release surfaces for the branded
xFactory intake and installer product family. The first named product is
`xFactory Workstation Intake`. Canonical intake contracts remain in
openxFactory, tenant Intune and Graph authority remains in OpsxFactory, and
workstation end-state requirements remain in CloudPC-Install.

This proposal was authorized directly from design discussion and did not derive
from an existing brainstorm or staging folder. It is therefore explicitly
ad hoc rather than assigned a fabricated staging identifier.
