# avatar-client-lab (delta) — qualify-avatar-live-voice

## MODIFIED Requirements

### Requirement: Repository and ownership boundary
The Flutter avatar client application and its generated Dart bindings SHALL live
in codexFactory under `apps/avatar-client-lab/` until the internal-live gate,
where `qualify-avatar-live-voice` extracts them into the private
`xfactory-avatar-client` repository governed by `repo-boundary-governance`,
while openxFactory retains
ownership of the neutral contracts, conformance fixtures, and acceptance
requirements.

#### Scenario: A neutral contract or fixture is edited from the codexFactory app
- **WHEN** the codexFactory `apps/avatar-client-lab/` app proposes a change to a neutral contract, registry, or shared conformance fixture
- **THEN** boundary validation MUST reject it and require the change in openxFactory instead

#### Scenario: A new neutral scenario is authored for the lab
- **WHEN** the lab needs a neutral session scenario usable by the runtime and web console
- **THEN** it MUST be contributed to openxFactory's shared fixtures, not forked into the codexFactory app

#### Scenario: The client is extracted at the internal-live gate
- **WHEN** `qualify-avatar-live-voice` performs the internal-live extraction
- **THEN** the application and its generated bindings MUST move to `xfactory-avatar-client` rather than being forked, and openxFactory's ownership of contracts, conformance fixtures, and acceptance requirements MUST be unchanged
