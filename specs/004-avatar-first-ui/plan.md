# Implementation Plan: Avatar-First UI Standard Alignment

**Branch**: `004-avatar-first-ui` | **Date**: 2026-07-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/004-avatar-first-ui/spec.md`

**Source of truth**: OpenSpec change `align-avatar-first-ui-standard`
(`openspec/changes/align-avatar-first-ui-standard/`), ratified-grade. This plan
covers only the five openxFactory UI artifacts the change owns; kernel
registries are read-only; shared contract metadata is touched only in the
serialized post-kernel final release step (Phase 3, deferred).

## Summary

Align the existing avatar-first UI standard, registered profile schema, shared
template, examples, and offline validator with the AVC kernel semantics, and
publish deterministic UI fixture shapes plus requirement-to-evidence mappings —
without building any Flutter widget, provider adapter, or live client. The work
is documentation-and-validation only: Markdown (the standard), YAML (schema,
template, examples, fixtures), and a Python offline validator. All new runtime
fields are additive with closed defaults so existing static profiles stay valid;
kernel-owned ceilings and registries are consumed read-only; runtime
compatibility is pinned by exact content-addressed coordinates; and the final
contract release (manifest/CHANGELOG/README + annotated tag) is serialized after
the kernel release. The eight `AFU-*` requirements and twenty-five scenarios are
each bound to standard/schema/template/fixture evidence or a named successor.

## Technical Context

**Language/Version**: Python 3.11+ (offline validator `scripts/validate-avatar-first-ui.py`);
YAML 1.1 via PyYAML (schema, template, examples, fixtures); CommonMark Markdown
(the standard document).

**Primary Dependencies**: PyYAML (already the validator's only third-party
dependency); the OpenSpec CLI for strict spec validation. No web/UI framework,
no Flutter, no provider SDK, no network client — those are explicitly
out-of-scope successor concerns.

**Storage**: N/A. All artifacts are version-controlled files in the openxFactory
repository; no database or runtime state.

**Testing**: The offline validator run over the template, the four representative
examples, the compatibility fixture(s), and one negative fixture per enforced
rule class; `OPENSPEC_TELEMETRY=0 openspec validate align-avatar-first-ui-standard --strict`
and `--all --strict`; acceptance-map parity (8 requirements / 25 scenarios); and
`git diff --check`. No provider or runtime service is contacted.

**Target Platform**: Repository + CI (offline). The standard *describes* client
qualification targets (Windows desktop, web) but this feature ships no runnable
client; those targets are proven by successor changes.

**Project Type**: Single-repo governed contract-and-documentation artifacts —
one Markdown standard, one registered YAML schema, one YAML template, a YAML
examples/fixtures set, and one Python validator.

**Performance Goals**: The validator completes offline in a few seconds over the
whole artifact set; determinism (identical inputs → identical validator verdict
and fixture shapes) is the real target, not latency.

**Constraints**: Offline-only (no provider/runtime service); read-only
consumption of kernel capability/outcome/consent-purpose/state registries;
additive-with-closed-defaults backward compatibility for existing profiles;
content-addressed runtime-compatibility pins (no loose version range); shared
contract metadata (`contracts/manifest.yaml`, `contracts/CHANGELOG.md`,
`contracts/README.md`) changed only in the serialized post-kernel release; no
edits to kernel, reference-runtime, F0, DomainxFactory, Flutter, or deployment
files during parallel work.

**Scale/Scope**: 5 owned artifacts + a new `examples/avatar-first-ui/fixtures/`
directory; 4 representative example profiles + ≥1 compatibility fixture + ≥8
negative fixtures (one per enforced rule class, each with a stable
error/evidence ID); 8 `AFU-*` requirements / 25 scenarios traced.

**Unknowns**: None. The OpenSpec change is ratified-grade and the eight clarify
answers are encoded in `spec.md` (§ Clarifications, Session 2026-07-11). No
`NEEDS CLARIFICATION` remains.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Verdict | Notes |
|-----------|---------|-------|
| I. Contract-First, Domain-Neutral Core | PASS | Every edit stays domain-neutral. Per Q2=A the confirmation example is a neutral `confirmation-before-consequential-action` archetype (Ledgerx is inspiration only); domain persona catalogs and retention policies stay domain/kernel-owned and are referenced, not embedded (Q1=A, Q8=A). No domain vocabulary or policy lands here. |
| II. Governed Change Flow: OpenSpec Before Implementation | PASS | This is the single Speckit feature for OpenSpec change `align-avatar-first-ui-standard` (`code_surface: openxFactory`, `target_release: implemented`). OpenSpec holds governance decisions; Speckit `tasks.md` (next phase) holds implementation tasks — no duplication. |
| III. Document Lifecycle and Status Discipline | PASS | The standard carries a controlled `Status:` header (currently `draft`); on landing it moves to `Status: ratified` + `Ratified by: align-avatar-first-ui-standard` (an implement-phase step, not a silent edit). The acceptance-traceability supporting doc stays a `register`. |
| IV. Schema and Artifact Discipline | PASS | Schema/template/examples/fixtures carry `schema_version` + `kind`; `.template.yaml`/`.example.yaml` remain instantiation stubs; the standard is already in the README doc index; a fixtures README will be indexed there; no raw credentials; no host-absolute paths (references use repo-relative paths). |
| V. Validation Gates (NON-NEGOTIABLE) | PASS | Evidence is the extended offline validator + OpenSpec strict + compatibility/negative fixtures + acceptance-map parity + `git diff --check`. Any doc-health contested finding resolves via this cited change. Behavior is proven by fixtures, not assertion. |
| VI. Versioned, Content-Addressed Releases | PASS (final step DEFERRED) | The profile-schema revision allocates its `contract_bundle_version` at realization (never pre-reserved), updates manifest/CHANGELOG/README atomically, and publishes a matching annotated tag — all in the serialized Phase 3 after the kernel release. Runtime compatibility is pinned by exact commit/tag/digests (Q5). |
| VII. Fail-Closed Authority Boundaries | PASS | Kernel registries and ceilings are consumed read-only; new fields carry closed defaults; unresolvable persona/retention/ceiling references fail closed (Q1/Q4/Q8); provider/model text stays non-authoritative; validator registries are closed and reject unknown values. |
| Repository Constraints | PASS | Work runs in the `004-avatar-first-ui` worktree; explicit-path staging only; the validator is a governed, ratified validator (permitted runtime code); the aggregation-repo pin update happens outside this feature. |
| Development Workflow & Quality Gates | PASS | Lifecycle order followed (specify → clarify → **plan** → checklist/tasks → analyze → implement); clarifications encoded before planning; parallel siblings serialize their final shared-metadata commits (Phase 3). |

**Result**: PASS, no violations. Complexity Tracking is empty (see below).

## Project Structure

### Documentation (this feature)

```text
specs/004-avatar-first-ui/
├── plan.md              # This file (/speckit-plan output)
├── research.md          # Phase 0 — design decisions (all clarifications resolved)
├── data-model.md        # Phase 1 — profile entities, fields, rules, error-ID catalog
├── quickstart.md        # Phase 1 — offline validation/run guide
├── contracts/           # Phase 1 — artifact-contract design references
│   ├── profile-schema-outline.md    # additive schema deltas + closed defaults
│   ├── validator-rules.md           # rule catalog ↔ stable error/evidence IDs ↔ fixtures
│   └── fixture-shape.md             # deterministic fixture shape + evidence IDs
├── spec.md              # Clarified feature spec (specify/clarify phases)
├── clarify-questions.md # Answered clarify record
├── checklists/
│   └── requirements.md  # Spec quality checklist (16/16)
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root — the five owned UI artifacts + fixtures)

