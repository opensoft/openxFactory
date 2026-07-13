# Feature Specification: AVC Reference Runtime

**Feature Branch**: `003-avc-reference-runtime`

**Created**: 2026-07-11

**Status**: Draft

**Input**: OpenSpec change: `implement-avatar-reference-runtime` — a deterministic,
non-deployable reference implementation and conformance obligation set for the
neutral Avatar Client (AVC) protocol.

## User Scenarios & Testing *(mandatory)*

The consumers of this feature are not end users of a running service. They are
the people who must *trust the AVC protocol before it is ever deployed*:
the contract-kernel owner who defines neutral meaning, the runtime engineers
who implement in parallel with the kernel and F0 work, and the governance and
security reviewers who must be certain the reference code can never be mistaken
for — or turned into — a production deployment. Each story below is
independently demonstrable: any one of them alone yields reviewable value.

### User Story 1 - Deterministic proof of race-sensitive protocol behavior (Priority: P1)

The protocol owner needs evidence that the AVC kernel's race-sensitive
invariants actually hold — broker outcome determinism, retry idempotency,
two-channel media authorization, single-log event ordering, snapshot recovery,
control-lease loss, consent revocation, quota and duration limits, and
credential-free terminal replay — proven by tests that never touch wall-clock
time, randomness, the network, persistence, or Hermes.

**Why this priority**: This is the entire reason the feature exists. Schemas
alone cannot prove these behaviors; without deterministic proof, the protocol
is unverified. This story delivers the core value on its own.

**Independent Test**: Run the deterministic suite twice, including in a
randomized test order, with all clocks manually advanced and all authority
ports backed by in-memory fixtures. The suite exercises every invariant and
produces identical authoritative results on every run with no external
dependency.

**Acceptance Scenarios**:

1. **Given** a readiness, heartbeat, lease, cache, confirmation, or duration
   deadline, **When** the test advances the injected monotonic clock, **Then**
   the transition fires deterministically and repeats identically on rerun.
   (ARR-003-S01)
2. **Given** an in-progress attempt, **When** a test completes fake-provider and
   sideband operations in a different order, **Then** the runtime follows the
   declared state transitions rather than ambient scheduling. (ARR-003-S02)
3. **Given** an authenticated request and an exact-offer identity repeated before
   grant consumption or expiry, **When** preflight runs again, **Then** the same
   cached grant is returned and at most one fake provider call exists.
   (ARR-004-S01)
4. **Given** a reused request ID with a changed offer fingerprint, **When**
   preflight runs, **Then** it returns `idempotency_conflict`, discloses no prior
   answer, and creates no second call. (ARR-004-S02)
5. **Given** a session with a pending media leg, **When** a fresh authorized
   resume arrives for the same epoch, **Then** the runtime atomically terminates
   and abandons the pending leg before creating at most one replacement.
   (ARR-004-S03)
6. **Given** verified sideband and a valid, identity-matched lease
   acknowledgement for the active attempt, **When** both control channels are
   ready, **Then** exactly one authoritative `media_authorized` event is emitted
   for that epoch and leg. (ARR-005-S01)
7. **Given** an active attempt, **When** the injected clock passes lease expiry
   without renewal, **Then** governed commands and media authorization stop and
   provider termination is invoked idempotently. (ARR-005-S03)
8. **Given** a command ID delivered more than once, **When** the runtime
   processes it, **Then** it returns the first recorded result and does not
   repeat the effect. (ARR-006-S01)
9. **Given** an event appended after snapshot barrier `B` but before the snapshot
   through `B` is applied, **When** recovery runs, **Then** the snapshot is sent
   with `last_event_sequence = B` and the event is delivered exactly once in
   order. (ARR-006-S03)
10. **Given** the consent port reporting the bound version invalid, **When**
    revocation is processed, **Then** the lease is revoked and fake-provider
    termination completes within the injected five-second bound. (ARR-005-S05)
