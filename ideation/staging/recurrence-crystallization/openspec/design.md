# Design (draft): add-pattern-ledger

Status: draft
Draft slice of: ../recurrence-crystallization.md

## Record shapes (sketches — schemas are the deliverable)

```yaml
kind: episode                     # one per governed job
schema_version: 0.1.0
episode_id: ep:codex:2026-07-28:...        # digest-derived
envelope: {job_type: ..., domain: ..., refs: {...}}   # snapshot
plan_ref: {digest: sha256:...}             # the plan AS DATA (L3 freezes this)
spans:                                     # per-agent sub-spans
  - {agent: ..., steps: [{tool: ..., io_digest: sha256:..., payload_ref: null}]}
cost: {credits: ..., wall_ms: ..., human_touches: [...], meter_ref: ...}
replayability: pure | record-replay | live-only
consent: {episode_use: false, automation: false, pooling: false}  # default deny
labels_ref: ...                            # the outcome_label stream
```

```yaml
kind: outcome_label               # append-only; quality is a fold
schema_version: 0.1.0
episode_ref: ...
source: praise | gate_outcome | correction | adjudication
actor_ref: ...
grade: ...                        # per-source vocabulary, small
evidence_ref: ...
at: ...
```

```yaml
kind: recurrence_family           # tenant-scoped register entry
schema_version: 0.1.0
family_id: fam:<tenant>:<slug>
tenant_ref: ...
lane: whole-job | fragment
state: seed | forming | established | crystallizing | served | dormant
fingerprint: {structural: {...}, semantic_ref: ...}   # hybrid (TF-C2)
members: [{episode_ref: ..., confidence: ...}]
transitions: [{kind: merge|split|state, at: ..., provenance: ...}]
matcher: {version: ..., dispatch_precision: ...}
```

```yaml
kind: recurrence_forecast         # stored, maturity-dated, scored
schema_version: 0.1.0
family_ref: ...
horizon_days: 90
evidence_window: {from: ..., to: ..., instances: ...}
distribution: {...}               # predictive, not a point
cost_regime: current-ai-pricing   # declared assumption (RF-C3)
stability_half_life_days: ...
volumes: {raw: ..., fence_eligible: null}   # null until a fence exists
matures_at: ...
score_ref: null                   # filled when scored
```

```yaml
kind: crystallization_candidate   # the ledger's ONLY mutating output
schema_version: 0.1.0
candidate_id: ...
idempotency_key: <family_ref>+<evidence_window_digest>
family_ref: ...
forecast_ref: ...
evidence: {episode_refs: [...], cost_baseline: ...}
rationale: ...                    # cites episodes + forecast; praise-only invalid
suggested_rung: L2..L6            # advisory only
state: open | superseded | disposed
```

## Projection recipe

The ledger is a governed derived artifact: `recipe_version` + source-stream
digests (audit, run events, metering, labels) → deterministic records.
Regeneration replaces; hand-edits are nonconformant. This is
`governed-derived-model` applied to operational memory, and the reason a
label correction propagates everywhere at once — consumers hold digests,
not copies.

## Decisions carried from staging (context, not restated policy)

| Ruling | Effect here |
| --- | --- |
| D2 | `outcome_label` exists now; praise is one source, never a spend key |
| D3 | families are tenant-scoped; pooled twins are a later wave |
| D4 | candidate is an own kind in the suggestion grammar |
| V1 | memory-gateway consumed, not modified |
| Dials | `nomination_count_k`, `min_family_*`, `forecast_horizon`, `payload_retention` from the topic register |

## Open design points (to settle during implementation or review)

- Fingerprint semantic feature: embedding digest now vs ontology term refs
  when `add-domain-ontology-layer` lands (TF-Q1) — schema should hold either
  behind one `semantic_ref`.
- Fuzzy membership: `confidence` is in the member shape; whether forecasts
  weight by it or drop sub-threshold members (TF-Q5/RF-Q4).
- Where the sweep lane physically runs first (codexFactory nightly family,
  like doc-health/readiness) — realization detail, not contract.
- Episode backfill depth for warm-start beyond the MVP family (EL-Q3).
