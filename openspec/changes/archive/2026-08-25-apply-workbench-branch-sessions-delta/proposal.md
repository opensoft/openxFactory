---
code_surface: none — no module, test, workflow, schema, threshold or governed document changes. The whole of this packet is the restatement of an already-ratified spec delta plus the task-box tick that records its discharge. The promotion-fidelity family that reported the gap is untouched: this change clears its two findings by making canon match the ratified text, never by editing the check, its resolution rules, or `health/dispositions.yaml`.
target_release: implemented (promotion-only — the ratified text reaching canon IS the release; `code_surface: none`, so this change archives on landing with no separate realization evidence)
Status: ratified
Ratified: 2026-08-24 by Brett — in-session ruling, verbatim: "fix the workbench-branch-sessions promotion gap". That ruling is the ratification act for this packet, which adds no normative content of its own: its delta is the delta already ratified and archived 2026-08-01 by `add-workbench-branch-sessions`. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing its three-way floor on two axes rather than the one it needs: approver (`by Brett`) and date (`2026-08-24`).
Proposed: 2026-08-24
Origin: the promotion-fidelity family's FIRST LIVE CATCH, recorded as task 5.1 of `add-promotion-fidelity-check` ("openxFactory's own two findings ... Needs the same decision that gap needed: apply the ratified delta via a proper change, or record the non-promotion as deliberate") and in `docs/archive-record-discrepancies.md` § FU-DOM-CODEX's PREVENTION addendum of 2026-08-24/25.
---

# Proposal: apply-workbench-branch-sessions-delta

## Why

**A ratified ADDED requirement never reached canon, and a ratified MODIFIED
one arrived a scenario short.** The archived change
`add-workbench-branch-sessions`
(`openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/`) carried
two delta files. The `ideation-dashboard` one landed whole. The
`lifecycle-notebook-projection` one did not:

- Its ADDED requirement **"Branch-session notebooks"** — the per-session
  `xf-session-<topic>` notebook, its disjointness from the `xf-wb-` reference-set
  namespace, its creation-and-retirement lifetime, the refresh-notebook action,
  the worktree-local hybrid import path, and the `L1 notebook synthesis`
  authority ceiling on its output — is **absent** from
  `openspec/specs/lifecycle-notebook-projection/spec.md`. Not shortened, not
  reworded: absent, along with all five of its scenarios.
- Its MODIFIED requirement **"Corpus scan scope"** reached canon carrying the
  **pre-2026-08-01 body and three of its four ratified scenarios**. The missing
  scenario is "A canon book is offered a branch session's drafts". So is the
  amended body, which is where the delta wrote the normative sentences that
  scenario proves: that the scan is of the governed corpus **at the default
  branch**, that branch-session worktrees are named among the excluded nested
  working copies, and — the load-bearing sentence — that branch-session
  notebooks are the ONLY notebook surface permitted to read a worktree, may
  never contribute a source, a title or a repository name to a lifecycle book,
  and may not relax the exclusion for any book.

The archive act moved the packet; it did not touch the promoted spec.

**This is the class's first live catch, and it is in this repository's own
archive.** `add-promotion-fidelity-check` commissioned the check that compares
archived deltas to promoted specs — the prevention question codexFactory PR #85
left open by name after applying its own unpromoted delta. On its first run the
new family reported exactly two findings, both against
`2026-08-01-add-workbench-branch-sessions`, and the commissioning change
deliberately did not fix them: applying a ratified delta to canon is a
governance act belonging to its own change. That is recorded as its task 5.1,
which names the two lawful exits — apply the ratified delta via a proper
change, or record the non-promotion as deliberate. Brett ruled the first, in
the same shape and for the same reason he ruled the first for codexFactory.

**The realization is not in question — only the text is.** Branch sessions
shipped, session notebooks exist, and the namespace they occupy has since been
built on: `add-session-notebook-reconciliation` (archived 2026-08-13) added a
whole requirement governing the reconciliation of the `xf-session-` namespace
against live sessions. Canon therefore currently describes how to RETIRE a
notebook family whose defining requirement it never admitted, and tells a
reader scanning for a lifecycle book nothing about the one surface that is
allowed to read a worktree.

