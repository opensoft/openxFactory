# Spec Delta — worker-fleet-health

## ADDED Requirements

### Requirement: Standing fleet observation

The system SHALL evaluate worker-fleet health on a recurring schedule
independent of any work dispatch, covering three check families: GitHub
runner presence and online state for each expected runner group, heartbeat
freshness for each expected worker identity against the attestation max-age,
and the age of queued workflow jobs awaiting a monitored self-hosted runner
group.

#### Scenario: Fleet healthy between dispatches

- **WHEN** the scheduled evaluation runs with all expected runners online,
  all heartbeats within the attestation max-age, and no queued job older
  than the queue-age threshold
- **THEN** the evaluation reports zero findings and records the observation
  timestamp

#### Scenario: Runner offline between dispatches

- **WHEN** the scheduled evaluation runs and an expected runner reports
  `status` other than `online` while no workflow is dispatching
- **THEN** the evaluation produces a `runner_offline` finding naming the
  runner and its group

### Requirement: Fail-closed probe inputs

The probe SHALL treat unavailable, malformed, or unauthorized check inputs
as findings (`probe_input_unavailable`) and MUST NOT report fleet health as
green when any check family's input could not be obtained.

#### Scenario: Heartbeat API unreachable

- **WHEN** the heartbeat query fails or returns an unparseable payload
- **THEN** the probe emits a `probe_input_unavailable` finding for the
  heartbeat family and does not report the fleet as healthy

#### Scenario: Runner API error

- **WHEN** the runner-group query returns an error indicator
- **THEN** the probe emits a `probe_input_unavailable` finding for the
  runner family and does not report the fleet as healthy

### Requirement: Monitor independence from the observed fleet

The scheduled health evaluation MUST execute on hosted compute, and MUST NOT
depend on any member of the fleet it observes.

#### Scenario: Fleet entirely offline

- **WHEN** every self-hosted runner in every monitored group is offline
- **THEN** the scheduled evaluation still runs and reports the outage

### Requirement: Deduplicated labeled alert with recovery closure

Findings SHALL be surfaced as a single labeled GitHub issue per outage
episode: the caller SHALL create one issue carrying the health label when
findings exist and no such open issue exists, SHALL comment on the existing
open issue instead of creating a duplicate when one exists, and SHALL close
the open issue with a recovery comment only after the configured number of
consecutive healthy evaluations.

#### Scenario: New outage opens one issue

- **WHEN** an evaluation produces findings and no open issue carries the
  health label
- **THEN** the caller creates exactly one issue with the health label and
  the findings as its body

#### Scenario: Continuing outage does not duplicate

- **WHEN** an evaluation produces findings and an open issue already carries
  the health label
- **THEN** the caller adds a comment to that issue and creates no new issue

#### Scenario: Recovery closes after hysteresis

- **WHEN** evaluations report zero findings for the configured consecutive
  count while a health-labeled issue is open
- **THEN** the caller closes that issue with a recovery comment

### Requirement: Shared severity vocabulary

Findings SHALL carry reason codes drawn from the same vocabulary as the
dispatch-time readiness evaluation (for example `runner_offline`,
`runner_not_registered`, `heartbeat_stale`, `heartbeat_missing`), extended
with monitoring-specific codes (`queue_age_exceeded`,
`probe_input_unavailable`).

#### Scenario: Finding names gate vocabulary

- **WHEN** the probe reports a stale heartbeat
- **THEN** the finding's reason code is `heartbeat_stale`, matching the
  dispatch-time gate's reason for the same condition

### Requirement: Caller-configurable thresholds with probe defaults

The probe SHALL define defaults for heartbeat max-age (300 seconds, matching
the attestation contract), queue-age threshold (600 seconds), and recovery
hysteresis (2 consecutive healthy evaluations), and SHALL accept caller
overrides for each.

#### Scenario: Caller overrides queue-age threshold

- **WHEN** the caller supplies a queue-age threshold of 120 seconds and a
  queued job has waited 300 seconds
- **THEN** the probe reports `queue_age_exceeded` for that job

#### Scenario: Defaults apply without caller configuration

- **WHEN** the caller supplies no thresholds and a heartbeat is 250 seconds
  old
- **THEN** the probe reports no staleness finding

### Requirement: Read-only posture

The probe and its caller MUST NOT mutate any observed system: no runner
state changes, no job cancellations, no workflow dispatches, and no Hermes
writes. The only permitted writes are the health issue surface and the
evaluation's own output artifact.

#### Scenario: Outage produces no remediation action

- **WHEN** the evaluation detects an offline runner
- **THEN** the only state change is on the health issue surface; the
  runner, the queue, and the heartbeat store are untouched
