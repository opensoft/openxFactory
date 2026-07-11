# Implementation Plan: AVC Contract Kernel

**Branch**: `001-avc-contract-kernel` | **Date**: 2026-07-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-avc-contract-kernel/spec.md`

**Source of truth**: OpenSpec change `define-avatar-client-contract-kernel`
(proposal.md, design.md, three spec deltas, supporting-docs). Clarifications
encoded in spec.md `## Clarifications` (Session 2026-07-11) govern where the
ratified change left an implementation choice open.

## Summary

Publish the canonical, provider-neutral avatar-client (AVC) contract kernel as
YAML-serialized JSON Schema (draft 2020-12) artifacts under
`contracts/avatar-client/`, plus a single reference validator
`scripts/validate-avatar-client.py`, and realize a content-addressed release.

Technical approach: author the eight AVC schemas over one `shared-definitions`
module (`$ref`), express every closed vocabulary as a first-class **registry
data file** and enforce schema/registry parity in the validator, cover every
schema and every owned acceptance scenario with **language-neutral,
self-describing fixtures**, resolve every acceptance-map scenario through one
**consolidated evidence/disposition register**, and enforce redaction with a
**dual structural + content-scan** mechanism using bounded synthetic sentinels.
The validator additionally checks acceptance-map parity, evidence-register
completeness and status transitions, per-file digests over the full consumed
set, and the **F0 publication gate** — which pins the F0 sibling's source commit
and both F0-owned evidence-schema digests, validates the consumed evidence
instances against those pinned schemas, and fails closed on any mismatch. The
feature has two completion states: *implementation complete, publication pending
F0* and *realized* (tag + digests exist).

Primary requirements realized: FR-001–FR-034, SC-001–SC-010 (see spec.md).
This plan produces design artifacts only; the Speckit `tasks.md` (Phase 2) and
implementation follow.

## Technical Context

**Language/Version**: Python 3 (repo house style: `#!/usr/bin/env python3`,
`from __future__ import annotations`) for the reference validator. Contract
artifacts are **data**, not code: YAML-serialized JSON Schema **draft 2020-12**.

**Primary Dependencies**: `jsonschema.Draft202012Validator` and `PyYAML`
(`yaml.safe_load`) — both already established repo dependencies (used by
`scripts/validate-credential-contracts.py`, `validate-workflow-contracts.py`,
`validate-avatar-first-ui.py`). Standard library only otherwise: `hashlib`
(SHA-256 digests), `re` (content-scan denylist), `pathlib`, `argparse`,
`dataclasses`, `sys`. **No new third-party dependency is introduced.**

**Storage**: N/A (repository files). Content-addressing is git commit SHA plus
per-file SHA-256 digests recorded in `contracts/manifest.yaml`; there is no
database, socket, or runtime state (constitution Repository Constraints).

**Testing**: The validator is the deterministic evidence harness (constitution
Principle V). Canonical self-describing fixtures are the conformance suite;
`validate-avatar-client.py --strict` is the pre-push gate. Optional lightweight
`pytest` unit tests for the validator's own helpers may accompany it but are not
required for consumer conformance.

**Target Platform**: Repository tooling / CI (Linux) for authoring and gating.
Consumers (including the Dart Flutter client) execute the portable fixtures with
**any conformant draft-2020-12 implementation** — the Python validator is the
reference runner, not a required consumer dependency (FR-023, Q5).

**Project Type**: Contract-library + validator tooling (single project;
documentation/contract-first repository). No frontend/backend split.

**Performance Goals**: The full validation run (schemas, registries, all
fixtures, acceptance-map parity, evidence register, digests, redaction scan)
completes fast enough to serve as an interactive pre-push gate — target well
under ~10 seconds on a developer machine. No runtime latency budget applies
(latency evidence belongs to the F0 and live-qualification siblings).

**Constraints**: Deterministic and reviewable output; fail-closed on unknown
vocabulary/status/variance; no host-absolute paths (Principle IV — validator
resolves everything relative to `Path(__file__).resolve().parents[1]`); no
credentials, SDP, raw payloads, or high-cardinality identifiers in any committed
file (Principle VII; FR-018/SC-008); this change alone writes
`contracts/avatar-client/` and `scripts/validate-avatar-client.py`; shared
release metadata (`contracts/manifest.yaml`, `CHANGELOG.md`, `README.md`) is
touched only at the serialized final realization step.

