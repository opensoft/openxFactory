# Implementation Plan: contracts/clearing — the neutral clearing-dispatch contract family

**Branch**: `028-clearing-contracts` | **Date**: 2026-09-03 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/028-clearing-contracts/spec.md`

## Summary

Realize, as neutral openxFactory contract bytes, the artifacts the RATIFIED
change `add-clearing-dispatch-boundary` DECLARED and deferred: a new
`contracts/clearing/` family of five record shapes (sealed-bundle manifest,
permitted-operations register as schema + closed instance, operation report,
dispatch ledger record, single-door attestation), a packaged positive/negative
example corpus, a canonical `scripts/validate-clearing-dispatch.py`, CI wiring
on the existing gate pattern, `tests/clearing/`, and registration at the next
additive bundle cut. The MODIFIED requirements of the merged
`add-cpc-clearing-boundary` tighten two things this realization honours: field
(10) becomes a REQUIRED origin signature where the originating repository holds
an active row in `governance/factory-identity/register.yaml`, and the
policy-checked fields are RESOLVED FROM the register rather than read from the
bundle.

The approach is DERIVATIVE BY DESIGN. Every shape is authored against text that
is already ratified and against names the live `opensoft/xFactory` realization
already emits; nothing here proposes, widens, or reinterprets. Where the
ratified text needs a capability this repository does not yet have — a digest
subject for the manifest — it is acquired under the OWNING family's own stated
rule (a tranche addition of SUBJECTS to `signed-execution-chain`'s closed
enumeration) rather than by minting a second construction.

## Technical Context

**Language/Version**: Python 3.11+ (validators and tests); YAML 1.2 (contracts).

**Primary Dependencies**: `jsonschema` (draft 2020-12) and `PyYAML` for schema
validation; the pinned openXwallet reader for Ed25519 public-key decoding and
signature verification; the in-repo `xfc-jcs-sha256-1` digest implementation
that `signed-execution-chain` already ships. No new third-party dependency is
introduced.

**Storage**: Files in the repository. The contracts are data; there is no
runtime store.

**Testing**: pytest, `tests/clearing/`, run as `python3 -m pytest tests/ -q -m "not postgres"`.

**Target Platform**: CI (GitHub Actions, ubuntu-latest) and developer shells.

**Project Type**: Contract family + canonical validator + test suite in an
existing repository. Not an application.

**Performance Goals**: N/A — the validator runs over a bounded example corpus in
CI; sub-second is the practical expectation and no target is asserted.

**Constraints**:
- NO SECOND VOCABULARY. Digests, job envelopes, runner groups/labels/tiers,
  scoped credentials and handling classes belong to
  `signed-execution-chain`, `neutral-job-envelope`, `worker-enrollment-broker`,
  `credential-contracts` and `document-cataloging` respectively. This family
  references them and defines none of them.
- NO SPEC DELTA. This is realization. If a rule appears necessary that the
  ratified text does not carry, it is recorded as a finding for a successor
  change, not authored here.
- The bundle minor is allocated AT REALIZATION from the manifest at this
  branch's tip; a number is never reserved ahead of merge order.
- Test fixtures may carry no value that looks like real key material.

**Scale/Scope**: 6 new contract files, 1 one-member enum widening in an existing
schema, ~11 negative fixtures + ~6 positive examples, 1 validator, 1 CI job, 1
test package, 3 registration surfaces.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Assessment |
|---|---|
| **I. Contract-First, Domain-Neutral Core** | PASS. The family is domain-neutral: it names no domain, and the one place a concrete estate appears (the `readiness-diagnostic` entry's lanes and expected runners) is INSTANCE DATA in a registry, not schema vocabulary. A DomainxFactory could carry a different instance against the same schema. |
| **II. Governed Change Flow: OpenSpec Before Implementation** | PASS. Two ratified OpenSpec changes precede this work and this feature authors no requirement. `add-clearing-dispatch-boundary` declares `code_surface` and defers exactly this realization; per `release-realization` its archive gate is merged-plus-green realization evidence, which this feature produces. |
| **III. Document Lifecycle and Status Discipline** | PASS. The family README carries `Status: ratified` + `Ratified by: add-clearing-dispatch-boundary`, the form `contracts/worker-enrollment/README.md` uses. |
| **IV. Schema and Artifact Discipline** | PASS. Every YAML carries `schema_version` + `kind`; the register ships as schema + instance; no `.template.yaml` is needed because the register has a real instance. |
| **V. Validation Gates (NON-NEGOTIABLE)** | PASS. A canonical validator ships WITH the schemas, is wired into CI in the existing gate pattern, and every refusal it implements has a negative fixture and a test asserting the code by name. |
| **VI. Versioned, Content-Addressed Releases** | PASS. Registration in `contracts/manifest.yaml` with per-file `sha256`, a `contracts/CHANGELOG.md` entry, and a `contracts/releases/<minor>.digests.yaml` inventory built by the repository's own release tool. The annotated tag is Bundle Realization Order step 5 and is published at the LANDED commit after `verify-commit` passes there — the omission of that re-verification is precisely what made `contract-v3.1` defective, so it is named rather than repeated. |
| **VII. Fail-Closed Authority Boundaries** | PASS. Every cross-shape rule refuses rather than defaults: an unresolvable register, an unreadable factory-identity register, an absent digest implementation, and a missing openXwallet reader each REFUSE. There is no fallback path. |

No violations. Complexity Tracking is therefore omitted.

## Project Structure

### Documentation (this feature)

```text
specs/028-clearing-contracts/
├── plan.md              # This file
├── research.md          # Phase 0 output — conventions measured, decisions taken
├── data-model.md        # Phase 1 output — every shape, member by member
├── quickstart.md        # Phase 1 output — how to run and prove the family
├── contracts/           # Phase 1 output — the validator's CLI + refusal-code contract
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
contracts/clearing/                      # NEW family
├── README.md                            # Status: ratified / Ratified by:
├── sealed-bundle-manifest.schema.yaml
├── permitted-operations.schema.yaml
├── permitted-operations.registry.yaml   # the CLOSED instance, one member
├── operation-report.schema.yaml
├── dispatch-record.schema.yaml
├── single-door-attestation.schema.yaml
└── examples/
    ├── *.example.yaml                   # positives, one per shape
    └── negative/
        └── *.yaml                       # one per named refusal

