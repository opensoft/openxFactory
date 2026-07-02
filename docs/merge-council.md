# Readiness Review Council

`openxFactory` is domain-neutral. This document defines the neutral readiness-review concept that domain work should receive a documented readiness decision before final enforcement or high-risk action.

Engineering-specific merge council and merge readiness behavior now lives in:

- `opensoft/codexFactory/docs/pr-admission-merge-readiness.md`

## Neutral Readiness Rule

```text
validated domain work product
  -> readiness evidence collected
  -> unresolved risks summarized
  -> responsible review body evaluates readiness
  -> readiness record is written
  -> external enforcement or domain authority proceeds only if admitted
```

## Domain Examples

```text
codexFactory
  readiness review evaluates whether a pull request or repository change is ready to merge.

MedxFactory
  readiness review evaluates whether a clinical reasoning package is ready for clinician review, specialist escalation, or other governed clinical workflow step.
```

## Required Readiness Record

A readiness record should include:

```text
work product identifier
approved-scope reference
validation evidence
review participants or reviewing service
unresolved risks
readiness decision
next-state recommendation
audit timestamp
```

## openxFactory Ownership

openxFactory owns the generic readiness-review contract. Domain factory repos own the domain-specific evidence and review body details.
