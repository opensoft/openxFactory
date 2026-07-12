# Tasks: Exclude Worktrees From Notebook Projection

## 1. Contract (openxFactory)

- [x] 1.1 Add the corpus scan scope requirement to `lifecycle-notebook-projection` and pass strict OpenSpec validation.
- [x] 1.2 Update the `docs/lifecycle-notebook-projection.md` scope line to match the promoted wording.

## 2. Implementation (codexFactory)

- [x] 2.1 Filter `*-worktrees` containers out of the repository base list and prune documents below a nested `.git` entry in `scan()`.
- [x] 2.2 Add regression tests (worktree container excluded, nested clone excluded, governed doc still projects, no `-worktrees` repo title) and run the notebooklm test suite green.

## 3. Reconciliation And Evidence

- [x] 3.1 Verify the workspace dry-run reports zero worktree-derived operations (backlog dropped 230 -> 194 legitimate operations).
- [ ] 3.2 Apply the accumulated reconciliation backlog and confirm a clean follow-up dry-run.
- [ ] 3.3 Sync the aggregation repo's codexFactory (and openxFactory) submodule pointers.
