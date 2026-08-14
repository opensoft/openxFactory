# credential-contracts (delta)

## ADDED Requirements

### Requirement: Worker credentials are distributed by reference into ephemeral job scope

A credential consumed by a worker lane (a model-provider token or comparable worker-consumed secret) SHALL be distributed by reference: the secret is held in a vault as a LONG-LIVED, NON-ROTATING headless token, the lane fetches it per job using the runner's own federated workload identity, and the fetched value lives only in ephemeral job scope (environment plus a per-job configuration directory) — never written to host state, never persisted past the job. Rotation SHALL be a vault write (effective the next job, no host administration), the vault's access log SHALL serve as the per-fetch audit record, and a refreshable session-state credential (one its consumer rewrites in place) SHALL NOT be distributed by any channel: it is the wrong class, because an ephemeral copy's refresh silently stales the master. Where a per-install fetch identity does not yet exist, service-scoped materialization of the same non-rotating class into the same ephemeral job scope is a permitted degraded mode whose rotation cost (host administration) SHALL be recorded as a gap.

#### Scenario: Rotation is one vault write

- **WHEN** the operator writes a new token version to the vault secret
- **THEN** the next job's fetch consumes the new version with no host access, no service restart, and no lane change

#### Scenario: The session-file class is refused distribution

- **WHEN** a refreshable session-state credential is proposed for vault distribution or per-job copying
- **THEN** it is non-conforming — the conforming distribution is a non-rotating headless token, and the session file remains at most host-profile state

#### Scenario: Host state stays clean

- **WHEN** a worker job that fetched its credential completes or crashes
- **THEN** no credential material persists outside the discarded job scope, and a stale host-profile credential cannot affect the lane

#### Scenario: The degraded mode is permitted and recorded

- **WHEN** an install has no per-job fetch identity and materializes the token at service scope instead
- **THEN** the lane conforms (same secret class, same ephemeral job consumption) and the install records rotation-requires-host-administration as an open gap

### Requirement: The credential vault operator is an execution binding, never contract content

Who operates the worker-credential vault SHALL be a per-install execution binding following the client-infrastructure operating models — the operations factory where one is licensed, the client's own authorized IT channel where not — and the consuming lane SHALL be identical in both cases, receiving only bindings: an opaque secret reference and a fetch-identity identifier. Contract artifacts, lane definitions, and domain repositories SHALL NOT hard-code a vault operator, a vault product, or any secret value, and the bootstrap material for this pattern SHALL be reachable by a client licensing a single domain factory without the operations factory.

#### Scenario: An operations-factory-operated install

- **WHEN** the install's execution binding is operations-factory-executed
- **THEN** that factory operates the vault, mints and rotates the token, and grants the fetch identity read on exactly the lane's secret — and the lane consumes bindings only

#### Scenario: A client-operated install

- **WHEN** the client licenses the domain factory without an operations factory
- **THEN** the client's authorized IT channel operates a vault of its choice under the same contract, no licensor identity performs the privileged acts, and the identical lane consumes the client's bindings
