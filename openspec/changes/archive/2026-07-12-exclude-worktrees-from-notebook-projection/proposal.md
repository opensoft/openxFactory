code_surface: codexFactory
target_release: implemented

## Why

The nightly lifecycle-notebook sync dry-run reported ~230 pending operations,
~39 of which were triplicated sources from `xFactories/OpsxFactory-worktrees/`
— three feature-branch worktree checkouts the scan treated as a governed
repository named `OpsxFactory-worktrees`. Applying would have published
duplicate, unmerged branch content into the shared Ideation/Drafts/Canon
books under colliding titles, so the sync has been held and reconciliation
drift has accumulated. The promoted projection spec requires an OpenSpec
delta before the sync implementation changes its exclusions, and the scan
corpus was never a spec requirement at all — only prose in the standard
workflow doc.

## What Changes

- Add a corpus scan scope requirement to `lifecycle-notebook-projection`:
  the projection scans the openxFactory repository and each DomainxFactory
  under `xFactories/`, and excludes nested git working copies below a
  scanned repository root — feature-branch worktree checkouts (including
  `<repo>-worktrees/` containers), embedded clones, and nested submodule
  installs.
- Fix the codexFactory sync implementation's `scan()`: filter `*-worktrees`
  containers out of the repository base list and prune any document below a
  nested `.git` entry; add regression tests.
- Update the standard workflow doc's scope line to match the promoted
  wording.
- Unblock and apply the accumulated reconciliation backlog once the dry-run
  shows no worktree-derived operations.

## Capabilities

### Modified Capabilities

- `lifecycle-notebook-projection`: Adds the corpus scan scope requirement;
  book membership, framing, grounding, and hybrid behavior are unchanged.

## Impact

- **codexFactory:** `scripts/sync-notebooklm-books.py` scan filtering plus
  regression tests in `tests/notebooklm/`.
- **openxFactory:** the spec delta and the standard doc's scope line.
- **xFactory aggregation:** the nightly sync is unblocked; no runner change.
- **Notebooks:** no worktree source was ever applied — the defect was caught
  in dry-run — so reconciliation is additive/update-only for governed docs.