11. **Given** a request that exceeds the fixture tenant concurrency or duration
    cap, **When** preflight runs, **Then** the canonical quota or duration
    outcome is emitted with an attributed, credential-free usage record.
    (ARR-007-S05)

---

### User Story 2 - Parallel implementation with ordered final conformance (Priority: P2)

Runtime engineers must be able to build and test *before* the contract kernel is
released, using a provisional interface baseline confined to the test tree.
When the kernel is released, realization pins the exact released kernel,
disables the provisional seam, runs canonical fixtures, and proves that no
distributable path can reach the provisional interface — so parallel speed never
weakens the final conformance guarantee.

**Why this priority**: Enables the workstream to proceed concurrently with the
kernel and F0 branches. Valuable once P1 exists, because it governs how the
proven behavior graduates to canonical conformance.

**Independent Test**: With canonical schemas unpublished, run the suite through
the provisional adapter — deriving applicable `ACR-*` IDs from the digest-verified
shared baseline map and checking full coverage via the scenario-test map — and
confirm it never writes or claims a canonical contract. Then, with a released kernel,
record its coordinates in `realization-pin.yaml`, disable the provisional adapter, and
confirm the canonical run reproduces the same authoritative results and that no
reference module can import the provisional path.

**Acceptance Scenarios**:

1. **Given** canonical schemas are not yet published, **When** tests run,
   **Then** they may use the provisional adapter without writing or claiming a
   canonical contract. (ARR-002-S01)
2. **Given** a module in the reference package, **When** it imports the
   provisional test path, **Then** import-boundary validation fails.
   (ARR-002-S02)
3. **Given** release evidence recording a tag without the exact commit and
   required digests, **When** realization is validated, **Then** it fails.
   (ARR-002-S03)
4. **Given** the contract-kernel owner accepts a baseline variance and names the
   affected acceptance IDs, **When** the runtime consumes it, **Then** only the
   mapped tests and adapters reopen and no kernel or unrelated sibling file is
   edited. (ARR-002-S04, ARR-008-S04)
5. **Given** an applicable kernel `ACR-*` scenario, **When** it has no
   reference-runtime test and no explicit non-applicability disposition, **Then**
   conformance fails. (ARR-008-S01)
6. **Given** final canonical fixture execution, **When** it produces a different
   result from the provisional suite, **Then** realization fails and the mapped
   behavior is corrected. (ARR-008-S03)

---

### User Story 3 - Non-deployable, fail-closed, redacted safety boundary (Priority: P3)

A governance and security reviewer must be able to inspect the reference package
and be certain it cannot deploy, cannot hold a provider key, cannot persist
tenant data, fails closed when authority is missing, and emits only redacted
evidence.

**Why this priority**: The reference code lives in a shared, contract-first
repository whose constitution forbids anything that deploys, listens on a socket,
or holds provider keys. This story protects that boundary but depends on P1
producing runtime code to inspect.

**Independent Test**: Run boundary and redaction validation against the package
and its emitted records; confirm no deployment surface, no live provider SDK, no
credential loading, fail-closed authority outcomes, and zero protected content in
telemetry.

**Acceptance Scenarios**:

1. **Given** boundary validation scanning imports, exports, entrypoints, and
   repository files, **When** it runs, **Then** it finds no listener, deployable
   application, persistence adapter, live provider SDK, or deployment
   configuration. (ARR-001-S01)
2. **Given** reference-package code that attempts to load a provider key or make
   a network provider call, **When** boundary validation runs, **Then** it fails
   and routes that work to a separately approved live-runtime change.
   (ARR-001-S02)
3. **Given** an in-process runtime, **When** it is destroyed, **Then** no
   migration, durable-state cleanup, or recovery of secret grant material is
   required. (ARR-001-S03)
4. **Given** a profile that lacks a mapping for any required neutral avatar
   purpose, **When** preflight runs, **Then** media is denied before fake
   provider creation. (ARR-007-S01)
5. **Given** an all-session or selected-profile kill switch is active, **When**
   new matching requests arrive, **Then** they are denied and active leases are
   revoked only when the switch policy requests it. (ARR-007-S03)
