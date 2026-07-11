## Context

The AVC kernel describes a distributed protocol with several race-sensitive
invariants. The smallest useful proof is an in-process state machine driven by
deterministic ports. It should be executable in ordinary unit tests, readable
as reference code, and structurally incapable of being mistaken for a
production deployment.

The contract-kernel sibling owns neutral meaning. This change consumes the
`avatar-client-parallel-v1` interface baseline and stable `ACR-*` IDs while
both branches are active, then consumes the released schemas and fixtures by
exact commit and digest.

## Goals / Non-Goals

**Goals:**

- Prove core broker/control behavior deterministically and without live I/O.
- Make race, retry, lease, and recovery behavior explicit in small modules.
- Exercise fail-closed policy, consent, confirmation, and provider ports.
- Produce acceptance-ID-level conformance evidence.
- Keep path ownership disjoint so contract, F0, runtime, and UI work can proceed
  concurrently.

**Non-Goals:**

- Production deployment, networking, persistence, scaling, or operations.
- A live OpenAI adapter, provider key handling, WebRTC, or actual audio.
- Flutter code, UI assets, DomainxFactory overlays, or Hermes integration.
- Generated bindings or a second language implementation.
- Production performance, chaos, accessibility, or security qualification.

## Decisions

### 1. Use an explicit non-deployable package boundary

All implementation code lives under `xfactory/avatar_runtime/`. The package
root documents that it is reference-only and exports no application factory,
network listener, command-line service, deployment manifest, or persistent
repository. Importing a live network SDK from this package is forbidden by a
boundary test.

Tests live under `tests/avatar_runtime/`. No other repository path is changed
except this proposal's evidence. The package can be deleted without migrating
runtime state because it creates none.

### 2. Inject every nondeterministic or authoritative dependency

The core receives narrow ports for:

| Port | Deterministic implementation | Future production owner |
| --- | --- | --- |
| clock | manually advanced monotonic and wall clocks | runtime platform |
| IDs | queued stable identifiers | cryptographic ID source |
| provider | in-memory call/answer/sideband/hangup fake | qualified server adapter |
| policy | immutable fail-closed bundle | Hermes/policy service |
| consent | versioned fixture authority | domain consent authority |
| operation execution | idempotent fixture handler | governed workflow service |
| usage sink | in-memory append-only records | metering/telemetry system |

Tests advance clocks and complete port futures explicitly. The core never calls
ambient wall time, random UUID generation, sleep, filesystem persistence, or a
network API.

### 3. Permit a test-only provisional interface seam

Parallel implementation needs contract-shaped values before the kernel release
exists. A provisional adapter may live only under
`tests/avatar_runtime/provisional/`; it represents `avatar-client-parallel-v1`
and stable acceptance IDs. Production/reference package modules depend on
internal typed values, not copied JSON Schema files.

Final realization requires the canonical validator and fixtures from an exact
kernel commit. The final suite disables the provisional adapter, verifies that
no package import reaches it, and records the release tag, commit, file digests,
interface-lock digest, and acceptance-map digest. A test-only seam may remain
for historical fixture replay but cannot be the default or release evidence.

### 4. Separate media-attempt and logical-session state

The logical session owns epoch, active client instance, policy and consent
versions, event sequence, state revision, pending commands, and workflow
projection. A media attempt owns request ID, exact-offer fingerprint, attempt
status, provider call reference, held answer, scoped control descriptor,
readiness deadline, lease, and terminal result.

One logical session permits at most one pending or connected media leg. A fresh
authorized resume atomically terminates and abandons the prior pending attempt
before creating another. State transitions are declared in tables and reject
unknown predecessors or terminal-state mutation.

### 5. Model AVC-02 as one total result function

Broker preflight returns exactly one typed `grant`, `denial`, or `terminal`
result for every request. Only a grant can contain an answer or control
credential. Exact retries may receive the same unconsumed grant from an
in-process, TTL-bounded secret cache; changed requests fail with
`idempotency_conflict`; connected, expired, abandoned, and revoked attempts
return credential-free terminal outcomes.

Durable behavior is simulated only as a credential-free idempotency record in
memory. Destroying and reconstructing the runtime proves that secret grant
material is not required for terminal replay.

### 6. Make media authorization an explicit two-channel barrier

The fake provider has separate create, sideband-open, sideband-verified, and
hangup states. The broker holds the answer until sideband verification. The
control path separately validates `lease_ack` against transport-derived
identity and the active attempt. Only the conjunction emits authoritative
`media_authorized` for the same epoch and media leg.

Readiness timeout, heartbeat, lease expiry, consent invalidation, and kill
switches all terminate or revoke through the same idempotent provider port.
No fake provider event can directly execute a tool or author workflow state.

### 7. Use one event log and an atomic snapshot barrier

Accepted commands are deduplicated by command ID and return the recorded
result. Revision-guarded commands fail on stale state. Observations and
authoritative results append to one sequence with producer-authority checks.

Recovery fixes barrier `B`, projects AVC-12 through `B`, buffers events after
`B`, sends the snapshot with `last_event_sequence = B`, then drains buffered
events in order. Buffer overflow aborts and restarts recovery. Historical
replay is not exposed.

### 8. Keep authority adapters fail-closed

Policy and consent fixtures resolve identity references, required neutral
purposes, speech gates, retention, quotas, and confirmation rules. Missing or
unknown values deny preflight or reject commands. The memory-gateway consent
schema is never treated as media authority. The fixture operation handler uses
an external-operation idempotency key and records effects only after a valid,
unexpired confirmation decision.

### 9. Treat observability as structured, redacted evidence

The runtime emits bounded records containing stable test IDs, hashed or fixture
references, state transitions, timings from the injected clock, usage outcome,
and reason codes. A validator rejects SDP, credentials, raw transcript/media,
provider payloads, and arbitrary identifiers.

### 10. Keep parallel implementation separate from ordered realization

The branch can implement and pass provisional deterministic tests while F0 and
the kernel proceed. It cannot realize until the kernel has a published commit
and digests. An accepted kernel variance names affected acceptance IDs; only
those tests and adapters reopen.

## Risks / Trade-offs

- A fake provider can overstate real feasibility -> F0 and live qualification
  remain independent gates.
- A provisional adapter can drift -> final conformance disables it and runs
  canonical fixtures by exact digest.
- Reference code can be deployed accidentally -> no listener, entrypoint,
  network SDK, persistence, or deployment files; boundary tests enforce this.
- In-memory behavior may hide distributed races -> this change proves protocol
  determinism, not deployment correctness; chaos belongs to pilot hardening.
- One large test matrix can become opaque -> map every case to stable `ACR-*`
  and `ARR-*` IDs and keep module-level tests focused.

## Migration Plan

1. Scaffold ports, typed internal values, deterministic clocks/IDs, and the
   test-only provisional adapter.
2. Implement session, attempt, outcome, control, event, snapshot, authority,
   consent, usage, and kill-switch modules with focused tests.
3. Add the complete deterministic acceptance suite and redaction/boundary
   checks.
4. Consume accepted kernel variances by acceptance ID without editing sibling
   files.
5. Pin the released kernel, run canonical fixtures with the provisional adapter
   disabled, and record conformance evidence.
6. Run strict validation and archive after the non-deployable reference package
   is merged and green.

## Open Questions

- The production deployment home, network framework, provider SDK, distributed
  cache, and operational telemetry are decided by `qualify-avatar-live-voice`.
- Hermes ports replace fixtures in `avatar-pilot-hardening`; this proposal does
  not select a Hermes transport.
