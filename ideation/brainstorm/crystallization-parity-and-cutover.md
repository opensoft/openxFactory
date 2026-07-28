# Parity Proof and Staged Cutover — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A crystallized capability earns authority through three ordered
proofs — replay parity against the acceptance corpus, shadow parity
dry-running beside live AI solves, and a canary cutover with sentinel
sampling thereafter — each a workflow-gate-contract instance; equivalence is
judged by declared predicates (AI-judged where semantic, since judging is
far cheaper than solving), disagreements are adjudicated evidence that can
correct either side (sometimes the code is right and the old AI answer was
sloppy), and no capability goes authoritative without its demotion triggers
already wired.
Topics: crystallization, parity, shadow-run, canary, cutover, equivalence,
adjudication, workflow-gate-contract, dry-run, demotion
Repository context: openxFactory (neutral proof-stage vocabulary and gate
profiles)
Captured: 2026-07-28

## Possible feats

- **Proof-stage vocabulary** — `replay | shadow | canary` as controlled
  registry statuses with per-rung gate profiles.
- **Equivalence adjudication record** — disagreement + adjudicator + verdict
  + corpus/spec consequence, bidirectional by design.
- **Shadow orchestration** — dry-run the capability beside the authoritative
  AI solve, compare, never touch the world twice.
- **Demotion trigger bundle** — auto-demote conditions shipped as part of
  promotion, not added after incidents.

## Position in the packet

Second document of the run/renew arc: receives built capabilities from the
[build pipeline](crystallization-build-pipeline.md), replays the
[acceptance corpus](crystallization-requirements-mining.md), runs shadows
through [dispatch](crystallization-dispatch-and-fences.md) plumbing, and
hands demotion triggers to
[drift and lifecycle](crystallization-drift-and-lifecycle.md).

## Three proofs, in order

```text
1. replay parity   pre-deploy, cheap, repeatable
     run the acceptance corpus (cassettes for side effects); every
     equivalence predicate green; counterexamples correctly refused
2. shadow parity   live traffic, bounded window
     instances still solved authoritatively by AI; the capability
     DRY-RUNS beside them (BP-C5 makes this possible); outputs compared;
     N instances or M days, whichever is later; doubles marginal cost
     briefly — a declared line in the build budget (EC)
3. canary cutover  authority transfers gradually
     capability authoritative on a rising fraction; AI path continues on
     the remainder and, after full cutover, on the sentinel sample (LC);
     auto-demote on trigger, human review on repeated demote
```

Rung scales rigor: an L3 playbook might need replay + a short shadow; L5/L6
code earns longer shadows and slower canaries. `live-only` families (no
cassettes) lean almost entirely on shadow — one reason their practical
ceiling is lower (RQ).

## Equivalence and adjudication

Predicates come from the spec (RQ-C2): structured outputs compare
mechanically; semantic outputs may be AI-judged — the judge is a bounded
micro-agent seeing two artifacts and a rubric, orders of magnitude cheaper
than the solve itself, so "AI checks the code that replaced AI" is
economically sound, not ironic.

Disagreements are **adjudicated, not auto-scored against the capability**:

- capability wrong → counterexample enters the corpus; build revises;
- AI wrong → the old episode gets a correcting label (EL-C2) — the corpus
  quietly improves, and this will happen more than expected: crystallized
  determinism exposes the sloppiness of some praised historical solves;
- both defensible → the equivalence predicate was too strict or the spec
  under-determined; the SPEC revises.

Every adjudication is recorded evidence; adjudicator identity (human, Lead
persona, judge panel) scales with rung and risk.

## Demotion ships with promotion

No capability becomes authoritative without its exit wired: the demotion
trigger bundle (post-condition breach rate over threshold, sentinel
disagreement rate, fence-miss surge, dependency advisory) is part of the
promotion gate's evidence. Demotion is cheap by construction — the AI path
never left — so triggers should be aggressive early and relax with tenure.

## Claims

- **PV-C1** — Three ordered proofs (replay → shadow → canary), each a
  workflow-gate-contract instance with rung-scaled gate profiles.
- **PV-C2** — Equivalence is declared predicates: mechanical where
  structured, AI-judged where semantic; judge cost ≪ solve cost keeps this
  honest.
- **PV-C3** — Disagreements are bidirectional adjudicated evidence — they
  can correct the capability, the historical episode, or the spec.
- **PV-C4** — Demotion triggers are shipped and armed at promotion time;
  authority without a wired exit is a gate failure.
- **PV-C5** — Shadow cost is a declared build-budget line item, bounded by
  N instances / M days, never open-ended.

## Open questions

- **PV-Q1** — Statistical standard for shadow windows: fixed N, or
  sequential tests that stop early on strong evidence?
- **PV-Q2** — Adjudicator assignment by rung/risk: where exactly does human
  adjudication become mandatory?
- **PV-Q3** — Long-horizon jobs (multi-day workflows): shadow whole jobs, or
  shadow per-step against playbook stages?
- **PV-Q4** — May replay evidence alone promote low-risk L3 playbooks
  (skipping shadow) to keep small wins cheap?
- **PV-Q5** — Canary schedule ownership: neutral default curve with domain
  overlay overrides?

## Related

- [Requirements Mining](crystallization-requirements-mining.md) — predicates
  and corpus.
- [Build Pipeline](crystallization-build-pipeline.md) — dry-run capability
  and budget.
- [Learning Loop](crystallization-learning-loop.md) — sentinel sampling
  after full cutover.
