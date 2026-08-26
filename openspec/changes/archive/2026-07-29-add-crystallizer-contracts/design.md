## Context

The staged rulings this change realizes: SYB-C2's corrected evaluation
order (ceilings → value per eligible rung → selection), D5 (codexFactory
builds for every domain; consuming domain owns fitness), D7 (rung
vocabulary frozen L0–L6), D11 (effect classes; v1 dispatch will admit only
`pure`/`idempotent`), and the authority fragment's constitutional line:
crystallization must never widen authority. The load-bearing shape decision
made at drafting: a crystallized capability binds as a **worker class on an
existing archetype** rather than a new archetype — so the promoted
five-archetype vocabulary and the constitutional permission matrix apply to
it verbatim, and conservation is a subset check against the configuration
it replaces, not a new constitution.

## Record shapes (sketches — schemas are the deliverable)

```yaml
kind: crystallization_decision      # the ONLY path from candidate to spend
schema_version: 1
decision_id: dec:<tenant>:<family-slug>:<date>
candidate_ref: cand:...             # must be an open pattern-ledger candidate
family_ref: fam:...
ceiling: {rung: L3, source: overlay|default, reason_ref: ...}   # resolved FIRST
valuation:                          # one row per ELIGIBLE rung only
  - rung: L3
    expected_value: ...
    deflation_factor: ...           # AI-price decline assumption
    survival_factor: ...            # pattern half-life from the forecast
    nontoken_value: {latency: ..., determinism: ..., compliance: ...}
outcome: funded | not_yet
funded:                             # present iff outcome=funded
  rung: L3
  budget_cap: ...
  abort_rule: "stop at 120% of estimate; persist partials; return actuals"
  proof_obligations: [replay, shadow]      # consumed by exit 3
not_yet:                            # present iff outcome=not_yet
  reasons: [...]
  renominate_when: "..."
approvals:                          # the braid — no single layer suffices
  domain_fitness_ref: ...
  tenant_budget_ref: ...            # clearance envelope or liaison approval
  consent_check: {automation_tier: granted}
decision_ladder_rung: 1|2|3         # 3 (EV) requires calibration evidence
```

```yaml
kind: crystallization_spec          # the episode-mined micro-spec
schema_version: 1
spec_id: cspec:<family-slug>:v1
decision_ref: dec:...
family_ref: fam:...
mined:
  invariants: [...]                 # each citing episode refs
  parameters: [...]                 # observed types + ranges
  branches: [...]                   # divergent-episode conditionals
  counterexamples: [...]            # MANDATORY; failed/corrected episodes
acceptance_corpus:
  episode_refs: [...]
  equivalence_predicates: [...]     # per output type; never byte goldens
  cassettes_ref: ...                # record-replay episodes only
  corpus_digest: sha256:...
scope_fence: {predicate: ..., derived_from: observed-support, digest: sha256:...}
effect_class: pure | idempotent | compensable | irreversible
miner: {version: ..., evidence_bounds: {episodes: N, span: ..., ranges: ...}}
ratification: {mode: auto|human, scaled_by: [rung, risk]}
```

```yaml
kind: crystallization_build         # envelope profile for the governed job
schema_version: 1
job_type: crystallization_build     # ordinary codexFactory job (D5)
spec_ref: cspec:...
consuming_domain: MedxFactory       # owns fitness gates; codexFactory executes
budget: {cap: ..., abort: ...}
acceptance:                         # ALL required to pass build
  corpus_green: true
  dry_run_proven: true
  leak_scan_clean: true             # no literal traceable to tenant payloads
  binding_reviewed: true            # authority conservation (below)
provenance_manifest:                # gapless chain, regeneration-first
  episodes: [sha256:...]
  corpus_digest: sha256:...
  spec: {id: ..., digest: ...}
  builder: {identity: ..., version: ...}
  toolchain: {bench_pins: ...}
artifact: {digest: sha256:..., packaging: playbook|profile|program,
           residence: <declared home, see lean below>}
```

```yaml
kind: crystallization_consent       # one grant per tier; default deny
schema_version: 1
tenant_ref: tenant:...
tier: episode_use | automation | pooling
scope: {family_category: ...}       # automation tier only
condition: {spot_check: {rate: 0.1}}   # optional (AU-Q4 design option)
granted_by: ...                     # tenant authority per roles-authority-model
state: granted | revoked
```

Crystallized-executor binding (additive omnigent-domain-overlay fields):

```yaml
worker_classes:
  - name: packet_capture_playbook
    archetype: generate             # EXISTING vocabulary — unchanged
    crystallized: true
    capability_ref: cap:...         # exit-3 registry id
    automation_rung: L3
    replaces_configuration: coding_agent   # conservation baseline
    permissions: {read_workspace: true, write_artifacts: true,
                  run_validations: true, propose_admission: false,
                  execute_final_action: false, access_secrets: false}
    throttle: {schedule_ref: dials.young_throttle}
rung_ceilings:                      # per task category, with reasons
  - category: doc-workflow
    ceiling: L5
    reason: "mechanically checkable outputs; no subject-affecting judgment"
  - category: clinical-judgment     # e.g. Medx overlay
    ceiling: L3
    reason: "regulatory posture: judgment never crystallizes past playbook"
```

## Artifact residence — the staged lean (BP-Q1 / AL-Q2)

The build contract requires `artifact.residence` + digest to be DECLARED;
this table is the recommended realization, recorded here so exit 2 inherits
a lean instead of a blank:

| Rung | Artifact | Home |
| --- | --- | --- |
| L3 | frozen playbook (data, not code) | a workflow-contract instance in the owning domain repo, digest-pinned |
| L4 | specialist micro-agent profiles | the domain's Omnigent overlay, rendered into omnigent-install like existing profiles |
| L5/L6 | programs | `capabilities/<capability-id>/` in the owning domain repo (codexFactory builds; consuming domain hosts + reviews), executed on governed benches via omnigent-install |

Graduation to a dedicated repo stays available for hot or cross-domain
capabilities; platform-owned homes belong to the cross-tenant wave.
Reachability through the exit-3 dispatch junction only — residence never
implies invocability.

## Decisions carried from staging (context, not restated policy)

| Ruling | Effect here |
| --- | --- |
| SYB-C2 | ceilings resolve before valuation; value only eligible rungs |
| D5 | codexFactory executes builds; consuming domain owns fitness gates |
| D7 | `automation_rung` L0–L6 frozen; decisions select L2–L6 (L0/L1 = not_yet) |
| D11 | `effect_class` declared at spec time; enforcement is exit 3's |
| AU-Q3 lean | ONE crystallized class shape with a rung field, not per-rung-band classes |
| Undeclared ceiling | defaults to L3 — code rungs always need an explicit overlay ruling |

## Open design points (settle at implementation or review)

- Corpus-bar values per rung stay dials (`corpus_bar_L3`,
  `corpus_bar_L5_plus`); the spec-intake gate reads them.
- Ratification scaling thresholds (auto vs human) by rung × risk class —
  proposal leans auto below L4 and non-subject-affecting, human otherwise.
- The spot-check condition shape on T2 (AU-Q4) — carried as an optional
  field; semantics firm up at first tenant use.
- Whether `crystallization_spec` ratification reuses the gate-intent /
  gate-action-record machinery from the dashboard family — likely yes at
  realization; not contract-coupled now.
- Equivalence-predicate signing authority (RQ-Q4) — leaning: domain Lead
  proposes, tenant authority countersigns, mirroring binding signatures.
