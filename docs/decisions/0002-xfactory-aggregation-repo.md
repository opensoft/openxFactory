# Decision 0002: xFactory Aggregation Repository

Status: ratified
Kind: reference
Decision: accepted

Date: 2026-07-02

## Context

The workspace contains multiple related repositories:

- `openxFactory`, the open reference stack and canonical xFactory contract
  source.
- install or subsystem repositories such as `Hermes-Install`,
  `Omnigent-Install`, and `AgentTower`.
- DomainxFactory repositories such as `MedxFactory`, `LedgerxFactory`,
  `OpsxFactory`, `AdxFactory`, and `codexFactory`.

Earlier docs sometimes treated `openxFactory`, `openWorkflow`, and the
`xFactory layer` as interchangeable. That made repository ownership unclear.
The architecture now distinguishes the stack from the layer:

```text
openxFactory
  open reference stack and canonical contract source

xFactory layer
  domain-neutral contracts, gates, routing, traceability, state, source
  authority, memory promotion, credentials, and audit
```

## Decision

Create and use a top-level `xFactory` aggregation repository to pin workspace
submodules.

The top-level `xFactory` repository owns workspace assembly:

```text
xFactory/
  openxFactory/
  installs/
    hermes-install/
    omnigent-install/
    agenttower/
  xFactories/
    AdxFactory/
    LedgerxFactory/
    MedxFactory/
    OpsxFactory/
    codexFactory/
```

`openxFactory` remains the canonical open reference stack and contract source.
It should not need to pin every DomainxFactory consumer.

Each DomainxFactory must declare the `openxFactory` version, tag, or commit it
consumes. Domain factories upgrade deliberately after compatibility validation.

## Rules

- The top-level `xFactory` repo may pin `openxFactory`, install repos, subsystem
  repos, and DomainxFactory repos as submodules.
- `openxFactory` owns canonical xFactory layer contracts and standards.
- DomainxFactory repos own domain-specific Hermes overlays, memory boundaries,
  Omnigent expert routing, tools, workflows, checks, schemas, examples, and
  enforcement adapters.
- DomainxFactory repos must pin or declare the compatible `openxFactory`
  contract version they consume.
- `openxFactory` changes must preserve compatibility rules and version
  contracts so domain factories are not broken by surprise.
- `openxFactory` should not depend on DomainxFactory submodule pins to be valid.

## Current Remote Decisions

The top-level aggregation repo uses the current reachable remotes:

```text
openxFactory/                 -> git@github.com:opensoft/openxFactory.git
installs/omnigent-install/    -> git@github.com:opensoft/Omnigent-Install.git
installs/hermes-install/      -> git@github.com:FarHeap/Hermes-Install.git
installs/agenttower/          -> git@github.com:opensoft/AgentTower.git
xFactories/AdxFactory/        -> git@github.com:opensoft/AdxFactory.git
xFactories/LedgerxFactory/    -> git@github.com:opensoft/LedgerxFactory.git
xFactories/MedxFactory/       -> git@github.com:opensoft/MedxFactory.git
xFactories/OpsxFactory/       -> git@github.com:opensoft/OpsxFactory.git
xFactories/codexFactory/  -> git@github.com:opensoft/codexFactory.git
```

`opensoft/Hermes-Install` is not currently reachable. If Hermes moves, mirrors,
or forks to Opensoft later, update the parent `xFactory` submodule remote in a
separate reviewed change.

## Consequences

Benefits:

- A complete xFactory workspace can be cloned from one top-level repo.
- `openxFactory` remains stable as the contract source instead of becoming a
  registry of all domain consumers.
- Domain stacks can upgrade `openxFactory` deliberately and validate before
  adoption.
- Install and subsystem repos stay operationally separate while still being
  pinned for release assembly.

Trade-offs:

- Contributors must understand two compatibility mechanisms: submodule pins in
  the top-level aggregation repo and contract version declarations inside each
  DomainxFactory.
- Existing sibling clones must be converted into submodule entries carefully so
  local work is not overwritten.
- The legal domain stack name must be normalized before adding a legal
  submodule. Current templates use `LegalxFactory`; the user may prefer
  `LawxFactory`.
