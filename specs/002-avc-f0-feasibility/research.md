# Phase 0 Research: Avatar Brokered-Call F0 Feasibility Harness

**Feature**: 002-avc-f0-feasibility | **Date**: 2026-07-11

The clarified spec and the registered protocol/schema already pin most parameters
(candidate profile, 70-trial/6-group matrix, timing bounds, credential contract, evidence
paths, control-stub decision, fixture policy). This document resolves the remaining
implementation unknowns. There are no open `NEEDS CLARIFICATION` items.

## R1. Language and runtime

- **Decision**: Python 3.12, pinned via `.python-version`; deps hash-locked in a committed
  lock file under `experiments/avatar-brokered-call/`; the lock digest + Python version feed
  the immutable candidate-profile digest (FR-002).
- **Rationale**: The design mandates a pinned runtime and maintained WebRTC/WebSocket
  libraries; Python has mature async WebRTC (`aiortc`) and WSS (`websockets`) stacks and is
  the language of the repo's runtime modules (`xfactory/avatar_runtime/`).
- **Alternatives considered**: Node/TypeScript (viable WebRTC via `wrtc`, but diverges from
  the repo runtime language); Go/`pion` (excellent WebRTC, but new toolchain for no benefit);
  a browser-driven harness via Playwright (heavier, non-deterministic timing, harder to keep
  tenant-data-free) — rejected.

## R2. WebRTC media peer and held-answer gate

- **Decision**: `aiortc` for the `RTCPeerConnection`, the outbound audio track (fed by the
  generated fixture), and the constrained data channel. The provider SDP **answer is
  withheld** (never passed to `setRemoteDescription`) until both sideband verification and
  the in-harness control/lease authorization complete; "answer applied" and "first media"
  are recorded as distinct markers after authorization.
- **Rationale**: `aiortc` is maintained, pure-Python, gives precise programmatic control over
  when the answer is applied — exactly the ordering F0 must prove (FR-007/FR-008). No
  hand-rolled media stack (design constraint).
- **Alternatives considered**: hand-rolled SRTP/ICE (explicitly prohibited); libwebrtc via
  bindings (heavy build, no ordering benefit) — rejected.

## R3. Sideband control channel

- **Decision**: `websockets` client for the provider sideband WSS; sideband `open` and
  `verified` are separate markers. A bounded injected delay (F0-B) and an
  attach/verify failure (F0-C, → `media_readiness_timeout`) are driven by the harness.
- **Rationale**: Lightweight, async, well-suited to a single outbound control socket.
- **Alternatives considered**: `aiohttp` WS (heavier dependency for one socket) — rejected.

## R4. Brokered call creation and provider-call registry

- **Decision**: Create calls via `httpx` POST to the brokered `/v1/realtime/calls` surface;
  every created call ID is entered into an in-memory registry the moment it is known, so
  cleanup can terminate it even on interruption (FR-005). The provider request ID is stored
  only as a SHA-256 hash in evidence (schema `provider_request_id_hash`).
- **Rationale**: Registering the call ID before any further step is what makes bounded
  cleanup and the "at most one provider call" (exact-retry) assertion measurable.
- **Alternatives considered**: the `openai` SDK (adds surface and its own retry/logging that
  could obscure the single-call assertion and leak payloads) — rejected in favor of explicit
  `httpx` calls the harness fully controls.

## R5. In-harness simulated control / lease stub (Q6)

- **Decision**: A local async state machine models `lease_ack` → `media_authorized` ordering.
  It has no Hermes or external control-plane dependency and imports no reusable runtime code.
  It exposes only: request-readiness, grant-authorization (only after sideband verified), and
  revoke. Authorization is authoritative and gates answer application.
- **Rationale**: F0 measures the *ordering contract*, not a live control plane; a stub keeps
  the experiment self-contained and within the non-goals (no reusable broker/Hermes).
- **Alternatives considered**: real control-plane integration (adds a live dependency +
  deployment surface, violating non-goals); a flagged dual-mode (doubles surface for no F0
  benefit) — rejected.

## R6. Monotonic instrumentation

- **Decision**: `time.monotonic_ns()` for all offsets, measured from `t_provider_create_accepted`
  (t=0). Persist the ~13 protocol markers (`t_offer_ready` … `t_peer_terminal`) as integer
  millisecond offsets; wall-clock (`started_at`/`completed_at`) is coarse run metadata only.
- **Rationale**: Monotonic nanosecond timing is immune to wall-clock adjustment and precise
  enough for the 2,000–5,000 ms bounds; the timing path does no blocking I/O.
- **Alternatives considered**: `time.time()` (wall-clock skew) — rejected.

## R7. Deterministic audio fixture (Q7)

- **Decision**: One deterministic synthetic **speech**-plus-silence clip generated per harness
  revision by a pinned offline neural TTS (e.g. a `piper`-class engine) with a pinned voice
  model, fixed text, and fixed synthesis parameters (no randomness/seed drift), followed by a
  fixed trailing silence long enough to exceed the `server_vad` 500 ms silence window and
  close the turn. Both the generator parameters and the generated-byte SHA-256 are pinned in
  run metadata; **no** binary audio is committed and **no** real-user recording is used.
