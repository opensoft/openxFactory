# repo-boundary-governance (delta) — qualify-avatar-live-voice

## MODIFIED Requirements

### Requirement: Neutral avatar-client repository boundary
The reusable Flutter avatar implementation SHALL live in a private,
independently released repository named `xfactory-avatar-client`, created by
`qualify-avatar-live-voice` at the internal-live gate through extraction of the
codexFactory `apps/avatar-client-lab/` home that `implement-avatar-client-lab`
ratified. From creation it SHALL
own the Flutter application and packages, client bindings, pure reducers, UI
and platform adapters, the trusted local disclosure/media gate, constrained
control and media clients, and client tests. It SHALL pin the compatible
openxFactory bundle tag plus exact contract commit and digests and MUST NOT
contain a standard provider API key, server tool
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

#### Scenario: The lab home is extracted at the internal-live gate
- **WHEN** `qualify-avatar-live-voice` reaches the internal-live gate
- **THEN** the codexFactory `apps/avatar-client-lab/` application and its generated bindings MUST be extracted into `xfactory-avatar-client` under this boundary
- **AND** admitting that repository to the xFactory aggregation MUST remain a separate reviewed change
