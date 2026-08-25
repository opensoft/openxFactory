# Brainstorm: Session Teardown Must Not Orphan Its Notebook

Status: brainstorm
Kind: architecture
Captured: 2026-08-10
Repository context: openxFactory
Related capability: `workbench-branch-sessions` (007), `lifecycle-notebook-projection`

Free-form capture. Non-normative.

## The observed gap

Two orphaned `xf-session-openxfactory-*` notebooks were found on 2026-08-10
(a live probe's session and a 2026-07-27 demo topic) whose branches and
worktrees had been removed WITHOUT the abandon-session path — so
`retire_session_notebook`/`TORN_NOTEBOOK` never ran, and the notebooks
survived their sessions. Both were verified dead (no branch, no worktree,
joint-liveness signal negative) and hand-deleted.

Two structural facts make this a class, not an accident:

1. **The governed retire path refuses dead sessions.** `--session-ref
   --session-retire` resolves liveness first and refuses a branch with no
   live worktree — correct for preventing invented sessions, but it means
   an already-torn-down session's notebook CANNOT be retired through the
   governed path at all. The only remedy is a hand `nlm notebook delete`,
   which is exactly the ungoverned act the family tries to avoid.
2. **No sweep covers the `xf-session-` namespace.** The orphan sweep is
   deliberately scoped to `xf-wb-*`; lifecycle books are guarded by the
   capacity guard; session notebooks have neither a sweep nor a
   post-mortem reconciliation. An orphan costs shared-account quota
   forever and silently misrepresents the set of live sessions.

## Directions worth staging

- A `--session-sweep` (or an extension of the existing sweep) that lists
  `xf-session-*` notebooks, recomputes each one's (repository, branch)
  liveness with the SAME joint signal the bootstrap uses, and retires the
  dead ones — report-only by default, `--apply` to act.
- Alternatively or additionally: make hand-removal harder to do
  incompletely — the teardown that removes a session worktree (whatever
  invokes `git worktree remove` on a session path) could be required to go
  through the abandon path, with the notebook retire recorded.
- Decide whether an orphaned session notebook is evidence worth an
  import-before-retire pass (the FR-041 return path) or is scratch that
  dies with its session.
