# Implementation Plan: Resolved Council Seats

**Branch**: `026-add-resolved-council-seats` | **Date**: 2026-08-28 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/026-add-resolved-council-seats/spec.md`

**Governed By**: `openspec/changes/add-resolved-council-seats/`

## Summary

Publish a domain-neutral, machine-checkable council-convening handoff in
openxFactory. A trusted DomainxFactory producer supplies one resolved
`required_seats` roster plus reproducible rule/candidate provenance; a consumer
independently evaluates the cited immutable rule and freezes the matching roster
before it creates seat jobs. The provider realization consists of a closed Draft
2020-12 schema, a deterministic validator, indexed positive and negative
fixtures, requirement-to-evidence mapping, and release registration. Hermes and
codexFactory remain separate successor features and activate together without a
legacy parser or reconstructed roster path.

## Technical Context

**Language/Version**: Python 3.12 for the validator and tests; YAML and JSON
Schema Draft 2020-12 for portable contract artifacts.

**Primary Dependencies**: Python standard library, PyYAML, jsonschema with
FormatChecker, pytest, OpenSpec CLI, and the existing contract release verifier.
No new runtime dependency is introduced.

**Storage**: Repository YAML/Markdown artifacts and fixtures only. No database,
service, credential, or deployed state is added by the neutral realization.

**Testing**: Focused pytest contract suite; validator self-test over the indexed
fixture corpus; schema meta-validation; negative cases pinned to stable finding
codes; strict OpenSpec validation; existing non-PostgreSQL repository suite.

**Target Platform**: Linux development and CI environments. Consumers may be
implemented on other platforms but must reproduce the portable fixture verdicts.

**Project Type**: Domain-neutral contract family and standalone conformance CLI;
no listening service or UI.

**Performance Goals**: Validate the complete packaged corpus in under 30 seconds
on the repository CI runner; all checks are linear in fixture and roster size.

**Constraints**: Fail closed; closed top-level shapes; unique non-empty roster;
immutable 40-hex rule and candidate revisions; no host-absolute paths, secrets,
private keys, raw provider payloads, or tenant data; no network lookup inside the
portable validator; no legacy payload acceptance; bundle version allocated only
at realization.

**Scale/Scope**: One neutral schema family, one validator, one indexed corpus
covering three standing seats and at most one conditionally required seat in the
first conformance profile, plus two downstream successor features. The contract
does not cap future domain rosters beyond non-empty uniqueness.

## Constitution Check

*GATE: Passed before Phase 0 and re-checked after Phase 1 design.*

| Principle / constraint | Pre-research | Post-design | Evidence |
|---|---|---|---|
| I. Contract-First, Domain-Neutral Core | PASS | PASS | The schema describes a neutral producer/consumer handoff; engineering candidate classes, GitHub gathering, and seat models stay in codexFactory |
| II. Governed Change Flow | PASS | PASS | Ratified change `add-resolved-council-seats` hands off one-to-one to this feature; OpenSpec keeps governance tasks while Speckit will own implementation tasks |
| III. Document Lifecycle And Status | PASS | PASS | Planning artifacts remain feature-local; canonical documents will use controlled headers and cite the governing change |
| IV. Schema And Artifact Discipline | PASS | PASS | Every new YAML artifact will carry `schema_version` and `kind`; paths are repository-relative; private keys and credentials are structurally absent |
| V. Validation Gates | PASS | PASS | Indexed fixtures, stable refusal codes, validator self-test, pytest, and strict OpenSpec are mandatory before realization |
| VI. Versioned Content-Addressed Releases | PASS | PASS | New neutral family is registered in manifest/changelog and the next available bundle is allocated late; digest inventory/tag work occurs only on the exact landed candidate |
| VII. Fail-Closed Authority Boundaries | PASS | PASS | Missing, malformed, duplicate, unknown, stale, opaque, or unevaluable inputs refuse; producer identity alone never establishes roster correctness |
| Worktree and shared-tree discipline | PASS | PASS | All openxFactory work occurs in this feature worktree; downstream repositories use their own successor features |
| Runtime scope constraint | PASS | PASS | Only contracts, fixtures, validator, tests, and documentation are added; no provider integration or deployment lives here |

No constitutional exception or complexity waiver is required.

### Release Classification

The openxFactory publication adds a previously absent neutral contract family,
so its repository release surface is additive and uses the next available minor
bundle allocated at realization. Operational activation remains intentionally
breaking: Hermes begins requiring the new fields at the same cutover in which
codexFactory begins emitting them. The obsolete, previously uncontracted payload
is not admitted through a deprecation parser or compatibility branch.

## Project Structure

### Documentation (this feature)

```text
specs/026-add-resolved-council-seats/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── acceptance-map.yaml
│   ├── conformance-corpus.md
│   ├── council-convening-envelope.md
│   └── successor-handoff.md
├── checklists/
│   └── requirements.md
└── tasks.md                    # Generated later by /speckit-tasks
```

### Source Code And Canonical Artifacts (repository root)

```text
contracts/
├── council-convening/
│   ├── README.md
│   ├── resolved-council-convening.schema.yaml
│   └── fixtures/
│       ├── index.yaml
│       ├── positive/
│       │   ├── standing-roster.yaml
│       │   └── conditional-seat-required.yaml
│       └── negative/
│           ├── roster-absent.yaml
│           ├── roster-empty.yaml
│           ├── roster-malformed.yaml
│           ├── roster-duplicate.yaml
│           ├── roster-unknown-seat.yaml
│           ├── roster-standing-incomplete.yaml
│           ├── roster-mismatch.yaml
│           ├── provenance-opaque.yaml
│           ├── rule-revision-unavailable.yaml
│           ├── fact-missing.yaml
│           ├── condition-result-drift.yaml
│           └── candidate-head-stale.yaml
├── manifest.yaml
├── CHANGELOG.md
└── README.md

