# Domain Omnigent Execution Boundary

Status: draft

`openxFactory` is domain-neutral and no longer owns an engineering-specific Omnigent/Polly constitution.

## Neutral Rule

Domain Omnigent layers execute bounded domain work under Hermes policy and openxFactory/xFactory gates.

```text
Hermes
  owns intent, policy, approval, memory, and governance history.

openxFactory / xFactory
  owns contracts, gates, traceability, routing, state transitions,
  memory/knowledge provider bindings, and audit.

Domain Omnigent layer
  executes bounded domain work under the approved contract.
```

## Memory And Expert Knowledge

Domain Omnigent workers do not attach directly to authoritative expert memory,
root-truth DBs, vector indexes, graph stores, source workspaces, case-pattern
stores, playbooks, or evaluation memory for governed work.

They request bounded expert context through `xfactory.memory.context_packet`.
The xFactory Memory Gateway verifies caller identity, expert profile, workflow
purpose, provider binding, source-authority policy, allowed knowledge scope,
usage/audit policy, and migration route before provider I/O. Direct provider
access is limited to read-only, operator-scoped, non-production or shadow
diagnostics and can never create authoritative expert context.

## Domain Implementations

Engineering-specific Omnigent rules now live in:

- `codeXfactory/codexFactory/docs/engineering-omnigent-constitution.md`
- `codeXfactory/codexFactory/docs/omnigent-coding-agent-workflow.md`

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
