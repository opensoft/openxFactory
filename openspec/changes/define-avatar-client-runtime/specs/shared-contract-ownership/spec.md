# shared-contract-ownership Specification

## ADDED Requirements

### Requirement: Avatar-client contract ownership and consumer pinning
openxFactory SHALL own the canonical avatar-client contract kernel — the
AVC schemas, shared definitions, event and command registries, fixtures,
compatibility rules, and the schema/fixture validator — under
`contracts/avatar-client/`, authored as YAML-serialized JSON Schema (draft
2020-12) and registered in `contracts/manifest.yaml` under the repository
contract changelog policy.

Consumer repositories SHALL own their language bindings and local adapters
and SHALL pin the exact compatible openxFactory commit and per-file
digests. Bindings MAY be hand-written or generated; either way the consumer
SHALL prove conformance by executing the canonical valid, invalid,
compatibility, and redaction fixtures of the pinned contract release in its
CI. Provider DTOs, generated bindings, copied schemas, and client models
MUST NOT become canonical neutral semantics.

#### Scenario: Avatar runtime contract is introduced
- **WHEN** a schema governs shared session requests, grants, events, confirmations, retention, personas, commands, or snapshots
- **THEN** its canonical schema, registry entries, and conformance fixtures MUST live under `openxFactory/contracts/avatar-client/`

#### Scenario: Client models drift from the pinned contract
- **WHEN** a consumer's models fail the canonical fixture suite of its pinned contract release
- **THEN** the consumer's release validation MUST fail

#### Scenario: Provider event is added
- **WHEN** a provider adds or changes an event or field
- **THEN** it MUST remain in the owning provider adapter unless a reviewed cross-provider semantic requirement justifies a neutral contract evolution

### Requirement: Avatar runtime reference ownership
openxFactory SHALL own the deterministic broker/control reference modules,
the fail-closed authority stub, the contract validator, and the server-side
provider adapter shape needed to prove the neutral contracts, all as
non-deployable reference code under `xfactory/avatar_runtime/`. Production
deployment, hosting, and operations SHALL be defined by the
live-qualification successor change consistent with repo-boundary
governance. The client repository SHALL own only distributable client
concerns.

DomainxFactories SHALL specialize through the avatar-first UI profile (the
domain overlay carrier) plus consent purposes in the extended consent
profile, each pinned to a compatible contract release. A domain overlay
MUST NOT copy or fork the broker protocol, authority rules, or canonical
event and command vocabulary.

#### Scenario: Server-side provider integration is implemented
- **WHEN** code creates provider calls, holds a provider key, attaches sideband control, or configures tools and prompts
- **THEN** that code MUST live in the openxFactory reference runtime or a separately approved server trust boundary and MUST NOT live in the distributable client

#### Scenario: Domain overlay adopts the runtime
- **WHEN** a DomainxFactory publishes persona, speech-gate, consent-purpose, retention, or handoff specialization
- **THEN** it MUST identify its immutable overlay version and compatible contract release without redefining neutral authority or transport semantics
