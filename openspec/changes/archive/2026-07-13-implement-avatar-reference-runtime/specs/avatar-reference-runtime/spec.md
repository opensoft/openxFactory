# avatar-reference-runtime Specification

## ADDED Requirements

### Requirement: Non-deployable reference package boundary
openxFactory SHALL provide the AVC reference implementation only under
`xfactory/avatar_runtime/` with tests under `tests/avatar_runtime/`. The package
SHALL expose no network listener, application factory, deployment manifest,
persistent repository, provider credential loading, or live provider SDK. Its
purpose SHALL be deterministic contract proof, not production service.

#### Scenario: Reference package is inspected for deployment surfaces
- **WHEN** boundary validation scans package imports, exports, entrypoints, and repository files
- **THEN** it MUST find no listener, deployable application, persistence adapter, live provider SDK, or deployment configuration

#### Scenario: Live provider code is proposed
- **WHEN** reference-package code attempts to load a provider key or make a network provider call
- **THEN** boundary validation MUST fail and route that work to a separately approved live-runtime change

#### Scenario: Reference state is discarded
- **WHEN** the in-process runtime is destroyed
- **THEN** no migration, cleanup of durable state, or recovery of secret grant material may be required

### Requirement: Parallel interface seam and final contract pin
The avatar reference runtime SHALL confine any `avatar-client-parallel-v1`
adapter to `tests/avatar_runtime/provisional/` while the sibling kernel is active.
Package code SHALL depend on internal typed values rather than copied canonical
schemas. Final realization SHALL pin the released kernel tag, exact commit,
file digests, interface-lock digest, and acceptance-map digest, run canonical
fixtures with the provisional adapter disabled, and prove package code cannot
import the provisional path.

#### Scenario: Parallel implementation starts before kernel release
- **WHEN** the canonical schemas are not yet published
- **THEN** tests MAY use the provisional adapter without writing or claiming a canonical contract

#### Scenario: Provisional adapter is imported by package code
- **WHEN** any module under `xfactory/avatar_runtime/` imports the provisional test path
- **THEN** import-boundary validation MUST fail

#### Scenario: Final conformance uses only a tag
- **WHEN** release evidence records a tag without exact commit and required digests
- **THEN** runtime realization MUST fail

#### Scenario: Kernel variance is accepted
- **WHEN** the contract-kernel owner changes a baseline item and identifies affected acceptance IDs
- **THEN** the runtime MUST reopen mapped tests and MUST NOT edit the kernel or unrelated sibling files

### Requirement: Fully injected deterministic dependencies
The runtime core SHALL receive clock, ID, provider, policy, consent, operation,
and usage behavior through explicit ports with deterministic in-memory
implementations. Core tests MUST NOT depend on ambient wall time, random ID
generation, sleeping, filesystem persistence, network access, or Hermes
availability.

#### Scenario: Time-dependent transition is tested
- **WHEN** a readiness, heartbeat, lease, cache, confirmation, or duration deadline is exercised
- **THEN** the test MUST advance an injected monotonic clock and produce the same result on repeated runs

#### Scenario: Provider response is reordered
- **WHEN** a test completes fake provider and sideband operations in a different order
- **THEN** the runtime MUST follow declared state transitions rather than ambient scheduling

#### Scenario: Authority dependency is unavailable
- **WHEN** policy, consent, or operation authority returns unavailable or unknown
- **THEN** the runtime MUST deny or reject the operation using the closed contract outcome

### Requirement: Deterministic session results and media-attempt lifecycle
The runtime SHALL model logical sessions separately from media attempts and
SHALL implement the kernel's `grant | denial | terminal` result function,
exact-offer retry equivalence, changed-offer conflict, one instance and media
leg per session, fresh-resume replacement, process-memory-only grant retry
cache, credential-free terminal replay, terminal cache destruction, tenant
caps, and duration outcomes.

#### Scenario: Equivalent pending request is retried
- **WHEN** the same authenticated request and exact offer identity are repeated before grant consumption or expiry
- **THEN** the runtime MUST return the same cached grant and MUST create at most one fake provider call

#### Scenario: Request identity changes
- **WHEN** a request ID is reused with a changed offer fingerprint or non-volatile field
- **THEN** the runtime MUST return `idempotency_conflict`, disclose no prior answer, and create no second call

#### Scenario: Fresh authorized resume replaces a pending leg
- **WHEN** a fresh request and valid resume reference arrive for the same logical session and epoch
- **THEN** the runtime MUST atomically terminate and abandon the pending leg before creating at most one replacement

#### Scenario: Secret cache is destroyed
- **WHEN** an attempt connects, expires, is abandoned, or is revoked
- **THEN** all cached answer and scoped credential material MUST be removed while a credential-free terminal outcome may remain

#### Scenario: Another client instance competes
- **WHEN** a second instance requests a session with an active lease
- **THEN** the runtime MUST return `second_instance_denied` without revoking the active instance

### Requirement: Two-channel media authorization and leased control
The fake provider and control state SHALL keep provider create, held answer,
sideband verification, lease acknowledgement, media authorization, heartbeat,
lease expiry, reconnect credential, and termination as explicit transitions.
`media_authorized` SHALL be emitted only after sideband and authenticated
control acknowledgement match the same session, epoch, instance, attempt, and
media leg. Readiness, heartbeat, lease, revocation, and termination bounds SHALL
follow the kernel.

