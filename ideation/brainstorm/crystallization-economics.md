# Crystallization Economics: When to Spend Tokens to Build Software — Brainstorm

Status: staged
Kind: architecture
Summary: The "over a threshold, build it" trigger is an investment decision
under uncertainty with its own maturity ladder (human judgment → count
threshold → expected value with an uncertainty guard → budgeted portfolio),
whose expected-value form must discount savings by AI-price deflation and
pattern survival, must weigh non-token value (latency, determinism,
auditability, compliance) that does not deflate, and must select a ladder
rung, budget cap, and abort rule — not a boolean — with the tenant's
crystallization budget as the consent-to-spend surface.
Topics: crystallization, economics, roi, threshold, token-budget,
cost-accountability, deflation, portfolio, practice-clearance,
efficiency-audit
Repository context: openxFactory (neutral decision-record schema; thresholds
and budgets are tenant/domain policy content)
Captured: 2026-07-28
Organized: 2026-07-29 into the
[recurrence-crystallization staged topic](../staging/recurrence-crystallization/recurrence-crystallization.md)
(staged); kept as design history.

## Possible feats

- **Crystallization decision record** — candidate ref, chosen rung, expected
  value with intervals, budget cap, abort rule, approvals; idempotent per
  (family, evidence window).
- **Crystallization budget envelope** — a tenant policy object (rides the
  client-policy-wizard spend-ceiling pattern) that funds and caps builds per
  period.
- **Deflation-aware value model** — savings streams discounted by expected
  inference-price decline and pattern survival.
- **Decision-ladder config** — which decision rung a tenant/domain runs at,
  itself policy.

## Position in the packet

First document of the invest/build arc: consumes candidate packets from the
sensing arc ([forecasts](crystallization-recurrence-forecasting.md) over
[families](crystallization-task-families.md)), chooses whether/what to build
on the [automation ladder](crystallization-automation-ladder.md), and hands
approved decisions to [requirements mining](crystallization-requirements-mining.md)
and the [build pipeline](crystallization-build-pipeline.md). Every number it
uses is scored later by [accounting](crystallization-accounting.md).

## The decision has its own ladder

Do not start with math nobody trusts. Rungs of decision maturity:

1. **Human judgment over an evidence packet (MVP)** — the sensing arc
   presents family + forecast + costs; a person decides. This is already a
   huge step over "nobody noticed the repetition."
2. **Count threshold** — "k occurrences in W days" auto-nominates; human
   clears. The user's original framing, kept as the honest first automation.
3. **Expected value with an uncertainty guard** — build when
   E[value] > 0 **and** P(payback within T) > p. Distributions come from RF;
   the guard stops coin-flip builds.
4. **Budgeted portfolio** — candidates ranked by expected value per build
   token; fund greedily within the period's crystallization budget
   (knapsack). This is the steady-state: the question stops being "is this
   worth building?" and becomes "is this the best thing to build this
   month?"

## The expected-value form (rung 3+)

For candidate family f at ladder rung L over horizon H:

```text
value(f, L) =
    Σ_t  E[instances_t]                       (RF volume, regime-declared)
        × (marginal_cost_AI − marginal_cost_L)  (from ledger cost vectors)
        × survival(t)                           (RF stability half-life)
        × deflation(t)                          (AI price decline factor)
  − build_cost(L)          (estimated; calibrated by CA over time)
  − maintain_cost(L, H)    (drift-repair expectation, DL)
  − risk_premium(L)        (correlated-failure exposure, AU)
  + nontoken_value(L)      (latency, determinism, auditability, compliance)
```

Two terms deserve emphasis because naive ROI omits them and systematically
overbuilds:

- **Deflation** — inference prices fall and cheaper models improve. A
  capability that pays back in 24 months may never pay back, because by
  month 12 the L1 recall-assisted path costs a fraction of today. Token
  savings are a **melting asset**; discount them like one.
- **Non-token value does not melt** — a deterministic, millisecond,
  fully-auditable path can justify building even where tokens alone never
  would (a gate that must be reproducible; a Medx check that must behave
  identically every time; an offline-capable step). Sometimes this term is
  the whole case, and the spec should let it be.

## Budget as the consent surface

A tenant sets a **crystallization budget** per period — the wizard's
spend-ceiling pattern applied to self-improvement spend. The budget is the
consent instrument: no platform-initiated build spends tenant money without
an envelope that covers it, and clearance rides the same rails as practice
adoption (auto-clear envelope for low-risk/low-cost builds, human liaison
above it — see
[practice clearance](practice-clearance-and-project-realization.md)). The
Domain Hermes efficiency mandate
([cost accountability](cost-accountability-and-efficiency-model.md)) is the
natural nominating persona; the tenant accounting function is the natural
budget owner.

## Decisions select a shape, not a boolean

An approved decision fixes: the target **rung** (build the L3 playbook now,
not the L6 program — see AL ratchet), the **budget cap** with an abort rule
(stop at 120% of estimate, return actuals, renominate), and the **proof
obligations** (which parity stages before authority). Under-building is
recoverable (climb later, evidence in hand); over-building is sunk.

## Claims

- **EC-C1** — The trigger is an investment decision under uncertainty with a
  maturity ladder; the count threshold is a legitimate early rung, not the
  end state.
- **EC-C2** — Savings streams are discounted by AI-price deflation and
  pattern survival; omitting either systematically overstates ROI and
  overbuilds.
- **EC-C3** — Non-token value (latency, determinism, auditability,
  compliance, offline) is a first-class term and is sometimes the entire
  justification.
- **EC-C4** — A decision selects rung, budget cap, abort rule, and proof
  obligations — never a bare build/don't-build bit.
- **EC-C5** — The tenant crystallization budget plus the clearance envelope
  is the consent surface; there is no silent spend path.

## Open questions

- **EC-Q1** — Default guard values (T, p) per rung and risk class — and who
  ratifies them (domain policy vs. tenant policy)?
- **EC-Q2** — Risk premium before incident data exists: fixed schedule by
  rung and authority class, replaced by experience as CA accumulates?
- **EC-Q3** — Deflation curve source: operator-maintained assumption
  (reviewed quarterly), or derived from observed metering prices?
- **EC-Q4** — Nominating vs. deciding personas: efficiency mandate nominates,
  but does the decision sit with the Domain Lead, the tenant accounting
  bench, or a joint gate?
- **EC-Q5** — Platform-funded builds (cross-tenant families): separate
  budget and chargeback model — see
  [cross-tenant](crystallization-cross-tenant.md).

## Related

- [Recurrence Forecasting](crystallization-recurrence-forecasting.md) — the
  distributions consumed here.
- [Automation Ladder](crystallization-automation-ladder.md) — the rung being
  purchased.
- [Crystallization Accounting](crystallization-accounting.md) — where every
  number used here gets graded.
