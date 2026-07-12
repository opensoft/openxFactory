# Phase 1 Data Model: AVC Reference Runtime

**Feature**: 003-avc-reference-runtime | **Date**: 2026-07-11

All entities are **in-memory, immutable-by-default typed values** (frozen dataclasses) plus a
small number of mutable state-holder objects (`LogicalSession`, `MediaAttempt`, `EventLog`).
No entity is persisted; destroying the runtime discards them with no migration (FR-003, SC-009).
Field types are described technology-neutrally; concrete typing lives in `xfactory/avatar_runtime/values.py`.

## Closed registries (fail-closed enums — VII, FR-010)

Every registry below is **closed**: an unrecognized value is rejected, never coerced. Deferred
values fail closed.

- **SessionState**: `active`, `terminated`.
- **AttemptStatus**: `created`, `provider_call_created`, `answer_held`, `sideband_open`,
  `sideband_verified`, `authorized`, `connected`, `abandoned`, `expired`, `revoked`,
  `timed_out`, `terminated`.
- **PreflightKind**: `grant`, `denial`, `terminal`.
- **OutcomeCode** (terminal/denial reasons): `idempotency_conflict`, `second_instance_denied`,
  `readiness_timeout`, `lease_expired`, `consent_revoked`, `killed`, `quota_exceeded`,
  `duration_exceeded`, `purpose_unmapped`, `authority_unavailable`, `confirmation_stale`,
  `connected`, `abandoned`, `expired`, `revoked`.
  - *Design note (D1)*: `OutcomeCode` is kept as one unified registry for now, intentionally
    spanning both terminal-status echoes (`connected`/`abandoned`/`expired`/`revoked`) and
    denial/terminal reason codes. If the released kernel splits these into distinct registries, this
    model follows suit (a terminal-status vs reason-code split) and reopens only the mapped outcome
    tests (FR-006); until then the unified closed set stays fail-closed on unknown values.
- **PurposeId**: the closed set of required neutral avatar purposes (from the acceptance/policy
  fixture); a profile missing a mapping denies preflight (FR-028).
- **EventKind**: `observation`, `authoritative_result`.
- **ProducerAuthority**: `client`, `provider`, `runtime_authority` — only `runtime_authority`
  may append an `authoritative_result` (FR-026).
- **ReasonCode**: closed set of redaction-safe reason codes for telemetry.
- **DispositionKind** (conformance): `mapped`, `non_applicable`.

## Core state entities

### LogicalSession  (session.py — D4, FR-011)

| Field | Meaning |
|-------|---------|
| `session_id` | Stable logical identity. |
| `epoch` | Monotonic fencing token; bumped on authorized resume. |
| `active_instance_id` | The one client instance holding the session (≤1). |
| `policy_version`, `consent_version` | Bound authority versions. |
| `state_revision` | Guard value for conditional commands. |
| `event_sequence` | Reference to the single `EventLog`. |
| `pending_commands` | Command-id → recorded result (dedupe). |
| `pending_attempt` | ≤1 `MediaAttempt` in a pending/connected status. |
| `workflow_projection` | AVC-12 projection derived from the event log. |

- **Invariants**: at most one active instance and at most one pending/connected media leg
  (FR-011). A fresh authorized resume atomically terminates + abandons the prior pending attempt
  before creating ≤1 replacement (FR-015). A second instance under an active lease →
  `second_instance_denied`, active instance untouched (FR-017).

### MediaAttempt  (attempt.py — D4)

| Field | Meaning |
|-------|---------|
| `request_id` | Broker request identity. |
| `offer_fingerprint` | Exact-offer identity for idempotency. |
| `status` | `AttemptStatus`. |
| `provider_call_ref` | Reference into the fake provider (≤1 create per grant). |
| `held_answer` | Provider answer, withheld until sideband verification; cleared on terminal. |
| `control_descriptor` | Scoped control credential (grant-only). |
| `readiness_deadline` | Injected-clock deadline for sideband readiness. |
| `lease` | `ControlLease` (see below). |
| `terminal_result` | Credential-free terminal outcome (replayable). |

**State transitions** (reject unknown predecessor or terminal mutation — D4):

```text
created ─▶ provider_call_created ─▶ answer_held ─▶ sideband_open ─▶ sideband_verified
                                                                        │
                                          (identity-checked lease_ack)  ▼
                                                                    authorized ─▶ connected
any non-terminal ─▶ { abandoned | expired | revoked | timed_out | terminated }   (terminal)
```

Terminal states are immutable. `answer_held`/`control_descriptor` are erased on entering any
terminal state, but a credential-free `terminal_result` may remain (FR-016, SC-009).

### PreflightResult  (broker.py — D5, FR-012)

Tagged union produced by the AVC-02 total function; exactly one per request:

- **Grant**: `{ request_id, offer_fingerprint, answer, control_descriptor, expires_at }` — the
  **only** kind carrying answer/credential.
