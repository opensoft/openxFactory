# Architecture

This project designs a multi-project AI software development factory.

## Roles

### Hermes

Hermes is the portfolio and governance layer.

Hermes owns:

- portfolio and project management
- policy
- memory
- approval control
- cross-project dashboards
- OpenSpec-managed change state
- merge council coordination

Hermes may read Spec Kit artifacts for status and traceability, but Hermes does not run Spec Kit implementation commands.

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

### Omnigent/Polly

Omnigent is the repo-level agent orchestration platform.

Polly is the engineering orchestrator inside Omnigent. Polly plans engineering work, decomposes approved scope into small orthogonal features, delegates implementation to coding agents, runs deterministic checks, and coordinates local branch review before PR creation.

Polly owns:

- repo-level engineering decomposition
- feature dependency DAGs
- traceability artifacts
- branch preparation
- local deterministic checks
- local pre-PR branch review
- PR creation after admission

### Spec Kit

Spec Kit is the feature-level development process used by Omnigent/Polly.

Spec Kit owns:

- feature specification
- clarification
- implementation planning
- generated tasks
- pre-implementation analysis
- task execution by coding agents

Spec Kit is not the portfolio source of truth. It consumes Hermes-approved OpenSpec scope.

### GitHub

GitHub is the canonical enforcement layer.

GitHub owns:

- pull requests
- status checks
- branch protection
- merge queue
- code review records
- final merge enforcement

## Authority Model

```text
Hermes + OpenSpec
  owns intent, approval, portfolio policy, and change history

Omnigent/Polly + Spec Kit
  owns repo execution, feature planning, implementation, and local review

GitHub
  owns PR state, protected branch policy, and final merge enforcement
```

