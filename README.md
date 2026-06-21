# openWorkflow

`openWorkflow` documents the AI software development factory used by Opensoft and related Hermes-managed projects.

The factory combines:

- Hermes for portfolio governance, policy, memory, approvals, and dashboards.
- OpenSpec for managed specification changes and durable requirements history.
- Omnigent/Polly for repo-level engineering orchestration.
- Spec Kit for feature-level implementation flow.
- GitHub for pull requests, status checks, branch protection, merge queue, and final merge enforcement.

## Core Boundary

OpenSpec belongs to Hermes.

Spec Kit belongs to Omnigent/Polly.

Hermes decides what is approved to pursue. Polly decides how approved engineering work is decomposed and executed. Spec Kit is used only after a feature has passed Hermes approval and Polly has accepted the feature for implementation.

## Documentation

- [Omnigent Constitution](docs/omnigent-constitution.md)
- [Architecture](docs/architecture.md)
- [Workflow Contract](docs/workflow-contract.md)
- [Traceability Model](docs/traceability-model.md)
- [Feature Decomposition Standard](docs/feature-decomposition.md)
- [Deployment and Worker Model](docs/deployment-worker-model.md)
- [Merge Council and Readiness Reports](docs/merge-council.md)

## Status

This repository is documentation-first. It should not contain live credentials, production memory-provider databases, runtime secrets, or generated agent workspaces.