**Scale/Scope**: 8 schemas + 1 shared-definitions module + 9 registry files
(8 vocabularies + consent purposes) + acceptance map (17 requirements /
72 scenarios) + evidence register + interface-lock (incl. F0 evidence pin) +
redaction config + a fixture suite (valid/invalid/boundary/compatibility/
unknown-field/unknown-authority/redaction/adversarial per schema and per owned
scenario) + one validator + release-metadata edits. Bounded and enumerable.

**Unknowns**: None outstanding. The spec carries 0 `[NEEDS CLARIFICATION]`
markers; all seven clarify decisions are encoded. Phase 0 (research.md) records
the resulting engineering decisions and rejected alternatives.

## Constitution Check

*GATE: evaluated against openxFactory Constitution v1.0.0. Must pass before
Phase 0 and be re-checked after Phase 1.*

| Principle | Verdict | Basis |
|-----------|---------|-------|
| I. Contract-First, Domain-Neutral Core | **PASS** | Only neutral contracts land under `contracts/avatar-client/`. No domain vocabulary/policy. AVC-07/AVC-08 ship schema+fixtures only; persona/retention instances stay domain-owned (FR-001, Q2). |
| II. Governed Change Flow (OpenSpec → one Speckit feature) | **PASS** | Single Speckit feature for `define-avatar-client-contract-kernel`; `code_surface: openxFactory`. Speckit `tasks.md` will own implementation decomposition; the OpenSpec `tasks.md` remains the governance handoff — mapped, not duplicated (see Design Note 1). Two completion states honor "archives only on merged, green realization evidence" (FR-034). |
| III. Document Lifecycle & Status Discipline | **PASS** | Data artifacts carry `schema_version` + `kind` (Principle IV). The only prose doc, `contracts/avatar-client/README.md`, is linked into the repo README index and carries a controlled `Status:` header at realization. No `standard` claim is made without the promoted spec/contract backing it. |
| IV. Schema and Artifact Discipline | **PASS** | Every YAML carries `schema_version` + `kind`; no `.template`/`.example` live-config for AVC-07/08 (Q2); no host-absolute paths; no raw credentials (bounded sentinels only, Q3); new docs linked into the README index. |
| V. Validation Gates (NON-NEGOTIABLE) | **PASS** | `validate-avatar-client.py` is the local gate run before push; OpenSpec `validate --all --strict` also required. Behavior proven by deterministic fixtures + validator output, not assertion. Contested findings resolved by cited change/disposition. |
| VI. Versioned, Content-Addressed Releases | **PASS** | Five coordinated values (per-file `contract_schema_version`, `contract_bundle_version`, annotated `contract-v1.7` tag, exact commit + per-file SHA-256 digests, CHANGELOG entry). Version allocated at realization (next minor after `contract-v1.6`); additive = minor. Digests span the full consumed set (FR-022). |
| VII. Fail-Closed Authority Boundaries | **PASS** | Closed registries reject unknown values; deferred features fail closed; committed evidence redacted (dual enforcement); F0 gate fails closed on missing schema/digest mismatch/validation failure/unknown status/variance (FR-033). No model authority in this surface. |
| Repository Constraints | **PASS** | Work confined to the feature worktree; explicit-path staging; no runtime code that deploys/listens/holds keys — the validator is an explicitly ratified per-repo validator (OpenSpec task 3.2). Aggregation pin is a later, separate sync step. |
| Development Workflow & Quality Gates | **PASS** | Lifecycle order respected (specify → clarify → **plan** → checklist → tasks → analyze → implement), run from the worktree. `/speckit.analyze` must be clean before implementation. |

**Result: PASS (initial and post-Phase-1). No principle is violated; no
Complexity Tracking entry is required.**

Two design choices add machinery but are *required by* the constitution and the
ratified change rather than discretionary, so they are recorded as Design Notes
(below) instead of Complexity Tracking rows:

- **Registry-as-data-file + schema/registry parity check** (vs. inline enums):
  Principle VII requires closed registries as first-class, versioned artifacts;
  the parity check is how "closed" is proven when JSON Schema cannot import an
  external enum. Justified, not excess.
- **Self-describing fixture envelope + fixture index** (vs. bare instances):
  required by Q5/FR-019/FR-023/SC-009 so any draft-2020-12 implementation can
  run conformance without the Python validator.

## Project Structure

### Documentation (this feature)

