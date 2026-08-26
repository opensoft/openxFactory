# Coupling Crystallization to the Self-Learning Loop — Brainstorm

Status: staged
Kind: architecture
Summary: Crystallization is the missing consolidation stage of the existing
Hermes self-learning system — episodic memory (episodes) → semantic memory
(families, forecasts) → procedural memory (capabilities) — but absorbing a
family's traffic starves the learner and blinds drift detection, so
sentinel sampling (an adaptive ε of instances still solved by AI, floor
above zero) is mandatory while a capability holds authority, serving triple
duty as drift detector, fresh-corpus source, and honest counterfactual for
savings; credit assignment becomes two-level — episodes train solving,
scored outcomes train investing — and praise stays one label among several
so the reward signal cannot be gamed into the build trigger.
Topics: crystallization, self-learning, memory-consolidation,
sentinel-sampling, exploration, credit-assignment, praise, reward,
knowledge-lifecycle, memory-gateway
Repository context: openxFactory (extends the knowledge lifecycle's
experiential path with a procedural promotion target)
Captured: 2026-07-28
Organized: 2026-07-29 into the
[recurrence-crystallization staged topic](../staging/recurrence-crystallization/recurrence-crystallization.md)
(staged); kept as design history.

## Possible feats

- **Procedural promotion target** — the knowledge lifecycle's promotion
  gate gains a second artifact kind: executable capability, not only Root
  Truth atom.
- **Sentinel sampling policy** — adaptive ε per capability with a nonzero
  floor, cost-accounted as declared exploration spend.
- **Two-level credit assignment** — outcome labels credit capability health
  AND back-propagate to the crystallization decision that created it.
- **Multi-source label rule** — praise, gate outcomes, corrections, and
  adjudications jointly define episode quality; no single signal triggers
  builds.

## Position in the packet

Fourth document of the run/renew arc, and the packet's bridge to what
already exists: it extends the experiential path of
`docs/knowledge-lifecycle-model.md`, consumes
[dispatch](crystallization-dispatch-and-fences.md) fallbacks, feeds
[drift](crystallization-drift-and-lifecycle.md) and
[accounting](crystallization-accounting.md), and gives
[forecasting](crystallization-recurrence-forecasting.md) and
[economics](crystallization-economics.md) their meta-learning signal.

## Consolidation: the memory framing

The knowledge lifecycle already moves experiential patterns from Tenant
memory through de-identify and promotion gates into Root Truth — usage
becomes **knowledge**. Crystallization adds the second consolidation
target biology uses: usage becomes **procedure**. Episodic → semantic →
procedural; System 2 rehearses, System 1 takes over. This framing earns its
keep in one design consequence: consolidation is a *promotion through
gates*, not a separate learning system — the same memory-gateway promotion
port (M1: promotions are explicit and reviewed) governs it, with a new
artifact kind on the far side.

## Learning starvation, and sentinels

Cut over a family to code and the self-learner never sees that work again:
frozen competence, stale counterfactuals, drift invisible until an
incident. The fix is deliberate exploration:

- **Sentinel sampling** — ε of the family's instances are still solved by
  the AI path (or dual-run beside the capability). Adaptive ε: high at
  cutover, decaying with agreement, **rising** on drift suspicion, floored
  above zero for as long as the capability holds authority.
- **Triple duty** — sentinels detect drift (disagreement), refresh the
  corpus (fresh episodes for regeneration), and anchor the savings
  counterfactual (what the AI path *actually* costs now — see CA-C1).
  One ε buys all three; that efficiency is the argument for sentinels over
  three separate mechanisms.
- **Cost honesty** — sentinel spend is declared exploration expense in the
  economics (EC), not overhead hidden in savings claims.

Cheap variants matter: async replay sentinels (AI re-solves yesterday's
instance offline) cost less than live dual-runs and suffice for slow-drift
families; takeover sentinels (AI authoritative on the sample) preserve
end-to-end reality best. Which mode per family is policy.

## Two-level credit assignment

Today praise labels a solve. After crystallization the same signals split:

- **Solve level (exists)** — labels on episodes keep training how work is
  done: corpora, matcher, playbooks.
- **Invest level (new)** — realized outcomes (actual recurrence vs.
  forecast, actual build cost vs. estimate, actual lifespan vs. half-life,
  realized vs. promised savings) credit or debit **the decision that
  crystallized** — training the nominator, the forecaster, and the
  threshold policy themselves. The factory learns to invest, not just to
  solve.

Goodhart guard: praise is one label in a stream (EL-C2) alongside gate
outcomes, corrections, and adjudications. Nothing that spends money keys
off praise alone — otherwise the loop learns to farm praise-shaped work.

## Claims

- **LC-C1** — Crystallization is the consolidation stage of the existing
  self-learning system: a new promotion target through the existing
  gateway promotion port, not a rival learning mechanism.
- **LC-C2** — Sentinel sampling is mandatory while a capability holds
  authority: adaptive ε with a nonzero floor, mode (dual-run / async
  replay / takeover) chosen per family.
- **LC-C3** — Sentinel spend is declared exploration expense; its triple
  duty (drift, corpus, counterfactual) is the efficiency argument that
  justifies it.
- **LC-C4** — Credit assignment is two-level: episodes train solving;
  scored decision outcomes train investing.
- **LC-C5** — Fallback and sentinel-disagreement episodes go to the front
  of the learning queue; they are the frontier where the next fence
  expansion and the next regeneration come from.

## Open questions

- **LC-Q1** — ε defaults by rung and risk class, and the decay/rise
  schedule — neutral table or wholly policy?
- **LC-Q2** — Where does invest-level learning state live — Domain Hermes
  policy memory via the gateway, so it is itself governed and auditable?
- **LC-Q3** — Does praise need schema and vocabulary now (currently
  informal), or do gate outcomes + corrections suffice as v1 labels?
- **LC-Q4** — Async replay sentinels compare against a world that already
  moved (the instance was served hours ago) — how much staleness before
  replay sentinels stop counting as drift evidence?
- **LC-Q5** — Should sentinel disagreement adjudication reuse the parity
  adjudication record (PV-C3) verbatim? (Leaning yes — one record kind,
  two contexts.)

## Related

- `docs/knowledge-lifecycle-model.md` — the lifecycle this extends.
- [Parity and Cutover](crystallization-parity-and-cutover.md) —
  adjudication machinery shared with sentinels.
- [Crystallization Accounting](crystallization-accounting.md) — consumer of
  sentinel counterfactuals and producer of decision scores.
