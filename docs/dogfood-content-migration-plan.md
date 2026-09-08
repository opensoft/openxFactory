# Domain Neutralization and Engineering Content Migration Plan

Status: draft

This plan defines how `openxFactory` remains domain-neutral while engineering-specific workflow content moves to `codeXfactory/codexFactory`.

## Principle

```text
openxFactory
  owns domain-neutral contracts, gates, traceability, routing, state transitions, and audit.

codexFactory
  owns coding and engineering agents, Spec Kit engineering flow, branch review, PR admission, merge readiness, and repo-centered engineering workflow.

MedxFactory
  owns clinical and medical reasoning agents, patient modeling, diagnostic dreams, simulation, and clinician review workflows.
```

Do not treat `openxFactory` as the software engineering factory. It is the neutral workflow rail used by multiple domain factories.

## Migration Rule

Use copy-first migration.

```text
1. Create or update the engineering-domain canonical copy in codexFactory.
2. Replace the openxFactory copy with a domain-neutral contract or pointer.
3. Preserve source references and audit history.
4. Do not move secrets, credentials, runtime state, databases, generated workspaces, or production memory stores.
5. Do not delete legacy source docs in the same change that creates canonical domain copies unless explicitly approved.
```

## Target Repositories

```text
openxFactory
  target role: domain-neutral workflow substrate

codexFactory
  target role: engineering xFactory implementation

MedxFactory
  target role: medical xFactory implementation
```

## Completed / Current Engineering Split

The first engineering-domain docs were created in `codeXfactory/codexFactory`:

```text
docs/engineering-xfactory-domain.md
docs/engineering-omnigent-constitution.md
docs/omnigent-coding-agent-workflow.md
docs/spec-kit-engineering-flow.md
docs/feature-decomposition-traceability.md
docs/pr-admission-merge-readiness.md
docs/engineering-worker-model.md
```

Core `openxFactory` docs were rewritten or narrowed to domain-neutral contracts:

```text
README.md
docs/architecture.md
docs/workflow-contract.md
docs/omnigent-constitution.md
docs/feature-decomposition.md
docs/spec-kit-stage-ownership.md
docs/pr-admission.md
docs/merge-council.md
docs/merge-master.md
docs/deployment-worker-model.md
```

## Remaining Migration Slices

### FEAT-XFACTORY-001: Engineering examples and proof harnesses

Move repo-centered examples and proof harnesses to `codexFactory` or mark them as legacy references.

Candidate source paths:

```text
openxFactory/examples/
openxFactory/openspec/changes/archive/*/evidence/*pr*
openxFactory/openspec/changes/archive/*/evidence/*merge*
```

Acceptance criteria:

```text
engineering examples live in codexFactory
openxFactory keeps only domain-neutral examples or pointers
no generated runtime state is moved
```

### FEAT-XFACTORY-002: Contract split

Review `openxFactory/contracts` and separate neutral workflow contracts from engineering-specific schemas.

Acceptance criteria:

```text
neutral contracts remain in openxFactory
engineering-specific contracts move to codexFactory
contract provenance is preserved
```

### FEAT-XFACTORY-003: Archived OpenSpec cleanup

Archived OpenSpec evidence may remain as history, but README and active docs should not point to engineering-specific archived material as current canonical policy.

Acceptance criteria:

```text
history remains auditable
current canonical links point to domain-neutral openxFactory docs or engineering codexFactory docs
```

### FEAT-XFACTORY-004: Install repo pointer cleanup

Install repo docs should point to either:

```text
openxFactory for neutral workflow contracts
codexFactory for engineering execution
MedxFactory for medical execution
```

## Stop Conditions

Stop and return to Hermes approval if any migration step:

```text
touches secrets, credentials, production memory, databases, or generated workspaces
moves runtime code while only a documentation split is approved
changes submodule pointers without explicit approval
removes historical audit evidence
changes domain authority boundaries without approval
```

## Success Criteria

The split is complete when:

```text
openxFactory reads as domain-neutral
codexFactory owns software engineering implementation docs
MedxFactory owns medical implementation docs
openxFactory points to domain factories instead of embedding their execution details
Frappe, vector DBs, agents, and repo tools are not treated as authority layers
```
