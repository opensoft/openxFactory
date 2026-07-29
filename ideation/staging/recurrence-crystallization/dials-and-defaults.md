# Crystallization Dials and Staged Defaults

Status: staged
Kind: register
Summary: The declared-dials register for the crystallization contract
family — every tunable the fragments reference (nomination thresholds,
forecast horizons, sentinel rates, corpus bars, retention, proof windows,
decision guards, hysteresis, throttles) with a staged default, an owning
policy layer, and its source claim, following the governed-derived-model
declared-dials pattern so the OpenSpec changes inherit defaults instead of
inventing constants.
Topics: crystallization, dials, defaults, sentinel-sampling, corpus-bar,
forecast-horizon, retention, canary, hysteresis, throttles
Repository context: openxFactory (neutral defaults; owners tune within
policy)
Staging ID: `openxFactory:staging:recurrence-crystallization`
Source: staged defaults distilled 2026-07-29 from the brainstorm packet's
open questions (EC-Q1, RQ-Q1, EL-C4, PV-C5/Q5, LC-Q1, DL-Q1/Q5, AU-Q5,
TF-Q3, RF-Q1/Q3); values are starting positions, deliberately conservative,
each expected to be re-tuned by the accounting calibration board once real
data exists.
Target capabilities: none (supporting defaults register — no deltas)

## The register

| Dial | Staged default | Owner | Source |
| --- | --- | --- | --- |
| `nomination_count_k` | 3 occurrences in 30 days auto-nominates | tenant policy | EC decision ladder rung 2 |
| `min_family_register` | 2 instances to register a family | neutral default | TF-Q3 |
| `min_family_forecast` | 3 instances before a forecast is emitted | neutral default | RF-Q3 |
| `forecast_horizon` | 90 days primary; 30/365 auxiliary | neutral default | RF-Q1 |
| `decision_guard` | fund only if payback ≤ 90 days AND P(payback) ≥ 0.7 (EV rung) | tenant policy | EC-Q1 |
| `build_abort` | abort at 120% of estimate; persist partials, return actuals | tenant policy | EC-C4 |
| `corpus_bar_L3` | ≥ 3 episodes including ≥ 1 counterexample | domain policy | RQ-Q1 |
| `corpus_bar_L5_plus` | ≥ 20 episodes including ≥ 3 counterexamples, plus fence review | domain policy | RQ-Q1 |
| `payload_retention` | tool-I/O payloads 90 days; digests indefinite | tenant policy | EL-C4 |
| `shadow_window` | ≥ 20 instances or 14 days, whichever is later | domain policy | PV-C5 |
| `canary_curve` | 10% → 50% → 100%, one clean week per step | domain policy | PV-Q5 |
| `sentinel_epsilon_start` | 0.20 at full cutover | domain policy | LC-Q1 |
| `sentinel_epsilon_floor` | 0.02 while the capability holds authority (never zero) | neutral default | LC-C2 |
| `demotion_hysteresis` | re-promotion thresholds 2× stricter than the demotion trigger that fired | neutral default | DL-C2 |
| `disuse_retirement` | 2 consecutive dormant quarters auto-proposes retirement | tenant policy | DL-C5, DL-Q5 |
| `young_throttle` | rate/output caps at 25% of observed family volume, relaxing one step per clean, proof-fresh month | domain policy | AU-C4, AU-Q5 |

## Reading rules

- **Owner** is the layer whose policy may tune the dial; neutral defaults
  hold until it does. Neutral-owned dials (`sentinel_epsilon_floor`,
  `demotion_hysteresis`, registration minima) are floors/ratios with
  constitutional flavor — tunable only by contract revision, not by tenant
  preference.
- Every dial is expected to be **re-tuned by evidence**: the accounting
  calibration board (CA-C2) scores the predictions these dials gate, and a
  dial whose default keeps producing bad calls is a finding, not a fact of
  life.
- The MVP (primary doc, D8) runs with these values as-is except
  `sentinel_epsilon_start`, which stays at 0.20 *without decay* for the
  MVP's whole life — the first family's job is to generate honest
  counterfactuals, not to maximize savings.