6. **Given** an emitted record containing SDP, a credential, provider payload,
   raw transcript/media content, or an arbitrary identifier, **When** redaction
   validation runs, **Then** it fails and the record is not published.
   (ARR-007-S04)

---

### Edge Cases

- **Hostile / forged identity**: A control acknowledgement whose transport-derived
  identity does not match the active session, instance, and attempt must not
  contribute to media authorization.
- **Cross-client isolation**: A second client instance competing for a session
  under an active lease is denied without disturbing the active instance.
- **Retry ambiguity**: Exact-offer repeats collapse to one grant; any changed
  non-volatile field or offer fingerprint becomes an idempotency conflict.
- **Secret-cache destruction**: On connect, expiry, abandonment, or revocation,
  answer and scoped-credential material is removed, yet a credential-free
  terminal outcome may still be replayed.
- **Sideband ordering and failure**: Sideband that is late or absent at the
  readiness deadline withholds authorization and terminates the leg.
- **Stale control epoch**: A reconnect presenting an old epoch or rotated
  credential is rejected without changing current state.
- **Duplicate commands and stale revisions**: Repeated command IDs replay the
  recorded result; guarded commands with an older expected revision are rejected
  without appending a transition.
- **Snapshot race and buffer overflow**: Events arriving during snapshot
  projection are ordered after the barrier; overflow aborts and restarts recovery
  from a fresh snapshot with no partial or historical replay.
- **Authority claim from an observation**: A client or provider observation that
  claims approval, execution, consent, or workflow completion is rejected as an
  authoritative transition.
- **Confirmation supersession**: A decision referencing an expired or superseded
  confirmation cannot execute a fixture operation; a fresh confirmation is
  required.
- **Authority unavailable**: Policy, consent, or operation authority that is
  unavailable or returns an unknown value denies or rejects the operation using
  the closed contract outcome.
- **Runtime pulls a forbidden dependency**: If the runtime package imports any
  third-party, test-only, provider, or network dependency, boundary validation
  fails.

## Clarifications

### Session 2026-07-11

- Q: What framework/runner hosts the deterministic suite? → A: `pytest` with pinned
  test-only dependencies; parametrize the ARR/ACR matrix; prove order-independence
  with `pytest-randomly` across multiple recorded seeds; a failing seed MUST be
  reproducible from reported output. (Q1)
- Q: What minimum Python version does the reference package target? → A: Python 3.11+
  (matching the existing `xfactory/` floor); no 3.12-only syntax in the reference
  package. (Q2)
- Q: What third-party dependency policy applies to runtime vs tests? → A:
  `xfactory/avatar_runtime/` is standard-library-only; tests and repo validators MAY
  use pinned repo-approved dependencies (PyYAML, jsonschema, pytest, pytest-randomly);
  the boundary validator enforces that the runtime package imports no test, provider,
  or network dependency. (Q3)
- Q: How is the boundary + provisional-import prohibition evidenced? → A: deterministic
  static AST / import / export / file-surface boundary tests plus a standalone
  `scripts/validate-avatar-runtime.py` repo gate that detects provisional-test imports,
  network/provider SDKs, listeners, application factories, persistence, credential
  loading, deployment files, and forbidden entrypoints — without executing runtime
  code. (Q4)
- Q: Where is the applicable `ACR-*` set read during parallel work? → A: the conformance
  checker consumes the versioned shared baseline map
  `openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml`
  (`avatar-client-parallel-v1`), verifying its source commit and digest, and switches to
  the digest-pinned released `contracts/avatar-client/acceptance-map.yaml` at realization;
  non-applicability dispositions live in the mapping artifact (Q6); no second
  hand-maintained ACR enumeration is kept under the runtime tests. (Q5)
- Q: How is the scenario→test mapping made machine-checkable? → A: a checked-in
  `tests/avatar_runtime/conformance/scenario-test-map.yaml` maps each required ARR/ACR
  scenario ID to one or more collected pytest node IDs, or to an allowed
  non-applicability disposition with rationale; the checker compares it against the
  acceptance map(s) and the collected test set and fails on missing, duplicate, dangling,
  skipped-required, or unknown mappings. (Q6)
