# Recurrence Forecasting: Predicting How Often a Task Returns — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The crystallization trigger needs, per family, a predictive
distribution of future instance counts over a declared horizon plus a
stability outlook (pattern half-life) — start with a count-threshold MVP and
a Gamma-Poisson model with empirical-Bayes priors learned across families,
declare the cost-regime assumption because demand is price-elastic
(crystallizing makes the task cheap, which changes how often it is asked
for), and score every forecast against actuals or the forecaster is
decoration.
Topics: crystallization, recurrence-forecasting, demand-prediction,
empirical-bayes, seasonality, cold-start, jevons, pattern-stability,
episode-ledger
Repository context: openxFactory (neutral forecast record schema; models are
implementation detail behind it)
Captured: 2026-07-28

## Possible feats

- **Forecast record schema** — family ref, horizon, predictive distribution,
  stability outlook, cost-regime assumption, model/version, evidence window.
- **Empirical-Bayes prior service** — priors by family covariates learned
  from the whole ledger history.
- **Business-calendar binding** — tenant/domain calendars (month-end, sprint
  cadence, campaign cycles) as seasonality features.
- **Forecast scoring lane** — every emitted forecast is later scored against
  actuals; scores feed priors (see
  [accounting](crystallization-accounting.md)).

## Position in the packet

Third document of the sensing arc: consumes
[family](crystallization-task-families.md) instance histories from the
[episode ledger](crystallization-episode-ledger.md); its forecast records are
the primary input to the
[economics decision](crystallization-economics.md).

## What the decision layer actually needs

Not "will this recur?" but: **the distribution of instance counts over
horizon H, and how long the pattern will stay solvable the same way.** Both
matter — a family recurring 50×/quarter that mutates monthly is a worse
investment than one recurring 10×/quarter that has been byte-stable for a
year. So the forecast record carries two parts:

- **Volume** — P(N instances in next H) as a distribution, not a point.
- **Stability** — a pattern-half-life estimate from intra-family drift
  (how much do recent episodes' plans/inputs vary vs. older ones) and
  upstream volatility (do the tools/sources this family touches change
  often). Stability feeds the survival term in the economics model.

## Model ladder (build the cheap rungs first)

1. **Count threshold (MVP)** — "seen k times in W days" with human judgment.
   Honest, transparent, and sufficient to prove the loop end-to-end.
2. **Gamma-Poisson** — conjugate rate model per family; predictive is
   negative binomial; exposure-window aware (a family first seen 10 days ago
   has 10 days of exposure, not the ledger's lifetime).
3. **Seasonality** — business calendars as features: month-end close
   (Ledgerx), sprint cadence (codex), campaign cycles (Adx), clinic schedules
   (Medx). Calendars are tenant/domain content, not neutral constants.
4. **Trend/burst** — growth terms or Hawkes-style self-excitation only if
   calibration scores demand them. Resist sophistication the scores don't
   ask for.

## Cold start: priors across families

Two observations cannot estimate a rate — but the ledger holds hundreds of
other families whose covariates (domain, `job_type`, subject count, fragment
vs. whole-job) predict recurrence class. Empirical Bayes: fit priors over
those covariates, so a new family starts from "families shaped like this
usually recur ~weekly" and updates from its own counts. This is the
meta-learning move: **the system learns what kinds of work recur** as a
transferable asset.

## Two honesty problems

- **Censoring** — the ledger only sees submitted work. Expensive AI
  suppresses demand: people batch, defer, or don't bother. Observed rate
  underestimates latent demand.
- **Price elasticity (Jevons)** — once crystallized and cheap, the task gets
  asked for more. Post-crystallization volume routinely exceeds the
  forecast. Good for ROI, fatal for naive calibration — so every forecast
  declares its **cost-regime assumption** ("at current AI pricing and
  friction"), and post-cutover actuals are scored against a
  regime-adjusted expectation, not the raw pre-cutover forecast.

## Claims

- **RF-C1** — Forecasts are predictive distributions with a declared horizon
  and evidence window; point counts are not an acceptable output shape.
- **RF-C2** — Cold start is handled by empirical-Bayes priors over family
  covariates learned from the whole ledger, not by waiting for long
  histories.
- **RF-C3** — Demand is price-elastic; forecasts declare their cost-regime
  assumption, and calibration distinguishes forecast error from regime
  change.
- **RF-C4** — Stability (pattern half-life) is forecast alongside volume and
  is an equal input to the investment decision.
- **RF-C5** — Every forecast is stored and later scored against actuals;
  the model ladder is climbed only when calibration scores demand it.

## Open questions

- **RF-Q1** — Standard horizons: one (90 days) or a small set (30/90/365)
  aligned to budget periods?
- **RF-Q2** — Who owns business calendars — Tenant Hermes content consumed
  by the domain forecaster?
- **RF-Q3** — Minimum evidence to emit a forecast at all (below it, the
  family is `forming` and undecidable)?
- **RF-Q4** — How do fuzzy family matches count — fractional instances
  weighted by match confidence (TF-Q5), or excluded?
- **RF-Q5** — Where does the forecaster run — a bounded read-only worker on
  the nightly sweep cadence, like the gap-scan pattern in
  [practice suggestion generation](domain-practice-suggestion-generation.md)?

## Related

- [Task Families](crystallization-task-families.md) — the counting unit.
- [Crystallization Economics](crystallization-economics.md) — the consumer.
- [Crystallization Accounting](crystallization-accounting.md) — the scorer.
