# Recursive Inference Domain Pilots — Brainstorm

Status: brainstorm
Kind: plan
Summary: codexFactory is the safest first recursive-inference pilot, with progressively stricter later experiments in OpsxFactory, LedgerxFactory, and MedxFactory only after task-specific quality, coverage, privacy, and disclosure gates are proven.
Topics: governed-recursive-inference, domain-pilots, codexfactory, opsxfactory, ledgerxfactory, medxfactory, evaluation, rollout, councils, feat-request
Repository context: openxFactory (cross-domain pilot ladder); codexFactory (first domain fixtures); Omnigent-Install (runtime); later DomainxFactory consumers
Captured: 2026-07-30

## Possible feats

- **codexFactory recursive-evidence pilot** — evaluate cross-repository and
  cross-artifact analysis on low-sensitivity engineering corpora.
- **Recursive pilot conformance packet** — require baseline comparisons,
  quality/coverage evidence, safety posture, and cost results before activation.
- **Domain adoption ladder** — separate exploratory, governed, and
  high-assurance recursive task classes.
- **Council evidence-compiler pattern** — create one cited recursive evidence
  packet before independent Hermes council review.

## Focus

This document isolates adoption order and candidate workloads. Recursive
inference should not be enabled family-wide because domains differ sharply in
data sensitivity, verification strength, terminal consequences, and the cost
of missed evidence.

The first pilot should maximize measurable long-context difficulty while
minimizing privacy and authority risk.

## First pilot: codexFactory

Candidate workloads:

1. **Cross-repository release-impact analysis**
   - input: pinned repository/file manifests across the xFactory family;
   - output: typed dependency and impact findings with complete coverage;
   - validation: known dependency edges, changed-path fixtures, and reviewer
     adjudication.

2. **Large PR evidence synthesis**
   - input: base/head diff, codebase slices, review threads, CI, and contract
     refs;
   - output: cited findings and unresolved-risk packet;
   - validation: seeded defects and comparison with existing PR-review lanes.

3. **OpenSpec/Speckit cross-artifact consistency**
   - input: spec, plan, tasks, implementation evidence, and relevant code;
   - output: missing, conflicting, and unsupported requirement mappings;
   - validation: deterministic link/schema checks plus seeded semantic defects.

4. **Corpus-wide contradiction and supersession discovery**
   - input: brainstorm, staging, proposal, promoted spec, contract, and README
     manifests;
   - output: candidate contradictions with lifecycle and provenance;
   - validation: known historical transitions and human disposition.

5. **Repository architecture map**
   - input: large code/docs corpus;
   - output: component/dependency map with evidence and coverage;
   - validation: build manifests, package graphs, and maintainer review.

The initial choice should favor a task with a stable accepted-output set and
seedable failures. Cross-repository release impact or Speckit consistency may
offer the cleanest ground truth.

## Initial pilot posture

```text
domain: codexFactory
data: public, synthetic, or engineering-internal without secrets
runtime: isolated typed combinators
depth: one
children: approved frame/generate/verify profiles only
coverage: targeted and complete variants evaluated separately
models: strong-root/cheap-leaf and homogeneous baselines
cache: compiled context only; no cross-request result reuse
terminal output: assemble-for-admission artifact
approval: existing Hermes/human review
```

Exit evidence would include:

- comparison with direct, retrieval, and deterministic baselines;
- quality, coverage, false-confidence, and correction measures;
- per-branch and total cost/latency;
- sandbox and authority-subset tests;
- prompt-injection and scope-escape fixtures;
- trajectory/replay inspection;
- explicit failure and partial-result behavior;
- operator assessment of debuggability.

## Later domain candidates

### OpsxFactory

Promising tasks:

- incident timeline construction over logs, configuration, tickets, and
  runbooks;
- fleet-wide drift analysis;
- change-impact review across managed nodes.

Risks:

- operational secrets and credentials in logs;
- volatile evidence;
- pressure to let analysis cross into privileged action.

