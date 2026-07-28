# Capability Drift, Renewal, and Retirement — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Drift is the expected operating condition of a crystallized
capability, arriving in four classes (input, world, requirement, dependency)
detected by signals the system already emits (fallback trends,
post-condition breaches, sentinel disagreement, delayed corrections,
dependency advisories) and answered by a cost-ordered response ladder with
hysteresis — observe → shrink fence → regenerate from a refreshed corpus →
demote rung → retire — under a standing capability-health surface
(doc-health's operational sibling) that also retires disused capabilities
proactively while preserving lineage forever.
Topics: crystallization, drift, capability-health, regeneration, demotion,
retirement, doc-health, fence, sentinel, lifecycle
Repository context: openxFactory (neutral drift-signal and health-report
schemas; thresholds are domain/tenant policy)
Captured: 2026-07-28

## Possible feats

- **Drift-signal taxonomy** — the four classes with their source signals,
  as a controlled vocabulary on health events.
- **Capability-health surface** — standing per-capability scorecard +
  portfolio report, with auto-fixable vs. contested finding classes like
  doc-health.
- **Regeneration lane** — corpus refresh → re-mine → rebuild → re-prove as
  one governed, mostly-automatic sequence.
- **Disuse auto-retirement** — dormant capabilities proposed for retirement
  on a policy clock, lineage preserved.

## Position in the packet

Third document of the run/renew arc: consumes signals from
[dispatch](crystallization-dispatch-and-fences.md) (fence misses,
post-condition breaches), the
[learning loop](crystallization-learning-loop.md) (sentinel disagreement),
and the [episode ledger](crystallization-episode-ledger.md) (delayed
corrections); its responses re-enter the
[build pipeline](crystallization-build-pipeline.md) (regeneration) and
update the [registry](crystallization-capability-registry.md).

## Four drift classes

- **Input drift** — traffic moves outside the fence: fence-miss and
  fallback rates trend up. The capability is still right; the world asks
  different questions. Cheapest to answer (fence revision or corpus
  refresh).
- **World drift** — external systems change behavior: post-condition
  breaches, cassette mismatches on re-record, tool errors. The capability
  is now wrong about the world.
- **Requirement drift** — what "good" means moved: sentinel adjudications
  start favoring the AI path, praise patterns shift, downstream corrections
  rise on outputs that pass post-conditions. The subtlest class — the
  capability is right by the old spec and wrong by the living standard.
- **Dependency drift** — toolchain/API deprecations and advisories. Arrives
  on a calendar, not a metric; the only class detectable before it bites.

## The response ladder (cost-ordered, with hysteresis)

```text
observe        annotate health, tighten sentinel rate (ε up), wait
shrink fence   retreat to the sub-region still proven; misses fall back
               to AI — capacity degrades gracefully, correctness doesn't
regenerate     refresh corpus (recent episodes in, stale out) → re-mine →
               rebuild → re-prove; cheap BECAUSE the pipeline is the asset
               (BP-C4); this is the default repair
demote rung    L5 → L3, or any rung → AI; routine operation (AL-C4)
retire (melt)  family returns fully to the AI path; registry entry
               archived with full lineage, never deleted
```

Hysteresis matters: thresholds for stepping down must be tighter than for
stepping back up, or a borderline capability flaps between rungs and burns
its proof budget on oscillation.

## Capability-health: doc-health's sibling

Same instincts, operational target: a standing checker producing findings
in two classes — **auto-actionable** (fence shrink within policy, sentinel
rate bump, regeneration under budget) and **contested** (demotion,
retirement, anything spending real money), which need a cited decision or a
disposition, exactly like doc-health's contested findings. The portfolio
view rolls up: savings run-rate per capability, drift posture, proof
freshness, disuse.

**Zombie control:** a capability whose family stopped recurring is pure
liability — registry bloat, security surface, maintenance obligation.
Dormancy beyond a policy window auto-proposes retirement. Retirement
archives; lineage and evidence persist (audit continuity outlives
authority).

## Claims

- **DL-C1** — Drift is the expected operating condition, priced into the
  build decision (EC's maintain term) — never an incident category alone.
- **DL-C2** — Responses form a cost-ordered ladder with hysteresis;
  the cheapest adequate response wins, and flapping is a defect of the
  thresholds, not the capability.
- **DL-C3** — Regeneration is the default repair; the pipeline, not the
  artifact, is the durable asset.
- **DL-C4** — Capability-health is a standing governed surface with
  auto-actionable vs. contested finding classes, mirroring doc-health.
- **DL-C5** — Disused capabilities are proposed for retirement on a policy
  clock; retirement preserves lineage forever.

## Open questions

- **DL-Q1** — Signal thresholds and windows per class — neutral defaults
  with domain overlay tightening?
- **DL-Q2** — Which responses are auto vs. approval-gated, by rung and
  authority class?
- **DL-Q3** — World-drift cassette policy: scheduled re-record of recorded
  tool I/O (freshness), or re-record only on mismatch evidence?
- **DL-Q4** — Requirement drift detection needs sentinel adjudication at a
  meaningful rate — is there a cheaper leading indicator?
- **DL-Q5** — Portfolio review cadence and owner (domain efficiency mandate
  vs. tenant accounting bench — likely both, different questions)?

## Related

- [Dispatch and Fences](crystallization-dispatch-and-fences.md) — signal
  source.
- [Build Pipeline](crystallization-build-pipeline.md) — the regeneration
  lane.
- [Learning Loop](crystallization-learning-loop.md) — sentinel machinery
  and ε policy.