```text
specs/001-avc-contract-kernel/
├── plan.md              # This file (/speckit-plan output)
├── research.md          # Phase 0 output — engineering decisions
├── data-model.md        # Phase 1 output — artifact/entity model
├── quickstart.md        # Phase 1 output — validation/run guide
├── contracts/
│   └── README.md        # Phase 1 output — interface-surface inventory (plan-level)
├── spec.md              # Clarified specification
├── clarify-questions.md # Clarify block + accepted answers
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root — the realized deliverable)

```text
contracts/avatar-client/                       # OWNED EXCLUSIVELY BY THIS CHANGE
├── shared-definitions.schema.yaml             # common $ref target
├── avc-01-session-request.schema.yaml
├── avc-02-session-result.schema.yaml          # discriminated grant|denial|terminal
├── avc-04-session-event.schema.yaml           # incl. AVC-05 transcript payload
├── avc-06-structured-confirmation.schema.yaml
├── avc-07-retention-profile.schema.yaml
├── avc-08-persona-profile.schema.yaml
├── avc-11-session-command.schema.yaml
├── avc-12-state-snapshot.schema.yaml
├── registries/
│   ├── session-result-reasons.registry.yaml   # exactly 15 reasons
│   ├── events.registry.yaml
│   ├── commands.registry.yaml
│   ├── retention-classes.registry.yaml
│   ├── capabilities.registry.yaml
│   ├── interaction-modes.registry.yaml
│   ├── session-outcomes.registry.yaml
│   ├── fallback-modes.registry.yaml
│   └── consent-purposes.registry.yaml         # exactly 3 neutral purposes
├── fixtures/
│   ├── index.yaml                             # self-describing fixture-case manifest
│   └── <schema>/<case>.yaml                    # valid|invalid|boundary|compat|
│                                               # unknown-field|unknown-authority|
│                                               # redaction|adversarial cases
├── acceptance-map.yaml                        # realized from supporting-docs map
├── evidence-register.yaml                     # consolidated evidence/disposition (Q4)
├── interface-lock.yaml                        # frozen decisions + f0_evidence_pin (Q6)
├── redaction/
│   ├── denylist-patterns.yaml                 # content-scan patterns (validator config)
│   └── sentinels.yaml                         # bounded synthetic sentinels
└── README.md                                  # avatar-client contract index (Status header)

scripts/
└── validate-avatar-client.py                  # reference validator (unpinned tooling)

# Shared release metadata — edited ONLY at the serialized final realization step:
contracts/manifest.yaml                        # + avatar-client entries w/ per-file digests
contracts/CHANGELOG.md                         # + contract-v1.7 entry
contracts/README.md                            # + avatar-client family in doc index
```

**Structure Decision**: Single-project, contract-first layout. All canonical
artifacts live under `contracts/avatar-client/` (this change's exclusive write
surface); the sole executable is the ratified validator under `scripts/`. Shared
release metadata files are the only intentional write overlap with the UI
sibling and are touched atomically only at realization, after F0 `PASS`. The F0
evidence pin is folded into `interface-lock.yaml` (an `f0_evidence_pin` block) so
it is covered by the already-enumerated interface-lock digest rather than adding
a separate pinned file.

## Design Notes

1. **Two task lists, not duplicated (Principle II).** The OpenSpec change's
   `tasks.md` (1.x–4.x) is the governance handoff and stays authoritative for
   *governance* milestones. The Speckit `tasks.md` produced in Phase 2 is
   authoritative for *implementation* decomposition. This plan maps its artifacts
   to the OpenSpec tasks (e.g. shared-definitions+schemas → 2.x, fixtures+validator
   → 3.1/3.2, release → 3.3, governance/handoff → 4.x) without restating them.
2. **F0-owned evidence schemas (Principle I / Q6).** `f0-results.schema.yaml`
   and `f0-interface-impact.schema.yaml` are authored and versioned by
   `qualify-avatar-brokered-call-feasibility`. This change never copies or
   co-owns them; it records `{f0_source_commit, f0_results_schema_sha256,
   f0_interface_impact_schema_sha256}` in `interface-lock.yaml` and the validator
   loads the pinned schemas from the F0 change path, verifies the digests,
   validates instances, then reads status — failing closed on any mismatch.
3. **Redaction config placement (Q1/Q3).** `redaction/denylist-patterns.yaml`
   and `redaction/sentinels.yaml` are validator configuration shipped in the
   release commit alongside the tooling; they are content-addressed by the commit
   but are NOT in the per-file-digested *semantic* consumed set enumerated in
   FR-022 (which is: 8 schemas, shared-definitions, registries, consent-purpose
   registry, fixtures, acceptance map, interface lock, evidence register). This
   keeps the pinned semantic surface exactly as Q1 enumerated it.

## Complexity Tracking

*No Constitution Check violations. No entries required.*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
