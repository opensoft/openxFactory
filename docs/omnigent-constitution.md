# Domain Omnigent Execution Boundary

`openxFactory` is domain-neutral and no longer owns an engineering-specific Omnigent/Polly constitution.

## Neutral Rule

Domain Omnigent layers execute bounded domain work under Hermes policy and openxFactory/xFactory gates.

```text
Hermes
  owns intent, policy, approval, memory, and governance history.

openxFactory / xFactory
  owns contracts, gates, traceability, routing, state transitions, and audit.

Domain Omnigent layer
  executes bounded domain work under the approved contract.
```

## Domain Implementations

Engineering-specific Omnigent rules now live in:

- `opensoft/codexFactory/docs/engineering-omnigent-constitution.md`
- `opensoft/codexFactory/docs/omnigent-coding-agent-workflow.md`

Medical-specific Omnigent rules live in:

- `opensoft/MedxFactory`

## Boundary

```text
codexFactory
  uses Omnigent to run coding and engineering agents.

MedxFactory
  uses Omnigent to run clinical and medical reasoning agents.
```

`openxFactory` keeps only the domain-neutral authority boundary.
