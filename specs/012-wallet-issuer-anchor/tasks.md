# Tasks: Wallet Issuer Anchor (S2)

**Feature**: 012-wallet-issuer-anchor | **Branch**: `012-wallet-issuer-anchor` | **Date**: 2026-08-24
**Input**: [spec.md](./spec.md) · [plan.md](./plan.md) · [research.md](./research.md) · [data-model.md](./data-model.md) · [quickstart.md](./quickstart.md)

Scope guard (ratified tasks §3.1): NO schema edit, NO manifest entry, NO CHANGELOG line, NO bundle cut. Validator + packaged specimens + spec artifacts only.

## Phase 1 — Setup

- [x] T001 Baseline evidence: validator self-test green on the untouched tree (exit 0; corpus counts recorded in implementation notes as the pre-S2 half of SC-002).

## Phase 2 — User Story 1: a review-authority grant without an issuer is refused (P1)

- [x] T002 [US1] Add named constants beside `CUSTODY_REGISTRY_PATH`: `REVIEW_ACT_TOKEN = "review"` (cited to review-authority-intake requirement 1), `ROOT_ISSUER_OPERATOR_TOKEN = "Brett Heap"` (comment cites HEC `docs/roles-and-authority.md:103-140`), machine-shape regex. Class detection in `check_grant()`: REVIEW-CLASS iff token ∈ `scope.acts`; no other trigger.
- [x] T003 [US1] Fire `issuer-unrecorded` on a REVIEW-CLASS grant with absent/falsy `issued_by` (sequential: skips anchor comparison). Register `OXWR-R1`/`OXWR-R2` rows in REQUIREMENTS (FR-006). Module docstring gains rule (t).
- [x] T004 [P] [US1] Specimen `grant-review-authority-omits-issued-by.yaml` — header pins `issuer-unrecorded`, requirement `OXWR-R1`; body otherwise schema-valid (resolving audience, legal posture, tier within ceiling).

## Phase 3 — User Story 2: root grants answer to the operator anchor alone (P2)

- [x] T005 [US2] Root-anchor rule: ROOT review-class grant with `issued_by` ≠ exact operator token fails `root-issuer-unanchored`; message distinguishes machine-named values (wallet-id resolution or machine shape) from the legacy string (`opensoft`) and other unanchored values. Exact match, fail-closed, no normalization.
- [x] T006 [P] [US2] Specimen `grant-review-root-issuer-is-a-machine.yaml` — pin on the subject token (machine branch), requirement `OXWR-R2`.
- [x] T007 [P] [US2] Specimen `grant-review-root-issuer-says-opensoft.yaml` — pin on the word `legacy` (legacy branch, not merely the code), requirement `OXWR-R2`.

## Phase 4 — User Story 3: non-review grants stay untouched (P3)

- [x] T008 [US3] Self-test boundary guard: synthesized schema-valid `post_transaction` root grant with NO `issued_by` must validate with ZERO findings inside the self-test (fails loudly as `boundary-guard-failed` otherwise).

## Phase 5 — Polish & Cross-Cutting

- [x] T007x Gates: full sweep exit 0 with post-S2 counts recorded as SC-002 evidence; five packaged positives unchanged; `pytest tests/wallet_yaml_syntax_gate/ -q`; `openspec validate --all --strict`.
- [x] T010 Orchestrator cross-check: FR-001…FR-008 / SC-001…SC-003 walk marking satisfied-by-evidence; nothing silent.

## Dependencies

T002 → T003 → T005 (codes must exist before specimens can fail for their reasons);
T004/T006/T007 need their codes but are independent of each other ([P]);
T008 after T002–T003 (guard proves the class boundary the detection drew);
gates last.

## Implementation strategy

Single-module widening: constants → class detection → two codes → REQ rows →
specimens → boundary guard → full-sweep evidence. Every intermediate state stays
green except the deliberate window between code landing and specimens joining
(coverage closure tolerates uncovered rows only as failures — so code+rows land
in one commit with specimens, keeping every committed tree self-test-green).