scripts/
└── validate-council-convening.py

tests/council_convening/
├── test_contract.py
└── test_validator_cli.py

openspec/specs/roles-authority-model/
└── spec.md                     # Promotion target when realization archives
```

Downstream successor surfaces, changed only in their own features:

```text
xFactory-Hermes-Install/
├── src/hermes_install/domain/council_orchestration.py
├── src/hermes_install/domain/wallet_convening_admission.py
├── tests/unit/test_council_orchestration.py
└── tests/pg/test_wallet_exercises.py

codexFactory/
├── scripts/merge_master/seat_resolution.py
├── .github/workflows/council-lane-reusable.yml
├── .github/workflows/council-deliberation-worker.yml
└── .github/workflows/scripts/council_seat_signing.py
```

**Structure Decision**: Use a focused `contracts/council-convening/` family
rather than widening the copied v1 Hermes job envelope. The resolved roster is
a cross-system admission contract with its own release lifecycle, while the
general envelope remains domain-extensible. The neutral validator checks closed
shape, deterministic set arithmetic, provenance binding, fixture parity, and
stable refusal outcomes; each consumer supplies its own immutable-rule resolver
at the trust boundary and must reproduce the portable corpus independently.

## Delivery Sequence

1. Add the closed schema, fixture index, positive/negative corpus, and thin
   standalone validator with deterministic finding codes.
2. Add focused tests proving schema closure, fixture indexing, correct roster
   set arithmetic, stale/opaque/unevaluable refusal, and CLI exit semantics.
3. Register the family in `contracts/README.md`, `contracts/manifest.yaml`, and
   `contracts/CHANGELOG.md`; update release metadata only during the serialized
   realization cut.
4. Record local provider evidence without claiming canonical promotion, merge,
   tag, deployment, or OIDC; the archive operation promotes the ratified delta
   only after provider and successor realization evidence has landed.
5. Create/record the Hermes successor feature: validate the cited rule through
   an injected resolver, freeze roster/provenance in the admission snapshot,
   issue one job per seat, reject unlisted returns, compare rich-return outcome
   fields only, and retain verdict-less failure/recovery behavior.
6. Create/record the codexFactory successor feature: resolve in the trusted
   preparation job, bind exact GitHub facts and immutable rules provenance,
   submit the new envelope, and replace the shared/root-key path with one
   job-local ephemeral Ed25519 key per seat job under the governed OIDC subject.
7. Run the shared corpus independently in both successors, rehearse the
   coordinated hard cutover, and keep live deployment/OIDC/release evidence open
   until an authorized operator performs those acts.

## Complexity Tracking

No constitution violations require justification.
