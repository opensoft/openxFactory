# Contract: Injected Ports

**Feature**: 003-avc-reference-runtime | **Date**: 2026-07-11

The reference runtime exposes exactly **one** external interface surface: the seven injected
ports its core depends on (design D2, FR-007). These are the "contracts" of this internal
library — every nondeterministic or authoritative dependency is a narrow port with a deterministic
in-memory implementation supplied by tests. The core **must not** call ambient wall time, random
id generation, sleep, filesystem persistence, or a network API (SC-004).

Ports are defined as `typing.Protocol` classes in `xfactory/avatar_runtime/ports.py` (structural,
stdlib-only). Signatures below are contract sketches — argument/return **shapes** are normative;
exact Python types live in code.

## ClockPort  (clocks.py fixture: `ManualClock`)

| Method | Contract |
|--------|----------|
| `monotonic() -> int` | Returns the current injected monotonic tick. Never reads the OS clock. |
| `wall() -> Timestamp` | Returns the injected wall time (for record timing only, never for control decisions). |
| `advance(ticks) -> None` | **Test-only** driver: moves the monotonic clock forward, firing any due deadline deterministically. |

*Invariant*: every readiness/heartbeat/lease/cache-TTL/confirmation/duration deadline is evaluated
against `monotonic()`; identical `advance()` sequences yield identical results (FR-008, SC-003).

## IdPort  (ids.py fixture: `QueuedIdSource`)

| Method | Contract |
|--------|----------|
| `next(kind) -> Id` | Returns the next queued deterministic id for `kind` (request/session/attempt/lease/...). No randomness/UUID. |

## ProviderPort  (fakes/: `FakeProvider`)

Models a media provider as an explicit four-state machine — no network, no audio (design D6).

| Method | Contract |
|--------|----------|
| `create(offer) -> CallRef` | Creates ≤1 call per grant; returns a held answer reference. |
| `open_sideband(call_ref) -> None` | Transitions to `sideband_open`. |
| `verify_sideband(call_ref) -> None` | Transitions to `sideband_verified` (a precondition of authorization). |
| `hangup(call_ref) -> None` | **Idempotent** termination; safe to call repeatedly on timeout/expiry/revoke/kill. |

*Invariant*: no provider event may directly execute a tool or author workflow state (D6); only the
conjunction of sideband verification + identity-checked `lease_ack` yields `media_authorized`.

## PolicyPort  (authority.py fixture: immutable `PolicyBundle`)

| Method | Contract |
|--------|----------|
| `resolve(identity_ref) -> PolicyBundle \| Unavailable` | Fail-closed: `Unavailable`/unknown → deny preflight or reject command (FR-010, FR-028). |

Resolves required neutral `PurposeId` set, speech gates, retention, quotas, and confirmation rules.

## ConsentPort  (consent.py fixture: versioned authority)

| Method | Contract |
|--------|----------|
| `binding(subject_ref) -> ConsentBinding \| Unavailable` | Returns version + validity; unavailable → fail closed. |
| `is_valid(binding) -> bool` | Invalid → push revocation, revoke lease, terminate provider within the injected 5-second bound (FR-023). |

*Invariant*: the memory-gateway consent schema is **never** media authority (FR-030).

## OperationPort  (operations.py fixture: idempotent handler)

| Method | Contract |
|--------|----------|
| `execute(external_operation_key, confirmation_decision, effect) -> OperationRecord \| Rejected` | Executes idempotently under `external_operation_key`; records effects **only** after a valid, unexpired confirmation; stale/superseded confirmation → `Rejected`, fresh confirmation required (FR-029). |

## UsagePort  (usage.py fixture: in-memory sink)

| Method | Contract |
|--------|----------|
| `record(usage) -> None` | Appends an attributed, **credential-free** usage record. |
| `check_caps(tenant_ref) -> Ok \| QuotaExceeded \| DurationExceeded` | Over-cap → canonical `quota_exceeded`/`duration_exceeded` outcome + usage record (FR-032). |

## Boundary contract (negative interface — FR-001, FR-004a)

The package **must not** expose or import: a network listener, an application/ASGI/WSGI factory,
a deployment manifest, a persistence adapter, provider-credential loading, a live provider SDK,
or the test-only provisional path. This negative contract is enforced statically by
`tests/avatar_runtime/boundary/scanner.py` (shared by the in-suite boundary test and
`scripts/validate-avatar-runtime.py`), which inspects imports, exports, entrypoints, and file
surfaces without executing runtime code (SC-005, SC-010).
