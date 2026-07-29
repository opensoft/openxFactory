code_surface: openxFactory (contracts/schemas pattern-ledger record family + scripts/validate-pattern-ledger.py — schemas, examples, and validator only; sweep worker and runtime projection lanes are successor realizations)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)

## Why

The factory's self-learning already makes the *next* solve of a repeated task
somewhat better (recall-assisted context packets), but nothing in the
contract family can answer the questions that decide whether repetition is
worth converting into software: what work keeps coming back, what did each
occurrence cost, was the outcome actually good, and how often — and for how
long — will it return? Without those records, crystallization decisions are
hunches, savings claims are self-graded, and the efficiency mandate the
cost-accountability model gives the Domain Hermes has no evidence substrate.
This change adds the sensing half only — records and rules, no spend — so
the decision and build contracts (`add-crystallizer-contracts`) and the
runtime junction (`add-capability-steward`) land on evidence that already
exists.

## What Changes

- Add the `pattern-ledger` capability: five neutral record kinds —
  `episode`, `outcome_label`, `recurrence_family`, `recurrence_forecast`,
  `crystallization_candidate` — as schemas under `contracts/schemas/` with
  positive and negative examples.
- Require episodes to be **derived projections** of the runtime's existing
  audit, run-event, metering, and label streams (governed-derived-model
  discipline) — no second authoritative store, digests-not-copies for every
  consumer.
- Make outcome an **append-only label stream** (`praise | gate_outcome |
  correction | adjudication`) folded into episode quality, so praise becomes
  a record and late corrections re-grade history.
- Make recurrence families **tenant-scoped register entries** with recorded
  merge/split transitions, whole-job and fragment mining lanes, and a
  versioned matcher whose dispatch-time precision is a visible metric.
- Make forecasts **scored instruments**: predictive distribution + declared
  horizon + evidence window + cost-regime assumption + stability half-life,
  stored with a maturity date and graded against actuals.
- Bound the ledger's autonomy: its only mutating output is the
  `crystallization_candidate` (suggestion grammar: idempotency, suppression,
  evidence-citing rationale), and a candidate **cannot schedule work, spend
  budget, or execute anything**.
- Stamp consent scope (`episode_use | automation | pooling`, default deny)
  on every episode at capture; downstream uses honor the tiers (the pooling
  tier is frozen into the enum now but unused until the cross-tenant wave).
- Declare nomination thresholds and retention windows as **dials** owned by
  policy layers (staged defaults in the topic's
  `dials-and-defaults.md`), not contract constants.
- Add `scripts/validate-pattern-ledger.py` enforcing schema conformance,
  vocabularies, default-deny consent, family transition legality, and
  candidate idempotency/suppression rules; register artifacts in
  `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and
  `contracts/README.md`.

## Capabilities

### New Capabilities

- `pattern-ledger`: episode capture and derivation rules, outcome-label
  folding, family register semantics, forecast scoring discipline, candidate
  autonomy boundary, consent-scope gating, and the bounded read-only sweep.

### Modified Capabilities

- None. Verified during staging (topic decision record): `memory-gateway`
  is consumed, not modified — its M1 promotion requirement constrains the
  promotion candidate record, not the promoted artifact's kind (V1); the
  optional `family_hint` envelope field is deferred, so `neutral-job-envelope`
  is untouched this wave (V2).

## Out of Scope

- Anything that spends: decision records, budgets, builds, specs, fences —
  successor change `add-crystallizer-contracts`.
- Anything that routes or executes: registry, dispatch junction, proof
  stages, sentinels, capability-health — successor change
  `add-capability-steward`.
- Cross-tenant pooling, platform capabilities, DTN promotion of crystallized
  capabilities — a later wave (the topic's out-of-wave declaration); T3 is
  enum-frozen here, nothing more.
- The L2 result cache — owned by the ontology packet's result-cache
  brainstorm; unrelated to this change's records.

## Dependencies and Sequencing

First of the topic's three ordered exits; no dependency on the other two.
Consumes promoted capabilities as-is: `governed-derived-model` (projection
discipline), `memory-gateway` (metering M3, promotion M1), the
cost-accountability clock-in shape (still brainstorm — cited as evidence
source, not restated as policy). The MVP family (packet-capture mechanics,
topic decision D8) supplies retrospective episode fixtures for the validator
before any live capture exists.
