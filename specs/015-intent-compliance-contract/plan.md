# Implementation Plan: Intent Compliance Contract

**Branch**: `015-intent-compliance-contract` | **Date**: 2026-08-26 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/015-intent-compliance-contract/spec.md`

## Summary

Realize the ratified neutral intent-compliance contract as five closed YAML/JSON
Schema record kinds, safe templates and examples, a self-testing canonical
validator, and one additive content-addressed release. The validator follows
existing trust-anchor and multi-kind contract patterns: parse YAML once, run
Draft 2020-12 schema checks, apply cross-record semantic rules, self-test an
indexed positive/negative corpus, and optionally scan a consumer repository.

## Technical Context

**Language/Version**: Python 3.11+ and YAML/JSON Schema Draft 2020-12

**Primary Dependencies**: Python standard library, PyYAML, jsonschema,
referencing; existing repository release and manifest validators

**Storage**: Version-controlled YAML schemas, templates, examples, and digest
inventory; no runtime database or registry service

**Testing**: pytest plus executable validator self-test, repository scan, strict
OpenSpec validation, manifest/digest validation, and contract-release gates

**Target Platform**: Repository validation on Linux CI and local developer
workstations

**Project Type**: Contract family plus validation CLI

**Performance Goals**: Validate the packaged corpus and a normal consumer
repository in under five seconds on CI-class hardware

**Constraints**: Fail closed; no raw intent/provider/credential evidence; no
domain-specific veto vocabulary; all released bytes content-addressed; no
host-absolute paths; registry instances remain consumer-owned

**Scale/Scope**: Five schema kinds, five templates, a compact positive corpus,
single-fault negative fixtures covering every normative requirement, one
runtime race harness, and one additive bundle release

## Constitution Check

*GATE: Passed before research and re-checked after design.*

- **I Domain neutrality**: PASS. Schemas encode closed neutral shapes; concrete
  codexFactory classes remain in the successor repository.
- **II Governed flow**: PASS. PR #349 merged the OpenSpec change and Brett
  ratified it; this is the single Speckit implementation handoff.
- **III Lifecycle**: PASS. Ratification has a dated, cited record; archive waits
  for merged release and first-conformer evidence.
- **IV Artifact discipline**: PASS. Every YAML carries `schema_version` and
  `kind`; templates/examples are non-live stubs; no credentials are stored.
- **V Validation**: PASS by plan. The public validator, fixture corpus, pytest,
  OpenSpec, doc-health, manifest, and release gates are explicit tasks.
- **VI Releases**: PASS by plan. Bundle number is allocated after tag refresh;
  manifest, changelog, inventory, commit, and annotated tag are coordinated.
- **VII Authority**: PASS. Unknown variants, stale state, unsafe evidence, and
  unresolved authority fail closed.

Post-design check: PASS. No constitution exception or complexity waiver is
required.

## Project Structure

### Documentation (this feature)

```text
specs/015-intent-compliance-contract/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── validator-cli.md
└── tasks.md
```

### Source Code (repository root)

```text
contracts/intent-compliance/
├── README.md
├── veto-class-vocabulary.schema.yaml
├── policy-allowance.schema.yaml
├── policy-allowance-revocation.schema.yaml
├── policy-allowance-registry.schema.yaml
├── compliance-decision.schema.yaml
├── *.template.yaml
└── examples/
    ├── positive/
    └── negative/
scripts/
└── validate-intent-compliance.py
tests/intent-compliance/
├── test_intent_compliance_validator_gate.py
└── test_intent_compliance_negative_corpus.py
contracts/manifest.yaml
contracts/CHANGELOG.md
contracts/releases/contract-v2.3.digests.yaml
contracts/README.md
```

**Structure Decision**: Keep the family self-contained under
`contracts/intent-compliance/`; expose one repository-root validator consistent
with other canonical families; keep pytest coverage in a focused matching
directory; update only the shared release surfaces at final integration.

## Complexity Tracking

No constitution violations require justification.
