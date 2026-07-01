# Terminology And Repository Topology

Status: shared xFactory standard
Repository context: openxFactory
Purpose: distinguish the xFactory layer from the openxFactory reference stack
and from domain-specific DomainxFactory stacks.

## Core Terms

`xFactory` names the overall product family and repository aggregation space.
The top-level `xFactory` repository is a coordination repo. It pins compatible
stack, install, and domain repositories as submodules so a complete workspace
can be cloned and inspected at known revisions.

`openxFactory` names the open reference stack and contract source. It contains
the domain-neutral xFactory layer plus shared standards for Hermes, memory,
Omnigent, AgentTower, credentials, source authority, traceability, and domain
factory scaffolding.

`xFactory layer` names the domain-neutral layer inside `openxFactory` and every
DomainxFactory. It owns the generic contract for job envelopes, gates, routing,
traceability, state transitions, audit, source authority, memory promotion, and
handoff boundaries.

`DomainxFactory` names an instantiated domain stack that consumes
`openxFactory` contracts and specializes them for one kind of expert work.
Examples include `MedxFactory`, `LawxFactory` or `LegalxFactory`,
`LedgerxFactory`, `OpsxFactory`, `AdxFactory`, and `codexFactory`.

## Repository Layers

```text
xFactory repository
  top-level aggregation repo
  pins compatible stack, install, and domain repos

  openxFactory/
    open reference stack and canonical domain-neutral contracts

  installs/
    hermes-install/
    omnigent-install/
    agenttower/

  xFactories/
    MedxFactory/
    LegalxFactory or LawxFactory/
    LedgerxFactory/
    OpsxFactory/
    AdxFactory/
    codexFactory/
```

The top-level `xFactory` repo is allowed to know about all submodules because
its job is workspace assembly and version pinning.

`openxFactory` should not need to pin DomainxFactory repos. A domain stack must
know which `openxFactory` version it consumes, but `openxFactory` should not
need to know which domain stack versions exist or are deployed.

## Stack Versus Layer

`openxFactory` is a stack.

It may document, standardize, or pin pieces such as:

- Hermes and Hermes memory-provider contracts
- Omnigent execution contracts
- AgentTower integration contracts
- xFactory workflow, gate, traceability, audit, and credential standards
- domain factory starter surfaces
- source authority and memory promotion standards

The `xFactory layer` is one layer inside that stack.

It owns:

- workflow contracts
- job envelopes
- gates and admission states
- state transitions
- traceability edges
- routing contracts
- source authority levels
- memory and policy promotion contracts
- credential grant contracts
- review records
- audit records
- handoff boundaries between governance, execution, and enforcement systems

The `xFactory layer` does not own domain truth, customer truth, raw memory
stores, production credentials, domain agent behavior, or final external
enforcement.

## DomainxFactory Compatibility Direction

Compatibility flows from each DomainxFactory to `openxFactory`.

```text
DomainxFactory stack.yaml
  -> pins consumed openxFactory repo, tag, version, or commit
  -> declares which xFactory contract set it implements
  -> specializes Hermes, memory, Omnigent, tools, workflows, checks, and outputs
```

The reverse should not be required.

```text
openxFactory
  should not need to pin MedxFactory, LegalxFactory, LedgerxFactory, OpsxFactory,
  AdxFactory, or codexFactory to remain valid.
```

This direction protects domain factories from accidental breakage. An
`openxFactory` change may introduce a new contract version, but a DomainxFactory
continues to run against its pinned compatible version until it explicitly
upgrades and validates.

## DomainxFactory Internal Shape

A DomainxFactory contains its own xFactory layer binding plus domain-specific
overlays.

```text
DomainxFactory
  xFactory layer binding
    consumed openxFactory version
    contract compatibility declaration
    gate and traceability implementation

  Domain Hermes
    reusable domain policy, memory boundaries, source authority, review rules

  Client Hermes
    tenant policy, local integrations, staff, credentials, client memory

  Customer Hermes
    customer-specific memory, consent, preferences, journey state

  Domain Omnigent
    expert routing, workers, tools, validation, output templates

  Enforcement adapters
    domain-specific systems that enforce final state
```

## Submodule Policy

Use submodules at the top-level `xFactory` repo for workspace aggregation and
known-good release assembly.

Use version declarations inside DomainxFactory repos for contract compatibility.

Do not use `openxFactory` submodules to pin every DomainxFactory. That would
invert the ownership direction and make the contract source depend on its
consumers.

## Naming Notes

`DomainxFactory` is the generic placeholder name. Concrete repos should use
product names:

| Domain | Preferred concrete stack name |
| --- | --- |
| Medical | `MedxFactory` |
| Legal | `LegalxFactory` or `LawxFactory`, choose one canonical repo name |
| Accounting / finance | `LedgerxFactory` |
| IT operations | `OpsxFactory` |
| Marketing / advertising | `AdxFactory` |
| Software engineering | `codexFactory` |

The legal stack currently appears in intake templates as `LegalxFactory`.
If `LawxFactory` is preferred, update the intake templates, taxonomy docs, and
submodule names together so the repo has one canonical legal stack name.
