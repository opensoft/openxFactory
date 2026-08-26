# Staged: a session notebook never outlives its session

Status: staged
Kind: capability-proposal
Summary: Give the workspace a governed way to retire the NotebookLM notebook of
a branch session that no longer exists, so a session torn down outside the two
governed endings cannot leave its notebook alive on the shared account forever.
Organized 2026-08-10 from the `session-teardown-notebook-coupling` brainstorm at
the point the gap stopped being theoretical: two orphans were found on the live
account, both had to be deleted BY HAND, and the hand delete is precisely the
ungoverned act the session-notebook design exists to prevent.
Topics: session-notebooks, branch-sessions, notebook-projection, orphan-reconciliation, shared-account-quota, fail-closed
Repository context: openxFactory owns both halves — the session notebook
lifecycle (`ideation-dashboard`, promoted from workbench-branch-sessions) and
the sync that operates the projection (`lifecycle-notebook-projection`); the
notebooks live on ONE account shared across the family, so a wrong delete is
someone else's live session
Staging ID: openxFactory:staging:session-notebook-reconciliation
Source: `ideation/brainstorm/session-teardown-notebook-coupling.md` (2026-08-10,
filed with PR #161 alongside the hand deletion it records)
Target capabilities: MODIFIED `lifecycle-notebook-projection` (a fourth sync
mode: reconcile the `xf-session-` namespace against live sessions, report-only
by default) and MODIFIED `ideation-dashboard` (the session-notebook lifecycle
gains a THIRD retirement route, for a session that ended without one)

## Why this is staged now

The brainstorm named two structural facts. Both are still true, and the second
is what makes this a class rather than an incident:

1. **The governed retire path refuses a dead session.** `--session-ref
   --session-retire` resolves liveness first and refuses a branch with no live
   worktree. That refusal is CORRECT and must stay: it is what stops the sync
   inventing a session and deleting a notebook that belongs to a live one. But
   it also means the one case that needs cleaning — a session that is already
   gone — has no governed door at all.
2. **No sweep covers `xf-session-`.** The orphan sweep is deliberately scoped to
   `xf-wb-*`; the lifecycle books have the capacity guard; session notebooks have
   neither. An orphan holds shared-account quota forever and, worse, misstates
   the set of live sessions to anyone reading the account.

The forcing event: on 2026-08-10 two orphans were found (a probe's session from
that morning, and a demo topic from 2026-07-27), verified dead, and deleted by
hand. The deletion was recorded, which is the best available outcome and still
the wrong shape — a human comparing titles to git state is exactly the judgment
this capability should be making from the joint liveness signal.

## Claims

1. Orphan detection MUST be FORWARD-DERIVED. The alias transform is lossy
   (`notebook_alias` strips `draft/` and lowercases), so a title cannot be
   inverted to a `(repository, branch)` key. The only sound direction is the one
   `session_target_for_alias` already uses: compute every live session's own
   alias and treat an `xf-session-` notebook matching none of them as dead.
2. The sweep MUST FAIL CLOSED on incomplete knowledge. Deleting on a partial
   live set is the one failure that destroys work: if any session repository
   cannot be enumerated (absent checkout, git error, unreadable worktree list),
   the run MUST refuse the whole reconciliation rather than retire what it could
   not account for. A missing repository looks exactly like a dead session, and
   the difference is not recoverable after the delete.
3. The sweep MUST be scoped to THIS WORKSPACE's session repositories. The
   account is shared; a session notebook whose repo-slug names a repository this
   workspace does not carry is someone else's, and is not this run's to judge.
4. Report-only by default, `--apply` to act — the property every other mode of
   this sync already has, and the one that lets a human read the verdict before
   any deletion.
5. Retirement MUST go through the SAME adapter operation the governed endings
   use (`retire`, never `delete`), so the prefix and key-derived-title guards
   that PR #49 hardened apply identically here.

## Open questions

1. **Is an orphaned session notebook evidence?** The brainstorm asks whether an
   import-before-retire pass (the FR-041 return path) is owed. Leaning NO for
   the first cut: a session notebook is derived from the session's own worktree
   documents, and a session that no longer exists has no worktree to import
   back into. A notebook holding hand-added sources is the only case where this
   is lossy, and it argues for reporting what a retirement would discard rather
   than for a whole import pass.
2. **Should hand teardown be made harder?** The brainstorm's second direction —
   route every session-worktree removal through the abandon path. Out of scope
   here: this topic closes the hole, and narrowing the hand path is a separate
   change with its own compatibility surface (probes and crash recovery
   legitimately remove worktrees).
3. **Cadence.** Manual for now, like the rest of the sync. Whether the nightly
   lane should run the reconciliation report belongs with the doc-health
   nightly question, not here.

## Exit path

One OpenSpec change against `lifecycle-notebook-projection` (the new mode, its
fail-closed rule, and the scoping rule) and `ideation-dashboard` (the third
retirement route in the session-notebook lifecycle), realized in
`scripts/sync-notebooklm-books.py` with unit coverage over the derivation and
the refusal, and a recorded dry-run against the live account as realization
evidence.
