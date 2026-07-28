# Dispatch, Scope Fences, and Fallback — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Crystallized capabilities are reached through exactly one junction —
at job admission, before any planner runs: fingerprint → registry lookup →
deterministic fence check → execute at the capability's rung →
post-condition validation — with every ambiguity, fence miss, execution
failure, or post-condition breach falling back to the intact AI path as a
recorded, cause-tagged episode; fallbacks are the frontier signal that
drives fence expansion, and the dispatch decision itself is cost-budgeted so
deciding never rivals solving.
Topics: crystallization, dispatch, scope-fence, fallback, routing,
post-conditions, neutral-job-envelope, capability-registry, audit-continuity
Repository context: openxFactory (dispatch contract at the xFactory routing
layer; fences authored per capability)
Captured: 2026-07-28

## Possible feats

- **Dispatch junction contract** — the admission-time match/fence/execute/
  validate sequence with audit-shape parity across paths.
- **Fallback episode tagging** — cause taxonomy (`no-family-match`,
  `fence-miss`, `execution-error`, `postcondition-fail`, `risk-override`,
  `sentinel`) recorded on every AI-path fallback.
- **Frontier queue** — fence-adjacent fallbacks accumulated per family as
  fence-expansion and re-crystallization evidence.
- **Dispatch overhead metering** — the decision cost as a first-class
  metric with a declared budget.

## Position in the packet

First operational document of the run/renew arc: reads the
[registry](crystallization-capability-registry.md), enforces fences authored
by [requirements mining](crystallization-requirements-mining.md), applies
the match precision of [task families](crystallization-task-families.md),
and generates the fallback/sentinel episodes that feed
[drift](crystallization-drift-and-lifecycle.md) and the
[learning loop](crystallization-learning-loop.md).

## The junction

Placement matters: **at job admission, before planning** — the whole point
is to skip the planner when a cheaper path exists.

```text
envelope arrives
  → fingerprint (TF matcher; cheap features first)
  → registry lookup: any active capability claiming this family?
  → fence check: deterministic predicate over envelope + inputs
  → risk check: instance-level overrides (stakes, subject flags)
  → execute at the capability's rung
  → post-conditions: the spec's invariants, checked on the output
  → emit with provenance: "served by <capability>@<version> (rung Ln)"
any step fails or abstains
  → AI path (unchanged from today), episode tagged with fallback cause
```

Design properties:

- **One junction, no side doors.** A capability reachable outside dispatch
  breaks audit continuity, fence enforcement, and accounting in one stroke.
  The registry is dispatch's only source (CR-C2).
- **Fences are deterministic.** The gray zone belongs to the AI path, not to
  a clever classifier. A small in-scope classifier MAY pre-screen *toward*
  fallback (cheap veto) but never *toward* execution beyond the fence.
- **Post-conditions always run.** The capability's output only counts as
  done after the spec's invariants pass; a breach falls back to AI **and**
  files a drift signal. This is the "never silently wrong" backstop at the
  instance level.
- **Precedence is conservative.** Multiple claimants: most specific fence
  wins; overlap or tie → AI path. Fragment capabilities compose inside
  playbooks rather than competing at the top level.

## Fallbacks are the frontier

Every fallback is a labeled, high-information episode: `fence-miss` events
that the AI then solved successfully are exactly the evidence that widens
the fence next revision; `postcondition-fail` events are drift or spec-gap
evidence; clusters of `no-family-match` near an existing family are matcher
training data (TF-C5). The frontier queue per family is the standing
answer to "what should this capability learn to handle next?"

## The dispatch decision must stay cheap

Fingerprint + lookup + fence must cost a negligible fraction of a solve —
budget it explicitly (structural features and digest lookups; embeddings
only when cheap features are inconclusive, and then preferably async for
mining rather than inline for dispatch). If deciding starts to rival
solving for thin tasks, the junction is broken; metering watches this.

## Claims

- **DS-C1** — Dispatch precedes planning and is the single entry to every
  crystallized capability; side-door invocation is a conformance violation.
- **DS-C2** — Fences are deterministic predicates; ambiguity resolves to the
  AI path; no classifier may extend execution beyond the fence.
- **DS-C3** — Post-conditions from the spec run on every crystallized
  output before it counts as done; breaches fall back AND file drift
  signals.
- **DS-C4** — Every fallback is recorded with a cause from a controlled
  taxonomy and accumulates in the family's frontier queue.
- **DS-C5** — Dispatch overhead carries a declared budget and is metered;
  the junction's own cost is part of the economics.

## Open questions

- **DS-Q1** — Physical placement: hermes-install runtime (admission) vs.
  omnigent-install (execution edge) — or a contract both implement?
- **DS-Q2** — Does the envelope grow an optional `family_hint` so repeat
  submitters can pre-key dispatch (with the fence still authoritative)?
- **DS-Q3** — Interactive/synchronous jobs: how much dispatch latency is
  acceptable before the junction must answer (fence-only fast path)?
- **DS-Q4** — Instance risk overrides: which signals (subject-affecting,
  spend above X, novel parameter values) force the AI path or a lower rung
  even inside the fence?
- **DS-Q5** — Is the emitted provenance line subject-visible by default
  (transparency), or tenant-policy-controlled?

## Related

- [Capability Registry](crystallization-capability-registry.md) — the lookup
  source of truth.
- [Task Families](crystallization-task-families.md) — the matcher and its
  feedback loop.
- [Drift and Lifecycle](crystallization-drift-and-lifecycle.md) — consumer
  of fence-miss and post-condition signals.
