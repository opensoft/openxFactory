# Verification record: Factory MCP authorization profile

Status: record
Kind: report
Lane: openxfactory-5 (openXfactory-5)

This record keeps the evidence the feature's success criteria demand, in the
order it was made. Every run names the tree it ran on. Runs used a Python 3.12
virtual environment built from `requirements/hermes-runtime-contracts.lock`
with `--require-hashes`, the command CI's `pytest-suite` runs
(`research.md` R-11). `jsonschema` is 4.25.1.

## 1. Baseline on `main` `93d13d6c`

- `tests/factory-mcp/`: **88 passed, 203 subtests passed**. This matches feature
  037's final record (88 tests, 203 subtests).
- The same module under a system interpreter that carries a URI format-checker
  package CI's lock does not: 4 failed (`invalid_json_schema` where the tests
  expect `invalid_pointer` or `remote_or_unsafe_schema_reference`). These are
  environment failures, on `main`. That is why every run here uses the
  CI-matched environment.
- Probes of `main`'s validator are recorded in `research.md` § *Starting point,
  measured*.

## 2. Specify, clarify, plan, checklists, tasks, analyze

- **Specify**: `spec.md`, with the requirements-quality checklist
  `checklists/requirements.md`, which passed in one pass.
- **Clarify**: no question. The ratified packet decides every material question
  (spec § Clarifications). The lane's coordinator accepted the verdict, and the
  skipped `before_specify` hook, when it resumed the seat (2026-10-09T17:2xZ).
- **Plan**: `plan.md`, `research.md` (R-1 to R-17), `data-model.md`,
  `contracts/interface.md`, `quickstart.md`. Constitution Check: PASS before and
  after design.
- **Checklists**, run with no focus argument, so at maximum coverage: seven
  domain checklists (`contract`, `security`, `diagnostics`, `outcomes`,
  `compatibility`, `governance`, `acceptance`), 97 items. The pass found seven
  gaps in `spec.md`, each fixed and noted at its item: FR-013's exact
  comparison; the offline limit of a shared audience; runtime token checks
  placed out of scope; FR-019's moving of the unreleased wording; SC-008, the
  engineering domain's expected signals; the operations domain's position; and
  the statement that this feature edits no packet file and lands on its own
  word.
- **Tasks**: `tasks.md`, T001 to T028, red-first by construction.
- **Analyze, round 1** (read-only pass, then fixed under the brief's "Fix what
  analyze finds"):

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| D1 | CRITICAL | Constitution IV requires new documents to be linked into README's document index. The plan relied on the runbook link, while features 034, 035 and 038 each have a README Documentation bullet. | Fixed: one README Documentation bullet (T024a); plan row IV updated. |
| B1 | MEDIUM | FR-012's "within the field's bounds" deferred to research. | Fixed: FR-012 states 1 to 2048 characters. |
| B2 | MEDIUM | FR-005's "path" could be read decoded. | Fixed: "as written in the URI, not decoded". |
| F1 | MEDIUM | T025 pushes the branch at the stop; the plan's step 6 did not say so. | Fixed: plan step 6 aligned. |
| D2 | LOW | The constitution names a bare `openspec validate`, while the repository validates through its pinned CLI. | Kept: the pinned entrypoint is the repository's documented practice, and stricter. |
| E1 | LOW | FR-018 (runbook) has a review-only witness. | Kept: documentation has no executable witness. |

Coverage after the fixes: 19 of 19 functional requirements and 8 of 8 success
criteria map to tasks, with no unmapped task, no placeholder and no
duplication. No CRITICAL finding remains.
