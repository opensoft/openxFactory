# Implementation Plan: AVC Reference Runtime

**Branch**: `003-avc-reference-runtime` | **Date**: 2026-07-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/003-avc-reference-runtime/spec.md`;
OpenSpec change `implement-avatar-reference-runtime` (`design.md`, `tasks.md`,
`specs/avatar-reference-runtime/spec.md`, `supporting-docs/avatar-reference-runtime-acceptance-map.yaml`);
project constitution v1.0.0.

## Summary

Build a deterministic, non-deployable Python reference implementation of the neutral
Avatar Client (AVC) protocol under `xfactory/avatar_runtime/`, exercised entirely by
`tests/avatar_runtime/`. The runtime is an in-process state machine driven by seven
injected ports (clock, ID, provider, policy, consent, operation, usage) so that broker
preflight, media-attempt lifecycle, AVC-02 outcomes, two-channel media authorization,
leased control, a single sequenced event log, snapshot recovery, fail-closed authority,
consent revocation, usage/quota, kill switches, and redacted telemetry can all be proven
without wall-clock time, randomness, network, persistence, or Hermes. A test-only
provisional adapter (confined to `tests/avatar_runtime/provisional/`) lets implementation
proceed against the `avatar-client-parallel-v1` baseline before the kernel releases; final
realization pins the exact released kernel and runs canonical fixtures with the provisional
seam disabled. Conformance is enforced by a checked-in scenario→test map and a standalone
static boundary gate.

**Technical approach** (all pinned in the spec's Clarifications, Session 2026-07-11):

- Runtime core is **standard-library-only**; tests and the validator gate may use pinned
  test-only dependencies (`pytest`, `pytest-randomly`, `PyYAML`, `jsonschema`).
- Determinism is proven with `pytest` + `pytest-randomly` over **multiple recorded seeds**;
  any failing seed is reproducible from reported output.
- The package boundary and provisional-import prohibition are enforced by **execution-free
  static AST/import/export/file-surface analysis**, exposed both as in-suite boundary tests
  and as a standalone `scripts/validate-avatar-runtime.py` repo gate indexed in the README.
- The applicable `ACR-*` set is **derived from an acceptance map** — the digest-verified
  shared baseline map during parallel work, the digest-pinned released map at realization —
  never a second hand-maintained enumeration.
- Conformance completeness lives in `tests/avatar_runtime/conformance/scenario-test-map.yaml`;
  the five release coordinates + final results live in
  `tests/avatar_runtime/conformance/realization-pin.yaml` (`schema_version` + `kind`).

## Technical Context

**Language/Version**: Python 3.11+ (matches the existing `xfactory/` floor; no 3.12-only
syntax in the reference package).

**Primary Dependencies**:
- *Runtime core (`xfactory/avatar_runtime/`)*: Python standard library only — no third-party,
  test, provider, or network imports.
- *Tests & validator (`tests/avatar_runtime/`, `scripts/validate-avatar-runtime.py`)*: pinned
  repo-approved dev deps — `pytest`, `pytest-randomly`, `PyYAML`, `jsonschema`.

**Storage**: N/A — in-memory only. The runtime creates no durable state; destroying it requires
no migration, cleanup, or secret-grant recovery (FR-003, SC-009).

**Testing**: `pytest` with `pytest-randomly` (order-independence over multiple recorded seeds,
reproducible failing seed); a standalone execution-free static gate
`scripts/validate-avatar-runtime.py`; a conformance checker validating the scenario→test map
against the acceptance map(s) and the collected test set.

**Target Platform**: Local developer + CI (POSIX/Linux, Python 3.11+). **Non-deployable** —
there is no runtime deployment target, listener, or entrypoint by design (FR-001).

**Project Type**: Single-project internal reference library + deterministic test suite.

**Performance Goals**: N/A in throughput terms. The only performance-shaped requirement is that
the suite is fast, hermetic, and time-independent (all deadlines exercised via the injected
clock, not real elapsed time).

**Constraints**: No wall-clock time, randomness, network, filesystem persistence, or Hermes
dependency in any test (SC-004); runtime core stdlib-only (SC-005); boundary provable from
static gate output alone (SC-010); ownership limited to `xfactory/avatar_runtime/`,
`tests/avatar_runtime/`, and the narrow governance exception `scripts/validate-avatar-runtime.py`
plus its single README validator-index line (FR-036, SC-008).

**Scale/Scope**: 8 runtime-owned `ARR-*` requirements / 34 `ARR-*` scenarios plus the applicable
kernel `ACR-*` set; ~15 stdlib-only runtime modules; a fakes/fixtures layer; a provisional
adapter; a boundary+conformance tooling layer; ~15 focused test modules.

**Unknowns**: None. All prior `NEEDS CLARIFICATION` were resolved in the clarify phase
(Q1–Q8, Session 2026-07-11); see [research.md](./research.md).

## Constitution Check

*GATE: evaluated before Phase 0 and re-confirmed after Phase 1 design. Result: **PASS** — no
violations, Complexity Tracking empty.*

| Principle | Assessment | Verdict |
|-----------|------------|---------|
| I. Contract-First, Domain-Neutral Core | Reference implementation of the **neutral** AVC protocol; no domain vocabulary/policy; consumes neutral contracts read-only via ports and the acceptance map. Adds no domain-specific behavior. | PASS |
| II. Governed Change Flow (OpenSpec before impl) | This is the single Speckit feature handed off from OpenSpec change `implement-avatar-reference-runtime` (`code_surface: openxFactory`, `target_release: implemented`). OpenSpec owns governance; this plan owns implementation; task lists are not duplicated. | PASS |
| III. Document Lifecycle & Status | No new governance document is introduced. Speckit artifacts (plan/research/data-model/quickstart/contracts) are feature working docs. YAML artifacts carry `schema_version` + `kind`. | PASS (N/A surface) |
| IV. Schema & Artifact Discipline | New YAML artifacts `scenario-test-map.yaml` and `realization-pin.yaml` carry `schema_version` + `kind`; the validator is linked into the README validator index; no raw credentials; committed docs use repo-relative paths only. | PASS |
| V. Validation Gates (NON-NEGOTIABLE) | Feature ships `scripts/validate-avatar-runtime.py` + the deterministic pytest suite as its Principle V gate, run every feature commit and before push; OpenSpec artifacts already pass strict validation; behavior proven by deterministic tests, not assertion. | PASS |
| VI. Versioned, Content-Addressed Releases | Feature allocates no contract version; it **consumes** them. Realization pins the released kernel by tag + exact commit + per-file digests + interface-lock digest + acceptance-map digest, recorded in `realization-pin.yaml`; a bare tag fails realization (FR-005). | PASS |
| VII. Fail-Closed Authority Boundaries | Closed registries (reason/outcome/purpose/state enums reject unknowns); fail-closed policy/consent/operation authority; observations are non-authoritative (producer-authority checks); telemetry redacted (no credentials/payloads/tenant data/high-cardinality ids). | PASS |
| Repo Constraint — governed reference runtime only | Runtime is the exception the constitution allows: a governed reference implementation ratified by an OpenSpec change that **nothing deploys, listens on a socket, or holds provider keys for**; boundary tests + gate enforce this. | PASS |
| Repo Constraint — shared-tree / worktree discipline | All work in the feature worktree; explicit-path staging; commit only `specs/003-avc-reference-runtime/` this phase. | PASS |
| Workflow — lifecycle order & clarifications | specify → clarify (encoded) → plan (this). Material ambiguities resolved and encoded before planning. `/speckit.analyze` (no critical findings) precedes implement. | PASS |

**Post-Design re-check**: The Phase 1 design (module map, data model, port contracts,
conformance artifacts) introduces no new third-party runtime dependency, no deployment surface,
and no sibling-path write. Constitution Check remains **PASS**.

## Project Structure

### Documentation (this feature)

```text
specs/003-avc-reference-runtime/
├── plan.md              # This file (/speckit-plan output)
├── research.md          # Phase 0 — decisions & rationale (clarifications consolidated)
├── data-model.md        # Phase 1 — entities, state machines, closed registries
├── quickstart.md        # Phase 1 — how to run the suite, gate, and conformance check
├── contracts/
│   ├── ports.md         # Phase 1 — the seven injected port contracts
│   └── conformance-artifacts.md  # Phase 1 — schemas for scenario-test-map.yaml & realization-pin.yaml
├── spec.md              # Clarified feature spec (specify + clarify phases)
├── clarify-questions.md # Clarify Q&A record
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 — created by /speckit-tasks (NOT this command)
```

### Source Code (repository root)

```text
xfactory/avatar_runtime/          # stdlib-only, non-deployable reference package
├── __init__.py                   # reference-only doc; exports typed values + runtime factory; NO app factory/listener
├── ports.py                      # Protocol: ClockPort, IdPort, ProviderPort, PolicyPort, ConsentPort, OperationPort, UsagePort
├── values.py                     # frozen typed values + closed registries (reason/outcome/purpose/state enums)
├── clocks.py                     # ManualClock (monotonic + wall), advance()
├── ids.py                        # QueuedIdSource (deterministic id sequence)
├── session.py                    # LogicalSession state machine (epoch, instance, one-leg, fresh-resume replacement)
├── attempt.py                    # MediaAttempt state machine + transition tables
├── broker.py                     # AVC-02 total preflight: grant|denial|terminal, idempotency, caps, second-instance
├── grant_cache.py                # process-memory-only, TTL-bounded grant retry cache + credential-free terminal record
├── control.py                    # control lease: epoch fencing, lease_ack identity, heartbeat, expiry, reconnect rotation
├── media_authz.py                # two-channel barrier → single media_authorized; readiness timeout; idempotent termination
├── events.py                     # single sequenced event log; producer-authority checks
├── commands.py                   # command validation (lease/epoch/allowlist/expected-revision), dedupe by command id
├── snapshots.py                  # atomic snapshot barrier B, post-barrier buffer, ordered drain, overflow restart
├── authority.py                  # fail-closed policy resolution: purposes, speech gates, retention, quotas, confirmation rules
├── consent.py                    # versioned consent binding; invalidation → revocation within injected 5s bound
├── operations.py                 # fixture operation handler; external-operation idempotency key; confirmation validity
├── usage.py                      # in-memory append-only usage records; quota/duration outcomes
├── killswitch.py                 # all-session + per-profile kill switches
├── telemetry.py                  # structured redacted records + redaction validator
└── runtime.py                    # in-process assembly wiring ports + modules; destroy() creates no durable state

