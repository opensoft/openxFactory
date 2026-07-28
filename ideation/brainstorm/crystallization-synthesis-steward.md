# Synthesis: The Capability Steward — Run, Watch, Renew — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The run/renew arc composes seven atomic pieces — registry,
dispatch, parity, drift/lifecycle, learning-loop coupling, accounting, and
cross-tenant pooling — into the Capability Steward: the operating plane
that routes each arriving instance to the cheapest proven rung behind a
deterministic fence with the AI path always intact, discharges proof
obligations (replay → shadow → canary), keeps a sentinel fraction of
traffic on the AI path so drift detection, corpus freshness, and savings
counterfactuals stay honest, answers drift with the cheapest adequate
response, and closes the flywheel by writing every fallback, disagreement,
and scored prediction back into the Pattern Ledger.
Topics: crystallization, steward, dispatch, parity, drift, sentinel,
capability-registry, accounting, cross-tenant, synthesis
Repository context: openxFactory (the run/renew-arc contract family as one
subsystem)
Captured: 2026-07-28

## Possible feats

- **Capability Steward subsystem contract** — registry-driven dispatch,
  proof discharge, sentinel regime, drift response, and accounting as one
  declared operating plane.
- **Renewal loop contract** — the named write-backs from operations into
  the Pattern Ledger (fallback episodes, sentinel episodes, adjudications,
  scored predictions).
- **Steward role definition** — who answers the pager: the operating
  persona/lane that owns health responses within policy (BP-Q3's answer).

## Members and their joints

Atomic members: [registry](crystallization-capability-registry.md) (CR),
[dispatch](crystallization-dispatch-and-fences.md) (DS),
[parity](crystallization-parity-and-cutover.md) (PV),
[drift and lifecycle](crystallization-drift-and-lifecycle.md) (DL),
[learning loop](crystallization-learning-loop.md) (LC),
[accounting](crystallization-accounting.md) (CA),
[cross-tenant](crystallization-cross-tenant.md) (XT).

```text
            registry (CR) — the one source dispatch may read
                │ digest-pinned, derived hot index
                ▼
arriving   ► DISPATCH (DS): fingerprint → fence → rung → post-conditions
instances       │                      │
                │ served               │ any miss/breach/risk-override
                ▼                      ▼
          crystallized path        AI path (unchanged; always intact)
                │                      │
                │◄── sentinel ε (LC) ──┤   fresh episodes, drift votes,
                │                      │   live counterfactuals
                ▼                      ▼
          PROOF & WATCH: replay/shadow/canary gates (PV);
          drift signals → cheapest adequate response (DL):
          observe → shrink fence → regenerate → demote → retire
                │
                ▼
          ACCOUNT (CA): savings vs. sentinel counterfactual;
          score every stored prediction; portfolio + automation share
                │
                ▼
          RENEWAL LOOP: fallbacks, adjudications, scores, pooled
          statistics (XT) → written back to the Pattern Ledger
```

The joints:

- **One registry, one junction (CR-C2 × DS-C1).** Safety composes only
  because there is exactly one place authority is looked up and exactly one
  place it is exercised. Every bypass proposal downstream ("just call the
  script") is this subsystem's recurring governance fight; the contract
  should name it a conformance violation now.
- **The AI path is infrastructure, not legacy (DS × DL × PV).** Fallback,
  demotion, sentinels, and adjudication all assume the expensive path
  stays warm. The steady state is a *blend* — never "the AI is gone" —
  and the blend ratio is the automation-share metric (CA-C3).
- **Sentinels are the keystone (LC-C2/C3).** Remove them and three members
  fail quietly at once: drift detection loses its requirement-drift sense
  (DL), accounting loses honest counterfactuals (CA-C1), regeneration
  loses fresh corpora (BP via DL-C3). ε is the single most load-bearing
  policy number in the packet.
- **Renewal closes the flywheel.** The Steward's exhaust is the Pattern
  Ledger's intake: fallback causes retrain the matcher (TF-C5), scored
  forecasts update priors (RF-C5 via CA-C2), frontier queues seed the next
  decision (LC-C5). Operating the system *is* the learning program.

## Tensions to hold

- **Sentinel spend vs. staleness** — every sentinel is deliberately paying
  the old price; every skipped sentinel rots the counterfactual and the
  drift sense. The ε schedule (LC-Q1) is where economics and epistemics
  bargain; it should be a scored policy, not a constant.
- **Auto vs. approved responses** — fence shrinks and regenerations under
  budget want to be automatic (drift waits for no one); demotions and
  retirements spend trust and want approval. The auto/contested split
  (DL-C4, doc-health's pattern) is the compromise — but the line will
  move with confidence, and the contract should expect re-drawing.
- **Hot path vs. governance** — dispatch runs per job; the registry is
  reviewed YAML. The derived-index answer (CR-C1) resolves it, at the cost
  of one more regeneration lane to operate — governed-derived-model
  earning its keep a third time.
- **Per-tenant truth vs. pooled leverage (XT)** — the Steward operates
  tenant-scoped capabilities and platform capabilities with per-tenant
  fences; health and accounting must roll up both without letting pooled
  aggregates leak tenant specifics (XT-C1's operational echo).

## Claims rollup (details in the atomic docs)

CR-C1..C5 (governed registry, sole-source dispatch, digests-not-payloads,
lifecycle-mirrored spine, pinned consumption) · DS-C1..C5 (junction before
planning, deterministic fences, post-conditions always, cause-tagged
fallbacks, budgeted overhead) · PV-C1..C5 (three proofs, predicate
equivalence, bidirectional adjudication, demotion-with-promotion, budgeted
shadow) · DL-C1..C5 (drift as operating condition, cost-ordered ladder,
regeneration-first, capability-health, disuse retirement) · LC-C1..C5
(consolidation framing, mandatory sentinels, declared exploration spend,
two-level credit, frontier priority) · CA-C1..C5 (sentinel-anchored
counterfactuals, scored predictions, automation share, normalization,
riding the accountability chain) · XT-C1..C5 (statistics-first pooling,
hardened leak scans, platform capabilities as product, DTN promotion,
demand-derived roadmap). Synthesis-level additions:

- **SYC-C1** — The steady state is a governed blend of rungs with the AI
  path as permanent infrastructure; "fully automated" is not a state this
  system has.
- **SYC-C2** — The Steward's exhaust is contractually the Pattern Ledger's
  intake; a deployment without the renewal write-backs is nonconformant,
  not merely incomplete.
- **SYC-C3** — ε (the sentinel rate) is a first-class, scored policy object
  with an owner — the packet's most load-bearing number.

## Open questions

- **SYC-Q1** — Is the Steward a role (persona/lane with a pager), a
  contract implemented by existing runtime components, or both — and per
  domain or per install?
- **SYC-Q2** — Ordering of first proofs: does the MVP discharge shadow
  parity manually (human compares) before any orchestration exists?
- **SYC-Q3** — What does the Steward surface to the ideation dashboard /
  gate console family — is capability-health a new panel on existing
  surfaces rather than a new UI?

## Related

- [Synthesis: The Pattern Ledger](crystallization-synthesis-pattern-ledger.md)
  — intake of the renewal loop.
- [Synthesis: The Crystallizer](crystallization-synthesis-crystallizer.md)
  — source of proof obligations.
- [Overview](crystallization-overview.md) — the full flywheel.