```text
docs/
└── avatar-first-ui-standard.md          # UPDATE: four authoritative axes vs client-local
                                         #   presentation modes; Hermes-layer defaults;
                                         #   media-authorization/held-answer; AVC-02
                                         #   denial/terminal; control-loss vs media-loss;
                                         #   safe rendering; persona reference & disclosure;
                                         #   workflow boundary; accessibility evidence boundary

contracts/schemas/
└── avatar-first-ui-profile.schema.yaml  # UPDATE (additive, closed defaults): runtime
                                         #   compatibility coords; surface default; interaction
                                         #   mode + speech gate; selected readiness/heartbeat/
                                         #   lease; outcome/fallback slots; media-authorization
                                         #   pending; consent-purpose mappings; persona
                                         #   reference; retention overlay refs; structured
                                         #   accessibility baseline

templates/ui/
└── avatar-first.yaml                    # UPDATE: regions, controls, authority sources,
                                         #   media/recording awareness, fallback behavior,
                                         #   handoff boundary, reserved-feature defaults

examples/avatar-first-ui/
├── README.md                            # UPDATE: index the four archetypes + fixtures
├── domain-overlays.example.yaml         # UPDATE: neutral archetypes (customer avatar-first,
│                                        #   client hybrid, domain conventional-first,
│                                        #   confirmation-before-consequential-action)
└── fixtures/                            # NEW (Q3=A): deterministic UI fixtures
    ├── README.md                        #   fixture index + evidence-ID map
    ├── compatibility/                   #   ≥1 legacy/static profile that stays valid
    └── negative/                        #   ≥1 fixture per enforced rule class, each with
                                         #   a stable error/evidence ID

scripts/
└── validate-avatar-first-ui.py          # EXTEND: state axes; safe outcomes; held-answer/
                                         #   media authorization; selected values vs
                                         #   kernel-owned ceilings; control fallbacks;
                                         #   purpose mappings; persona-reference resolution;
                                         #   retention-policy refs; structured accessibility;
                                         #   forbidden/reserved modes; parity; stable error IDs;
                                         #   baseline vs final-realization modes

# DEFERRED — Phase 3, serialized AFTER the kernel release (NOT edited in parallel work):
contracts/manifest.yaml                  # profile-schema revision + next bundle version
contracts/CHANGELOG.md                   # matching release entry
contracts/README.md                      # integration note
# + annotated contract-v<major>.<minor> tag at the realized commit
```

