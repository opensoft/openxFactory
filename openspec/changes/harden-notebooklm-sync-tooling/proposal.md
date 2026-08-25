---
code_surface: openxFactory (`scripts/sync-notebooklm-books.py`, a new `scripts/notebooklm_sync/` package, the NotebookLM sync tests, and repository-local scoped Python quality gates)
target_release: implementation_pending — code-only tooling hardening; no contract bundle or release tag
Status: draft
Proposed: 2026-08-25 as an ad hoc implementation-quality change requested after the live oversized-source readiness defect was corrected and its surrounding debt was measured.
---

# Proposal: harden-notebooklm-sync-tooling

## Why

The NotebookLM sync CLI is a 2,214-line multi-responsibility module with a
2,333-line primary test module. Its current surface passes its behavioral suite,
but scoped analysis reports 46 basedpyright errors, 36 Ruff findings, and 36
repository programming-checker violations, leaving high-risk provider, profile,
session, Git, and hosting seams difficult to review safely.

## What Changes

- Split the production CLI by responsibility while preserving the existing
  executable path, flags, mode precedence, public helper imports, and observable
  behavior.
- Split the monolithic test module along the same responsibility boundaries
  without weakening cases or reducing discovery under pytest or unittest.
- Replace untyped provider JSON, mutable implicit state, dynamic module seams,
  and test fakes with explicit typed boundaries; use no type suppressions.
- Resolve the scoped Ruff and programming-checker findings without changing
  lifecycle projection semantics or optional-integration failure policy.
- Add reproducible repository-local quality commands that fail on new Ruff,
  basedpyright, or programming-checker debt in the NotebookLM sync surface.

## Capabilities

### New Capabilities

- `notebooklm-sync-tooling-quality`: Repository-local quality and compatibility
  gates for the NotebookLM sync implementation and its tests.

### Modified Capabilities

None. `lifecycle-notebook-projection` remains the owning product capability,
but this change does not alter scan membership, book identity, dry-run/apply
behavior, parity, source mutation rules, hosting/profile policy, or session
semantics.

## Impact

- Affected implementation: `scripts/sync-notebooklm-books.py` and a new
  `scripts/notebooklm_sync/` package.
- Affected tests: `tests/notebooklm/test_sync_notebooklm_books.py` and focused
  successor modules plus non-collectable shared support.
- Affected tooling: a checked-in scoped quality-gate entry point and its tests.
- Compatibility: the hyphenated CLI path and existing flags remain unchanged;
  helper symbols imported by current tests remain available during extraction.
- Contracts and releases: no files under `contracts/` change and no contract
  bundle is cut; the new OpenSpec capability governs code quality only.
