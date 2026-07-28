# Recurrence Crystallization: Turning Repeated AI Work into Governed Software — Brainstorm

Status: brainstorm
Kind: reference
Summary: This overview anchors a nineteen-document packet proposing
recurrence crystallization — the factory notices which expensively-AI-solved
task families keep returning, predicts their recurrence and stability,
decides under a tenant-consented budget whether to spend tokens building a
cheaper dedicated path (a rung on a seven-step ladder from cached results
through frozen playbooks to pure code), has Hermes mine the solved episodes
into requirements and acceptance corpora, builds through codexFactory as
ordinary governed work under strict authority conservation, dispatches
future instances behind deterministic scope fences with the AI path intact,
and keeps a sentinel fraction on AI so learning, drift detection, and
savings claims stay honest — extending the existing self-learning loop with
a procedural consolidation stage.
Topics: crystallization, recurrence, self-learning, automation-ladder,
episode-ledger, pattern-ledger, crystallizer, steward, economics,
domain-hermes, efficiency-audit, dtn-register
Repository context: openxFactory (cross-factory; a future crystallization
contract family)
Captured: 2026-07-28

## Possible feats

- **Pattern Ledger** — episodes, families, forecasts, and candidate
  nomination as one Domain-Hermes-owned sensing surface.
- **Crystallizer** — decision, micro-spec mining, and governed build under
  a three-layer approval braid.
- **Capability Steward** — registry-driven dispatch, proof gates, sentinel
  regime, drift response, and accounting as one operating plane.
- **Crystallization contract family** — the neutral schemas (episode,
  family, forecast, candidate, decision, fence, registry record, health
  report) the three subsystems exchange.

## The idea in one paragraph

A task arrives that we have no set way to handle, so the factory solves it
the expensive way — several Hermes personas deliberating, Omnigent workers
executing — and we praise the agents; the self-learning layers absorb a
little. It comes back; we solve it again; the learner absorbs more. Today
that loop tops out at *recall-assisted solving*: memory makes the next solve
somewhat better, but every instance still pays for planning and judgment.
Crystallization takes the loop further: **predict** which task families will
keep returning and how long they will stay stable, and when the forecast
clears a threshold the tenant has funded, **spend tokens once** — Hermes
mines the solved episodes into requirements, an acceptance corpus, and a
scope fence; codexFactory builds the dedicated path as ordinary governed
work — so that future instances run **without AI or with a fraction of the
tokens**, behind a fence that routes anything unfamiliar straight back to
the expensive path that never went away.

## Where each beat of the original framing landed

| The framing | Where it landed |
| --- | --- |
| "solve it with expensive AI, several agents" | the L0/L1 rungs; every solve leaves an episode — [episode ledger](crystallization-episode-ledger.md) |
| "reward our agents with praise" | praise as one label in the append-only outcome stream (EL-C2, Goodhart-guarded in LC-C5) |
| "self-learning hermes learned a little" | today's ceiling, L1 recall-assisted (AL); crystallization framed as its consolidation stage — [learning loop](crystallization-learning-loop.md) |
| "we see the same or similar task" | fingerprints and recurrence families — [task families](crystallization-task-families.md) |
| "predict how often this will occur" | volume + stability forecasts — [recurrence forecasting](crystallization-recurrence-forecasting.md) |
| "if over a threshold, spend the tokens" | the decision ladder, deflation-discounted EV, tenant budget as consent — [economics](crystallization-economics.md) |
| "hermes defines the requirements" | episode-mined micro-spec + corpus + fence — [requirements mining](crystallization-requirements-mining.md) |
| "make actual coded software" | the ladder's upper rungs, built as governed codexFactory jobs — [ladder](crystallization-automation-ladder.md), [build pipeline](crystallization-build-pipeline.md) |
| "handle it without AI / reduced tokens" | fence-guarded dispatch with AI fallback and sentinels — [dispatch](crystallization-dispatch-and-fences.md) |

## The flywheel

```text
        SOLVE (expensive, governed)          ◄────────────────────┐
          │  every run leaves an episode                          │
          ▼                                                       │
   ┌─ PATTERN LEDGER ──────────────────────┐                      │
   │  episodes → families → forecasts      │                      │
   │  nominate: crystallization_candidate  │                      │
   └──────────────┬────────────────────────┘                      │
                  ▼                                               │
   ┌─ CRYSTALLIZER ────────────────────────┐                      │
   │  decide (rung, budget, abort)         │   fallbacks,         │
   │  specify (spec + corpus + fence)      │   sentinels,         │
   │  build (governed codex job,           │   adjudications,     │
   │         authority-conserving)         │   scored forecasts   │
   └──────────────┬────────────────────────┘   flow back up       │
                  ▼                                               │
   ┌─ CAPABILITY STEWARD ──────────────────┐                      │
   │  prove (replay → shadow → canary)     │                      │
   │  dispatch behind fences; AI intact    │──────────────────────┘
   │  watch drift; regenerate/demote/melt  │
   │  account: sentinel counterfactuals    │
   └───────────────────────────────────────┘
```

