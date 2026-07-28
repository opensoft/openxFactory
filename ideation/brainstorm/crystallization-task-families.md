# Task Fingerprints and Recurrence Families — Brainstorm

Status: brainstorm
Kind: architecture
Summary: "The same task, again" needs a two-tier identity — a task family
(the recurring, crystallizable pattern) and a task instance (one occurrence
with parameters) — recognized by a hybrid fingerprint (semantic retrieval for
recall, structural match for precision), maintained as living register
entries that merge and split with provenance, and mined at sub-task
granularity because the best crystallization unit is often a step fragment
shared across many different jobs.
Topics: crystallization, task-fingerprint, recurrence-family, similarity,
clustering, episode-ledger, ontology, semantic-context, micro-agents,
dispatch
Repository context: openxFactory (neutral fingerprint/family schema; per-domain
canonicalization in overlays)
Captured: 2026-07-28

## Possible feats

- **Task fingerprint schema** — structural features + semantic intent digest
  computed per episode.
- **Family register** — governed register of recurrence families with
  merge/split provenance and lifecycle states.
- **Fragment mining lane** — frequent-subsequence mining over plan/step
  traces to find shared sub-task families.
- **Trainable matcher with dispatch feedback** — fence rejections and
  fallbacks become labeled errors that improve family assignment.

## Position in the packet

Second document of the sensing arc: consumes the
[episode ledger](crystallization-episode-ledger.md), gives
[forecasting](crystallization-recurrence-forecasting.md) its unit of count,
gives [requirements mining](crystallization-requirements-mining.md) its
corpus boundary, and gives
[dispatch](crystallization-dispatch-and-fences.md) its match key.

## Two-tier identity

- **Family** — the pattern worth predicting and possibly crystallizing:
  "reconcile a monthly statement export against the ledger and produce a
  discrepancy report." Families own forecasts, corpora, fences, and
  capabilities.
- **Instance** — one envelope that lands in a family with specific
  parameters (which month, which account). Instances are counted, priced,
  and dispatched.

The identity question is asymmetric on purpose: mining can be generous
(recall-oriented — better to over-group and split later), but dispatch must
be strict (precision-oriented — a wrong family match at execution time is a
correctness hazard, handled by fences in
[dispatch](crystallization-dispatch-and-fences.md)).

## The fingerprint

Feature classes, cheapest first:

1. **Envelope-structural** — `job_type`, `domain`, which neutral refs are
   populated and their kinds (per neutral-job-envelope), overlay fields
   present.
2. **Workflow shape** — the plan record's step/gate type sequence (from the
   episode's plan record), compared as a graph/sequence, tolerant to
   parameter noise.
3. **Tool surface** — the set/sequence of tool and worker archetypes touched.
4. **Input schema shape** — types and structure of inputs, never values.
5. **Intent semantics** — an embedding of the request/goal text, and — where
   the domain has an ontology — the semantic task and artifact types from
   [ontology-grounded routing](ontology-grounded-micro-agent-routing.md).
   Ontology terms are the better long-term key: they are governed vocabulary,
   embeddings are not.

Hybrid matching: retrieve candidate families semantically (5), confirm
structurally (1–4). Semantic-only clustering over-groups ("answer a
question" swallows everything); structural-only splits families on
parameter noise.

## Families are living objects

Register discipline, like the DTN candidate register: a family record has a
lifecycle (`seed → forming → established → crystallizing → served → dormant`),
and every merge or split is an explicit recorded transition, never a silent
re-clustering. History matters because forecasts (RF) and corpora (RQ) are
keyed by family — a silent split would corrupt both.

## Fragment mining: the granularity insight

The recurring unit is often **not the whole job**. Frequent-subsequence
mining over plan records finds step fragments shared across different
families — "normalize this CSV export," "draft the gate-evidence summary" —
that recur far more often than any whole job does. Fragment families are
prime candidates for the specialist rung of the
[automation ladder](crystallization-automation-ladder.md) (they are exactly
micro-agent-shaped: single purpose, typed I/O, bounded context — see
[micro-agent task contract](omnigent-micro-agent-task-contract.md)), and a
crystallized fragment lowers the cost of every family that contains it.
Whole-job and fragment mining run as parallel lanes over the same ledger.

## The matcher is a learned, measured artifact

Family assignment will be wrong sometimes. The system's own operation
produces labels: dispatch fence rejections, fallback episodes, and parity
disagreements are all "this instance was not what the family thought"
signals. The matcher must be versioned, evaluated (precision at dispatch is
the metric that matters; recall at mining is cheap to be generous on), and
retrained on these labels — a small, governed model or ruleset, not an
ungoverned judgment call at dispatch time.

## Claims

- **TF-C1** — Identity is two-tier: families own forecasts, corpora, fences,
  and capabilities; instances are counted and dispatched. No third tier.
- **TF-C2** — The fingerprint is hybrid: semantic features for recall during
  mining, structural features for precision at dispatch; ontology terms
  replace raw embeddings as domains publish ontologies.
- **TF-C3** — Families merge and split only through recorded register
  transitions carrying provenance, because forecasts and corpora are keyed
  by family identity.
- **TF-C4** — Fragment mining over plan records is first-class; sub-task
  families are often the highest-leverage crystallization units and are
  micro-agent-shaped.
- **TF-C5** — The matcher is a versioned, evaluated artifact trained on
  dispatch feedback; its dispatch-time precision is a registry-visible
  quality metric.

## Open questions

- **TF-Q1** — Who computes and governs embeddings — gateway-mediated
  provider, per the same rails as memory providers?
- **TF-Q2** — Canonicalization rules per `job_type` (what counts as
  parameter vs. structure) — neutral defaults with domain overlay
  re-tightening, like the envelope itself?
- **TF-Q3** — Minimum family size to surface in the register (2? 3?), and
  does a single spectacularly expensive episode justify a family of one?
- **TF-Q4** — Are families tenant-scoped with cross-tenant twins linked
  later (leaning yes — consent boundaries first, see
  [cross-tenant](crystallization-cross-tenant.md)), or global from birth?
- **TF-Q5** — Fuzzy membership: does an instance carry a match confidence
  that downstream consumers (forecast weighting, dispatch strictness) use,
  or is membership binary with a gray zone routed to AI?

## Related

- [Episode Ledger](crystallization-episode-ledger.md) — the mined substrate.
- [Ontology-Grounded Micro-Agent Routing](ontology-grounded-micro-agent-routing.md)
  — semantic typing this fingerprint should converge with.
- [Dispatch and Fences](crystallization-dispatch-and-fences.md) — where
  matching precision becomes a safety property.
