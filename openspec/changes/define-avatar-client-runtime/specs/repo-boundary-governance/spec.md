# repo-boundary-governance Specification

## ADDED Requirements

### Requirement: Neutral avatar-client repository boundary
The reusable Flutter avatar implementation SHALL live in a private,
independently released repository named `xfactory-avatar-client`, created by
the `implement-avatar-client-lab` successor change. From creation it SHALL
own the Flutter application and packages, client bindings, pure reducers, UI
and platform adapters, constrained control and media clients, and client
tests. It SHALL pin the exact compatible openxFactory contract commit and
digests and MUST NOT contain a standard provider API key, server tool
handler, server provider configuration, or a copied neutral schema without
pin and fixture-conformance validation.

The openxFactory repository SHALL remain the canonical owner of contracts
and the reference server trust boundary. The future conventional web console
and its bindings SHALL remain outside the client repository until separately
approved.

#### Scenario: Client repository is created
- **WHEN** the successor change creates `xfactory-avatar-client`
- **THEN** it MUST be private and independently releasable, identify openxFactory as contract and server-control owner, and contain no provider keys or server tool handlers

#### Scenario: Privileged provider code is proposed in the client
- **WHEN** code would create provider calls with a standard key, configure server prompts or tools, execute functions, or attach privileged sideband control
- **THEN** repository-boundary validation MUST reject the code and route it to the server trust boundary

### Requirement: Avatar-client release evidence
Release evidence obligations SHALL activate at the internal-live gate, not
at repository creation: from that gate, every `xfactory-avatar-client`
release SHALL identify source revision, Flutter and platform versions, the
pinned openxFactory contract commit and digests, canonical
fixture-conformance results, dependency lock, secret-scan result, test
evidence, and rollback target, and release automation SHALL fail when any
of these is missing, a dependency is unpinned, or a secret is detected.
Before the internal-live gate the client MAY consume contracts by
co-checkout path reference. SBOM, dependency-license review, and the formal
accessibility audit SHALL be required at the pilot gate rather than per
release.

#### Scenario: Client is released for internal live use
- **WHEN** a client version is proposed for the internal-live ring
- **THEN** its release evidence MUST contain the pinned contract, fixture-conformance, dependency-lock, secret-scan, test, and rollback references

#### Scenario: Client and server are incompatible
- **WHEN** the client contract pin or capability requirements do not match the deployed broker
- **THEN** preflight MUST block live media and governed commands and MUST offer only a compatible upgrade, text fallback, or handoff

### Requirement: Deferred aggregation and web-console integration
Adding `xfactory-avatar-client` to the top-level xFactory aggregation SHALL
require a separate reviewed change that records path, remote, visibility,
exact validated commit, checkout, compatibility, update, and rollback
behavior. The conventional web console SHALL require its own repository,
contract pin, authentication handoff, and ownership decision, and the
production deployment home for the avatar control runtime SHALL be decided
by the live-qualification successor change consistent with this
capability's routing of runtime operations to install repositories.

#### Scenario: Aggregation integration is proposed
- **WHEN** xFactory proposes pinning `xfactory-avatar-client`
- **THEN** a dedicated change MUST define and verify gitlink path, remote, commit, checkout, compatibility, update, and rollback behavior

#### Scenario: Web operations console begins
- **WHEN** a later slice implements dense administration or interactive workflow editing
- **THEN** it MUST define a separate web repository and binding boundary rather than extending the Flutter client