- Q: Where are the release pin and conformance results recorded? → A:
  `tests/avatar_runtime/conformance/realization-pin.yaml`, with explicit `schema_version`
  and `kind`, kept inside the runtime-owned test surface and validated as part of final
  conformance. (Q7)
- Q: How does the suite/boundary check join the shared gate and documentation index? → A:
  add `scripts/validate-avatar-runtime.py` to the README validator index and run it plus
  the deterministic pytest suite for every feature commit and before push; this validator
  script is the narrow governance exception to the runtime/test paths and edits no
  sibling-owned contract, F0, UI, domain, deployment, or release-metadata path. (Q8)

## Requirements *(mandatory)*

### Functional Requirements

**Boundary and parallel seam**

- **FR-001**: The reference implementation MUST reside only within its designated
  reference package path (`xfactory/avatar_runtime/`), with all tests under the
  designated test tree (`tests/avatar_runtime/`), and MUST expose no network listener,
  application factory, deployment manifest, persistent repository, provider-credential
  loading, or live provider SDK. The runtime package MUST import only the Python
  standard library; boundary validation MUST fail if it imports any third-party,
  test-only, provider, or network dependency. (ARR-001-S01)
- **FR-002**: Boundary validation MUST fail when reference-package code attempts
  to load a provider key or make a network provider call, and MUST route such work
  to a separately approved live-runtime change. (ARR-001-S02)
- **FR-003**: Destroying the in-process runtime MUST require no migration, durable
  state cleanup, or recovery of secret grant material. (ARR-001-S03, ARR-004-S04)
- **FR-004**: Any `avatar-client-parallel-v1` provisional adapter MUST be confined
  to the designated provisional location under the test tree
  (`tests/avatar_runtime/provisional/`); reference and distributable code MUST depend
  on internal typed values rather than copied canonical schemas, and import-boundary
  validation MUST fail if any reference module imports the provisional path.
  (ARR-002-S01, ARR-002-S02)
- **FR-004a**: Boundary and provisional-import validation MUST be performed by
  deterministic static AST / import / export / file-surface analysis that does not
  execute runtime code, and MUST be exposed as a standalone `scripts/validate-avatar-runtime.py`
  repo gate (alongside in-suite boundary tests) that detects provisional-test imports,
  network/provider SDKs, listeners, application factories, persistence, credential
  loading, deployment files, and forbidden entrypoints. (ARR-001-S01, ARR-002-S02)
- **FR-005**: Final realization MUST pin the released kernel tag, exact commit,
  per-file digests, interface-lock digest, and acceptance-map digest, and MUST
  fail if realization evidence records a tag without the exact commit and all
  required digests. These five coordinates and the final conformance results MUST be
  recorded in `tests/avatar_runtime/conformance/realization-pin.yaml`, carrying explicit
  `schema_version` and `kind`, and validated as part of final conformance. (ARR-002-S03)
- **FR-006**: When the contract-kernel owner accepts a baseline variance and names
  the affected acceptance IDs, the runtime MUST reopen only the mapped tests and
  adapters and MUST NOT edit the kernel or unrelated sibling files. (ARR-002-S04,
  ARR-008-S04)

**Injected determinism**

- **FR-007**: The runtime core MUST receive clock, ID, provider, policy, consent,
  operation, and usage behavior through explicit injected ports with deterministic
  in-memory implementations. (ARR-003)
- **FR-008**: Every time-dependent transition — readiness, heartbeat, lease, cache
  TTL, confirmation, and duration deadlines — MUST be driven by advancing an
  injected monotonic clock and MUST produce identical results on repeated runs.
  (ARR-003-S01, ARR-008-S02)
- **FR-009**: Reordering fake-provider and sideband operations MUST cause the
  runtime to follow declared state transitions rather than ambient scheduling.
  (ARR-003-S02)
