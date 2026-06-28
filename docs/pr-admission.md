# External Admission Contract

`openWorkflow` is domain-neutral. This document defines the neutral admission concept: a domain work product must not advance to external enforcement until required evidence and review gates are satisfied.

Engineering-specific PR admission now lives in:

- `opensoft/opencodexFactory/docs/pr-admission-merge-readiness.md`

## Neutral Admission Rule

```text
domain work product complete
  -> validation evidence collected
  -> domain review completed
  -> admission packet prepared
  -> governance/admission gate passed
  -> external enforcement system invoked where applicable
```

## Domain Examples

```text
opencodexFactory
  PR admission controls whether an implementation branch may open or proceed as a repository pull request.

MedxFactory
  clinical admission controls whether a diagnostic package, treatment review, or clinician-facing recommendation may proceed to clinician review.
```

## openWorkflow Ownership

openWorkflow owns:

```text
admission state vocabulary
required evidence concept
traceability requirement
review record requirement
handoff to external enforcement or domain authority
```

Domain factories own the domain-specific admission packet format and execution details.
