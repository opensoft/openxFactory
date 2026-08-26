# shared-contract-ownership Specification

## Purpose
Defines how `openxFactory` owns shared factory contracts, how install repos pin
contract compatibility, how submodules are sequenced, and how evidence is
preserved from proposal through merge readiness.
## Requirements
### Requirement: Canonical contract home
`openxFactory` SHALL define the canonical home for shared factory contracts that
govern behavior between factory subsystems or across DomainxFactories. Migrated
contracts SHALL preserve source provenance and consumer compatibility
expectations. Domain-specific artifact schemas and workflow gate contracts MAY
live in the owning DomainxFactory when they preserve upstream `openxFactory`
references.

#### Scenario: Shared schema is introduced
- **WHEN** a schema or contract governs behavior between two or more factory subsystems or DomainxFactories
- **THEN** the canonical contract MUST be defined or referenced from `openxFactory/contracts/`

#### Scenario: Domain artifact schema is introduced
- **WHEN** a schema defines a domain-specific artifact such as a software PR admission packet, clinical review package, operations runbook result, ledger close packet, or campaign workflow artifact
- **THEN** the canonical implementation schema MUST live in the owning DomainxFactory
- **AND** the artifact MUST retain required upstream `openxFactory` scope, gate, and traceability references

#### Scenario: Subsystem adapter needs a contract
- **WHEN** an install repo needs a runtime adapter, generated client, smoke fixture, or pinned schema copy
- **THEN** the install repo MAY keep an implementation copy but MUST identify the corresponding `openxFactory` contract version or owning DomainxFactory contract version

#### Scenario: Existing schema is migrated
- **WHEN** a shared schema is copied from an install repo into `openxFactory/contracts/`
- **THEN** the canonical copy MUST identify the source path, intended consumers, compatibility reference, and adapter ownership rule

### Requirement: Contract version pinning
Install repositories SHALL pin compatible contract versions or commits from
`openxFactory` before runtime adapters are treated as compatible.

#### Scenario: Install repo consumes a contract
- **WHEN** `Hermes-Install` or `Omnigent-Install` consumes a shared contract
- **THEN** it MUST document which `openxFactory` contract version or commit it is compatible with

#### Scenario: Contract changes incompatibly
- **WHEN** a shared contract change would break an install repo adapter or smoke test
- **THEN** the change MUST be split from adapter migration or explicitly approved as a breaking change

### Requirement: Submodule sequencing
`openxFactory` SHALL document submodule intent and update procedures before
adding install repositories as submodules.

#### Scenario: Submodule is proposed
- **WHEN** a change proposes adding `Hermes-Install` or `Omnigent-Install` as a submodule
- **THEN** a decision record MUST document the remote, path, pinned commit, update process, and rollback process

#### Scenario: Hermes-Install remote is unresolved
- **WHEN** `Hermes-Install` still points to a non-Opensoft remote and the target umbrella repo is `opensoft/openxFactory`
- **THEN** the Hermes submodule MUST NOT be added until the move, fork, mirror, or external remote decision is approved

### Requirement: Evidence preservation
Each repo-boundary feature SHALL preserve traceability evidence from proposal
through merge readiness. Content migration features SHALL also preserve source
inventory and post-merge install repo link/update evidence where applicable.

#### Scenario: Feature proceeds to PR admission
- **WHEN** a repo-boundary feature is ready for PR
- **THEN** the feature MUST have a proposal or change record, acceptance criteria, implementation diff, local check result, branch review result, and PR admission packet

#### Scenario: Feature proceeds to merge
- **WHEN** a repo-boundary feature is considered for merge
- **THEN** merge council MUST have a merge readiness report that references the relevant OpenSpec change, feature slice, and evidence artifacts

#### Scenario: Content migration feature proceeds to merge
- **WHEN** a dogfood content migration feature is considered for merge
- **THEN** merge readiness MUST include source provenance, copy-first compliance, and evidence that source repos were not destructively changed in the same PR

### Requirement: Avatar-client contract ownership and consumer pinning
openxFactory SHALL own the canonical avatar-client contract kernel — the AVC
schemas, shared definitions, session-outcome, event, command, and
consent-purpose registries, fixtures, compatibility rules, and the
schema/fixture validator — under
`contracts/avatar-client/`, authored as YAML-serialized JSON Schema (draft
2020-12) and registered in `contracts/manifest.yaml` under the repository
contract changelog policy.

Each published bundle SHALL have one matching manifest version, changelog
entry, annotated tag, exact release commit, and per-file digests. Consumer
repositories SHALL own their language bindings and local adapters and SHALL
record the compatible bundle tag while pinning the exact openxFactory commit
and per-file digests. Bindings MAY be hand-written or generated; either way the consumer
SHALL prove conformance by executing the canonical valid, invalid,
compatibility, and redaction fixtures of the pinned contract release in its
CI. Provider DTOs, generated bindings, copied schemas, and client models
MUST NOT become canonical neutral semantics.