- **FR-010**: When policy, consent, or operation authority is unavailable or
  returns an unknown value, the runtime MUST deny or reject the operation using the
  closed contract outcome (fail closed). (ARR-003-S03)

**Session results and media-attempt lifecycle**

- **FR-011**: The runtime MUST model logical sessions separately from media
  attempts and MUST permit at most one pending or connected media leg and at most
  one active client instance per logical session. (ARR-004)
- **FR-012**: Broker preflight MUST return exactly one typed `grant | denial |
  terminal` result for every request, and only a grant may carry an answer or a
  control credential. (ARR-004, applicable ACR-*)
- **FR-013**: An exact repeated request and offer identity presented before grant
  consumption or expiry MUST return the same cached grant and MUST create at most
  one fake provider call. (ARR-004-S01)
- **FR-014**: A reused request ID with a changed offer fingerprint or non-volatile
  field MUST return `idempotency_conflict`, disclose no prior answer, and create no
  second call. (ARR-004-S02)
- **FR-015**: A fresh authorized resume for the same logical session and epoch MUST
  atomically terminate and abandon the pending leg before creating at most one
  replacement. (ARR-004-S03)
- **FR-016**: On connect, expiry, abandonment, or revocation the runtime MUST
  remove all cached answer and scoped-credential material while a credential-free
  terminal outcome may remain for replay. (ARR-004-S04)
- **FR-017**: A second client instance requesting a session that holds an active
  lease MUST receive `second_instance_denied` without revoking the active instance.
  (ARR-004-S05)

**Two-channel media authorization and leased control**

- **FR-018**: The runtime MUST emit `media_authorized` exactly once and only after
  sideband verification and an authenticated lease acknowledgement match the same
  session, epoch, instance, attempt, and media leg. (ARR-005-S01)
- **FR-019**: A control acknowledgement whose transport-derived identity does not
  match the active session, instance, and attempt MUST be rejected and MUST NOT
  contribute to media authorization. (ARR-005-S01, hostile-identity)
- **FR-020**: When sideband is unavailable at the selected readiness deadline, the
  runtime MUST withhold authorization, terminate the fake provider leg, and return
  the closed timeout outcome. (ARR-005-S02)
- **FR-021**: When the injected clock passes lease expiry without renewal, governed
  commands and media authorization MUST stop and provider termination MUST be
  invoked idempotently. (ARR-005-S03)
- **FR-022**: A reconnect presenting a stale epoch or rotated credential MUST be
  rejected without changing current state. (ARR-005-S04)
- **FR-023**: When the consent port reports the bound version invalid, the runtime
  MUST push revocation, revoke the lease, and complete fake-provider termination
  within the injected five-second bound. (ARR-005-S05)

**Single-log command, event, and snapshot recovery**

- **FR-024**: Commands MUST be validated against lease, epoch, allowlist, and
  conditional expected revision; a guarded command carrying an older expected
  revision MUST be rejected without appending the requested transition.
  (ARR-006-S02)
- **FR-025**: A command ID delivered more than once MUST return the first recorded
  result and MUST NOT repeat its effect. (ARR-006-S01)
- **FR-026**: Observations and authoritative results MUST append to a single
  sequenced event log under producer-authority checks; an observation that claims
  approval, execution, consent, or workflow completion MUST be rejected as an
  authoritative transition. (ARR-006-S05)
- **FR-027**: Recovery MUST fix an atomic snapshot barrier `B`, send the snapshot
  with `last_event_sequence = B`, buffer post-barrier events, drain them exactly
  once in order, and abort and restart from a fresh snapshot on buffer overflow
  without exposing partial or historical replay. (ARR-006-S03, ARR-006-S04)

**Fail-closed authority, revocation, usage, and telemetry**

- **FR-028**: A profile lacking a mapping for any required neutral avatar purpose
  MUST cause preflight to deny media before fake provider creation. (ARR-007-S01)
