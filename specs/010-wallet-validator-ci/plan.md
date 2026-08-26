# Implementation Plan: Wallet Validator CI Gate (S1)

**Branch**: `010-wallet-validator-ci` | **Date**: 2026-08-23 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/010-wallet-validator-ci/spec.md`

## Summary

Wire the existing, unmodified `scripts/validate-openxwallet.py` into a new GitHub Actions
workflow named `wallet-validation` that runs on every PR targeting main (drafts included),
fails closed within a 10-minute budget, and proves both directions every run: packaged
negative specimens must fail with declared reasons (validator layer 1) and the live tree
must pass clean (layer 2). Per convener authorization (Clarification Q6 / FR-011) the
delivered scope additionally includes the kind-aware syntax-gate helper
(`scripts/wallet-yaml-syntax-gate.py`) with its pytest suite, closing QA's proved
invalid-YAML fail-open, and `.github/CODEOWNERS` owner-routing the gate surfaces.
A README section records the single post-merge operator act that upgrades the check
from advisory to required. The validator's code, schemas, and
rules are untouched; no register is created (S4's deliverable).

## Technical Context

**Language/Version**: Python 3.12 (CI via `actions/setup-python@v5`, matching
`doc-health-reusable.yml`); workflow YAML

**Primary Dependencies**: pyyaml + jsonschema>=4.18 + rfc3339-validator — hard requirements of the validator,
whose module the syntax-gate helper importlib-loads (so ALL THREE are required for
every check run, gate included). CI installs all three explicitly.

**Storage**: N/A (no state; read-only validation)

**Testing**: Validator-native self-test (research.md R3) PLUS a dedicated pytest suite
for the convener-authorized syntax gate: `tests/wallet_yaml_syntax_gate/` (4 cases,
see research.md R7).

**Target Platform**: GitHub Actions, `ubuntu-latest`

**Project Type**: CI wiring in a contract-governance repository (no runtime service)

**Performance Goals**: Full two-layer sweep well under the 10-minute fail-closed budget
(observed tree size ≈3.4k files)

**Constraints**: Validator semantics locked (FR-002); warnings-pass-log-only (FR-010,
Q3 ruling); single named exclusion is validator-native (Q5) while kind-aware syntax
hardening lives in the committed helper per convener authorization (FR-011, Q6);
least privilege (`permissions: contents: read`); check name literal
`wallet-validation` for branch-protection pinning (FR-007)

**Scale/Scope**: Original build was one workflow + one README section; Phase 7
(convener authorization) added the syntax-gate helper, its pytest suite, and
`.github/CODEOWNERS`. Deliberately nothing beyond those.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design — PASS.*

| Principle | Verdict | Notes |
|---|---|---|
| I. Contract-first neutral core | PASS | Adds no domain vocabulary or behavior; wires a neutral validator |
| II. Governed change flow | PASS | Realizes named successor S1 of ratified `add-wallet-carried-review-authority`; speckit feature per protocol handoff |
| III. Document lifecycle/status | PASS | Spec/plan remain Draft until realization evidence; README addition carries no status claim |
| IV. Schema & artifact discipline | PASS | Workflow YAML is not a governed schema artifact; no credentials; repo-relative paths only; README section linked from existing doc surface |
| V. Validation gates (NON-NEGOTIABLE) | PASS by construction | The feature's entire purpose is making a validator a required pre-push gate; implementation evidence will include green runs of `validate-openxwallet.py`, `openspec validate --all --strict`, and affected repo validators |
| VI. Versioned content-addressed releases | PASS | No `contracts/` artifact touched; no bundle cut |
| VII. Fail-closed authority boundaries | PASS | FR-006 fail-closed on error/timeout; `permissions: contents: read`; operator settings act kept human-only (PART III floor) |

**Shared-tree/worktree discipline**: all work performed in feature worktree
`openxFactory-worktrees/010-wallet-validator-ci`; root checkout untouched on `main`.

## Project Structure

### Documentation (this feature)

```text
specs/010-wallet-validator-ci/
├── plan.md              # This file
├── research.md          # Phase 0 output — decisions & rationale
├── data-model.md        # Phase 1 output — entities touched by the check
├── quickstart.md        # Phase 1 output — runnable validation scenarios
├── clarify-questions.md # Clarification record (specify/clarify phase)
├── checklists/          # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
.github/workflows/
└── wallet-validation.yml        # NEW — the check
.github/CODEOWNERS               # NEW — owner-routing of gate surfaces (convener ruling)
README.md                        # MODIFIED — "Wallet validation gate" section (FR-007)
scripts/validate-openxwallet.py  # UNCHANGED (FR-002)
scripts/wallet-yaml-syntax-gate.py # NEW — FR-011 kind-aware syntax gate helper
tests/wallet_yaml_syntax_gate/     # NEW — pytest coverage for the helper
contracts/openxwallet/**           # UNCHANGED
```

**Structure Decision**: Single-project CI wiring. The diff is one workflow file, one
README section, the FR-011 helper with its tests, and CODEOWNERS routing.
`contracts/` skipped deliberately — this feature exposes no external interface
contract; the interface IS the check name and exit semantics documented in
quickstart.md.

## Complexity Tracking

No constitution violations to justify — table intentionally empty.
