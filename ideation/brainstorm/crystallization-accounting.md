# Crystallization Accounting: Realized Savings and Calibrated Predictions — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The ex-post half of the money brain: a savings ledger that only
credits capabilities against sentinel-anchored counterfactuals (never
self-graded estimates), a calibration board where every ex-ante number —
recurrence forecasts, build estimates, pattern half-lives, risk premiums —
is scored against actuals and the scores update the priors (the invest-level
learner's training data), normalization rules that keep demand growth and
token-price deflation from inflating claimed wins, and a portfolio surface
whose headline metric is automation share — the fraction of governed
instances served above the recall-assisted rung.
Topics: crystallization, accounting, savings-ledger, counterfactual,
calibration, automation-share, cost-accountability, metering, portfolio
Repository context: openxFactory (neutral ledger/calibration schemas; rides
the cost-accountability chain)
Captured: 2026-07-28

## Possible feats

- **Crystallization savings ledger** — per-instance cost on the served path
  vs. sentinel-anchored counterfactual, rolled up per capability.
- **Calibration board** — every stored prediction scored against actuals;
  scores feed empirical-Bayes priors (RF) and estimate models (EC/BP).
- **Automation-share metric** — the packet's north-star operational number,
  tracked like corpus canon share.
- **Normalization rules** — per-instance accounting, demand-growth
  separation, token-price indexing.

## Position in the packet

Fifth document of the run/renew arc: consumes metering and the
[episode ledger](crystallization-episode-ledger.md)'s cost vectors on both
paths, the [learning loop](crystallization-learning-loop.md)'s sentinel
actuals, and the stored predictions of
[forecasting](crystallization-recurrence-forecasting.md),
[economics](crystallization-economics.md), and the
[build pipeline](crystallization-build-pipeline.md); publishes to the
[registry](crystallization-capability-registry.md) cost profiles and the
portfolio surface.

## Counterfactual discipline

"The capability saved 40M tokens" requires knowing what the AI path *would
have* cost — and that number decays: models cheapen, recall improves, the
task itself shifts. Rules:

- **Sentinels are the anchor.** The ε sample's actual AI-path costs (LC-C3)
  are the living counterfactual; between sentinel observations, estimates
  interpolate from the last anchor, clearly marked as interpolation.
- **No self-graded savings.** A capability with a stale sentinel anchor
  (no fresh AI-path observation within policy window) reports
  "savings unverifiable," not a rosy estimate. This single rule keeps the
  whole flywheel honest — everything downstream (budgets, roadmaps,
  invest-level learning) trusts these numbers.
- **Full-cost accounting.** Savings net out build amortization, maintenance
  and regeneration spend, sentinel/exploration spend, and dispatch
  overhead. A capability can be marginally cheap and net-negative; the
  ledger must be able to say so.

## The calibration board

Every ex-ante number the packet produces is a stored record with a maturity
date; when actuals arrive, it gets scored:

| Prediction | Produced by | Scored against |
| --- | --- | --- |
| recurrence distribution | RF | realized instance counts (regime-adjusted) |
| pattern half-life | RF | observed drift events / capability lifespan |
| build estimate | EC/BP | build actuals |
| maintain estimate | EC | regeneration + incident spend |
| savings projection | EC | ledger realized savings |

Scores update the empirical-Bayes priors (RF-C2) and estimate models — this
is precisely the invest-level training data of LC-C4. An unscored predictor
is decoration (RF-C5); the calibration board is where that rule is
enforced.

## Normalization honesty

- **Per-instance, then volume.** Jevons growth (RF-C3) multiplies instances
  after cutover; report savings-per-instance and volume separately so
  demand growth never masquerades as efficiency.
- **Token-price indexing.** Report raw token savings AND cost normalized to
  a price index (EC-C2's deflation, applied retrospectively) — a capability
  can "save more tokens" every month while saving less money.
- **Human time is real.** Where episodes carried human touches (EL-Q2),
  reclaimed human minutes are reported alongside tokens — often the larger
  number and the more decision-relevant one.

## The portfolio surface

Rolls up for the efficiency mandate (domain) and the accounting bench
(tenant): **automation share** (fraction of governed instances served at L2+
— the corpus canon-share of operations; watch trends, not day deltas),
savings run-rate net of full costs, calibration scores by predictor,
risk concentration (how much work depends on one capability), and the
demand-derived roadmap feed
([cross-tenant](crystallization-cross-tenant.md)).

## Claims

- **CA-C1** — Savings are credited only against sentinel-anchored
  counterfactuals; stale anchors report "unverifiable," never estimates
  dressed as facts.
- **CA-C2** — Every ex-ante number is a stored, maturity-dated record that
  gets scored; scores flow back into priors and estimate models.
- **CA-C3** — Automation share is the packet's headline operational metric,
  tracked as a trend like corpus canon share.
- **CA-C4** — Accounting normalizes per-instance vs. volume and indexes
  token prices; demand growth and deflation are reported, not absorbed.
- **CA-C5** — The ledger rides the existing cost-accountability chain
  (worker clock-in → domain efficiency audit → tenant accounting → project
  accountant) — crystallization adds records, not a rival chain.

## Open questions

- **CA-Q1** — Credits unit: inherits cost-accountability's open question
  (tokens vs. normalized cost vs. wall-clock) — does crystallization force
  the answer (it needs cross-time comparability)?
- **CA-Q2** — Attribution for composed capabilities: a playbook using three
  crystallized fragments — who gets the savings?
- **CA-Q3** — Price index source and governance (same as EC-Q3's deflation
  curve — one artifact, two consumers?).
- **CA-Q4** — Reporting cadence and the report's lifecycle status (a
  `report` kind doc, nightly like corpus health?).
- **CA-Q5** — Do we account reviewer/adjudicator human time as a cost of
  the crystallization program itself (it is real and nontrivial early)?

## Related

- [Crystallization Economics](crystallization-economics.md) — the ex-ante
  half this grades.
- [Learning Loop](crystallization-learning-loop.md) — sentinel anchors and
  the invest-level learner.
- [Cost Accountability & Efficiency](cost-accountability-and-efficiency-model.md)
  — the chain this rides.