contracts/signed-execution-chain/
└── digest-construction.schema.yaml      # MODIFIED: +1 digest_subject member

scripts/
└── validate-clearing-dispatch.py        # NEW canonical validator

tests/clearing/                          # NEW
├── test_schemas.py
├── test_register_closure.py
├── test_validator_refusals.py
├── test_digest_by_reference.py
├── test_origin_signature.py
├── test_clearing_manifest_rows.py
└── test_clearing_gate_wiring.py

.github/workflows/                       # MODIFIED: one gate job, existing pattern
contracts/manifest.yaml                  # MODIFIED: family rows + bundle version
contracts/README.md                      # MODIFIED: native contract index rows
contracts/CHANGELOG.md                   # MODIFIED: the new additive entry
contracts/releases/contract-v<minor>.digests.yaml   # NEW inventory
openspec/changes/add-clearing-dispatch-boundary/    # MODIFIED: §6 ticks + note
```

**Structure Decision**: the family lives at `contracts/clearing/` with its
examples nested beneath it — the convention every family added since
`identity-brokering` follows (`contracts/<family>/examples/negative/`), rather
than the older root-level `examples/<family>/negative/`. The validator lives at
`scripts/validate-clearing-dispatch.py` (the canonical-validator location the
`code_surface` paragraph names verbatim), and its tests at `tests/clearing/`
per the per-family pytest convention.

## Phase 0 — Research

See [research.md](./research.md). Six questions were open at planning time and
all six are resolved there: the minor to allocate, whether the existing
`contracts/schemas/dispatch-record.schema.yaml` is this ledger, how the register
ships as schema-plus-instance, where the manifest digest's subject comes from,
how the validator reuses existing digest and key code, and how a fixture key is
written so secret scanning stays meaningful.

## Phase 1 — Design

- [data-model.md](./data-model.md) — every shape, member by member, each traced
  to the ratified sentence that requires it.
- [contracts/validator-cli.md](./contracts/validator-cli.md) — the validator's
  external interface: invocation, exit codes, finding format, and the CLOSED
  list of refusal codes with the ratified scenario each discharges.
- [quickstart.md](./quickstart.md) — the commands that prove the family, and
  what each is expected to print.

## Phase 2 — Task generation

`/speckit-tasks` derives `tasks.md` from the above. The dependency order is
forced by the artifacts themselves: the digest-subject widening precedes the
manifest schema (which references the subject); the register schema and instance
precede the validator (which resolves against them); every schema precedes its
examples; every example precedes the tests that assert it; and registration is
last because a `sha256` row is only correct once the file it addresses is final.