#### Scenario: Avatar runtime contract is introduced
- **WHEN** a schema governs shared session requests, results, events, confirmations, retention, personas, commands, or snapshots
- **THEN** its canonical schema, registry entries, and conformance fixtures MUST live under `openxFactory/contracts/avatar-client/`

#### Scenario: Contract bundle release identifiers disagree
- **WHEN** the manifest version, changelog release, annotated tag, release commit, or registered file digests do not identify the same realized bundle
- **THEN** release validation MUST fail and consumers MUST NOT be instructed to upgrade

#### Scenario: Consumer records only a contract tag
- **WHEN** a consumer records a bundle tag without the exact compatible commit and required file digests
- **THEN** consumer conformance MUST fail because the tag alone is not a content-addressed pin

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
domain overlay carrier), a mapping from neutral avatar purpose IDs to the
owning consent authority, and optional stricter domain purpose IDs, each
pinned to a compatible contract release. The memory-gateway consent profile
MAY be adapted by a domain but SHALL NOT become the neutral media-consent
contract. A domain overlay MUST NOT copy or fork the broker protocol,
authority rules, or canonical event and command vocabulary.

#### Scenario: Server-side provider integration is implemented
- **WHEN** code creates provider calls, holds a provider key, attaches sideband control, or configures tools and prompts
- **THEN** that code MUST live in the openxFactory reference runtime or a separately approved server trust boundary and MUST NOT live in the distributable client

#### Scenario: Domain overlay adopts the runtime
- **WHEN** a DomainxFactory publishes persona, speech-gate, consent-purpose, retention, or handoff specialization
- **THEN** it MUST identify its immutable overlay version, consent-authority mapping, and compatible contract release without redefining neutral authority or transport semantics

### Requirement: Tooling hosted in the publisher verifies released bytes, not a declared pin
Neutral tooling hosted inside `openxFactory` SHALL verify the shared contract it consumes by the released BYTES it reads — digest equality against its pinned value, and parity against the consumed checkout's own `contracts/manifest.yaml` — and SHALL NOT require the hosting repository to declare a consumption pin, because the publisher declares no pin on itself. A declared-pin check exists so that a consumer can never read one release while its repository declares another; that gap is real for a domain repo reading a submodule pin and structurally absent for tooling shipping inside the release it reads, and a question the publisher cannot honestly be asked MUST NOT be able to refuse it.

A checkout SHALL be treated as a publisher release only when it carries all of `contracts/manifest.yaml`, `contracts/schemas/`, and the contract family's own validator. Requiring every marker together is what separates a coherent release from a directory that merely contains a file with the right name — the same distinction manifest parity draws for a single schema, applied to the checkout as a whole. A tree missing any marker is NOT a publisher and SHALL take the consumer path with its declared pin intact.

Dropping the declared-pin question MUST NOT weaken any other link. The byte chain SHALL run unchanged and per request, and SHALL refuse on the request that first sees a drifted digest or a manifest disagreeing with its own bytes. Verification remains fail-closed throughout: an unreachable checkout, an absent schema, a digest mismatch, and a manifest disagreement each mean nothing may be treated as contract-conformant, and none of them may resolve to an implicit pass.

Nothing here changes how a consuming repository pins. A domain or install repo SHALL continue to declare the openxFactory release it consumes in its own `stack.yaml`, and tooling reading a contract from a checkout other than its own host SHALL continue to require that declaration.

#### Scenario: Tooling runs from a publisher checkout
- **WHEN** relocated neutral tooling loads a shared contract from the openxFactory checkout it is hosted in
- **THEN** the released bytes MUST be verified by digest and manifest parity
- **AND** the absence of a `stack.yaml` in that checkout MUST NOT refuse the load

#### Scenario: A consuming repository reads the same contract
- **WHEN** a domain or install repo consumes a shared contract from a pinned openxFactory checkout
- **THEN** its own declared `stack.yaml` consumption pin MUST still be required and MUST still be checked against the pinned release

#### Scenario: A release byte has drifted
- **WHEN** a consumed schema's bytes no longer hash to the pinned digest, or the checkout's manifest records a different digest than its own bytes
- **THEN** the load MUST refuse on the request that sees it
- **AND** publisher mode MUST NOT exempt it

#### Scenario: A tree only looks like a release
- **WHEN** the hosting repository carries some but not all of the publisher markers
- **THEN** it MUST NOT be treated as a publisher release
- **AND** the declared-pin requirement MUST apply to it unchanged

#### Scenario: A refusal reason cannot be established
- **WHEN** the consumed checkout cannot be resolved at all
- **THEN** verification MUST fail closed rather than treat the unanswered question as a pass

