# Design — Worker-Fleet Health Monitoring

## Context

The bounded Cloud PC worker fleet (today: `xfactory-artifact-cpc-brett01` in
group `xfactory-artifact-workers`, plus `xfactory-execution-lane-workers`) is
gated at **dispatch time** by `scripts/check-worker-readiness.py` +
`scripts/worker_readiness.py`: a fail-closed evaluation requiring a fresh
(≤300s) host heartbeat, an online non-busy GitHub runner, and matching
labels/profiles/boundaries. Sixteen workflows consume it.

That gate answers "may this job dispatch now?" It cannot answer "has the
fleet been dead since Tuesday?" — the codexFactory #156 failure, where a
queued smoke job rotted for six hours and 855 runs silently never
deliberated. The fleet needs a standing observer that runs when no work is
arriving.

Existing assets this design reuses rather than duplicates:

- `scripts/worker_readiness.py` — the evaluation vocabulary (reason codes
  like `runner_offline`, `heartbeat_stale`); the probe mirrors its severity
  vocabulary so an alert reads like a gate failure operators already know.
- Hermes readiness API (`/api/readiness/workers/<worker_id>`) — heartbeat
  source of truth, read-only token.
- GitHub Actions API — org runner-group membership/status and queued runs.
- `merge-master-approval.yml` — the labeled-issue notice pattern with
  graceful label-failure fallback.

## Goals / Non-Goals

**Goals:**

- Detect fleet death between dispatches within one cron interval (15 min).
- Detect silently-queued work (job older than threshold awaiting a
  self-hosted group).
- Surface exactly one open, deduplicated, labeled issue per outage episode;
  auto-close it on recovery.
- Fail-closed: probe errors (API unreachable, malformed payloads) are
  findings, never silent green.
- Run on hosted infrastructure so the monitor survives fleet death.

**Non-Goals:**

- Changing the dispatch-time readiness gate or any worker workflow.
- Remediation (no runner restarts, no host actions) — this change observes
  and reports; repair stays operator-run.
- OmniRoute egress-log signal (504 response-start rates) — noted as a future
  check family; not in this change's surface.
- Dashboard/visualization — the issue label is the v1 surface.

## Decisions

**D1 — Probe is pure evaluation over captured responses; the caller fetches.**
The openxFactory script takes JSON inputs (runner-group query, heartbeat
query, queued-runs query) and emits a findings document, exactly the
`check-worker-readiness.py` shape (file in, verdict JSON out, exit code
optional). This keeps the neutral repo free of live-network coupling, makes
the probe fully fixture-testable, and mirrors the existing gate's
workspace-contained file discipline. The xFactory caller workflow owns all
live API calls (`gh api`, Hermes curl) and writes the input files.
Alternative considered: probe fetches directly — rejected, it would smuggle
network/credential coupling into the neutral tooling home and defeat
fixture testing.

**D2 — Monitor runs hosted, never on the fleet.**
`runs-on: ubuntu-latest`. A self-hosted monitor cannot report its own
runner's death (the #156 lesson). Cost is trivial: three API reads per
15 minutes.

**D3 — Alert surface is one labeled, deduplicated, self-closing issue.**
Label `worker-fleet-health`. The caller lists open issues with the label: if
findings exist and none is open, create; if findings exist and one is open,
comment (updates the timestamped record without notification spam); if no
findings and one is open, close with a recovery comment. This follows the
merge-master-approval notice pattern, including file-the-record-even-if-
labeling-fails. Alternatives considered: failing the scheduled run only
(email-to-last-committer is invisible to anyone else and noisy per-run) —
rejected as the *sole* signal, though the run still exits non-zero on
findings so the Actions UI shows red; Teams/email webhooks — rejected for v1,
new dependency, no existing pattern in this repo.

**D4 — Thresholds are caller-supplied configuration, not probe constants.**
Queue-age threshold (default 600s), heartbeat max-age (default 300s, matching
the existing attestation contract), and the expected runner-group/worker-id
inventory are workflow env/inputs. The probe ships the defaults as its own
constants so it is meaningful standalone, and the workflow may override.
Rationale: fleet composition is deployment fact, not neutral contract.

**D5 — Severity vocabulary mirrors `worker_readiness.py` reason codes.**
Findings carry `runner_offline`, `runner_not_registered`,
`heartbeat_stale`, `heartbeat_missing`, `queue_age_exceeded`,
`probe_input_unavailable`, etc. Operators already read these from gate
failures; one vocabulary, two surfaces.

## Risks / Trade-offs

- [GitHub scheduled-cron drift: 15-min crons can slip or be skipped under
  load] → Accept for v1; the issue surface records last-healthy timestamps,
  and the probe's findings include `observed_at` so a stale monitor is
  itself visible. A monitor-self-health check is a named follow-up.
- [Issue-notification noise on flapping fleet] → Dedup + comment-instead-of-
  recreate means one issue per episode; a flap produces comments on one
  issue, not N issues. Auto-close requires two consecutive healthy probes
  (hysteresis) to avoid open/close oscillation.
- [Hermes readiness token expiry silently killing the heartbeat check] →
  Fail-closed: token/auth failure is a `probe_input_unavailable` finding,
  not a skip.
- [Queue-age false positives from intentionally-parked jobs] → v1 scopes
  queue-age to runs whose jobs target the monitored self-hosted groups;
  hosted-job queues are excluded. Threshold default (600s) exceeds every
  normal claim latency observed in the fleet's history.
- [Org-scoped API permissions: reading org runner groups needs more than the
  default repo token] → The caller uses the repo `GITHUB_TOKEN` against
  repo-scoped endpoints (`/repos/{repo}/actions/runners` lists org runners
  visible to the repo; `/actions/runs?status=queued` for queue age). Runner
  *group* membership is verified via the repo-visible runner list plus the
  group's repo allowlist already being xFactory-only (the 2026-09-01
  clearing-boundary ruling). If repo-scoped reads prove insufficient at
  realization, the caller gains one read-only org-scoped App token — a
  credential-contracts consumer, declared at tasks time.

## Migration Plan

Additive only: new script + new workflow. Rollback is deleting the workflow
file; the probe script is inert without a caller. Realization evidence: one
forced-unhealthy drill (probe run against fixture-shaped outage inputs via
`workflow_dispatch` with a `simulate_outage` input) files the labeled issue,
and the following healthy run closes it — both recorded in the change's
realization note.

## Open Questions

- Should the probe's findings JSON become a versioned schema under
  `contracts/schemas/` in a successor change? Deferred — v1 keeps it an
  internal artifact until a second consumer exists.