- **FR-029**: A decision referencing an expired or superseded confirmation version
  MUST prevent any fixture operation and MUST require a fresh confirmation; fixture
  operation execution MUST be idempotent under an external-operation idempotency
  key. (ARR-007-S02)
- **FR-030**: The memory-gateway consent schema MUST NOT be treated as media
  authority. (design §8)
- **FR-031**: When an all-session or selected-profile kill switch is active, new
  matching requests MUST be denied and active leases MUST be revoked only when the
  switch policy requests it. (ARR-007-S03)
- **FR-032**: A request that exceeds the fixture tenant concurrency or duration cap
  MUST emit the canonical quota or duration outcome and an attributed,
  credential-free usage record. (ARR-007-S05)
- **FR-033**: Emitted telemetry MUST be structured and redacted; any record
  containing SDP, a credential, a provider payload, raw transcript or media
  content, or an arbitrary high-cardinality identifier MUST fail redaction
  validation and MUST NOT be published. (ARR-007-S04)

**Acceptance-ID-complete conformance evidence**

- **FR-034**: Every runtime-owned `ARR-*` scenario and every applicable kernel
  `ACR-*` scenario MUST map to deterministic automated evidence or an explicit
  recorded non-applicability disposition; conformance MUST fail on any missing
  mapping, skipped required case, nondeterministic result, or prohibited path
  modification. The mapping MUST be a checked-in
  `tests/avatar_runtime/conformance/scenario-test-map.yaml` that binds each required
  ARR/ACR scenario ID to one or more collected test node IDs, or to an allowed
  non-applicability disposition with rationale; the conformance checker MUST compare
  it against the acceptance map(s) and the collected test set and MUST fail on missing,
  duplicate, dangling, skipped-required, or unknown mappings. (ARR-008-S01, ARR-008-S02)
- **FR-034a**: The required `ARR-*`/`ACR-*` set MUST be content-addressed rather than a
  second hand-maintained enumeration. The runtime-owned ARR map lives in the runtime
  test tree (`tests/avatar_runtime/conformance/avatar-reference-runtime-acceptance-map.yaml`,
  relocated at realization from the change supporting-docs so it is not archived away),
  and the applicable `ACR-*` set is derived from the released kernel map
  `contracts/avatar-client/acceptance-map.yaml`. At realization the enumerated
  required-set and both source digests MUST be frozen into
  `tests/avatar_runtime/conformance/realization-pin.yaml`; the `--final` checker sources
  the required-set authoritatively from the pin and cross-verifies each live map (when
  present) against its pinned digest and enumerated set, failing closed on drift. Because
  the required-set is pinned, it stays content-addressed and checkable after the sibling
  change directories archive. (During parallel work the checker consumed the
  `avatar-client-parallel-v1` baseline map from the kernel change supporting-docs; that
  source is retired at realization.) (ARR-002-S01, ARR-008-S01)
- **FR-035**: Final evidence MUST run with the provisional adapter disabled against
  canonical fixtures from the released acceptance map; if canonical execution disagrees
  with provisional behavior, realization MUST fail and the mapped behavior MUST be
  corrected. (ARR-008-S03)
- **FR-036**: Realization validation MUST fail if the implementation diff modifies
  any canonical contract, F0, UI, DomainxFactory, or deployment path. The only paths
  this feature writes are the runtime package (`xfactory/avatar_runtime/`), the test
  tree (`tests/avatar_runtime/`), the standalone gate `scripts/validate-avatar-runtime.py`,
  and its single README validator-index entry — a narrow, declared governance exception
  that touches no sibling-owned path. (ARR-008-S04)

### Key Entities *(include if feature involves data)*

- **Logical session**: The durable protocol identity owning epoch, active client
  instance, policy and consent versions, event sequence, state revision, pending
  commands, and workflow projection. At most one active instance and one media leg.
- **Media attempt**: A single media leg owning its request ID, exact-offer
  fingerprint, attempt status, provider call reference, held answer, scoped control
  descriptor, readiness deadline, lease, and terminal result.
