# Architecture

This project defines a domain-neutral xFactory workflow rail.

`openWorkflow` is not the engineering factory, the medical factory, or any other domain factory. It defines the contract, gate, traceability, routing, state, and audit model that domain factory repos use.

## Roles

### Hermes

Hermes is the governance and memory layer.

Hermes owns:

- intent approval
- policy authority
- memory and durable governance history
- portfolio or domain governance context
- approval control
- cross-project or cross-domain dashboards
- OpenSpec-managed change state
- review coordination

Hermes may read domain execution artifacts for status and traceability, but Hermes does not run domain agent implementation work directly.

### OpenSpec

OpenSpec is the durable spec-change ledger used by Hermes.

OpenSpec owns:

- current system specifications
- proposed changes
- change proposals
- delta requirements
- design notes
- implementation task intent
- archive history after accepted changes

OpenSpec remains the source of truth for approved requirement change intent.

### openWorkflow / xFactory

openWorkflow/xFactory is the domain-neutral workflow rail.

It owns:

- workflow contracts
- gate definitions
- state transitions
- traceability expectations
- routing contracts
- admission records
- review record requirements
- audit expectations
- handoff boundaries between governance, execution, and enforcement systems

openWorkflow does not define the domain-specific agent population. Domain factory repos define that.

### Domain Factory Repos

Domain factory repos specialize the neutral workflow rail for a domain.

Examples:

```text
opencodexFactory
  software, code, repository, and engineering workflows
  Omnigent runs coding and engineering agents

MedxFactory
  clinical, medical, patient, and diagnostic workflows
  Omnigent runs clinical and medical reasoning agents
```

A domain factory owns:

- domain-specific execution model
- domain-specific DocTypes or artifacts
- domain-specific agent population
- domain-specific validation outputs
- domain-specific review package shape
- domain-specific implementation guidance

### Domain Omnigent Layer

A domain Omnigent layer executes bounded domain work under Hermes policy and openWorkflow gates.

It may produce:

- proposals
- assessments
- simulations
- implementation artifacts
- review packets
- summaries
- traceability artifacts

It must not own:

- Hermes approval authority
- domain-neutral workflow contracts
- final clinical, business, or governance decisions
- final external enforcement controls

### External Enforcement Systems

External enforcement systems own final enforcement where applicable.

Examples:

```text
GitHub branch protection and merge queue for engineering repositories
clinical chart/order systems for medical workflows
compliance systems for regulated review records
```

The enforcement system depends on the domain.

## Authority Model

```text
Hermes + OpenSpec
  owns intent, policy, approval, memory, and change history

openWorkflow / xFactory
  owns contracts, gates, traceability, routing, state transitions, and audit rail

Domain factory repo
  owns domain-specific execution interpretation

Domain Omnigent layer
  executes bounded domain agent work under policy and gates

External enforcement system
  owns final enforcement where applicable
```

## Domain Examples

```text
opencodexFactory
  openWorkflow rail + engineering policy + coding agents + repo enforcement

MedxFactory
  openWorkflow rail + medical policy + clinical agents + clinician review
```

The two domain factories share workflow structure, but not domain artifacts or agent populations.
