## Context

Provider documentation establishes the intended Realtime call and sideband
surfaces, but the critical ordering and latency assumptions need direct
measurement. The experiment is intentionally narrower than live-provider
qualification: it proves whether the proposed handshake is feasible under a
lab profile and records where the provider differs.

The reviewed protocol and result schema live in `supporting-docs/`. The sibling
contract kernel owns neutral meaning; this change owns observations only.

## Goals / Non-Goals

**Goals:**

- Reproduce every mandatory F0 trial with deterministic identifiers.
- Measure sideband readiness, media authorization, first media, and hangup.
- Prove failure containment and retry behavior without tenant data.
- Produce machine-readable, redacted evidence and an explicit interface-impact
  report.
- Permit all sibling implementations to continue while the experiment runs.

**Non-Goals:**

- Qualifying any model or profile for internal-live or production use.
- Defining canonical AVC fields or changing sibling files.
- Implementing a reusable broker, client, Hermes integration, or deployment.
- Measuring production SLOs, broad network variance, cost, or accessibility.
- Testing GPT-Live before a supported API contract exists.

## Decisions

### 1. Use an isolated, disposable lab harness

The harness lives under `experiments/avatar-brokered-call/`. It uses one
externally supplied lab credential, generated audio, a dedicated provider
project, and no tenant identifiers or workflow payloads. A run creates bounded
calls, terminates every call in cleanup, and leaves no standing service.

The implementation pins its Python runtime and third-party dependencies. The
WebRTC and WebSocket protocol work uses maintained libraries rather than a
hand-rolled media stack. Secrets enter only through environment or approved
secret storage and never through command arguments or result files.

### 2. Keep the candidate profile immutable per evidence run

Each run records a profile digest covering model, voice, turn detection,
instructions, tools-disabled state, generated-audio fixture, timeout values,
library lock, and harness revision. The initial candidate is
`gpt-realtime-2.1` with the reviewed `server_vad` values. If the candidate is
unavailable or the API shape differs before a call can be tested, the result is
`INCONCLUSIVE`, not an inferred pass or fail.

### 3. Execute the complete trial matrix

| Trial | Controlled condition | Required observation |
| --- | --- | --- |
| baseline | Normal create and sideband attach | Answer remains held; sideband and control readiness precede media authorization |
| delayed sideband | Inject bounded attach delay | Success below configured deadline; timeout at or above hard ceiling |
| sideband failure | Fail attach or verification | No media authorization; answer not applied; call terminated |
| exact retry | Repeat identical request/offer identity | At most one provider call and equivalent result |
| changed retry | Reuse request ID with changed offer fingerprint | No prior answer returned and no second call under that request |
| revocation | Revoke after authorization | Immediate control event and provider termination within five seconds |
| cleanup | Interrupt or abort each phase | Every known call ID receives bounded termination and evidence records cleanup |

The harness may use an internal probe envelope corresponding to the provisional
AVC baseline, but it does not publish that envelope as a contract.

### 4. Measure with monotonic clocks and explicit boundaries

Every trial records monotonic offsets from provider-create acceptance for:
provider response, call-ID availability, sideband connection, sideband
verification, xFactory control readiness, media authorization, answer
application, first media, revocation request, hangup request, and confirmed
termination where observable. Wall-clock timestamps are coarse run metadata
only.

The readiness default is 3,000 milliseconds and the hard ceiling is 5,000
milliseconds. Revocation termination must be requested and confirmed, where
the provider exposes confirmation, within five seconds. Missing confirmation
cannot be treated as success.

### 5. Separate result classification from interface correction

`f0-results.json` validates against the registered schema and reports one of:

- `PASS`: every mandatory trial ran and every required assertion passed;
- `FAIL`: a mandatory trial produced a contrary, reproducible observation; or
- `INCONCLUSIVE`: a mandatory trial could not run or lacked sufficient evidence.

The companion `f0-interface-impact.yaml` is always emitted. It contains an
empty `variances` list on a clean pass. Each variance names affected `ACR-*`
IDs, observed provider behavior, evidence references, severity, proposed
contract correction, and whether sibling work can continue behind a closed
default. The contract-kernel owner disposes the variance.

### 6. Treat evidence as publishable by construction

The result writer uses an allowlist. It rejects credentials, SDP, raw headers,
raw provider payloads, audio, transcript content, arbitrary subject IDs, and
unbounded strings before writing. Evidence uses run/trial hashes and bounded
reason codes. A redaction failure makes the run `FAIL` and prevents commit.

### 7. Keep implementation parallel and integration ordered

No sibling is a start dependency. F0 can run while schemas, the deterministic
runtime, and UI assets are implemented. `FAIL` or `INCONCLUSIVE` blocks only
contract publication and downstream final pins. Accepted variances are applied
by the contract-kernel branch and then consumed by affected siblings.

## Risks / Trade-offs

- Provider availability can make a run inconclusive -> retain complete attempt
  metadata and rerun; never waive a mandatory trial.
- Network jitter can obscure thresholds -> record multiple trials and raw
  monotonic durations without storing protected payloads.
- Cleanup confirmation may be weak -> distinguish request accepted from
  termination observed and require the stronger assertion where available.
- The harness can drift into a prototype broker -> prohibit reusable runtime
  imports and keep all code under the experiment path.
- A provider variance can invalidate parallel work -> map it to specific
  acceptance IDs so only affected tests reopen.

## Migration Plan

1. Implement the isolated harness and redacting result writer.
2. Run offline self-tests for configuration, timing, cleanup, and redaction.
3. Execute the complete live trial matrix with a lab key and generated audio.
4. Validate and commit result, narrative, and interface-impact evidence.
5. Notify the contract-kernel owner; rerun only affected trials after an
   accepted interface correction.
6. Archive after strict validation and a terminal `PASS`, `FAIL`, or
   `INCONCLUSIVE` record. Only `PASS` satisfies the kernel publication gate.

## Open Questions

- Live profile promotion, production topology, and formal latency budgets stay
  in `qualify-avatar-live-voice`.
- GPT-Live remains disabled until OpenAI publishes an API contract and a new
  proposal defines its qualification profile.