- **Denial**: `{ request_id, outcome: OutcomeCode }` — credential-free.
- **Terminal**: `{ request_id, outcome: OutcomeCode }` — credential-free; replayable.

Rules: exact repeated request+offer before consumption/expiry → same cached grant, ≤1 provider
call (FR-013); reused request_id + changed offer/non-volatile field → `idempotency_conflict`,
no prior answer disclosed, no 2nd call (FR-014).

**Idempotency: volatile vs non-volatile offer fields** (U1, FR-014). The `offer_fingerprint`
is computed over the **non-volatile** request fields; changing any of them under a reused
`request_id` is an `idempotency_conflict`. **Volatile** fields (excluded from the fingerprint,
may differ on an exact retry) vs **non-volatile** (included; a change conflicts) are pinned below,
derived from the `avatar-client-parallel-v1` baseline map's AVC-01 request semantics and
**revisited at kernel realization** if the released map differs:

| Field class | Members (provisional, from baseline AVC-01) | Effect on retry |
|-------------|---------------------------------------------|-----------------|
| Non-volatile (in fingerprint) | session/subject identity, epoch, requested purposes, offer SDP media description, model-profile selector, tenant ref | change → `idempotency_conflict` |
| Volatile (excluded) | client-local timestamps, transport keep-alive/nonce values, retry counter, non-semantic transport metadata | may differ; still returns the same cached grant |

The exact partition is a fixture constant in the provisional adapter; realization reconciles it
against the released kernel and reopens only the mapped idempotency tests on any variance (FR-006).

### GrantCacheEntry  (grant_cache.py — D5, FR-016)

`{ request_id, offer_fingerprint, grant, expires_at }` in a **process-memory-only, TTL-bounded**
store, plus a separate credential-free idempotency record for terminal replay. On connect /
expiry / abandonment / revocation the answer + scoped credential material is removed; the
credential-free record may remain (proves terminal replay needs no secret material).

### ControlLease  (control.py — D6, FR-018..FR-022)

| Field | Meaning |
|-------|---------|
| `lease_id`, `session_id`, `epoch`, `instance_id`, `attempt_id` | Binding scope. |
| `transport_identity` | Transport-derived identity checked against `lease_ack` (FR-019). |
| `heartbeat_deadline`, `expiry_deadline` | Injected-clock bounds. |
| `reconnect_credential` | Rotated on reconnect; stale epoch/credential rejected (FR-022). |

### MediaAuthorization event  (media_authz.py — D6, FR-018)

`{ session_id, epoch, instance_id, attempt_id, media_leg }`. Emitted **exactly once**, only when
sideband verification **and** an identity-matched `lease_ack` agree on all five. Sideband missing
at `readiness_deadline` → withhold, terminate provider leg, `readiness_timeout` (FR-020). Lease
expiry stops governed commands + authorization and invokes idempotent provider termination
(FR-021).

## Event, command & recovery entities

### Command  (commands.py — D7, FR-024/FR-025)

`{ command_id, session_id, epoch, verb, expected_revision?, payload }`. Validated against lease,
epoch, allowlist, and (if guarded) `expected_revision`. Duplicate `command_id` → first recorded
result, no repeated effect (FR-025). Stale `expected_revision` → rejected, no transition appended
(FR-024).

### EventRecord + EventLog  (events.py — D7, FR-026)

`EventRecord = { sequence, kind: EventKind, producer: ProducerAuthority, payload, clock_ts }`
appended to **one** ordered `EventLog`. Producer-authority check: an `observation` from
`client`/`provider` that claims approval/execution/consent/workflow completion is rejected as an
authoritative transition (FR-026).

### Snapshot + RecoveryBuffer  (snapshots.py — D7, FR-027)

`Snapshot = { last_event_sequence: B, projection_through_B }`. Recovery fixes barrier `B`,
projects AVC-12 through `B`, buffers post-`B` events, sends the snapshot with
`last_event_sequence = B`, then drains the buffer exactly once in order. Buffer overflow aborts
and restarts from a fresh snapshot; no historical-replay endpoint exists.

## Authority, usage & telemetry entities

### PolicyBundle  (authority.py — D8, FR-028)

Immutable fixture resolving: identity references, required `PurposeId` set, speech gates,
retention, quotas, and confirmation rules. Missing/unknown → deny preflight or reject command
(fail closed).

### ConsentBinding  (consent.py — D8, FR-023/FR-030)

`{ subject_ref, version, valid }` from a versioned fixture authority. Invalid version → push
revocation, revoke lease, complete fake-provider termination within the **injected 5-second
bound** (FR-023). The memory-gateway consent schema is **never** treated as media authority
(FR-030).

### ConfirmationDecision + OperationRecord  (operations.py — D8, FR-029)

`ConfirmationDecision = { confirmation_version, valid_until, superseded }`. A stale/superseded
decision blocks any fixture operation and requires a fresh confirmation. `OperationRecord` uses
an `external_operation_key` for idempotent execution; effects are recorded only after a valid,
unexpired confirmation.