- **Broker preflight result**: Exactly one typed `grant`, `denial`, or `terminal`
  outcome per request; only a grant carries answer or control credential.
- **Grant retry cache**: A process-memory-only, TTL-bounded store returning an
  unconsumed grant for exact retries and holding no secret material after connect,
  expiry, abandonment, or revocation.
- **Control lease**: The fenced authorization to issue governed commands, bound to
  session/epoch/instance/attempt, with heartbeat and expiry bounds.
- **Media authorization event**: The single authoritative signal emitted only when
  both control channels agree for one epoch and leg.
- **Command**: A governed request validated against lease, epoch, allowlist, and
  expected revision, deduplicated by command ID.
- **Single event log**: One ordered sequence of observations and authoritative
  results with producer-authority checks and a snapshot barrier.
- **Snapshot barrier**: The recovery boundary `B` with `last_event_sequence = B`,
  bounded post-barrier buffering, ordered drain, and overflow restart.
- **Authority ports**: Injected policy, consent, operation, and usage authorities
  with immutable fail-closed fixtures.
- **Kill switch**: All-session and per-profile disablement controls affecting new
  requests and, per policy, active leases.
- **Telemetry record**: A bounded, redacted evidence record of stable test IDs,
  hashed or fixture references, transitions, injected-clock timings, usage outcome,
  and reason codes.
- **Provisional interface adapter**: A test-only representation of the
  `avatar-client-parallel-v1` baseline and stable acceptance IDs, unreachable from
  distributable code and disabled for final conformance.
- **Scenario-test map**: `tests/avatar_runtime/conformance/scenario-test-map.yaml` —
  the checked-in binding of each required ARR/ACR scenario ID to collected test node
  IDs or an allowed non-applicability disposition with rationale.
- **Boundary validator gate**: `scripts/validate-avatar-runtime.py` — the standalone,
  execution-free static analyzer of imports, exports, entrypoints, and file surfaces,
  indexed in the README validator list.