#### Scenario: Both control channels become ready
- **WHEN** sideband verification and a valid lease acknowledgement complete for the active attempt
- **THEN** the runtime MUST emit exactly one authoritative `media_authorized` event for that epoch and leg

#### Scenario: Sideband misses readiness
- **WHEN** sideband is unavailable at the selected readiness deadline
- **THEN** the runtime MUST withhold authorization, terminate the fake provider leg, and return the closed timeout outcome

#### Scenario: Lease expires while provider remains connected
- **WHEN** the injected clock passes lease expiry without renewal
- **THEN** governed commands and media authorization MUST stop and provider termination MUST be invoked idempotently

#### Scenario: Stale control epoch reconnects
- **WHEN** a reconnect presents an old epoch or rotated credential
- **THEN** the runtime MUST reject it without changing current state

#### Scenario: Consent is invalidated
- **WHEN** the consent port reports the bound version invalid
- **THEN** the runtime MUST push revocation, revoke the lease, and complete fake-provider termination within the five-second injected bound

### Requirement: Single-log command, event, and snapshot recovery
The runtime SHALL validate commands against lease, epoch, allowlist, and
conditional expected revision; deduplicate command IDs by returning recorded
results; enforce event-producer authority; and append accepted observations and
authoritative results to one sequence. Recovery SHALL use an atomic snapshot
barrier, bounded post-barrier buffering, ordered drain, overflow restart, and no
historical replay endpoint.

#### Scenario: Command is duplicated
- **WHEN** a command ID is delivered more than once
- **THEN** the runtime MUST return the first recorded result and MUST NOT repeat its effect

#### Scenario: Revision guard is stale
- **WHEN** a guarded command carries an older expected state revision
- **THEN** the runtime MUST reject it without appending the requested state transition

#### Scenario: Event arrives during snapshot projection
- **WHEN** an event is appended after barrier `B` but before the snapshot through `B` is applied
- **THEN** the runtime MUST send the snapshot with `last_event_sequence = B` and then deliver the event exactly once in order

#### Scenario: Recovery buffer overflows
- **WHEN** post-barrier events exceed the configured bound
- **THEN** recovery MUST abort and restart from a fresh snapshot without exposing partial replay

#### Scenario: Observation claims authority
- **WHEN** a client or provider observation claims approval, execution, consent, or workflow completion
- **THEN** producer-authority validation MUST reject the authoritative transition

### Requirement: Fail-closed authority, revocation, usage, and telemetry
The runtime SHALL provide immutable fail-closed policy and consent fixtures,
neutral consent-purpose mapping, implemented speech gates, effect-bound
confirmation, idempotent fixture operation execution, attributed usage records,
session and model-profile kill switches, and structured redacted telemetry. It
SHALL not infer media authority from memory consent or persist SDP, credentials,
raw provider payloads, transcript content, or media.

#### Scenario: Required purpose mapping is absent
- **WHEN** a profile lacks a mapping for any required neutral avatar purpose
- **THEN** preflight MUST deny media before fake provider creation

#### Scenario: Confirmation is stale or superseded
- **WHEN** a decision references an expired or superseded confirmation version
- **THEN** no fixture operation may execute and a fresh confirmation MUST be required

#### Scenario: Kill switch is active
- **WHEN** all-session or selected-profile creation is disabled
- **THEN** new matching requests MUST be denied and active leases MUST be revoked only when the switch policy requests it

#### Scenario: Telemetry contains protected content
- **WHEN** an emitted record contains SDP, a credential, provider payload, transcript/media content, or an arbitrary identifier
- **THEN** redaction validation MUST fail and the record MUST NOT be published

#### Scenario: Usage cap is reached
- **WHEN** a request exceeds the fixture tenant concurrency or duration cap
- **THEN** the runtime MUST emit the canonical quota or duration outcome and an attributed credential-free usage record

### Requirement: Acceptance-ID-complete deterministic evidence
The reference suite SHALL map every runtime-owned `ARR-*` scenario and every
applicable kernel `ACR-*` scenario to deterministic automated evidence. Final
evidence SHALL use canonical fixtures, run with the provisional adapter
disabled, and fail on a missing mapping, skipped required case, nondeterministic
result, or prohibited path modification.

#### Scenario: Required kernel scenario is unmapped
- **WHEN** an applicable `ACR-*` scenario has no reference-runtime test or explicit non-applicability disposition
- **THEN** conformance MUST fail

#### Scenario: Test changes with execution order
- **WHEN** the deterministic suite is repeated or randomized in test order
- **THEN** each case MUST produce the same authoritative results and evidence

#### Scenario: Canonical fixture disagrees with provisional behavior
- **WHEN** final canonical fixture execution produces a different result from the provisional suite
- **THEN** realization MUST fail and the mapped runtime behavior MUST be corrected

#### Scenario: Sibling-owned file changes
- **WHEN** the implementation diff modifies canonical contracts, F0, UI, DomainxFactory, or deployment paths
- **THEN** realization validation MUST fail
