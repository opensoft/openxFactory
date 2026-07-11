# avatar-brokered-call-feasibility Specification

## ADDED Requirements

### Requirement: Isolated and reproducible F0 environment
The F0 harness SHALL execute only against a dedicated lab provider project with
an externally supplied credential, generated audio, tools disabled, no tenant
data, and an immutable candidate profile identified by harness revision,
dependency-lock digest, model, voice, turn settings, timeout settings, and
fixture digest. The harness SHALL terminate every known call during cleanup and
SHALL NOT create a standing service or reusable production broker.

#### Scenario: A run is configured safely
- **WHEN** the harness starts with a valid lab credential and fully pinned candidate profile
- **THEN** it MUST record only redacted configuration digests and execute the selected bounded trials

#### Scenario: Tenant or consequential data is supplied
- **WHEN** a configuration contains tenant identifiers, tenant content, enabled tools, or a non-lab profile
- **THEN** preflight MUST reject the run before any provider call is created

#### Scenario: Candidate API cannot be exercised
- **WHEN** the candidate is unavailable or its API shape prevents a mandatory trial from starting
- **THEN** the run MUST report `INCONCLUSIVE` and MUST NOT infer provider behavior

### Requirement: Complete brokered-call trial matrix
F0 SHALL execute baseline, delayed-sideband, sideband-failure,
readiness-timeout, exact-retry, changed-retry, revocation, interrupted-run, and
cleanup trials. It SHALL hold the provider answer until sideband verification
and xFactory control readiness, and it SHALL distinguish provider call
creation, sideband readiness, media authorization, answer application, and
first media as separate observations.

#### Scenario: Baseline handshake succeeds
- **WHEN** provider create, sideband attach, and xFactory control acknowledgement complete within the configured deadline
- **THEN** media authorization MUST occur after both control channels are verified and before answer application or first media

#### Scenario: Sideband is delayed within the deadline
- **WHEN** sideband verification completes after an injected delay but before the configured deadline
- **THEN** the answer MUST remain held and the trial MAY pass after ordered media authorization

#### Scenario: Sideband fails
- **WHEN** sideband attachment or verification fails
- **THEN** the harness MUST NOT authorize media or apply the answer and MUST terminate the provider call

#### Scenario: Exact request is retried
- **WHEN** the same request and exact offer identity are retried after a simulated lost response
- **THEN** evidence MUST show at most one provider call and an equivalent unconsumed result

#### Scenario: Retry changes the offer
- **WHEN** the request ID is reused with a different offer fingerprint or another non-volatile field
- **THEN** the prior answer MUST NOT be disclosed and no second provider call may be created under that request ID

#### Scenario: A run is interrupted
- **WHEN** the harness stops during any trial phase
- **THEN** bounded cleanup MUST attempt termination for every known call ID and record the cleanup outcome

### Requirement: Readiness and revocation timing evidence
F0 SHALL measure durations with a monotonic clock. Media readiness SHALL use a
3,000-millisecond default and MUST NOT exceed the 5,000-millisecond neutral
ceiling. A revocation trial SHALL request provider termination immediately and
SHALL require observed termination within five seconds when the provider
exposes an observable terminal signal. Request acceptance and observed
termination SHALL remain separate evidence fields.

#### Scenario: Readiness completes within the selected deadline
- **WHEN** sideband and xFactory control become ready within the selected 1,000-to-5,000-millisecond value
- **THEN** the measured trial MAY pass its readiness assertion

#### Scenario: Readiness exceeds the deadline
- **WHEN** either required control channel misses the selected deadline
- **THEN** the trial MUST withhold media authorization, terminate the call, and fail if any media or answer application occurred

#### Scenario: Revocation meets the bound
- **WHEN** the harness revokes an authorized trial and observes provider termination within five seconds
- **THEN** it MUST record separate revocation-request, hangup-request, and terminal-observation offsets

#### Scenario: Termination cannot be confirmed
- **WHEN** a mandatory terminal signal is absent or arrives after five seconds
- **THEN** the revocation assertion MUST be `FAIL` or `INCONCLUSIVE` according to whether contrary behavior or missing evidence was observed

### Requirement: Redacted terminal evidence and variance handoff
Each run SHALL emit schema-valid machine-readable results, a human-readable
summary, and an interface-impact document. `PASS` requires every mandatory
trial and assertion to pass; a contrary mandatory observation is `FAIL`; a
missing or unexecuted mandatory observation is `INCONCLUSIVE`. Evidence MUST
exclude credentials, SDP, raw provider payloads, raw media, transcripts,
arbitrary subject identifiers, and unbounded strings. Every interface variance
SHALL name affected `ACR-*` IDs and be disposed by the contract-kernel owner.

#### Scenario: All mandatory assertions pass
- **WHEN** every mandatory trial executes with complete redacted evidence and every assertion passes
- **THEN** the overall result MUST be `PASS` and the interface-impact document MUST still be emitted

#### Scenario: A mandatory assertion is contradicted
- **WHEN** a reproducible observation violates required ordering, timing, retry, cleanup, or redaction behavior
- **THEN** the overall result MUST be `FAIL`

#### Scenario: Mandatory evidence is missing
- **WHEN** a required trial does not run or lacks sufficient observable evidence
- **THEN** the overall result MUST be `INCONCLUSIVE`, never `PASS`

#### Scenario: Provider behavior differs from the baseline
- **WHEN** an observation requires a neutral interface correction
- **THEN** F0 MUST record the variance and MUST NOT edit canonical contracts or sibling implementation files

### Requirement: Feasibility does not qualify live use
F0 SHALL establish only whether the brokered-call handshake is feasible under
the recorded lab conditions. Its result MUST NOT promote a provider profile,
enable internal-live or production media, satisfy production latency budgets,
or waive deterministic, security, accessibility, operational, and rollback
gates owned by successor changes.

#### Scenario: F0 passes
- **WHEN** the overall F0 result is `PASS`
- **THEN** the contract publication gate MAY proceed after variance disposition, but the provider profile MUST remain disabled for live rings

#### Scenario: Live use is proposed from F0 evidence alone
- **WHEN** an operator attempts to enable internal-live or production media using only F0 evidence
- **THEN** release validation MUST reject the promotion and require `qualify-avatar-live-voice`