- **Rationale**: `server_vad` triggers on speech-like energy, so a real (but synthetic) speech
  waveform is required to elicit a model response and observe `first_output_playable`; an
  offline engine keeps generation reproducible and tenant-data-free. Determinism is asserted
  by an offline test that regenerates and compares the byte digest.
- **Alternatives considered**: a committed WAV artifact (commits a binary + drift risk —
  rejected per Q7=A+); a pure sine/tone (may not reliably trip speech VAD); a cloud TTS
  (non-deterministic and a tenant-data/network dependency) — rejected.

## R8. Evidence validation and the two owned schemas

- **Decision**: Validate `f0-results.json` with `jsonschema` (Draft 2020-12) against the
  002-owned `experiments/avatar-brokered-call/schemas/f0-results.schema.yaml`. An offline
  drift test asserts that owned copy is byte-identical (sha256 `a52f2abe…`) to the registered
  supporting-docs copy. Author a new 002-owned `f0-interface-impact.schema.yaml` (carrying
  `schema_version` + `kind`) and validate `f0-interface-impact.yaml` against it.
- **Rationale**: The 001 clarify decision assigns ownership of both schemas to 002; keeping
  the authoritative copies in the owned surface with a digest drift-guard prevents divergence
  from the OpenSpec-registered snapshot while respecting the "don't edit supporting-docs"
  boundary.
- **Alternatives considered**: reading the schema straight from supporting-docs at runtime
  (works but leaves 002 without an owned, writable copy the decision requires); duplicating
  without a drift guard (silent divergence risk) — rejected.

## R9. Redaction allowlist and fail-closed scan

- **Decision**: Evidence is serialized only from typed result models whose fields are an
  explicit allowlist (durations, enums, hashes, bounded reason codes). Before writing, a
  scan rejects any prohibited class — credential material, SDP (`v=0`/`m=`/`a=` markers),
  raw provider payloads/headers, audio/transcript bytes, arbitrary/high-cardinality IDs, and
  unbounded strings (length-capped). A positive finding makes the run `FAIL` and blocks the
  write/commit (FR-017).
- **Rationale**: "Publishable by construction" (design decision 6) — allowlist-out beats
  denylist-scrub; the scan is a second, fail-closed safety net over logs/traces/crash output.
- **Alternatives considered**: post-hoc regex scrubbing of a free-form dict (denylist, easy to
  miss a class) — rejected.

## R10. Acceptance-map ingestion and ACR-ID sourcing (Q3)

- **Decision**: Read `openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml`,
  verify `interface_baseline == avatar-client-parallel-v1`, compute its SHA-256 and compare to
  a pinned expected digest in run config; record source path + commit + digest in evidence.
  F0 variances cite concrete IDs from the map — the F0-relevant requirements are **ACR-003**
  (brokered direct media with sideband control), **ACR-008** (consent / revocation bound),
  **ACR-011** (redacted telemetry & latency evidence), and **ACR-012** (deterministic-first
  release gating). Missing map, wrong baseline, or digest mismatch ⇒ run `INCONCLUSIVE`; F0
  never mints placeholder IDs. Disposition of variances stays with the contract-kernel owner.
- **Rationale**: Cited IDs must be real and traceable; a digest gate makes the citation
  reproducible and fails closed if the baseline moves.
- **Alternatives considered**: minting `ACR-TBD-*` placeholders (rejected per Q3); requiring a
  published register before running (couples 002 to kernel sequencing) — rejected.

## R11. Interrupted-run cleanup and revocation kill path

- **Decision**: A signal-handled, bounded cleanup routine iterates the call registry and
  requests termination for every known call ID, recording per-call cleanup outcome; it runs on
  normal end, on exception, and on interrupt. Revocation (F0-D) records `revocation_request`,
  `hangup_request`, and `terminal_observation` as separate offsets; missing terminal
  confirmation is `FAIL`/`INCONCLUSIVE`, never treated as success (FR-013/FR-014).
- **Rationale**: Separating request-accepted from termination-observed is a mandatory evidence
  distinction; bounded cleanup is the cross-cutting "interrupted-run/cleanup" behavior (Q4).
- **Alternatives considered**: best-effort cleanup without a registry (can orphan calls on
  interrupt) — rejected.

## R12. Trial-group realization (Q4)

- **Decision**: Exactly six group runners F0-A…F0-B…F0-F (baseline 20; delayed-sideband,
  sideband-failure, revocation, exact-retry, changed-retry 10 each; 70 total). Readiness-timeout
  is an assertion/path inside F0-C; interrupted-run and bounded cleanup are cross-cutting
  assertions exercised across all groups — none is a separate group. The `trial_groups`/`trials`
  arrays and the schema's exact-count `contains` constraints are honored by construction.
- **Rationale**: Keeps `f0-results.json` schema-valid and matches the protocol's F0-C
  description and always-on cleanup requirement.
- **Alternatives considered**: adding a 7th group (breaks the pinned schema) — rejected.