tests/avatar_runtime/
├── conftest.py                   # fixtures: manual clock, id source, fake provider, authority fixtures; seed recording
├── fakes/                        # in-memory FakeProvider (create/sideband-open/sideband-verified/hangup) + fail-closed fixtures
├── provisional/                  # avatar-client-parallel-v1 adapter (TEST-ONLY; unreachable from package); reads shared baseline map
├── boundary/
│   ├── scanner.py                # pure stdlib AST/import/export/file-surface scanner (shared by test + gate)
│   └── test_package_boundary.py  # asserts no deployment surface, stdlib-only runtime, no provisional import
├── conformance/
│   ├── scenario-test-map.yaml    # required scenario_id → test node id(s) | non-applicability disposition
│   ├── realization-pin.yaml      # five release coordinates + final conformance results (schema_version + kind)
│   └── check_conformance.py      # fails on missing/duplicate/dangling/skipped-required/unknown mappings
├── test_broker_preflight.py      # ARR-004 grant|denial|terminal, second-instance
├── test_media_attempts.py        # ARR-004 lifecycle, fresh-resume replacement, one-leg
├── test_avc02_outcomes.py        # ARR-004 idempotency, changed-offer conflict, caps/duration
├── test_grant_retry.py           # ARR-004 exact-retry cache, credential-free terminal replay, cache destruction
├── test_control_leases.py        # ARR-005 lease/epoch/heartbeat/expiry/reconnect rotation
├── test_media_authorization.py   # ARR-005 two-channel barrier, sideband timeout, hostile identity
├── test_commands.py              # ARR-006 validation, dedupe, revision guard
├── test_event_log.py             # ARR-006 single sequence, producer-authority checks
├── test_snapshots.py             # ARR-006 barrier B, post-barrier drain, overflow restart
├── test_authority_ports.py       # ARR-003/007 fail-closed policy/consent/operation, purpose mapping
├── test_consent_revocation.py    # ARR-005/007 invalidation → revoke within injected 5s
├── test_usage.py                 # ARR-007 quota/duration outcomes, attributed credential-free records
├── test_kill_switches.py         # ARR-007 all-session/per-profile deny + lease revoke
├── test_redaction_telemetry.py   # ARR-007 redaction validator rejects SDP/creds/payloads/media/ids
└── test_determinism.py           # ARR-003/008 clock-driven transitions, order-independence over seeds

