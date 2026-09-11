# Work Decomposition Contract

Status: draft

`openxFactory` is domain-neutral. This document defines the neutral requirement that approved work must be decomposed into bounded, traceable work units before domain execution.

Engineering-specific feature decomposition now lives in:

- `codeXfactory/codexFactory/docs/feature-decomposition-traceability.md`

## Neutral Requirement

Approved work must be decomposed into work units that are:

```text
bounded
traceable
reviewable
routable
gated
auditable
safe to validate within the domain workflow
```

## Domain Specialization

Different domain factories interpret work units differently.

```text
codexFactory
  decomposes software work into engineering features, tasks, tests, branch changes, and PR-ready slices.

MedxFactory
  decomposes medical work into patient issues, hypotheses, simulation scenarios, specialist pod reviews, and clinician review packages.
```

## openxFactory Ownership

openxFactory owns:

```text
the requirement to decompose approved work
the requirement to preserve traceability
the gate that blocks execution until decomposition is complete
the audit expectation that work units map back to approved intent
```

Domain factory repos own the domain-specific decomposition doctrine.
