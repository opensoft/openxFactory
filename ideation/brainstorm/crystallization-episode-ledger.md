# Episode Ledger: Outcome-Labeled Solution Traces — Brainstorm

Status: staged
Kind: architecture
Summary: Every governed job solved by the expensive AI path should leave an
episode — a replayable, cost-carrying, outcome-labeled trace derived from
records the runtime already produces (audit, run events, metering, praise) —
because the episode ledger is the single substrate that family mining,
recurrence forecasting, requirements corpora, parity replay, and savings
counterfactuals all consume.
Topics: crystallization, episode-ledger, solution-trace, audit, metering,
memory-gateway, cost-accountability, outcome-labels, replayability,
recurrence
Repository context: openxFactory (neutral episode schema; capture rides the
existing runtime evidence discipline)
Captured: 2026-07-28
Organized: 2026-07-29 into the
[recurrence-crystallization staged topic](../staging/recurrence-crystallization/recurrence-crystallization.md)
(staged); kept as design history.

## Possible feats

- **Neutral `episode` record schema** — envelope snapshot + trace refs + cost
  vector + label stream + replayability class.
- **Episode projection worker** — derives episodes from existing audit/run
  events/metering; no second truth store.
- **Outcome-label event stream** — praise, gate outcomes, and delayed
  corrections as append-only label events folded into episode quality.
- **Replayability classification at capture** — `pure | record-replay |
  live-only`, mirroring the result-cache cacheability classes.

## Position in the packet

First document of the sensing arc. Downstream:
[task families](crystallization-task-families.md) mines episodes into
families, [recurrence forecasting](crystallization-recurrence-forecasting.md)
predicts over them, [requirements mining](crystallization-requirements-mining.md)
curates them into acceptance corpora,
[parity](crystallization-parity-and-cutover.md) replays them, and
[accounting](crystallization-accounting.md) uses their cost vectors as
counterfactuals. Anchor: [overview](crystallization-overview.md).

## What an episode is

One governed job, solved by the expensive path, captured well enough that a
later system can (a) recognize its shape, (b) price what it cost, (c) know
whether the outcome was good, and (d) replay or simulate it. Composition:

- **Envelope snapshot** — the neutral-job-envelope fields (`job_type`,
  `domain`, `subject_ref`, `client_ref`, `workflow_ref`, `gate_ref`,
  `artifact_refs`) plus the domain overlay's stricter fields. This is the
  fingerprinting surface.
- **Plan record** — what the planner decided to do (step graph), distinct
  from what execution did. Plans are the thing L3 playbook crystallization
  freezes, so they must be captured as data, not prose.
- **Step/tool trace** — per step: worker/persona identity, tool calls with
  recorded I/O (digest always; payload retention per redaction and consent
  policy), and intermediate decisions.
- **Cost vector** — rides the clock-in protocol from
  [cost accountability](cost-accountability-and-efficiency-model.md):
  `(action, credits_burned, outcome)` per worker plus wall time, model/effort
  identity, and human touches. Gateway usage metering (memory-gateway M3) is
  the authoritative meter where it applies.
- **Outcome label stream** — append-only events: completion acceptance, gate
  outcomes, the praise/reward the operator grants, and — critically — delayed
  corrections (a reopened task, a reverted artifact, a downstream complaint).
  Episode quality is a fold over this stream, never a single bit set at close.
- **Replayability class** — declared at capture: `pure` (same inputs →
  comparable outputs), `record-replay` (side-effecting, but recorded tool I/O
  supports cassette-style simulation), `live-only` (cannot be meaningfully
  replayed). Deliberately the same spirit as the cacheability classes in
  [result caching](ontology-compiled-context-and-result-caching.md).

## Derived, not duplicated

The runtime already emits audit records, run events, evidence records, and
budget/metering data. The episode ledger should be a **governed derived
projection** over those streams (governed-derived-model discipline: recipe +
sources + digest, regenerate rather than hand-edit), keyed for retrieval by
fingerprint. A second, independently-written truth store would rot against
the audit trail it shadows. The one genuinely new capture obligation is the
**plan record as data** and the **label stream** — praise is currently an
informal act; it needs a record kind.

Capture must be universal and near-free: you cannot know in advance which
tasks will recur, so every governed run gets an episode. Anything expensive
(payload retention, embedding computation) is deferred and policy-dialed.

## Consent and privacy at capture

Episodes are tenant (and sometimes subject) data. Capture stamps each episode
with the consent scope it was collected under — use-for-mining,
use-for-corpus, use-for-pooling are separate flags (tiers defined in
[authority and consent](crystallization-authority-and-consent.md)). The
de-identify gate from the knowledge lifecycle model applies before any
cross-tenant movement. Retention: digests indefinitely (lineage), payloads on
a policy TTL.

## Claims

- **EL-C1** — Every governed run emits an episode at negligible marginal
  cost, as a derived projection over records that already exist; capture is
  universal because recurrence is unknowable at solve time.
- **EL-C2** — Outcome labels are append-only events; episode quality is a
  fold over the stream, so delayed corrections can demote an episode that was
  praised at close.
- **EL-C3** — Replayability class is declared at capture, not inferred later;
  it determines which proof techniques (replay, cassette, shadow-only) a
  family can ever use.
- **EL-C4** — Tool I/O is digested always, retained as payload only under
  redaction/consent policy — payload retention is the expensive dial, and it
  is a policy dial, not an engineering constant.
- **EL-C5** — The ledger is the single substrate for family mining,
  forecasting, requirements corpora, parity replay, and savings
  counterfactuals; none of those may keep private episode copies.

## Open questions

- **EL-Q1** — Episode identity for multi-agent runs: one episode per job with
  per-agent sub-spans, or episodes per agent run with a job rollup? (Leaning
  per-job with sub-spans; the job is the recurrence unit.)
- **EL-Q2** — Do human-in-loop touches enter the cost vector, and at what
  price? Human minutes are usually the dominant real cost and the strongest
  crystallization argument.
- **EL-Q3** — Backfill: can episodes be reconstructed from existing audit
  history to warm-start family mining, or does the ledger start cold?
- **EL-Q4** — Where does the ledger live — gateway-governed store (expert
  case memory port is shaped right) vs. runtime evidence store with gateway
  read mediation?
- **EL-Q5** — Does praise need its own neutral record schema now (it is
  informal today), or is it folded into gate/acceptance outcomes until the
  reward loop matures?

## Related

- [Cost Accountability & Efficiency](cost-accountability-and-efficiency-model.md)
  — the clock-in cost vector and audit-selection ancestor.
- [Ontology-Compiled Context and Result Caching](ontology-compiled-context-and-result-caching.md)
  — sibling classes for reuse safety.
- `docs/knowledge-lifecycle-model.md` — experiential knowledge states this
  ledger feeds.
- `openspec/specs/memory-gateway/spec.md` — metering (M3) and promotion (M1)
  ports.
