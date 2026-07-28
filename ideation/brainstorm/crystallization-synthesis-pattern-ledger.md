# Synthesis: The Pattern Ledger — Sense Repetition, Predict Return — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The sensing arc's three atomic pieces — episode capture, family
fingerprinting, and recurrence forecasting — compose into one standing
subsystem, the Pattern Ledger: a gateway-governed derived surface over
records the runtime already emits, owned by Domain Hermes memory, that
continuously answers "what work keeps coming back, what does it cost, and
how often will it return?" and emits idempotent, evidence-carrying
crystallization-candidate records onto the same suggestion rails the
practice-adoption pipeline uses.
Topics: crystallization, pattern-ledger, episode-ledger, recurrence-family,
forecasting, domain-hermes, memory-gateway, suggestion-record, synthesis
Repository context: openxFactory (the sensing-arc contract family as one
subsystem)
Captured: 2026-07-28

## Possible feats

- **Pattern Ledger subsystem contract** — episodes + family register +
  forecast records as one gateway-governed surface with declared feeds.
- **`crystallization_candidate` record kind** — suggestion-grammar record
  (idempotency, evidence, rationale, suppression) emitted when a family
  crosses nomination criteria.
- **Sensing feedback intakes** — dispatch fallbacks retrain the matcher;
  realized counts score the forecaster.

## Members and their joints

Atomic members: [episode ledger](crystallization-episode-ledger.md) (EL),
[task families](crystallization-task-families.md) (TF),
[recurrence forecasting](crystallization-recurrence-forecasting.md) (RF).

```text
runtime streams (exist today)                     Pattern Ledger
  audit records ─┐
  run events ────┤   derived projection    ┌─ episodes (EL)
  metering ──────┼──────────────────────►──┤     keyed by fingerprint
  praise/labels ─┘                         ├─ family register (TF)
                                           │     merge/split provenance
  dispatch fallbacks ──(matcher training)──┤     whole-job + fragment lanes
  realized counts ─────(forecast scoring)──┼─ forecast records (RF)
                                           │     volume + stability
                                           ▼
                              crystallization_candidate records
                              → the Crystallizer (invest/build arc)
```

The joints that make it one subsystem rather than three features:

- **One substrate (EL-C5).** Families are views over episodes; forecasts
  are functions of family histories; corpora (downstream) are curated
  episode subsets. Nothing keeps private copies — every consumer keys back
  to episode digests, so a label correction (EL-C2) propagates everywhere
  at once.
- **Identity discipline (TF-C3) protects prediction (RF).** Forecasts are
  keyed by family; the register's recorded merge/split transitions are what
  let a forecast survive a re-clustering with its history intact.
- **Prediction closes its own loop (RF-C5 via CA).** The ledger stores its
  forecasts as records with maturity dates; the accounting arc scores them;
  the priors improve. The subsystem gets better at noticing *as a
  consequence of operating*.

## Ownership and placement

The Pattern Ledger is **Domain Hermes memory work**, mediated by the memory
gateway (episodes are experiential memory; the expert case-memory port is
the right shape; metering is already gateway-owned at M3). The trisection:
Domain Hermes owns pattern meaning (families, forecasts, nomination),
Tenant Hermes owns the consent flags episodes carry and the budget the
candidates will ask for, Subject visibility begins only downstream when
automation actually serves a subject. The compute is a bounded, read-only
sweep — the same shape as the practice pipeline's gap scan and the
nightly-sweep family: enumerate, project, score, emit records, mutate
nothing.

## The output contract: candidates on the suggestion rails

When a family crosses nomination criteria (decision-ladder rung 1-2:
count/forecast thresholds — EC owns what happens after), the Ledger emits a
`crystallization_candidate` — deliberately shaped like a
`practice_adoption_suggestion` (idempotency key: family + evidence window;
suppression while one is open; rationale citing evidence, "thin rationales
are embarrassing"): the domain SUGGESTS, the tenant clears, realization
goes through the front door. Candidate payload: family ref + forecast
record + cost baseline + provisional rung recommendation + evidence-bound
declaration. **The nomination is autonomous; the spend never is** — the
Ledger's autonomy boundary is exactly the practice pipeline's.

## Tensions to hold

- **Capture breadth vs. cost** — universal capture (EL-C1) is cheap only if
  payload retention stays a policy dial (EL-C4); corpus hunger (RQ) pushes
  retention up, privacy and storage push down. The dial will be fought
  over; put it in tenant policy from day one.
- **Mining generosity vs. dispatch precision** — one fingerprint feeds both
  (TF-C2); resolving it as "generous families, strict fences" means family
  counts systematically exceed what fences will ever claim — forecasts and
  the economics must use fence-eligible volume, not raw family volume, or
  ROI inflates.
- **Nomination eagerness vs. suggestion noise** — every threshold too low
  floods the clearance queue; too high and the flywheel never starts.
  Suppression + idempotency handle re-noise; the threshold itself should be
  a scored, tunable policy like everything else.

## Claims rollup (details in the atomic docs)

EL-C1..C5 (universal derived capture, append-only labels, replayability
classes, payload dial, single substrate) · TF-C1..C5 (two-tier identity,
hybrid fingerprint, register transitions, fragment lanes, measured matcher)
· RF-C1..C5 (distributions with horizons, empirical-Bayes cold start,
regime-declared elasticity, stability alongside volume, scored forecasts).
Synthesis-level additions:

- **SYA-C1** — The Pattern Ledger is one gateway-governed subsystem owned
  by Domain Hermes memory, computed by bounded read-only sweeps over
  existing runtime streams.
- **SYA-C2** — Its sole mutating output is the `crystallization_candidate`
  record, carried on the practice-suggestion rails with the same autonomy
  boundary: suggest, never spend.
- **SYA-C3** — Economics consumes fence-eligible volume, not raw family
  volume; the Ledger must report both.

## Open questions

- **SYA-Q1** — Sweep cadence: fold into the existing nightly sweep as a
  lane, or event-driven on episode milestones with a nightly reconcile?
- **SYA-Q2** — Does the Ledger nominate fragments (TF-C4) independently, or
  only when a whole-job candidate's mining reveals them (RQ-Q5)?
- **SYA-Q3** — Cold-start bootstrap: backfill episodes from audit history
  (EL-Q3) before the first nomination, or start counting from go-live?

## Related

- [Synthesis: The Crystallizer](crystallization-synthesis-crystallizer.md)
  — the candidate's consumer.
- [Domain Practice Suggestion Generation](domain-practice-suggestion-generation.md)
  — the rails and the autonomy boundary this reuses.
- [Overview](crystallization-overview.md) — the full flywheel.
