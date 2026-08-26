## 1. Baseline and gate

- [x] 1.1 Record the exact scoped Ruff, basedpyright, and programming-checker findings without suppressions
  - Baseline reproduced 2026-08-24 over `scripts/sync-notebooklm-books.py` and
    `tests/notebooklm/`: `uvx ruff check ...` (Ruff 0.16.4) reported 36
    findings; `uvx basedpyright ...` (basedpyright 1.39.10 / pyright 1.1.412)
    reported 61 errors and 1,626 warnings; the programming skill's
    `check-no-excuse-rules.py ...` reported 36 violations in five files.
    These are unsuppressed current-tool results; the proposal's earlier
    basedpyright measurement of 46 errors is retained as historical context.
- [x] 1.2 Add a repository-local command that runs all three checks over the declared NotebookLM sync surface
  - `python3 scripts/check-notebooklm-sync-quality.py` runs Ruff,
    basedpyright, and the programming checker over one shared path tuple.
- [x] 1.3 Add focused tests proving the gate includes production, tests, and extracted package files and excludes unrelated Python debt
  - `python3 -m pytest tests/notebooklm/test_sync_quality_gate.py -q` passed
    (2 tests); `--show-surface` exposes the exact governed path set and the
    basedpyright command is pinned to its zero-error contract.

## 2. Production boundaries

- [x] 2.1 Extract shared constants and typed immutable models while retaining wrapper re-exports
  - `scripts/notebooklm_sync/models.py` owns the frozen records and constants;
    the public script retains compatibility imports. Focused Ruff and
    basedpyright checks report zero findings.
- [x] 2.2 Extract the `nlm` subprocess and profile-binding boundary with typed provider rows and drift checks
  - `scripts/notebooklm_sync/nlm_client.py` owns subprocess JSON parsing,
    `NotebookRow`/`SourceRow`, bound-profile/cache state, and explicit reset
    hooks. The 95-test suite plus 7 subtests passes, including drift refusal.
- [x] 2.3 Extract corpus discovery without introducing a dependency on provider code
  - `scripts/notebooklm_sync/corpus.py` imports only shared models and stdlib;
    focused Ruff and basedpyright checks report zero findings and corpus tests
    remain green.
- [x] 2.4 Extract import planning and lifecycle reconciliation with typed manifest state
  - Planning, rendering/execution, lifecycle identity/creation, reconciliation,
    and oversized upload behavior now live in focused `notebooklm_sync`
    modules. `SyncManifest` is explicit, each extracted module passes Ruff and
    basedpyright, and the 95-test suite plus 7 subtests remains green.
- [x] 2.5 Extract hosting enforcement and parity reporting while preserving read-only behavior
  - `hosting.py` owns declaration parsing, validation, and injected profile
    enforcement; `parity.py` owns read-only reconciliation. Focused Ruff and
    basedpyright checks are clean and the compatibility suite remains green.
- [x] 2.6 Extract lazy workbench integration and targeted session synchronization without changing degradation or Git safety behavior
  - `workbench.py` owns the injected optional-integration flow while the public
    wrapper retains lazy dashboard loading; `session.py` owns targeted session
    resolution and synchronization. The combined sync/workbench suite passes
    with 101 tests plus 7 subtests.
- [x] 2.7 Extract fail-closed session sweeping and reduce the public script to compatibility exports plus CLI orchestration
  - Session discovery, import, sync, and fail-closed sweep logic now live in
    focused modules; three typed compatibility facades preserve the public
    script's monkeypatch seams. The wrapper is 217 lines, every production
    module is below 250 lines, CLI `--help` succeeds, and the combined sync and
    workbench suite passes with 101 tests plus 7 subtests.

## 3. Test boundaries

- [x] 3.1 Create non-collectable shared sync-test support with a checked dynamic loader and typed isolated fakes
  - `tests/notebooklm/_sync_test_support.py` validates each dynamic import,
    owns typed provider/registry doubles, and remains non-collectable.
- [x] 3.2 Split source import and lifecycle-book tests into focused modules
  - Source import and lifecycle projection cases now live in
    `test_source_import.py` and `test_lifecycle_books.py`; neither imports a
    `test_*.py` module.
- [x] 3.3 Split targeted session, session-import, and session-sweep tests into focused modules
  - Session lifecycle, refresh, import, binding, and namespace sweep cases now
    live in five responsibility-specific modules.
- [x] 3.4 Split hosting and profile-binding tests into a focused module with explicit state reset
  - Hosting declaration/refusal and profile-binding cases are separated, and
    every stateful class releases the bound profile in `tearDown`.
- [x] 3.5 Prove pytest and unittest discovery retain the pre-split test and subtest population and never invoke real `nlm`
  - The pre-split baseline was 118 tests plus 13 subtests. Final pytest
    collection finds 127 tests; pytest and guarded unittest both pass all 127
    plus the 13 pytest subtests, with the structural `nlm` refusal guard active.

## 4. Scoped debt remediation

- [x] 4.1 Resolve all scoped basedpyright errors without casts, ignore directives, or unbounded `Any`
  - The scoped command reports `0 errors, 0 warnings, 0 notes` at its declared
    basic mode with warnings configured as fatal; the programming checker also
    confirms no cast/ignore/`Any` escape hatch exists on the surface.
- [x] 4.2 Resolve mechanical Ruff findings and the latent loop-closure test defect
  - Ruff reports zero findings. The profile-answer subtest now binds each loop
    value in the injected lambda rather than closing over the moving variable.
- [x] 4.3 Replace broad and silent exception handling with explicit optional-integration and refusal boundaries
  - Extracted boundaries catch declared operation errors; the programming
    checker reports no broad, bare, or silent exception handling.
- [x] 4.4 Bring every new or touched production and test module below the repository size ceiling
  - The programming checker reports no size violations across 41 files; the
    largest governed module is 239 pure lines, below the 250-line ceiling.
- [x] 4.5 Enable the scoped quality command at a zero-finding baseline
  - `PROGRAMMING_CHECKER=... python3 scripts/check-notebooklm-sync-quality.py`
    passes Ruff, basedpyright, and the programming checker with zero findings.

## 5. Verification and evidence

- [x] 5.1 Run focused and full NotebookLM tests, pytest collection, and unittest discovery
  - Final evidence: 127 collected; pytest passed 127 tests plus 13 subtests;
    guarded unittest passed the same 127 tests.
- [x] 5.2 Run the zero-finding scoped quality command and the repository programming checker
  - Final evidence: Ruff clean, basedpyright zero, and no violations in 41
    files from `check-no-excuse-rules.py`.
- [x] 5.3 Run doc-health tests and `openspec validate --all --strict`
  - Strict OpenSpec validation passed all 75 artifacts. Doc-health passed all
    744 tests with one existing deprecation warning.
- [x] 5.4 Exercise CLI `--help`, a hermetic dry-run, and an invalid-input refusal through the public script path
  - Public-path probes returned `help=0`, `dry-run=0`, and argparse refusal
    `invalid-input=2` against an isolated provider stub. A regression test pins
    the default import date that previously made the dry run crash.
- [x] 5.5 Record realization evidence in this task ledger and commit the governed cleanup in reviewable atomic units
  - Governance artifacts are isolated in `4a2f76d9`; implementation and tests
    are isolated in `94630019`. Review remediation is split into provider
    refusal `41c721e0`, pre-provider input validation `52f2fc67`, optional
    adapter degradation `bc4ca1ea`, configured type diagnostics `1201dd60`,
    and mechanical test normalization `620613da`; this ledger records the
    realization evidence.