scripts/
└── validate-avatar-runtime.py    # standalone execution-free gate (imports boundary/scanner.py); README validator-index entry
```

**Structure Decision**: Single-project internal library. Runtime modules under
`xfactory/avatar_runtime/` are stdlib-only and grouped by protocol concern (session/attempt/
broker, control/media authorization, event-log/commands/snapshots, authority/consent/operations/
usage/killswitch, telemetry), assembled by `runtime.py`. Everything nondeterministic or
authoritative enters through `ports.py`. All tests, fakes, the provisional adapter, and the
conformance/boundary tooling live under `tests/avatar_runtime/`. The lone out-of-tree artifact
is `scripts/validate-avatar-runtime.py` (+ one README index line) — the spec-declared narrow
governance exception; it shares the pure `boundary/scanner.py` so the gate and the in-suite
boundary test enforce identical rules.

## Complexity Tracking

> No Constitution Check violations — this table is intentionally empty.

The single out-of-feature-tree write (`scripts/validate-avatar-runtime.py` + one README
validator-index line) is **not** a violation: constitution Principle IV requires new validators
to be linked into the README index and Principle V requires repo-local validators to gate pushes.
It is declared and bounded by FR-036 / SC-008 and touches no sibling-owned contract, F0, UI,
domain, deployment, or release-metadata path.

## Phase Outputs

- **Phase 0** → [research.md](./research.md): decisions, rationale, alternatives (all
  `NEEDS CLARIFICATION` resolved).
- **Phase 1** → [data-model.md](./data-model.md), [contracts/ports.md](./contracts/ports.md),
  [contracts/conformance-artifacts.md](./contracts/conformance-artifacts.md),
  [quickstart.md](./quickstart.md).
- **Phase 2** (tasks.md) is produced by `/speckit-tasks`, not this command.
