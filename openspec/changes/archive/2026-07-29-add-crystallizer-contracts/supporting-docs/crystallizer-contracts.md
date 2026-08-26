# Crystallizer Contracts — decision, spec mining, governed build

Status: staged
Kind: architecture
Summary: Declares the ADDED `crystallization-decision` and
`crystallization-build` contracts — an investment decision that resolves
ceilings before valuation, values each eligible rung with deflation and
survival discounting plus first-class non-token value, and selects rung,
budget cap, abort rule, and proof obligations under the tenant's
crystallization budget; an episode-mined micro-spec whose acceptance corpus
is the contract, whose scope fence is a requirement artifact, and which
declares an effect class; and a build that is an ordinary governed
codexFactory job with a mandatory provenance manifest, dry-run acceptance
criterion, data-leak scan, and regeneration-first maintenance.
Topics: crystallization-decision, crystallization-build, economics,
automation-ladder, requirements-mining, acceptance-corpus, scope-fence,
effect-class, provenance, codexfactory, release-realization
Repository context: openxFactory (neutral schemas; codexFactory both first
conformer and the cross-domain builder)
Staging ID: `openxFactory:staging:recurrence-crystallization`
Source: brainstorm docs
[economics](../../../../../ideation/brainstorm/crystallization-economics.md),
[automation ladder](../../../../../ideation/brainstorm/crystallization-automation-ladder.md),
[requirements mining](../../../../../ideation/brainstorm/crystallization-requirements-mining.md),
[build pipeline](../../../../../ideation/brainstorm/crystallization-build-pipeline.md),
[Crystallizer synthesis](../../../../../ideation/brainstorm/crystallization-synthesis-crystallizer.md);
rulings D5, D7, D11 (primary doc, 2026-07-29).
Target capabilities: `crystallization-decision` (ADDED),
`crystallization-build` (ADDED)

## The decision contract

A `crystallization_decision` record consumes a candidate and produces
either a funded shape or a recorded not-yet:

- **Evaluation order is fixed**: rung ceilings resolve first (from the
  authority fragment), value is computed per *eligible* rung, and only then
  is a rung selected — the queue never carries phantom ROI (SYB-C2 as
  corrected).
- **Valuation discounts like an investor**: expected savings streams carry
  AI-price deflation and pattern-survival factors (EC-C2 — token savings
  are a melting asset), and non-token value (latency, determinism,
  auditability, compliance, offline) is a first-class term that sometimes
  justifies the build alone (EC-C3).
- **The output is a shape, not a boolean**: target rung, budget cap, abort
  rule, and proof obligations (EC-C4). Declined candidates land in the
  not-yet ledger with reasons and re-nomination conditions (SYB-C1) —
  calibration data either way.
- **Consent surface**: no spend outside the tenant's crystallization
  budget envelope plus the clearance path (auto-clear under the envelope,
  liaison above it) (EC-C5). Tenants start on decision-ladder rungs 1–2
  (human judgment / count threshold); the expected-value rung activates
  once the accounting calibration board has data to trust.

## The spec-mining contract

A `crystallization_spec` (micro-spec, feat-spec-shaped, machine-drafted,
ratification scaled to rung and risk) carries:

- requirements mined as invariants, parameters, branches, and
  counterexamples, each citing episodes (RQ-C1); a corpus without failure
  cases is rejected at intake (RQ-C5);
- the **acceptance corpus as the operative contract**: curated episode
  refs, equivalence predicates per output type (never byte goldens),
  cassettes for `record-replay` steps, all digest-pinned (RQ-C2);
- the **scope fence as a requirement artifact** consumed verbatim by
  dispatch (RQ-C3), derived conservatively from observed support;
- a declared **`effect_class`**: `pure | idempotent | compensable |
  irreversible` (D11) — enforced at dispatch (v1 fences admit only the
  first two);
- regenerability: corpus digest + miner version → the same spec (RQ-C4).

## The build contract

`job_type: crystallization_build` — an ordinary governed engineering job
through existing factory lanes (BP-C1). **D5: codexFactory builds for
every domain; the consuming domain owns fitness gates** (BP-C2 — a named
cross-domain service seam). Hard gates: acceptance corpus green; sandbox
and dependency policy; the generated-code **data-leak scan** (no literal
traceable to tenant episode payloads); authority binding review (subset
rule, authority fragment); **dry-run/simulation mode as a build acceptance
criterion** (BP-C5 — shadow proof depends on it). Provenance manifest
chains capability → spec → corpus → episodes → original runs without gaps
(BP-C3); maintenance is regeneration-first with hand-patches gated as
exceptions that must fold back (BP-C4). Builds run budget-capped with
declared abort behavior; estimate-vs-actual feeds the calibration board.
Release rides `release-realization` (declared `code_surface`, merged +
green realization evidence).

## Rung vocabulary (D7 — frozen)

`automation_rung` is a controlled enum `L0–L6` (cold solve /
recall-assisted / memoized result / frozen playbook / specialist executors /
code with AI edges / pure code), carried by decisions, capability versions,
and dispatch records (AL-C2). Every family carries a reasoned
`rung_ceiling` (AL-C3); default motion is one rung per promotion (AL-C4).
L2 mechanics remain owned by the ontology packet's result-cache brainstorm.

## Open questions carried

Corpus bars' final values (staged defaults in the dials register; RQ-Q1);
playbook artifact residence — workflow-contract instance vs practice-catalog
entry vs new kind (AL-Q2); whether an L1 retrieval tune-up is a mandatory
pre-build stage (AL-Q3); equivalence-predicate signing authority (RQ-Q4 —
the most authority-laden artifact in the chain); artifact packaging and
repo topology (BP-Q1); bench/toolchain allowlist (BP-Q2); maintainer of
record (BP-Q3, pending the Steward role decision SYC-Q1).