**Structure Decision**: Single-repo, artifact-first. There is no application
source tree — the "implementation" is five governed artifacts plus a new
deterministic fixtures directory. The Python validator is the executable
evidence harness. Feature design artifacts live under
`specs/004-avatar-first-ui/`; the artifacts under change go at their canonical
repo paths above.

## Phases

### Phase 0 — Research (design decisions)

Output: [research.md](./research.md). Because all clarifications are resolved, Phase 0
records the *design* decisions that turn the clarified spec into concrete
artifact shapes: authoritative-axes-vs-presentation-mode modeling; media-
authorization/held-answer and AVC-02 outcome/fallback representation; interaction
mode / speech gate (provider_vad; server_vad reserved; push-to-talk reserved,
disabled); selected readiness/heartbeat/lease vs kernel-owned ceilings; content-
addressed runtime-compatibility coordinates; consent-purpose mappings; persona
reference-only vs the legacy embedded catalog (compatibility strategy); retention
overlay references; structured per-capability accessibility; the negative-fixture
rule-class taxonomy and stable error/evidence-ID scheme; the fixtures directory
and determinism inputs; additive-with-closed-defaults migration; validator
baseline-vs-final-realization mode selection; and the serialized post-kernel
release. Every entry is Decision / Rationale / Alternatives.

### Phase 1 — Design & Contracts

Prerequisites: research.md complete.

- [data-model.md](./data-model.md): the profile schema entities, their additive fields and
  closed defaults, validation rules traced to `FR-*`, persona/fallback/consent/
  retention/accessibility entity shapes, the authoritative-axes vs presentation-
  mode model, and the stable error/evidence-ID catalog.
- [contracts/](./contracts): artifact-contract design references — the additive profile-
  schema outline, the validator rule catalog mapping each rule to its stable
  error/evidence ID and its negative fixture, and the deterministic fixture shape.
