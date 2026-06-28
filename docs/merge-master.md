# Enforcement Action Controller

`openWorkflow` is domain-neutral. This document defines the neutral concept of converting a readiness decision into the next allowed enforcement or action state.

Engineering-specific Merge Master behavior now lives in:

- `opensoft/opencodexFactory/docs/pr-admission-merge-readiness.md`

## Neutral Rule

A readiness decision may produce one of several next-state actions:

```text
proceed
block
request changes
request more evidence
route to human review
allow emergency or exceptional override when policy permits
archive as rejected or superseded
```

The action controller must not bypass the external enforcement system or domain authority.

## Domain Examples

```text
opencodexFactory
  converts merge readiness into repository review, merge, block, or request-change posture.

MedxFactory
  converts clinical package readiness into clinician review, specialist escalation, reverification, or block posture.
```

## openWorkflow Ownership

openWorkflow owns the generic mapping between readiness states and next workflow states.

Domain factory repos own the specific enforcement/action details.
