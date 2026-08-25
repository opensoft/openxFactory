---
code_surface: openxFactory (a fourth `sync-notebooklm-books.py` mode reconciling the `xf-session-` namespace against live sessions — forward-derived, fail-closed, workspace-scoped, report-only by default; unit coverage over the derivation and every refusal)
target_release: none
Status: ratified
Ratified: Brett, 2026-08-10 — "fix the session teardown notebook gap"
Realized: merged to openxFactory main as 1b964ba (PR #163, 2026-08-10) and green on the implemented target — `tests/ideation-dashboard` 2850 passed / 5 skipped / exit 0 (2026-08-13), which carries this change's derivation and refusal coverage including `test_a_session_opened_from_a_feature_worktree_is_seen_as_live`. Recorded at the archive gate, which requires the evidence to exist rather than merely to be true.
---

# Proposal: add-session-notebook-reconciliation

## Why

A branch session's notebook is supposed to die with its session. The
`ideation-dashboard` capability already says so: on either governed ending — the
pull request MERGES, or a human ABANDONS — the worktree, the registry entry and
the session notebook are torn down together.

Sessions also end a third way, and that way retires nothing. A probe removes its
worktree and branch by hand. A crash leaves residue that someone clears. Neither
goes through `abandon-session`, so `retire_session_notebook` never runs, and the
notebook survives on an account shared across the whole family.

Two structural facts make this a class rather than an accident:

**The governed retire path refuses a dead session.** `--session-ref
--session-retire` resolves liveness first and refuses a branch with no live
worktree. That refusal is correct and this change does not touch it: it is what
stops the sync inventing a session and retiring a notebook that belongs to a
live one. But it means the ONE case that needs cleaning — a session that is
already gone — has no governed door at all. The only remedy left is a hand
`nlm notebook delete`, which is exactly the ungoverned act the session-notebook
design exists to prevent.

**No sweep covers `xf-session-`.** The orphan sweep is deliberately scoped to
`xf-wb-*`; the lifecycle books have the capacity guard; session notebooks have
neither a sweep nor a post-mortem reconciliation. An orphan holds shared-account
quota forever and misstates the set of live sessions to anyone reading the
account.

On 2026-08-10 both facts collected their bill: two orphans were found on the
live account (a probe's session from that morning, and a demo topic from
2026-07-27), verified dead by hand-comparing notebook titles against git state,
and deleted by hand. The deletion was recorded, which is the best outcome
available and still the wrong shape — comparing titles to worktrees is a
judgment this capability should be making from the joint liveness signal it
already owns.

## What Changes

A fourth sync mode, `--session-sweep`, which RECONCILES the `xf-session-`
namespace against the live-session set and retires what no session claims.

Five properties, each of which is a decision rather than an implementation
detail, and each of which exists because getting it wrong destroys work on a
shared account:

1. **Forward-derived detection.** `notebook_alias` is lossy — it strips `draft/`
   and lowercases — so a notebook title can never be inverted to a
   `(repository, branch)` key. Detection therefore runs in the only sound
   direction, the one `session_target_for_alias` already uses: compute every
   live session's own alias, and treat an `xf-session-` notebook matching none
   of them as dead.
2. **Fail closed on incomplete knowledge.** A session repository that cannot be
   enumerated — absent checkout, git failure, unreadable worktree list — looks
   EXACTLY like a set of dead sessions, and the difference is unrecoverable
   after a delete. Any such repository refuses the whole reconciliation rather
   than retiring what it could not account for.
3. **Scoped to this workspace's session repositories.** The account is shared. A
   session notebook whose repository slug names a repository this workspace does
   not carry belongs to someone else's workspace and is not this run's to judge;
   it is reported as out of scope, never retired.
4. **Report-only by default; `--apply` to act** — the property every other mode
   of this sync already has, and what lets a human read the verdict first.
5. **Retirement through `retire`, never `delete`.** The same adapter operation
   the governed endings use, so the session-prefix and key-derived-title guards
   apply here identically. An adapter without `retire` refuses loudly.

This also gives the session-notebook lifecycle its third retirement route, which
is the half of the gap the sweep cannot express on its own: a session that ended
without a governed ending is now reconcilable, and the record says a
reconciliation retired it rather than a human did.

## Impact

- `lifecycle-notebook-projection` — MODIFIED: the new mode, its fail-closed
  rule, and its scoping rule.
- `ideation-dashboard` — MODIFIED: the session-notebook lifecycle admits a third
  retirement route for a session that ended outside the two governed endings.
- `scripts/sync-notebooklm-books.py` — the mode, reusing `live_session_targets`,
  `session_repositories`, `notebook_alias` and `retire_session_notebook` rather
  than re-deriving any of them.
- No contract release: no schema changes, no new artifact kinds
  (`target_release: none`).

## Deliberately out of scope

- **Narrowing hand teardown.** The brainstorm's second direction — route every
  session-worktree removal through the abandon path — is a separate change with
  its own compatibility surface: probes and crash recovery legitimately remove
  worktrees, and forbidding that is a different argument from cleaning up after
  it.
- **Import-before-retire.** Whether an orphaned notebook is evidence worth the
  FR-041 return path stays open, and is answered NO for this cut: a session with
  no worktree has nothing to import back into. The report names how many sources
  a retirement would discard, so the one lossy case — a notebook carrying
  hand-added sources — is visible before `--apply` rather than argued about in
  the abstract.
- **Cadence.** Manual, like every other mode of this sync. Whether the nightly
  lane should run the report belongs with the doc-health nightly question.
