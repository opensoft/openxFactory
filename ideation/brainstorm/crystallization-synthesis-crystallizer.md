# Synthesis: The Crystallizer — Decide, Specify, Build — Brainstorm

Status: staged
Kind: architecture
Summary: The invest/build arc composes five atomic pieces — economics,
the automation ladder, requirements mining, the build pipeline, and
authority/consent — into the Crystallizer: the subsystem that takes a
crystallization candidate and returns either a registered, proof-obligated
capability or a recorded "not yet" with honest numbers, braiding the three
Hermes layers' approvals (Domain fitness, Tenant money and policy, Subject
transparency) around a build that is itself an ordinary governed
codexFactory job, so the factory recursively manufactures its own
shortcuts without ever widening authority or spending unconsented money.
Topics: crystallization, crystallizer, economics, automation-ladder,
requirements-mining, build-pipeline, authority-conservation, codexfactory,
synthesis
Repository context: openxFactory (the invest/build-arc contract family as
one subsystem)
Captured: 2026-07-28
Organized: 2026-07-29 into the
[recurrence-crystallization staged topic](../staging/recurrence-crystallization/recurrence-crystallization.md)
(staged); kept as design history.

## Possible feats

- **Crystallizer subsystem contract** — candidate in → decision record →
  micro-spec + corpus + fence → governed build → registered capability out,
  with the approval braid declared.
- **Decision-to-build handoff record** — one artifact carrying rung, budget
  cap, abort rule, and proof obligations from EC into RQ/BP.
- **Not-yet ledger** — declined/deferred candidates kept with reasons and
  re-nomination conditions (evidence for future priors).

## Members and their joints

Atomic members: [economics](crystallization-economics.md) (EC),
[automation ladder](crystallization-automation-ladder.md) (AL),
[requirements mining](crystallization-requirements-mining.md) (RQ),
[build pipeline](crystallization-build-pipeline.md) (BP),
[authority and consent](crystallization-authority-and-consent.md) (AU).

```text
crystallization_candidate (from the Pattern Ledger)
        │
        ▼
   DECIDE (EC on AL's menu, inside AU's ceilings)
     rung? budget cap? abort rule? proof obligations?
     ├── not yet → not-yet ledger (reasons, re-nomination conditions)
     └── fund ──► approval braid:
                    Domain Hermes    fitness to exist (spec gate ahead)
                    Tenant Hermes    budget + T1/T2 consent + clearance
                    Subject layer    transparency obligations set
        │
        ▼
   SPECIFY (RQ)
     mine corpus → invariants, parameters, branches, counterexamples
     author micro-spec + acceptance corpus + scope fence
     ratification scaled to rung and risk
        │
        ▼
   BUILD (BP — an ordinary governed codexFactory job)
     design → implement → corpus green → security + leak scan →
     authority binding (AU: ⊆ replaced config) → dry-run proven
        │
        ▼
   registered capability (status: shadow) + proof obligations
        → the Capability Steward (run/renew arc)
```

The joints:

- **The decision buys a shape (EC-C4 × AL).** Rung selection is the hinge
  between arcs: it sets RQ's corpus-size bar (RQ-Q1), BP's artifact kind
  (playbook vs. program), PV's proof rigor, and AU's throttle schedule.
  One field, five consumers — which is why `automation_rung` must be a
  controlled vocabulary (AL-C2), not prose.
- **Ceilings precede economics (AU-C5 → EC).** A candidate whose family
  ceiling caps at L3 must be valued at L3 — checking the ceiling after
  computing L6 ROI produces persistent phantom value in the queue.
- **The fence is the safety half of the spec (RQ-C3).** The Crystallizer's
  real product is not code — it is *code plus the predicate that says when
  the code may speak*. Everything the Steward does safely downstream
  (dispatch, canary, drift retreat) leans on the fence existing as a
  first-class, reviewed artifact.
- **Recursion with a floor (BP-C1).** The build is factory work like any
  other — same lanes, gates, evidence — and builds are themselves episodes,
  so the Crystallizer's own recurring work is subject to crystallization.
  The floor: authority conservation (AU-C1) is constitutional at every
  level of the recursion, so self-application can compound efficiency but
  never privilege.

## The braid, stated once

Domain decides **whether it should exist** (fitness, spec, ceiling); Tenant
decides **whether to pay and permit** (budget envelope, T1/T2, clearance);
Subject **sees** (provenance, and consents where the work touches them).
No single layer can push a capability into authority alone — the braid is
the packet's governance thesis in one sentence.

## Tensions to hold

- **Machine-authored specs vs. governance rigor** — micro-specs arrive at
  a volume humans won't deep-review; scaled ratification (auto below a
  risk line, human above) is the only workable posture, and where that
  line sits is a policy fight to have explicitly (RQ, AU-Q4).
- **Estimate uncertainty vs. decision confidence** — build costs are
  AI-estimated and initially poorly calibrated; the abort rule (EC-C4) is
  what makes acting on bad estimates survivable, and the not-yet ledger
  keeps declined candidates as calibration data too.
- **Premature crystallization** — the classic failure is building the
  wrong abstraction from the first three occurrences. Counterweights
  already in the design: stability forecasts (RF-C4), corpus-size bars by
  rung (RQ-Q1), the one-rung ratchet (AL-C4), and the melting-asset
  discount (EC-C2) that quietly punishes speculative heavy builds.

## Claims rollup (details in the atomic docs)

EC-C1..C5 (decision ladder, deflation + survival discounting, non-token
value, shape-not-boolean, budget-as-consent) · AL-C1..C5 (spectrum, rung
vocabulary, ceilings, ratchet, playbook workhorse) · RQ-C1..C5
(episode-cited specs, corpus-as-contract, fence-as-requirement,
regenerable specs, mandatory counterexamples) · BP-C1..C5 (ordinary
governed job, cross-domain service, provenance chain, regeneration-first,
dry-run criterion) · AU-C1..C5 (conservation, consent tiers, audit-shape
parity, throttles, overlay ceilings). Synthesis-level additions:

- **SYB-C1** — The Crystallizer's output is binary and honest: a
  registered, proof-obligated capability, or a not-yet record with reasons
  and re-nomination conditions — never a quiet drop.
- **SYB-C2** — Ceilings are resolved before valuation, value is computed per
  eligible rung, and only then is a rung selected; the queue never carries
  phantom ROI.
- **SYB-C3** — The approval braid is three-layer by construction; no layer
  can be collapsed into another without breaking the consent story.

## Open questions

- **SYB-Q1** — Where does the not-yet ledger live — the family register
  (TF) as a state, or the decision-record store?
- **SYB-Q2** — Can a tenant *request* crystallization (pull, not
  suggestion) — "we do this weekly, automate it" — entering the same
  braid from the tenant side?
- **SYB-Q3** — The Crystallizer's own first crystallization: which of its
  stages (corpus running? leak scanning?) hardens first, and does
  self-application get special review?

## Related

- [Synthesis: The Pattern Ledger](crystallization-synthesis-pattern-ledger.md)
  — the candidate source.
- [Synthesis: The Capability Steward](crystallization-synthesis-steward.md)
  — where proof obligations are discharged.
- [Overview](crystallization-overview.md) — the full flywheel.