The output should remain a review packet; privileged execution stays behind
Opsx gates and external enforcement.

### LedgerxFactory

Promising tasks:

- large reconciliation exception discovery;
- audit-support evidence assembly;
- policy and filing cross-reference analysis.

Risks:

- complete-coverage claims;
- financial confidentiality;
- numeric reduction errors;
- downstream reliance on apparently precise totals.

Deterministic accounting tools should perform arithmetic; recursive workers
should locate, classify, reconcile evidence, and expose exceptions.

### MedxFactory

Promising later tasks:

- longitudinal evidence and timeline assembly;
- guideline/source-corpus comparison;
- missing-evidence and contradiction discovery;
- convergence-packet preparation.

Non-goals:

- autonomous diagnosis;
- order signing or chart mutation;
- unrestricted patient-record or knowledge-provider access.

Medx adoption would require consent and subject-safety rails, approved provider
and residency posture, exact disclosure accounting where required, provenance
and complete-coverage evidence, independent challenge, and clinician-owned
decision.

## Councils and Hermes reasoning

Three patterns are possible:

### RLM before council

One governed recursive worker compiles a cited evidence packet; independent
council members review the same bounded packet. This is the leading pattern
because it controls corpus access and makes disagreement comparable.

### RLM per council member

Each reference agent independently explores the authorized corpus. This may
improve independence but multiplies cost, provider disclosure, and incomparable
coverage paths.

### RLM as acting synthesizer

The acting Hermes role uses recursive inference to inspect reference outputs
and evidence. This risks blurring advisory execution with Hermes decision
reasoning unless the output remains explicitly recommendation-only.

Early pilots should use RLM before council.

## Repository realization map

| Repository | Candidate responsibility |
| --- | --- |
| openxFactory | neutral contracts, invariants, examples, and conformance |
| Omnigent-Install | recursive runtime, sandbox, child-call broker, evidence capture |
| codexFactory | first worker profiles, prompts, task classes, fixtures, and evals |
| OpsxFactory | sandbox/worker-host and later operational domain adaptation |
| LedgerxFactory | financial evidence and coverage specialization |
| MedxFactory | clinical safety, consent, source, and human-gate specialization |
| xFactory aggregation | compatible version pins and cross-repo pilot corpus |

## Alternatives and tensions

- A generic synthetic benchmark is safer but may not predict real xFactory
  utility.
- A real cross-repo task gives immediate value but has evolving ground truth.
- Starting with a PR review leverages mature review lanes but may conflate RLM
  benefit with existing multi-agent expertise.
- Running the first pilot in Omnigent-Install alone proves infrastructure but
  not domain effectiveness.
- Council integration is compelling but should not precede basic evidence and
  cost validation.

## Open questions

- Which codexFactory workload has the best accepted ground truth and enough
  corpus size to expose a real RLM advantage?
- Should the first pilot use the official RLM library behind a strict sandbox,
  a minimal custom harness, or a typed combinator prototype?
- What threshold counts as success over the strongest non-recursive baseline?
- Which repository owns pilot evaluation datasets and sensitive execution
  traces?
- How many accepted runs are required before a governed task class activates?
- What specific evidence would justify moving from codexFactory to OpsxFactory
  or LedgerxFactory?

## Relationships

- [Recursive Strategy Routing](governed-recursive-inference-strategy-routing.md)
  defines when a pilot may choose recursive execution.
- [Model Topology and Economics](governed-recursive-inference-model-topology-and-economics.md)
  defines baseline and cost comparison.
- [Evidence and Coverage](governed-recursive-inference-evidence-coverage.md)
  defines acceptance evidence.
- [Medical Omnigent Harness Adaptation](medical-omnigent-harness-adaptation.md)
  supplies the later Medx authority and verification boundary.
- [Synthesis: Adoption and Councils](governed-recursive-inference-synthesis-adoption-and-councils.md)
  connects pilots to xFactory governance.