- [quickstart.md](./quickstart.md): the offline validation/run guide (how to run the
  validator, OpenSpec strict, acceptance-map parity, and `git diff --check`, with
  expected outputs) — a run guide, not implementation code.

Agent-context update: no `update-agent-context.sh` exists in this worktree, so
that optional step is skipped.

### Phase 2 — Tasks (NOT produced here)

`/speckit-tasks` will derive the dependency-ordered `tasks.md`. Anticipated task
groups mirror OpenSpec `tasks.md` 1.1–3.4: standard doc, profile schema, template
+ examples, validator + fixtures + acceptance-map parity, and the deferred
serialized release.

### Phase 3 — Serialized post-kernel realization (DEFERRED)

Runs only after the AVC kernel release lands. Consume any accepted kernel
variances through mapped UI fields only; pin and cross-check the exact released
capability/outcome/consent-purpose/state registries read-only (content-addressed
tag + commit + digests, no loose range); rebase to the latest bundle; allocate
the next available `contract_bundle_version` at realization; update
`contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and `contracts/README.md`
atomically for the profile-schema revision; publish the matching annotated tag;
and confirm no kernel/reference-runtime/F0/DomainxFactory/Flutter/deployment file
changed. This is the only step permitted to touch shared contract metadata, and
it serializes against sibling changes.

## Requirement coverage map

Every functional requirement maps to an owning artifact and phase (design detail
in `research.md` / `data-model.md` / `contracts/`):

| FR | Owning artifact | Phase | Design ref |
|----|-----------------|-------|-----------|
| FR-001, FR-002 | standard + schema (`presentation`, axes-vs-modes) | 1 | D1 |
| FR-003 | standard (Hermes-layer defaults) + template guidance | impl | existing §11 updated |
| FR-004 | standard (consequential values in work/review) | impl | D1 |
| FR-005, FR-006 | standard (client/web split, handoff URL constraints) | impl | data-model `handoff` |
| FR-007 | standard + schema (`fallback_slots`, controls) | 1 | schema outline |
| FR-008, FR-009 | standard + schema (`media`, `outcome_slots`) | 1 | D2 |
| FR-010 | standard (accessibility evidence boundary) | impl | D9 |
| FR-011 | standard + schema (`persona_reference`, disclosure) | 1 | D7 |
| FR-012 | standard + validator (safe rendering) | 1 | D2, rule `AFUV-UNSAFE-RENDER` |
| FR-013 | schema (carrier field list) | 1 | schema outline, data-model |
| FR-014 | schema (`consent_purpose_mappings`) | 1 | D6 |
| FR-015 | schema (`interaction_mode`, `speech_gate`) | 1 | D3 |
| FR-016 | schema (additive, closed defaults) | 1 | D12 |
| FR-017 | schema (`schema_version`/`kind`, read-only registries) | 1 | D5 |
| FR-018 | template | impl | validator rule `AFUV-TEMPLATE-SHAPE` |
| FR-019 | examples (4 archetypes + compat + negative) | 1 | D7, D10, D11 |
| FR-020 | validator (checks + stable error IDs) | 1 | validator-rules |
| FR-021 | validator (baseline vs realization, content-addressed) | 1 / 3 | D5, D13 |
| FR-022 | validator/acceptance-map parity | 1 | rule `AFUV-PARITY-ACCEPTANCE`, quickstart §4 |
| FR-023 | fixtures dir (`examples/avatar-first-ui/fixtures/`) | 1 | D11, fixture-shape |
| FR-024 | serialized post-kernel release | 3 (DEFERRED) | D14 |
| FR-025 | schema (`runtime_compatibility` coords) | 1 | D5 |
| FR-026 | schema (`timing`) + validator (ceilings read-only) | 1 | D4 |
| FR-027 | schema (`retention_overlay`) | 1 | D8 |
| FR-028 | schema (`accessibility_baseline`) | 1 | D9 |

Items marked "impl" are prose/content updates to the standard or template
authored in the implement phase; their shapes are already fixed by the schema
and validator designs above.

## Complexity Tracking

No Constitution Check violations. No entries required.