- **Kernel release pin**: The five coordinated realization coordinates — tag, exact
  commit, per-file digests, interface-lock digest, and acceptance-map digest — recorded
  with conformance results in `tests/avatar_runtime/conformance/realization-pin.yaml`
  (`schema_version` + `kind`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the 34 defined `ARR-*` scenarios have a mapped deterministic
  automated test.
- **SC-002**: Every applicable kernel `ACR-*` scenario — derived from the acceptance
  map (shared baseline map during parallel work, digest-pinned released map at
  realization) — has either a mapped deterministic test or a recorded
  non-applicability disposition in the scenario-test map; conformance reports 0
  unmapped applicable scenarios and 0 duplicate, dangling, skipped-required, or
  unknown mappings.
- **SC-003**: The full deterministic suite produces identical authoritative results
  across repeated runs and across randomized test order over multiple recorded seeds —
  0 nondeterministic results — and any failing seed is reproducible from reported
  output.
- **SC-004**: 0 tests depend on wall-clock time, randomness, network access,
  filesystem persistence, or Hermes availability.
- **SC-005**: The runtime package imports 0 third-party, test-only, provider, or
  network dependencies, and 0 import paths from reference or otherwise distributable
  code reach the provisional interface adapter or any live provider SDK.
- **SC-006**: Final realization records all 5 release-pin coordinates (tag, exact
  commit, per-file digests, interface-lock digest, acceptance-map digest) in the
  runtime-owned `realization-pin.yaml`; realization fails if any coordinate is missing.
- **SC-007**: 0 emitted telemetry records contain protected content (SDP,
  credentials, provider payloads, raw transcript or media, or arbitrary
  high-cardinality identifiers).
- **SC-008**: The implementation diff modifies 0 canonical contract, F0, UI,
  DomainxFactory, or deployment files; outside the runtime package and test tree it
  touches exactly 1 gate script (`scripts/validate-avatar-runtime.py`) plus its single
  README validator-index entry — the declared governance exception.
- **SC-009**: Destroying and reconstructing the runtime requires 0 items of secret
  grant material to replay a terminal outcome.
- **SC-010**: A reviewer can confirm the presence or absence of every required
  boundary (no listener, entrypoint, provider key, persistence, or live SDK) from the
  `scripts/validate-avatar-runtime.py` output alone, without reading the whole package.

## Assumptions

- **ACR applicability**: The authoritative set of applicable `ACR-*` scenarios is
  defined by an acceptance map, not by a hand-maintained enumeration. During parallel
  work the conformance checker consumes the versioned shared baseline map
  `openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml`
  (`avatar-client-parallel-v1`) with source-commit and digest verification; at
  realization it switches to the digest-pinned released
  `contracts/avatar-client/acceptance-map.yaml`. Any non-applicable `ACR-*` scenario
  carries an explicit recorded disposition in the scenario-test map rather than a
  silent omission.
- **Reference tooling** (clarified 2026-07-11): The reference package targets Python
  3.11+ (matching the existing `xfactory/` floor) and uses no 3.12-only syntax. The
  runtime package `xfactory/avatar_runtime/` is standard-library-only; the deterministic
  tests run under `pytest` with `pytest-randomly` (order-independence proven across
  multiple recorded seeds, any failing seed reproducible from reported output), and
  tests and repo validators may use pinned repo-approved dependencies (PyYAML,
  jsonschema, pytest, pytest-randomly). No additional runtime, service framework, or
  second-language implementation is introduced. Language-, tooling-, and path-level
  facts are governance boundaries pinned by the ratified source change and this
  clarification session, not requirement-body implementation leakage.
- **Deterministic sources**: The injected clock is a pair of manually advanced
  monotonic and wall clocks; the ID source is a queued deterministic sequence. The
  "five-second" revocation bound is measured on the injected clock, never in real
  elapsed time.
- **Fixture-configured limits**: Grant-cache TTL, recovery buffer bound, tenant
  concurrency and duration caps, and confirmation validity windows are deterministic
  fixture values chosen for the tests, not production tuning.
- **Historical-replay seam**: A test-only seam may remain for historical fixture
  replay, but it is never the default execution path and never counts as release
  evidence.
- **Task-list separation**: This specification expresses WHAT and WHY; the OpenSpec
  change and downstream Speckit tasks own HOW. The two task lists are not
  duplicated (constitution Principle II).

## Dependencies

- **Provisional baseline**: The `avatar-client-parallel-v1` interface baseline and its
  stable `ACR-*` acceptance IDs — read from the shared baseline map
  `openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml`
  with source-commit and digest verification — enable parallel implementation while the
  kernel and F0 branches are active.
- **Released kernel pin**: Final realization depends on an exact, content-addressed
  released kernel (tag + exact commit + per-file digests + interface-lock digest +
  acceptance-map digest), its canonical fixtures, and the released acceptance map
  `contracts/avatar-client/acceptance-map.yaml`.
- **Test and validation dependencies**: The deterministic suite and the
  `scripts/validate-avatar-runtime.py` gate may use pinned repo-approved dependencies
  (PyYAML, jsonschema, pytest, pytest-randomly); the runtime package itself takes none.
- **F0 variance handling**: An accepted F0 interface variance reopens only the
  mapped tests and adapters named by its acceptance IDs; unaffected test evidence
  remains valid.
- **Sibling ownership**: The contract-kernel sibling owns neutral meaning and
  canonical fixtures and is consumed read-only; this feature edits no canonical
  contract, F0, UI, DomainxFactory, or release-metadata file.

## Out of Scope

- Production deployment, a deployment entrypoint, networking, an HTTP or socket
  server, persistence or scaling, and operations.
- A live provider (e.g. network voice) adapter, provider-key handling, real-time
  media transport, or actual audio.
- UI or client widgets, DomainxFactory overlays, and Hermes integration or
  transport selection.
- Generated bindings or a second-language implementation.
- Production performance, chaos, accessibility, or security qualification.
- Any edit to canonical contracts, F0, or contract release metadata.
