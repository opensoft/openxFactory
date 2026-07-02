# Spec Kit Engineering Flow Pointer

`openxFactory` is domain-neutral and no longer owns the engineering-specific Spec Kit stage ownership policy.

Spec Kit is a software engineering feature-flow implementation and now belongs in `codexFactory`.

Canonical engineering-domain documentation:

- `opensoft/codexFactory/docs/spec-kit-engineering-flow.md`

## Neutral openxFactory Rule

openxFactory owns only the neutral sequence:

```text
approved intent
  -> decomposition gate
  -> domain execution gate
  -> validation gate
  -> review gate
  -> enforcement/admission gate
```

Domain factories decide which implementation mechanism runs inside the domain execution gate.

```text
codexFactory
  may use Spec Kit for software feature flow.

MedxFactory
  uses clinical issue, hypothesis, simulation, and specialist-review workflows instead.
```
