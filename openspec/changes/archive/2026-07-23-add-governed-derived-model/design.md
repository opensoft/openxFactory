# Design record: add-governed-derived-model

Realization-phase decisions (2026-07-23), resolving the open questions
carried from the staging topic (see `supporting-docs/governed-derived-model.md`):

## Declaration home: standalone `models/derived-model-conformance.yaml`

The staging lean was a `derived_models:` block in the domain's
`stack.yaml`, but that requires a MODIFIED delta to
`xfactory-domain-stack.schema.yaml`, which this change does not declare.
The declaration is therefore a standalone domain-owned document at the
convention path `models/derived-model-conformance.yaml` (template and
policy paths repo-root-relative), discovered by convention like the
hermes overlay. Wiring a pointer into the stack schema is deferred to a
future domain-stack schema revision.

## Validator host: new `scripts/validate-derived-models.py`

A single-purpose canonical validator (like `validate-memory-gateway.py`),
never copied into domain repos. Self-testing: packaged positive examples
under `examples/derived-models/` (the three proof-domain shapes) must
pass and `negative/` fixtures must fail for their declared
`# expected_failure:` reason, failing closed otherwise. Absence of a
domain declaration is not a failure — conformance is opt-in.

## Access bindings accept field locks OR gates

Line-verifying the ratified Medx templates showed invariant 3 is encoded
two ways in the wild: single-value field locks
(`truth_model_write_access: [read_only]`) and gate declarations
(`cannot_write_patient_truth_model: true`). The conformance declaration
binds either form (`{field, value}` or `{gate}`), and the validator
verifies whichever is declared. This is what keeps Medx conformance
declaration-only, with no template rewrites.

## generation_seed reproducibility semantics

SHOULD-level, documented in the vocabulary doc: for LLM-driven scenario
runs, reproducibility means seeded panel composition and digest-pinned
prompt packs — honest re-runnability of the setup, not bit-identical
output. Deterministic generators (Medx dream recipes) keep the strict
seed-as-identity rule.

## Manifest registration deferred to the contract-v1.16 bundle

Precedent: the omnigent contract family (ratified 2026-07-22) is not yet
listed in `contracts/manifest.yaml`; entries land with their bundle
release. The schema added here enters the manifest (with sha256,
`adapter_owner: domain factory repos`) when contract-v1.16 is cut —
tracked as task 1.2.