## This already happens here — organically

The repo's own history is the existence proof: `sync-notebooklm-books.py`,
the doc-health checker, and every `validate-*.py` began as repeated
manual/AI work someone hardened into a script. The cost-accountability
brainstorm already gives the Domain Hermes an efficiency mandate whose
audit selector targets *most-repeated* tasks; DTN-015 already seeds a
"learned handling rule / correction-promotion loop"; this morning's
ontology packet already designs the result-cache rung and the micro-agent
substrate. The packet industrializes what the culture already does by
hand — with forecasts instead of hunches, budgets instead of ad-hoc spend,
fences instead of hope, and lineage instead of orphan scripts.

## Eight principles that thread the packet

1. **The ladder, not the leap** (AL) — seven rungs; buy the cheapest rung
   that pays; ratchet on evidence.
2. **Episodes are the spec** (EL/RQ) — requirements, acceptance, parity,
   and savings all cite the same solved-episode substrate.
3. **Authority conservation** (AU) — crystallization never widens
   permissions; constitutional falses persist at every rung.
4. **Never silently wrong** (DS/PV) — fence before, post-conditions after,
   sentinels forever, provenance visible, AI fallback always intact.
5. **Regenerate, don't patch** (BP/DL) — capabilities are derived
   artifacts of episodes; the pipeline is the asset.
6. **Score every prediction** (RF/CA) — forecasts, estimates, half-lives
   all get graded; the priors improve; the factory learns to invest.
7. **Keep learning anyway** (LC) — sentinel ε with a nonzero floor
   prevents learning starvation and keeps counterfactuals honest.
8. **Ownership follows funding and consent** (EC/XT) — tenant budgets,
   three consent tiers, platform capabilities as priced product.

## Placement in the layer model

| Layer | Role in crystallization |
| --- | --- |
| Subject Hermes | transparency; consent where automation touches the subject |
| Tenant Hermes | crystallization budget, T1/T2/T3 consent, clearance, accounting |
| Domain Hermes | Pattern Ledger, nomination, micro-specs, rung ceilings, fitness gates |
| xFactory layer | dispatch junction, gates, registry contract, audit continuity |
| codexFactory | builds every domain's capabilities (cross-domain service seam) |
| Omnigent | executes builds; crystallized-executor class in the permission matrix |
| External enforcement | unchanged, final backstop for every rung including L6 |

## The ladder at a glance

L0 cold solve · L1 recall-assisted (today) · L2 memoized result (owned by
the result-cache brainstorm) · L3 frozen playbook (expected workhorse) ·
L4 specialist micro-agents · L5 code with AI edges · L6 pure code.
Ceilings from task nature, domain policy, authority. Details:
[automation ladder](crystallization-automation-ladder.md).

## Document map

Claim/question IDs use each doc's prefix (EL-C1, RF-Q3, …) so staging and
spec extraction can cite atomically.

**Sensing arc** → synthesis:
[Pattern Ledger](crystallization-synthesis-pattern-ledger.md)

- [Episode Ledger](crystallization-episode-ledger.md) (EL)
- [Task Fingerprints and Recurrence Families](crystallization-task-families.md) (TF)
- [Recurrence Forecasting](crystallization-recurrence-forecasting.md) (RF)

**Invest/build arc** → synthesis:
[Crystallizer](crystallization-synthesis-crystallizer.md)

- [Crystallization Economics](crystallization-economics.md) (EC)
- [Automation Ladder](crystallization-automation-ladder.md) (AL)
- [Requirements Mining](crystallization-requirements-mining.md) (RQ)
- [Build Pipeline](crystallization-build-pipeline.md) (BP)
- [Authority and Consent](crystallization-authority-and-consent.md) (AU)

**Run/renew arc** → synthesis:
[Capability Steward](crystallization-synthesis-steward.md)

- [Capability Registry](crystallization-capability-registry.md) (CR)
- [Dispatch and Scope Fences](crystallization-dispatch-and-fences.md) (DS)
- [Parity and Cutover](crystallization-parity-and-cutover.md) (PV)
- [Drift and Lifecycle](crystallization-drift-and-lifecycle.md) (DL)
- [Learning-Loop Coupling](crystallization-learning-loop.md) (LC)
- [Accounting](crystallization-accounting.md) (CA)
- [Cross-Tenant Pooling and Neutral Promotion](crystallization-cross-tenant.md) (XT)

