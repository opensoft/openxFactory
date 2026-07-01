# Architecture

This project defines the open reference stack for the xFactory family and the
domain-neutral xFactory layer inside that stack.

`openxFactory` is not the engineering factory, the medical factory, or any other
domain factory. It defines the open reference stack and canonical contracts that
domain factory repos consume.

The `xFactory layer` is the layer inside `openxFactory` and every DomainxFactory
that defines the contract, gate, traceability, routing, state, source authority,
memory promotion, credential, and audit model.

The top-level `xFactory` repository is an aggregation repo that pins
`openxFactory`, subsystem install repos, and DomainxFactory repos as submodules.
See [Terminology And Repository Topology](terminology-and-repo-topology.md) and
[Decision 0002](decisions/0002-xfactory-aggregation-repo.md).

The first product domain stack repositories are expected to be
`opensoft/MedxFactory`, `opensoft/OpsxFactory`, `opensoft/LedgerxFactory`,
`opensoft/AdxFactory`, and `opensoft/codexFactory`.

Credential access across those domain stacks is governed by the
[xFactory Credential Access Model](credential-access-model.md). Domain repos
declare credential requirements, clients bind those requirements to real secret
providers, Hermes approves runtime use, and Omnigent workers receive only
short-lived scoped grants.

Hermes Mixture of Agents reasoning is governed by
[Hermes Mixture Of Agents For xFactory](hermes-mixture-of-agents-for-xfactory.md).
Mixture of Agents is a Hermes reasoning pattern, not a new execution authority:
reference agents advise, the acting Hermes role synthesizes, Hermes gates
decide, the xFactory layer enforces, and Omnigent workers execute bounded work.

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

Hermes may use Mixture of Agents presets inside a domain, client, or customer
Hermes layer. A mix can improve reasoning quality by collecting independent
reference-agent opinions and synthesizing them through an acting Hermes role.
The mix output is evidence or recommendation only until the owning Hermes gate,
review council, accountable human, or external enforcement system approves the
next transition.

The native Hermes pattern is `panel_synthesis`. xFactory adds `scored_vote` and
`deliberative_council` protocols when the domain needs explicit scoring,
rebuttal rounds, consensus, dissent records, and audit-grade review.

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

### xFactory Layer

The xFactory layer is the domain-neutral workflow rail inside `openxFactory` and
inside every DomainxFactory.

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

The xFactory layer does not define the domain-specific agent population. Domain
factory repos define that.

### DomainxFactory Repos

DomainxFactory repos are instantiated domain stacks that consume `openxFactory`
contracts and specialize the xFactory layer for a domain.

Examples:

```text
codexFactory
  software, code, repository, and engineering workflows
  Omnigent runs coding and engineering agents

MedxFactory
  clinical, medical, patient, and diagnostic workflows
  Omnigent runs clinical and medical reasoning agents

OpsxFactory
  sysops, devops, IT administration, identity, infrastructure, and tenant operations
  Omnigent runs IT operations agents
```

A domain factory owns:

- domain-specific execution model
- domain-specific DocTypes or artifacts
- domain-specific agent population
- domain-specific validation outputs
- domain-specific review package shape
- domain-specific implementation guidance

### Domain Omnigent Layer

A domain Omnigent layer executes bounded domain work under Hermes policy and
xFactory layer gates.

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

xFactory layer
  owns contracts, gates, traceability, routing, state transitions, and audit rail

DomainxFactory repo
  owns domain-specific execution interpretation

Domain Omnigent layer
  executes bounded domain agent work under policy and gates

External enforcement system
  owns final enforcement where applicable
```
## Domain Examples

```text
codexFactory
  xFactory layer + engineering policy + coding agents + repo enforcement

MedxFactory
  xFactory layer + medical policy + clinical agents + clinician review

OpsxFactory
  xFactory layer + operations policy + IT agents + privileged action review
```

The two domain factories share workflow structure, but not domain artifacts or agent populations.
