# Pattern Ledger Contracts — episodes, families, forecasts, candidates

Status: staged
Kind: architecture
Summary: Declares the ADDED `pattern-ledger` contract family — five record
kinds (episode, outcome-label event, recurrence family, recurrence forecast,
crystallization candidate) computed as a governed derived projection over
audit, run-event, metering, and label streams the runtime already emits,
gateway-governed with consent flags stamped at capture, swept by a bounded
read-only nightly lane, and bounded by the autonomy rule that the Ledger
nominates but never spends.
Topics: pattern-ledger, episode-ledger, outcome-labels, recurrence-family,
recurrence-forecasting, crystallization-candidate, memory-gateway,
governed-derived-model, nightly-sweep
Repository context: openxFactory (neutral schemas; codexFactory first
conformer)
Staging ID: `openxFactory:staging:recurrence-crystallization`
Source: brainstorm docs
[episode ledger](../../brainstorm/crystallization-episode-ledger.md),
[task families](../../brainstorm/crystallization-task-families.md),
[recurrence forecasting](../../brainstorm/crystallization-recurrence-forecasting.md),
[Pattern Ledger synthesis](../../brainstorm/crystallization-synthesis-pattern-ledger.md);
rulings D2, D3, D4, V1 (primary doc, 2026-07-29).
Target capabilities: `pattern-ledger` (ADDED)

## The five record kinds

1. **`episode`** — one governed job solved on the expensive path: envelope
   snapshot (neutral refs + overlay fields), the plan record *as data* (the
   thing L3 freezes), step/tool trace (digests always; payload retention is
   a tenant dial), cost vector (worker clock-in + gateway metering, human
   touches included), replayability class (`pure | record-replay |
   live-only`, declared at capture — EL-C3), and consent flags (T1/T2/T3,
   default deny, stamped at capture). Identity ruling: **one episode per
   governed job with per-agent sub-spans** (resolves EL-Q1).
2. **`outcome_label`** (D2) — append-only event attached to an episode:
   source enum `praise | gate_outcome | correction | adjudication`, actor
   ref, grade/polarity, evidence ref. Episode quality is a fold over the
   stream (EL-C2): a later correction demotes an episode praised at close.
   Nothing that spends money keys off `praise` alone (LC-C5).
3. **`recurrence_family`** — register entry, **tenant-scoped** (D3):
   lifecycle `seed → forming → established → crystallizing → served →
   dormant`; merge/split only as recorded transitions with provenance
   (TF-C3); two mining lanes, whole-job and fragment (TF-C4); the matcher is
   versioned and its dispatch-time precision is a visible quality metric
   (TF-C5).
4. **`recurrence_forecast`** — predictive distribution over a declared
   horizon with evidence window, cost-regime assumption, and stability
   half-life (RF-C1..C4); stored with a maturity date and later scored
   (RF-C5). Reports **fence-eligible volume alongside raw family volume**
   (SYA-C3) so downstream economics never price traffic a fence will not
   claim.
5. **`crystallization_candidate`** (D4) — the Ledger's only mutating
   output: an own record kind in the suggestion grammar (idempotency key =
   family + evidence window; suppression while one is open; rationale that
   cites episodes and the forecast). Autonomy boundary: **nominate, never
   spend** (SYA-C2).

## Storage and compute posture

The Ledger is a **derived projection** over records that already exist —
audit, run events, gateway metering (M3), labels — under the
governed-derived-model discipline: recipe + sources + digest, regenerate
rather than hand-edit (EL-C1, EL-C5: consumers reference episodes by
digest; none keep private copies). It is gateway-governed Domain Hermes
memory (the expert case-memory port is the right shape). **V1 ruling: no
MODIFIED delta on `memory-gateway`** — the M1 promotion requirement
constrains the promotion candidate record, not the promoted artifact's
kind, so the procedural promotion target is consumption of the existing
port.

Compute: a bounded, read-only lane on the nightly-sweep cadence with
event-driven reconcile on family milestones (resolves SYA-Q1) — the same
shape as the practice pipeline's gap scan: enumerate, project, score, emit
records, mutate nothing.

## Requirement sketch for `add-pattern-ledger`

Schemas for the five record kinds under `contracts/schemas/` (each with
`schema_version` + `kind`); a deterministic validator; the derived-
projection recipe declaration; the consent-flag capture rule; the
nomination criteria as dials (see
[dials-and-defaults.md](dials-and-defaults.md)); the autonomy-boundary
requirement with a scenario proving a candidate cannot trigger spend.

## Open questions carried

- Backfill depth from existing audit history (EL-Q3) — the MVP does a
  manual retrospective for its one family; systematic backfill is a
  realization question.
- Embedding provider governance for semantic fingerprint features (TF-Q1)
  — gateway-mediated like memory providers, exact binding open.
- Canonicalization ownership per `job_type` (TF-Q2) — neutral defaults,
  domain overlay re-tightening.
- Fuzzy family membership: confidence-weighted counting vs binary with a
  gray zone routed to AI (TF-Q5, RF-Q4).
- Business-calendar ownership for seasonality (RF-Q2) — leaning Tenant
  Hermes content consumed by the domain forecaster.