## Hazards the design must keep in view

- **Premature crystallization** — building the wrong abstraction from
  three occurrences; countered by stability forecasts, corpus bars,
  the one-rung ratchet, and deflation discounting.
- **The melting asset** — AI prices fall; a slow-payback build may never
  pay back; token savings are discounted like the depreciating stream
  they are (EC-C2).
- **Correlated failure** — deterministic bugs fail at scale; throttles,
  post-conditions, and instant demotion bound the blast radius (AU-C4).
- **Learning starvation** — a starved learner goes blind to drift;
  sentinels are mandatory, not optional telemetry (LC-C2).
- **Goodharted praise** — money never keys off praise alone; labels are
  multi-source (LC-C5).
- **Automation bias** — humans stop checking what usually works;
  provenance visibility and spot-check consent conditions (AU-Q4) push
  back.
- **The zombie fleet** — unmaintained generated artifacts as security
  surface and debt; disuse retirement and regeneration-first keep the
  fleet pruned (DL-C5).
- **Tenant data in generated code** — memorized constants are leaks;
  the leak-scan gate exists from v1 and hardens for pooled builds
  (BP, XT-C2).

## MVP slice (prove the loop before the machinery)

One domain (codexFactory), one family chosen from real ledger evidence, and
the thinnest honest version of every stage: episodes as a manual projection
over existing audit for that family only; nomination by count threshold;
human decision with an evidence packet; an L3 playbook (no code rungs);
replay parity plus a human-compared shadow week; dispatch as a pre-planner
hook with a hand-written fence; sentinel ε fixed at ~0.2; savings tracked
in a spreadsheet-grade report. Every subsequent proposal then has a live
loop to harden rather than a paper design to defend.

## Naming

`recurrence crystallization` — the phase-change metaphor carries the whole
lifecycle honestly: solve fluidly, crystallize what repeats, melt back when
the world shifts (demotion/retirement), re-crystallize from fresh episodes.
Rejected: *distillation* (collides with the ML term that is only rung L4),
*habitization/proceduralization* (accurate but graceless), *graduation*
(implies one-way motion; melting is a feature).

## Relationship to existing work

| Existing | Relationship |
| --- | --- |
| knowledge lifecycle model (experiential path) | crystallization adds a procedural promotion target beside Root Truth atoms |
| memory gateway (M1 promotion, M3 metering) | promotion port governs consolidation; metering feeds cost vectors |
| cost-accountability brainstorm | efficiency mandate nominates; the accounting chain carries the ledger |
| practice suggestion/clearance/realization pipeline | candidates ride the same suggest→clear→realize rails and autonomy boundary |
| ontology & micro-agent packet (2026-07-28) | owns rung L2 (result cache) and the L4 substrate (micro-agents, semantic context) |
| governed-derived-model | applied twice: capabilities as derived artifacts of episodes; registry hot index as derived projection |
| workflow-gate-contract, release-realization | proof stages are gate instances; builds archive on realization evidence |
| omnigent-domain-overlay, credential-contracts, roles-authority-model | the permission matrix, custody, and signing rails AU extends |
| DTN register (esp. DTN-015) | the promotion vehicle for neutralizing proven capabilities |
| neutral-job-envelope | fingerprint surface; `crystallization_build` as a domain job type |

## Questions that span the packet

- Where exactly does the dispatch junction live (DS-Q1), and what is the
  platform actor in the three-layer vocabulary (XT-Q2)?
- Which decision-ladder rung do we *start* tenants on, and who ratifies
  the guard values (EC-Q1/Q4)?
- Does praise need a schema now, or do gate outcomes and corrections
  suffice as v1 labels (EL-Q5, LC-Q3)?
- Is the L3-playbook-workhorse hypothesis true in our metering data
  (AL-C5) — the single cheapest question to answer before any build?
- Neutral-first or domain-first schemas (CR-Q1) — the DTN pattern says
  prove in codexFactory, then neutralize?

## Promotion posture

Exit path: organize into a staging topic (`recurrence-crystallization`),
then split into ordered OpenSpec changes rather than one monster: (1) the
Pattern Ledger contract family (episode/family/forecast/candidate schemas —
pure sensing, no spend, lowest risk), (2) the Crystallizer decision + build
contracts, (3) the Steward runtime contracts (registry/dispatch/proof/
health), (4) cross-tenant pooling last, after a first domain proof. The
MVP slice can run under (1)+(2) with manual stand-ins for (3). Rung L2
stays with the ontology packet's result-cache proposal; this packet
consumes it as a rung.
