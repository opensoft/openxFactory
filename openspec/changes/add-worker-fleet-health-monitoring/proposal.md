---
code_surface: openxFactory (`scripts/worker_fleet_health.py` — the neutral health probe evaluating runner presence/online state, heartbeat freshness, and queued-job age from captured API responses; `tests/worker-fleet-health/` — the probe's fixture suite). CROSS-REPO REALIZATION, following the `add-nightly-dashboard-refresh` precedent: xFactory aggregation — one new scheduled caller workflow `.github/workflows/cpc-runner-health.yml` (hosted runner, cron + manual dispatch, issues the probe against the live GitHub Actions and Hermes readiness APIs, files/dedupes/auto-closes a labeled health issue). NO change to the dispatch-time readiness gate (`scripts/check-worker-readiness.py`, `scripts/worker_readiness.py`), to any worker workflow, to the heartbeat publisher, or to any contract bytes under `contracts/`.
target_release: none — this change moves no contract bytes. Realization lands as the probe script, its tests, and the scheduled caller; the bundle is untouched. The evidence gate is one forced-unhealthy drill (probe pointed at a fixture-shaped outage) producing a labeled issue, and one healthy run closing it, both recorded in the change's realization note.
---

# Add Worker-Fleet Health Monitoring

## Why

Worker-fleet readiness is only evaluated **at dispatch time**: sixteen
workflows gate on `check-worker-readiness.py`, but nothing watches the fleet
between dispatches. codexFactory issue #156 is the concrete failure this
produces — a smoke job sat `queued` for six hours with no runner ever
assigned, and 855 deliberation-worker runs completed "successfully" without
any seat ever executing, all invisible until a human audited by hand. A gate
that only fires when work arrives cannot detect that no work can flow.

## What Changes

- Add a neutral, domain-independent **fleet health probe**
  (`scripts/worker_fleet_health.py`) that evaluates three check families from
  captured API responses: (a) runner presence and online state per expected
  runner group, (b) heartbeat freshness against the existing 300-second
  attestation contract (Hermes readiness API), and (c) queued-job age —
  workflow jobs waiting on a self-hosted runner group beyond a threshold.
- Add a **scheduled caller** in the xFactory aggregation repo (cron +
  `workflow_dispatch`) that runs the probe on a **hosted** runner — a fleet
  monitor that depends on the fleet it watches cannot report the fleet's
  death — and turns findings into a single labeled GitHub issue, deduplicated
  against open health issues and auto-closed on recovery.
- Alerting follows the established `merge-master-approval.yml` notice
  pattern: `gh issue create` with a dedicated label, record preserved even if
  labeling fails.
- The probe is fail-closed on its own inputs (API errors are findings, never
  silent passes) and read-only against every system it touches.

## Capabilities

### New Capabilities

- `worker-fleet-health`: standing, between-dispatch monitoring of the bounded
  Cloud PC worker fleet — runner online state, heartbeat freshness, and
  queue-age signals, surfaced as a deduplicated, self-closing health issue.

### Modified Capabilities

<!-- No existing capability's requirements change. The dispatch-time readiness
     gate (consumed by worker workflows) keeps its contract unchanged; this
     change adds a complementary monitoring surface, not a gate change. -->

## Impact

- **openxFactory**: new `scripts/worker_fleet_health.py` +
  `tests/worker-fleet-health/`; no `contracts/` bytes move.
- **xFactory aggregation**: new `.github/workflows/cpc-runner-health.yml`
  (scheduled, hosted, `issues: write` + `actions: read` on the repo token,
  Hermes readiness token as a read-only secret reference).
- **No changes** to: the readiness gate, any existing worker workflow, the
  heartbeat publisher (Omnigent-Install), runner group membership, or CPC
  host configuration.
- **Operators** gain a single issue-labeled signal (`worker-fleet-health`)
  instead of silent fleet death.
