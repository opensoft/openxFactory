## ADDED Requirements

### Requirement: Durable immutable preauthorization binding

The reference authority SHALL require an explicitly initialized private store
and independently approved static selection. Claim SHALL atomically bind one
preauthorization to one exact source/repository/case/run/attempt. Same-context
refresh MUST retain the binding; competing runs, changed attempts, reset by
duplicate authorization, revoked scope or missing/replaced state MUST refuse.

#### Scenario: Concurrent claims have one durable winner
- **WHEN** valid observations for different runs compete for one preauthorization
- **THEN** exactly one run binds and ordinary authority restart preserves that winner

#### Scenario: Revocation or lost expected state refuses
- **WHEN** a bound authorization is revoked or its initialized store is absent, corrupt or observably replaced
- **THEN** no new/readback authority is returned and startup never silently resets it

### Requirement: Independent authenticated control-plane evidence

The service SHALL authenticate actual peer roles and verify independently signed
fixture observations before trusting run identity. Readers/workers MUST NOT
authorize selections, supply verification roots or register untrusted context.
Observations SHALL bind exact source/selection/preauthorization/context and
bounded current time. Simulated evidence MUST remain fixture-scoped.

#### Scenario: Reader fields cannot forge actual run identity
- **WHEN** a reader supplies a different context or the worker tries a privileged action with valid fixture credentials
- **THEN** the service refuses while a selected controller/reader positive path remains available

#### Scenario: Invalid signed evidence refuses
- **WHEN** signature, context, profile, freshness or selected root differs
- **THEN** no run binding or operational readiness results and errors reveal no raw sensitive payload

### Requirement: Authenticated admission and owning proof integration

The reference client SHALL authenticate the configured authority and bind its
approved full config/grant into existing bootstrap/admission. It MUST preserve
exact runtime config/source/protection/grant/lease and earliest-deadline checks.
The isolated flow SHALL use the owning proof implementation and independent
cleanup, retaining replay records and shared resources.

#### Scenario: Complete isolated path yields one owning proof
- **WHEN** static approval, authenticated assigned-run evidence and all existing independent admission gates agree
- **THEN** the owning proof verifies, repeated proof use refuses and independent cleanup reports the actual scoped result

#### Scenario: Failure or cancellation preserves authority boundaries
- **WHEN** revocation, expiry, changed source, service outage or runner death occurs
- **THEN** no false success is emitted and independent generation-bound cleanup/readback preserves retained/shared state

### Requirement: Source and fixture evidence cannot authorize operation

The implementation SHALL remain explicitly reference/fixture-scoped, bounded
and opt-in. Default operational bindings MUST refuse. Candidate source/CI
success MUST NOT authorize provider setup, protected dispatch, live GitHub
authentication, protected-machine receipts or human/domain acceptance.

#### Scenario: Reference profile cannot self-promote
- **WHEN** a caller supplies production scope, approval flags, alternate trust material or a claimed passed test
- **THEN** reference validation refuses or preserves fixture scope and operational gates remain unauthorized
