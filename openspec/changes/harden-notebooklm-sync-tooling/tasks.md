## 1. Baseline and gate

- [ ] 1.1 Record the exact scoped Ruff, basedpyright, and programming-checker findings without suppressions
- [ ] 1.2 Add a repository-local command that runs all three checks over the declared NotebookLM sync surface
- [ ] 1.3 Add focused tests proving the gate includes production, tests, and extracted package files and excludes unrelated Python debt

## 2. Production boundaries

- [ ] 2.1 Extract shared constants and typed immutable models while retaining wrapper re-exports
- [ ] 2.2 Extract the `nlm` subprocess and profile-binding boundary with typed provider rows and drift checks
- [ ] 2.3 Extract corpus discovery without introducing a dependency on provider code
- [ ] 2.4 Extract import planning and lifecycle reconciliation with typed manifest state
- [ ] 2.5 Extract hosting enforcement and parity reporting while preserving read-only behavior
- [ ] 2.6 Extract lazy workbench integration and targeted session synchronization without changing degradation or Git safety behavior
- [ ] 2.7 Extract fail-closed session sweeping and reduce the public script to compatibility exports plus CLI orchestration

## 3. Test boundaries

- [ ] 3.1 Create non-collectable shared sync-test support with a checked dynamic loader and typed isolated fakes
- [ ] 3.2 Split source import and lifecycle-book tests into focused modules
- [ ] 3.3 Split targeted session, session-import, and session-sweep tests into focused modules
- [ ] 3.4 Split hosting and profile-binding tests into a focused module with explicit state reset
- [ ] 3.5 Prove pytest and unittest discovery retain the pre-split test and subtest population and never invoke real `nlm`

## 4. Scoped debt remediation

- [ ] 4.1 Resolve all scoped basedpyright errors without casts, ignore directives, or unbounded `Any`
- [ ] 4.2 Resolve mechanical Ruff findings and the latent loop-closure test defect
- [ ] 4.3 Replace broad and silent exception handling with explicit optional-integration and refusal boundaries
- [ ] 4.4 Bring every new or touched production and test module below the repository size ceiling
- [ ] 4.5 Enable the scoped quality command at a zero-finding baseline

## 5. Verification and evidence

- [ ] 5.1 Run focused and full NotebookLM tests, pytest collection, and unittest discovery
- [ ] 5.2 Run the zero-finding scoped quality command and the repository programming checker
- [ ] 5.3 Run doc-health tests and `openspec validate --all --strict`
- [ ] 5.4 Exercise CLI `--help`, a hermetic dry-run, and an invalid-input refusal through the public script path
- [ ] 5.5 Record realization evidence in this task ledger and commit the governed cleanup in reviewable atomic units
