# openWorkflow

`openWorkflow` documents the domain-neutral xFactory workflow rail used by Opensoft domain factory projects.

It defines reusable contracts for:

- workflow gates
- state transitions
- traceability
- routing
- approval handoffs
- review records
- audit expectations
- authority boundaries between governance, workflow, execution, and enforcement layers

## Core Boundary

`openWorkflow` is domain-neutral.

```text
Hermes
  owns intent, policy, memory, approval, and governance history.

openWorkflow / xFactory
  owns contracts, gates, traceability, routing, state transitions, and audit.

Domain factory repos
  own domain-specific execution behavior.

Domain Omnigent layers
  run bounded domain agents under Hermes policy and openWorkflow gates.

External enforcement systems
  enforce final state where applicable.
```

Domain examples:

```text
opencodexFactory
  uses Omnigent to run coding and engineering agents.

MedxFactory
  uses Omnigent to run clinical and medical reasoning agents.
```

## Documentation

Core domain-neutral docs:

- [Architecture](docs/architecture.md)
- [xFactory Domain Factory Model](docs/xfactory-domain-factory-model.md)
- [Domain Factory Implementation Checklist](docs/domain-factory-implementation-checklist.md)
- [Workflow Contract](docs/workflow-contract.md)
- [Traceability Model](docs/traceability-model.md)
- [Roles and Authority](docs/roles-and-authority.md)
- [Repository Boundary Governance](openspec/specs/repo-boundary-governance/spec.md)
- [Shared Contract Ownership](openspec/specs/shared-contract-ownership/spec.md)

Engineering-domain implementation docs now belong in `opensoft/opencodexFactory`.

Medical-domain implementation docs belong in `opensoft/MedxFactory`.

## Domain Implementations

- `opensoft/opencodexFactory` — software, code, repo, and engineering xFactory domain stack.
- `opensoft/MedxFactory` — medical xFactory domain stack for clinical agents and medical workflows.

## OpenSpec Records

Active changes:

```text
none
```

Archived changes:

- [restructure-factory-repo-boundaries](openspec/changes/archive/2026-06-26-restructure-factory-repo-boundaries/proposal.md)
- [migrate-canonical-policy-to-openworkflow](openspec/changes/archive/2026-06-26-migrate-canonical-policy-to-openworkflow/proposal.md)

Canonical specs:

- [canonical-contract-migration](openspec/specs/canonical-contract-migration/spec.md)
- [canonical-policy-migration](openspec/specs/canonical-policy-migration/spec.md)
- [reference-proof-placement](openspec/specs/reference-proof-placement/spec.md)
- [repo-boundary-governance](openspec/specs/repo-boundary-governance/spec.md)
- [shared-contract-ownership](openspec/specs/shared-contract-ownership/spec.md)

## Install Repo Pins

`openWorkflow` pins approved install repo revisions under `installs/` when needed.

Current submodules:

- [installs/omnigent-install](installs/omnigent-install) -> `opensoft/Omnigent-Install`

Clone or refresh with:

```bash
git submodule update --init --recursive
```

Hermes install is not yet a submodule. Its canonical remote decision is still open; see [Decision 0001](docs/decisions/0001-install-repo-submodules.md).

## Status

This repository is documentation-first. It should not contain live credentials, production memory-provider databases, runtime secrets, generated agent workspaces, or domain-specific runtime data.
