## Context

The staged rulings this change realizes: D9 (neutral dispatch contract;
hermes-install admission is the first realization), D10 (artifacts
digest-pinned, authority status live-read — the demotion-speed vs
pin-discipline tension resolved), D11 enforcement (v1 fences admit only
`pure`/`idempotent`), the L2 seam rule (the result cache is a rung behind
the junction), and SYC-C1..C3 (the steady state is a governed blend with
the AI path as permanent infrastructure; the Steward's exhaust is
contractually the Pattern Ledger's intake; sentinel ε is the packet's most
load-bearing policy number). Sentinels and accounting fold into
`capability-health` rather than standing alone: they are how health is
*known*, not separate concerns.

## Record shapes (sketches — schemas are the deliverable)

```yaml
kind: crystallized_capability       # the registry record (git truth)
schema_version: 1
capability_id: cap:opensoft:packet-capture-playbook
family_refs: ["fam:opensoft:packet-capture-mechanics"]
tenant_ref: tenant:opensoft
rung: L3
version: 1
artifact: {digest: sha256:..., packaging: playbook, residence: "codexFactory workflows/"}
fence_ref: {digest: sha256:...}     # from the crystallizer spec, verbatim
effect_class: idempotent
provenance_ref: {digest: sha256:...}
permission_binding_ref: "overlay:codexFactory:packet_capture_playbook"
consent_scope: {episode_use: true, automation: true, pooling: false}
cost_profile: {measured_marginal: null, baseline_ai: null}   # accounting-written
health_ref: "health:cap:opensoft:packet-capture-playbook"    # steward-written
status: shadow    # candidate|building|shadow|canary|active|degraded|retired
status_history:   # transitions advance ONLY via proof-gate outcomes
  - {to: candidate, at: ..., gate_ref: ...}
  - {to: building, at: ..., gate_ref: ...}
  - {to: shadow, at: ..., gate_ref: ...}
authority: {serving: false, demoted_reason: null}   # LIVE-READ (D10)
demotion_triggers_ref: ...          # armed at promotion, never after
owner: {fitness: codexFactory, budget: tenant:opensoft}
dry_run: supported
```

```yaml
kind: dispatch_record               # one per junction decision
schema_version: 1
dispatch_id: disp:...
envelope_ref: ...
family_match: {family_ref: ..., confidence: ..., matcher_version: ...}
capability_ref: cap:...             # null on no-family-match
effect_class: idempotent            # copied at admission; D11-checked
path: crystallized | ai | dual      # dual = live sentinel comparison
fallback_cause: null                # no-family-match | fence-miss |
                                    # execution-error | postcondition-fail |
                                    # risk-override | sentinel
postconditions: {evaluated: true, passed: true, breaches: []}
provenance: "served by cap:...@1 (rung L3)"   # path-invariant record shape
overhead: {decision_ms: ..., decision_credits: ...}
```

```yaml
kind: adjudication_record           # ONE kind for parity AND sentinels
schema_version: 1
adjudication_id: adj:...
context: replay | shadow | canary | sentinel
capability_ref: cap:...
episode_ref: ep:...                 # the AI-path comparison run
disagreement: ...
verdict: capability_wrong | ai_wrong | spec_underdetermined
consequence: corpus_counterexample | episode_relabel | spec_revision
adjudicator: {kind: human | persona | judge_panel, ref: ...}
```

```yaml
kind: sentinel_policy               # per capability while authoritative
schema_version: 1
capability_ref: cap:...
epsilon: {current: 0.20, floor: 0.02, schedule: no-decay}   # MVP posture
mode: dual-run | async-replay | takeover
expense_ref: "budget:...:exploration"   # declared, never hidden in savings
```

```yaml
kind: capability_health_report      # standing scorecard (doc-health sibling)
schema_version: 1
capability_ref: cap:...
window: {from: ..., to: ...}
signals: {fallback_rate: ..., postcondition_breaches: ...,
          sentinel_disagreement: ..., corrections: ..., dormant_days: ...}
findings:
  - {class: auto | contested, rule: ..., action_or_disposition: ...}
drift_response: null                # observe|shrink-fence|regenerate|demote|retire
```

```yaml
kind: savings_entry                 # accounting; counterfactual discipline
schema_version: 1
capability_ref: cap:...
window: {from: ..., to: ...}
instances: {served: ..., sentinel: ..., fallback: ...}
counterfactual: {anchor_ref: adj:... , anchored_at: ...}   # REQUIRED fresh
net: {savings_per_instance: ..., volume: ..., full_cost_deductions: ...}
verdict: verified | unverifiable    # stale anchor -> unverifiable, never rosy
---
kind: calibration_score             # every ex-ante number graded on maturity
schema_version: 1
prediction_ref: fc:... | dec:...    # forecast, build estimate, half-life
actual: ...
score: ...
feeds: prior-update
```

## Decisions carried from staging (context, not restated policy)

| Ruling | Effect here |
| --- | --- |
| D9 | dispatch is a neutral contract; hermes-install admission realizes first |
| D10 | registry `artifact` pinned; `authority` live-read; demotion at next decision |
| D11 | junction admits `pure`/`idempotent` only in v1 |
| V2 | no envelope delta; fingerprints from existing fields |
| LC-Q5 lean | one adjudication record kind across parity and sentinels |
| SYC-C2 | renewal write-backs are contractual, not best-effort |

## Open design points (settle at implementation or review)

- Steward as role vs contract (SYC-Q1) — this change defines the
  contracts; whether a named steward persona/lane owns the pager is a
  realization decision per domain.
- Shadow-window statistics: fixed N vs sequential tests (PV-Q1) — dials
  register carries `shadow_window`; the gate profile may tighten.
- Replay-only promotion for low-risk L3 (PV-Q4) — leaning yes with the
  human-compared shadow retained for the MVP regardless.
- Dashboard surfacing (SYC-Q3) — capability-health as a panel on the
  existing gate-console family, not a new UI; realization-side.
- `degraded` as status vs health annotation (CR-Q3) — drafted as a status
  so authority and condition stay one read; revisit if the runtime wants
  the split.