## What Changes

- Promote the already-ratified `lifecycle-notebook-projection` delta of
  `add-workbench-branch-sessions` into
  `openspec/specs/lifecycle-notebook-projection/spec.md`: the ADDED requirement
  "Branch-session notebooks" with all five scenarios, and the MODIFIED
  requirement "Corpus scan scope" with its amended body and all four.
- The delta file in this packet is a **byte-for-byte copy** of
  `archive/2026-08-01-add-workbench-branch-sessions/specs/lifecycle-notebook-projection/spec.md`
  (identical SHA-256 `f6ffd39abeab7a1548a93ed78fda9a24d8da19606fbc5f30dc85fe013b0361cd`).
  Not a rewrite, not a re-derivation, not a reconciliation with anything learned
  since: the whole point of this change is that ratified content reaches canon
  unchanged. Any improvement to that text is a separate change with its own
  ratification.
- Nothing else. No requirement is added or removed beyond the ratified delta's
  own, no other capability is touched, no code, workflow, schema or test
  changes. The `ideation-dashboard` delta of the same archived change is NOT
  restated: it reached canon whole, and the family reports nothing against it.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `lifecycle-notebook-projection`: gains the requirement "Branch-session
  notebooks" as ratified on 2026-08-01, and its requirement "Corpus scan scope"
  is restated as ratified the same day — the default-branch scope, the
  branch-session worktree exclusion, and the only-surface-that-may-read-a-worktree
  sentence in the body, plus the fourth scenario that proves them.

## Impact

- openxFactory: `openspec/specs/lifecycle-notebook-projection/spec.md` gains one
  requirement with five scenarios and one scenario plus an amended body on
  another. Canon stops describing a notebook family it governs the retirement of
  but never admitted.
- Behavior: none. The described behavior was realized by
  `add-workbench-branch-sessions` and has been built on since; this change moves
  text, not state.
- The promotion-fidelity family's two live findings are cleared by application,
  which was the ruling — not by a `health/dispositions.yaml` entry, and not by
  editing the check.
- Task 5.1 of `add-promotion-fidelity-check` is discharged by this change's
  landing and is ticked in the same branch, append-discipline: the box text
  stands as written and one dated pointer line names this change. That change
  itself stays ACTIVE; its own archive gate is merge-plus-green on its code
  surface and is not this change's to close.
- Realization gate: promotion-only; `code_surface: none`, so this change
  archives on landing with no separate realization evidence.

## Recorded, not fixed

- **The ratified body carries a book count that a later change made stale.**
  "Corpus scan scope" as ratified on 2026-08-01 opens "The three LIFECYCLE
  BOOKS' projection SHALL scan ...", and "Branch-session notebooks" says a
  session notebook "SHALL NOT be one of the three lifecycle books". On
  2026-08-10 `split-ideation-book-per-repo` replaced the single shared Ideation
  book with one per governed repository, so the lifecycle family is now the two
  shared books plus one per repo — not three. Restating the ratified text
  faithfully therefore introduces a stale count into canon that would have been
  equally stale had the delta been promoted on time. It is named here rather
  than silently corrected because correcting it is a normative edit to ratified
  text, which is the one thing this change exists not to do; #85 set the
  precedent in the same words ("any improvement to that text is a separate
  change with its own ratification"). Nothing normative turns on the numeral:
  the classes are named explicitly in the same requirement ("any lifecycle
  book — Ideation, Working Drafts, or Canon"), and the exclusion rule is written
  against those names, not against a count. A successor change reconciling the
  count across `lifecycle-notebook-projection` is the lawful fix.
- **Latest-writer-wins was verified directly, not assumed.** No archived change
  after 2026-08-01 touches either requirement — the three later writers of this
  capability modify "Projection implementation ownership" (2026-08-05),
  "Derived notebook membership" plus an added "Projection capacity guard"
  (2026-08-10), and add "The session namespace is reconciled against live
  sessions" (2026-08-13). Applying the ratified text clobbers no later ratified
  work.