### UsageRecord  (usage.py — D8, FR-032)

`{ tenant_ref, attempt_ref, outcome: OutcomeCode, clock_ts }` — in-memory append-only,
attributed, **credential-free**. A request over the fixture tenant concurrency/duration cap emits
`quota_exceeded`/`duration_exceeded` + a usage record.

### KillSwitchState  (killswitch.py — D8, FR-031)

`{ scope: all_session|profile, profile_id?, active }`. Active → deny new matching requests;
revoke active leases **only** when the switch policy requests it.

### TelemetryRecord + redaction validator  (telemetry.py — D9, FR-033)

`{ test_id, hashed_or_fixture_refs, transition, clock_timing, usage_outcome, reason: ReasonCode }`.
The redaction validator rejects any record containing SDP, a credential, a provider payload, raw
transcript/media, or an arbitrary high-cardinality identifier; rejected records are not published.

**Detectable redaction criteria** (U2, FR-033). "Arbitrary high-cardinality identifier" is made
checkable by an **allowlist of stable field kinds** plus **pattern classes** for the rejected set;
the validator fails a record if a field is neither on the allowlist nor a permitted hashed/fixture
reference:

- **Allowlist (permitted, stable/low-cardinality)**: `test_id`, `scenario_id`, `reason`
  (`ReasonCode`), closed-registry enum values (state/outcome/purpose), fixture references
  (`fixture:<name>`), and salted digests (`sha256:<hex>` of an otherwise-sensitive value).
- **Rejected pattern classes**: SDP blocks (`m=`/`a=`/`v=` lines, ICE candidates), credential
  shapes (bearer/JWT/`sk-…`/PEM/API-key regexes — mirror `xfactory/memory_gateway.py`'s
  `SECRET_RE`), raw provider payload blobs, transcript/media byte content, and free-form
  identifiers matching high-entropy/opaque patterns (raw UUIDs, tokens ≥ N chars) that are **not**
  a salted digest or a fixture reference.

Realization may tighten the allowlist/patterns to the released kernel's telemetry contract; the
redaction test (T054) asserts each rejected class is caught and not published (SC-007).

## Terminology (glossary)

- **`lease_ack`** (V1) ≡ the spec's "control acknowledgement" (spec §FR-019). The two name the same
  concept: the authenticated control-path acknowledgement whose transport-derived identity must match
  the active session/instance/attempt. **Artifacts, code, and tests use `lease_ack`**; "control
  acknowledgement" appears only as the spec's prose synonym.
- **media leg** ≡ a `MediaAttempt` (one pending/connected media path per logical session).
- **provisional adapter** ≡ "provisional interface adapter" ≡ "provisional seam" — the test-only
  `avatar-client-parallel-v1` representation under `tests/avatar_runtime/provisional/`.

## Injected ports (see [contracts/ports.md](./contracts/ports.md))

`ClockPort` (monotonic + wall, manually advanced), `IdPort` (queued deterministic ids),
`ProviderPort` (fake create/sideband-open/sideband-verified/hangup), `PolicyPort`, `ConsentPort`,
`OperationPort`, `UsagePort`. The core never calls ambient wall time, random id generation, sleep,
filesystem persistence, or a network API (FR-007, SC-004).

## Conformance & realization artifacts (see [contracts/conformance-artifacts.md](./contracts/conformance-artifacts.md))

- **ScenarioTestMap** (`scenario-test-map.yaml`): required scenario_id → `{ disposition: mapped,
  test_node_ids: [...] }` **or** `{ disposition: non_applicable, rationale }`.
- **RealizationPin** (`realization-pin.yaml`): the five release coordinates + final conformance
  results, with `schema_version` + `kind`.

## Requirement → entity coverage (traceability)

| Requirement group | Primary entities |
|-------------------|------------------|
| FR-001..FR-006, FR-004a, FR-036 (boundary/seam/realization) | package layout, ProvisionalAdapter (test-only), boundary scanner, RealizationPin |
| FR-007..FR-010 (injected determinism) | all seven ports, ManualClock, QueuedIdSource |
| FR-011..FR-017 (session/attempt/AVC-02) | LogicalSession, MediaAttempt, PreflightResult, GrantCacheEntry |
| FR-018..FR-023 (media auth + leased control) | ControlLease, MediaAuthorization, MediaAttempt |
| FR-024..FR-027 (command/event/snapshot) | Command, EventRecord/EventLog, Snapshot/RecoveryBuffer |
| FR-028..FR-033 (authority/usage/telemetry) | PolicyBundle, ConsentBinding, ConfirmationDecision, OperationRecord, UsageRecord, KillSwitchState, TelemetryRecord |
| FR-034/FR-034a/FR-035 (conformance evidence) | ScenarioTestMap, acceptance map (read-only), RealizationPin |
