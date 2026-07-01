# Workflow Contract

This is the required domain-neutral xFactory workflow contract from approved intent through final enforcement.

`openWorkflow` defines the rail. Domain factory repos define the domain-specific execution.

## Required Workflow

1. Approved intent exists in a durable governance/specification record.
2. Hermes approves the intent for decomposition.
3. The appropriate domain factory accepts the approved scope.
4. The domain factory decomposes the scope into bounded, traceable, reviewable work units.
5. openWorkflow/xFactory gates determine which work units are admitted for execution.
6. The domain Omnigent layer runs bounded domain agents under the approved scope.
7. Deterministic checks or domain-specific validation run where applicable.
8. Domain review runs before any external enforcement or clinical/business action.
9. Hermes or the configured governance layer approves admission to the next state.
10. The external enforcement system enforces final state where applicable.
11. Evidence, review records, and traceability artifacts are archived.

## Handoff Rule

OpenSpec or another Hermes-approved intent record is used before domain execution.

```text
Hermes-approved intent
  -> openWorkflow/xFactory contract and gate context
  -> domain factory accepts the work
  -> domain factory decomposes into bounded work units
  -> domain Omnigent executes approved domain work
  -> deterministic/domain validation runs
  -> domain review package is produced
  -> Hermes/governance admits next state
  -> external enforcement system enforces final state where applicable
```

## Domain Specialization

The domain factory decides the agent population and domain artifacts.

```text
codexFactory
  uses Omnigent to run coding and engineering agents
  produces code changes, tests, branch reviews, PR admission packets, and merge readiness evidence

MedxFactory
  uses Omnigent to run clinical and medical reasoning agents
  produces patient-modeling artifacts, diagnostic hypotheses, simulations, reliability assessments, specialist reviews, and clinician review packages
```

The workflow rail remains the same. The domain execution differs.

## Non-Negotiable Gates

- No domain execution starts without approved intent.
- No domain execution starts outside the applicable domain factory boundary.
- No domain agent output becomes authoritative without the required workflow gates.
- No high-risk action proceeds without deterministic gate evaluation where required.
- No external enforcement occurs without a review/admission record.
- No domain-specific runtime data, secrets, credentials, production memory stores, or generated workspaces belong in `openWorkflow`.
- No clinical, engineering, or business final action is owned by openWorkflow itself.

## Initial Admission States

```text
proposed
approved-for-decomposition
decomposed
approved-for-execution
execution-ready
execution-complete
validation-passed
review-passed
approved-for-external-enforcement
enforcement-running
enforcement-blocked
enforcement-complete
archived
```

## Engineering Implementation Pointer

Engineering-specific implementation details live in `opensoft/codexFactory`.

That repo defines coding agents, engineering decomposition, Spec Kit engineering flow, branch review, PR admission, and merge readiness.

## Medical Implementation Pointer

Medical-specific implementation details live in `opensoft/MedxFactory`.

That repo defines clinical agents, patient truth modeling, diagnostic Dream-RAG, Root Truth DBs, simulation, foundational data reliability, specialist pods, and clinician review packages.
