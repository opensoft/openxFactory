code_surface: openxFactory (contracts/schemas crystallization-decision / crystallization-spec / crystallization-build / crystallization-consent record family + additive omnigent-domain-overlay schema fields (crystallized-executor binding, rung ceilings) + canonical validator scripts/validate-crystallizer-contracts.py and the validate-omnigent-contracts.py extension — contracts, examples, validators only; decision lane, miner, and build execution are successor realizations)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified by: Brett's approval of `add-crystallizer-contracts` on 2026-07-29, on the recurrence-crystallization staging decision record D1–D11 + V1–V2 carried as design context — notably D5 (codexFactory builds for every domain, consuming domain owns fitness), D7 (frozen L0–L6 rung vocabulary), D11 (effect classes; v1 dispatch admits only pure/idempotent), the corrected SYB-C2 evaluation order (ceilings resolve before valuation), and the drafting-time shape ruling that crystallized executors bind as worker classes on the EXISTING five archetypes so the promoted constitutional matrix requirement covers them verbatim and authority conservation is a mechanical subset check; the carried open design points (corpus-bar dial values, ratification scaling thresholds, the T2 spot-check condition shape, equivalence-predicate signing authority) are deliberately deferred to implementation and successor changes.

## Why

The sensing half is canon: `pattern-ledger` (realized `contract-v1.19`)
produces evidence-carrying crystallization candidates — and, by
constitutional rule, a candidate can never schedule work or spend budget.
Nothing governed can act on one yet. This change adds the middle of the
flywheel: the investment decision that is the only path from nomination to
spend, the episode-mined micro-spec whose acceptance corpus is the
contract and whose scope fence declares jurisdiction, the build as an
ordinary governed codexFactory job with unbroken provenance, and the
authority half — consent tiers and the crystallized-executor binding under
strict authority conservation. Without it, the ledger's candidates are a
well-evidenced wishlist; with it, the factory can convert repetition into
governed cheaper paths while the constitutional lines (nominate-never-
spend, conservation, effect-class caution) hold at every step.

## What Changes

- Add `crystallization-decision`: the decision record as the **only path
  to spend** — consumes an open candidate; resolves rung ceilings BEFORE
  valuation; values each eligible rung with AI-price deflation and
  pattern-survival discounting plus first-class non-token value; selects a
  shape (rung, budget cap, abort rule, proof obligations), never a
  boolean; funds only inside the tenant crystallization budget and
  clearance envelope; records declined candidates in a not-yet ledger with
  re-nomination conditions; starts tenants on decision-ladder rungs 1–2
  with the expected-value rung gated on calibration evidence; freezes the
  `automation_rung` vocabulary at L0–L6 (D7).
- Add `crystallization-build`: the episode-mined micro-spec (invariants,
  parameters, branches, mandatory counterexamples — all citing episodes);
  the acceptance corpus as the operative contract (equivalence predicates,
  cassettes, digest-pinned, regenerable); the scope fence as a requirement
  artifact consumed verbatim by dispatch; the declared `effect_class`
  (D11); the build as an ordinary governed job (`crystallization_build`)
  executed by codexFactory for every domain with the consuming domain
  owning fitness gates (D5); the gapless provenance manifest and
  regeneration-first maintenance; dry-run mode and the generated-artifact
  data-leak scan as build acceptance criteria; budget caps with declared
  abort behavior.
- Add `crystallization-consent`: the three independently grantable,
  default-deny tiers — `episode_use` (per tenant), `automation` (per
  family category, optionally condition-carrying), `pooling` (frozen,
  consumer-less until the cross-tenant wave) — with subject-visible
  provenance where automation touches a subject, and the three-layer
  approval braid no single layer can collapse.
- Extend `omnigent-domain-overlay` (additive): the **crystallized-executor
  binding** — a worker class marked `crystallized` carrying
  `capability_ref`, `automation_rung`, `replaces_configuration`, and a
  young-capability throttle schedule, mapping to an EXISTING neutral
  archetype (the five-archetype vocabulary is deliberately unchanged) so
  the promoted constitutional matrix requirement covers it verbatim; the
  mechanical authority-conservation rule (effective permissions and
  credential families ⊆ the replaced configuration's); and per-category
  **rung-ceiling declarations** with a conservative L3 default for
  undeclared categories.
- Add the canonical validator for the new record family and extend the
  omnigent overlay validator for the binding and ceiling rules; examples
  continue the MVP packet-capture corpus (a decision, micro-spec, fence,
  and binding for the family the ledger already nominates).

## Capabilities

### New Capabilities

- `crystallization-decision`: decision records, evaluation order, valuation
  discipline, budget/clearance consent surface, not-yet ledger, decision-
  ladder maturity, and the frozen rung vocabulary.
- `crystallization-build`: micro-spec mining, acceptance corpus, scope
  fence, effect class, governed build job, provenance and regeneration,
  dry-run/leak-scan/budget gates.
- `crystallization-consent`: the T1/T2/T3 tier contract and the approval
  braid.

### Modified Capabilities

- `omnigent-domain-overlay`: two ADDED requirements (crystallized-executor
  binding; rung-ceiling declarations). The neutral archetype vocabulary
  and the generalized permission matrix are deliberately not modified —
  a crystallized class maps to an existing archetype and inherits the
  constitutional falses from the promoted matrix requirement as written.

## Out of Scope

- Everything that routes or operates: registry, dispatch junction, proof
  stages (replay/shadow/canary), sentinels, drift, capability-health,
  accounting — successor change `add-capability-steward` (exit 3).
  Audit-shape parity and throttle *enforcement* land there; this change
  only declares the binding-time facts they need.
- Cross-tenant pooling and any T3 consumer; platform capabilities; DTN
  promotion of crystallized capabilities (later wave).
- The L2 result cache (owned by the ontology packet's result-cache
  brainstorm; consumed as a rung).
- Final artifact-residence policy: the design doc records the rung→home
  lean (BP-Q1/AL-Q2); the build contract requires residence + digest
  declaration, and each domain's first realization fixes its home.

## Dependencies and Sequencing

Second of the topic's three ordered exits. Consumes as-is: `pattern-ledger`
(`contract-v1.19`: candidates, episodes, forecasts), `credential-contracts`
(grants/bindings; code holds no secrets), `roles-authority-model` (who
signs), `workflow-gate-contract` (intake/fitness/review gates),
`release-realization` (build archive evidence), `governed-derived-model`
(spec/corpus regenerability). Exit 3 depends on the records this change
defines (decisions carry proof obligations; bindings carry throttle
schedules; fences and effect classes are what dispatch enforces).
