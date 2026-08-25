---
code_surface: none — this change's whole diff is governance text: one spec delta restating already-ratified requirements, this proposal, its tasks, its origin declaration, the promotion of that delta into `openspec/specs/lifecycle-notebook-projection/spec.md`, and one README record row. No script, workflow, schema, contract, test, or runtime artifact moves, in this repository or any other. Nothing under `contracts/` changes, so no bundle is cut and no digest set moves.
target_release: promotion-only — the ratified text reaching canon IS the release; archives on landing (`code_surface: none`), per `release-realization`'s doc-only default rather than the merge-plus-green gate.
Status: ratified
Ratified: 2026-08-24 by Brett — "apply via a proper change", the ruling on the two open promotion-fidelity findings, recorded in `openspec/changes/add-promotion-fidelity-check/tasks.md` task 5.1 ("RULED (2026-08-24, Brett, the same four-question round): APPLY VIA A PROPER CHANGE — the PR #85 equivalent, with its drift-check-before-apply discipline"). That ruling is the ratification act for this packet, which adds no normative content of its own: its delta is the delta already ratified 2026-07-26 and archived 2026-07-31 by `add-workbench-branch-sessions`. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing the three-way floor on two axes — approver (`by Brett`) and date (`2026-08-24`).
Proposed: 2026-08-24
Origin: `openspec/changes/add-promotion-fidelity-check/tasks.md` task 5.1, and the two findings the promotion-fidelity family reports against this repository's own archive.
---

# Proposal: apply-branch-sessions-deltas

## Why

**Two ratified requirement-deltas never reached the promoted spec.** The
archived change `add-workbench-branch-sessions`
(`openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/`)
carried a `lifecycle-notebook-projection` delta with one ADDED requirement
and one MODIFIED one. Neither is in canon:

- **ADDED `Branch-session notebooks`** is absent from
  `openspec/specs/lifecycle-notebook-projection/spec.md` entirely — the
  requirement that a branch session may carry one `xf-session-<topic>`
  notebook synced from the session's worktree, that the session and
  workbench reference-set namespaces are disjoint so the `xf-wb-*` orphan
  sweep can never take a live session's notebook, that the notebook is
  retired with the session, that the refresh-notebook action grants no
  authority beyond the sync, that hybrid source-return imports land inside
  the session worktree under the unchanged header contract, and that the
  output carries `L1 notebook synthesis` authority. Five scenarios with it.
- **MODIFIED `Corpus scan scope`** reached canon carrying the text of its
  PREVIOUS writer, `2026-07-12-exclude-worktrees-from-notebook-projection`,
  and none of the 2026-07-26 amendment. Absent: the scoping of the rule to
  the three LIFECYCLE BOOKS at the default branch, branch-session worktrees
  named inside the nested-working-copy exclusion, the sentence making
  branch-session notebooks the ONLY notebook surface permitted to read a
  worktree while never contributing a source, title, or repository name to
  a lifecycle book, and the fourth scenario "A canon book is offered a
  branch session's drafts". Canon says three scenarios; the ratified text
  says four.

The archive commit `a0ea7666` (2026-07-31, "Archive
add-workbench-branch-sessions") moved the packet and edited the README. It
did not touch the promoted spec — `git show a0ea7666 --
openspec/specs/lifecycle-notebook-projection/spec.md` is empty.

**A reader of canon today is told the wrong thing twice.** The promoted
capability describes a projection with no session surface at all, and states
a worktree exclusion with no exception — so the one notebook family that is
supposed to read a worktree has no standing in canon, and the guarantee that
it never leaks into a lifecycle book is nowhere stated. The later
`The session namespace is reconciled against live sessions` requirement
(archived 2026-08-13) then governs the `xf-session-` namespace in a spec
that never established it.

**This was found by the check commissioned for exactly this class.** The
promotion-fidelity family (`add-promotion-fidelity-check`, merged
`73766b48`) reports both findings against this repository's own archive on
its first run; they are recorded in that change's tasks §3.2 and §5.1 and
were deliberately not fixed inside it, because applying a ratified delta to
canon is a governance act belonging to its own change. §5.1 named the two
lawful exits — apply the ratified delta via a proper change, or record the
non-promotion as deliberate — and Brett ruled the first, the same ruling and
the same discipline codexFactory PR #85 carried for the equivalent gap in
`merge-master-approval`.

## What Changes

- Promote the already-ratified delta for `lifecycle-notebook-projection`
  into `openspec/specs/lifecycle-notebook-projection/spec.md`: the ADDED
  requirement `Branch-session notebooks` with its five scenarios, and the
  MODIFIED requirement `Corpus scan scope` with its amended body and fourth
  scenario.
- The delta file in this packet is a **byte-for-byte copy** of
  `archive/2026-08-01-add-workbench-branch-sessions/specs/lifecycle-notebook-projection/spec.md`
  (identical SHA-256
  `f6ffd39abeab7a1548a93ed78fda9a24d8da19606fbc5f30dc85fe013b0361cd`). Not a
  rewrite, not a re-derivation, not a reconciliation with anything learned
  since 2026-07-26: the whole point of this change is that ratified content
  reaches canon unchanged. Any improvement to that text is a separate change
  with its own ratification.
- Nothing else. No requirement is added or removed beyond those two, no
  other capability is touched, and no code, workflow, contract, or test
  changes.

## Drift, checked before applying

The ratified text may clobber no later ratified work, so the affected region
of the promoted spec was walked through history BEFORE the delta was
applied. Three commits touched
`openspec/specs/lifecycle-notebook-projection/spec.md` after the 2026-07-31
archive:

| commit | date | what it touched |
| --- | --- | --- |
| `d5e6d428` | 2026-08-05 | `Projection implementation ownership` body and scenarios |
| `e9a4be6e` | 2026-08-10 | `Derived notebook membership` body and scenarios; appended `Projection capacity guard` |
| `18a4ffc3` | 2026-08-13 | appended `The session namespace is reconciled against live sessions` |

None touched either affected title. Measured rather than asserted: the
`Corpus scan scope` region hashes to
`bbb402c4eecb4f9ddee7dfec161ed407d8910fe76536ea10aa38438d447e3d57` at its
2026-07-12 introduction (`1efa5756`), at the source packet's archive commit
(`a0ea7666`), at all three later commits above, and at the pre-apply head —
byte-identical across every one. `Branch-session notebooks` hashes ABSENT at
every one of those commits: it has never been in canon, so nothing can be
overwritten. No archived `lifecycle-notebook-projection` delta carries a
`RENAMED` block, so neither title was retired by a later change, and the
2026-08-01 packet is the LATEST archived writer of both — the only other
writer of `Corpus scan scope` is the 2026-07-12 packet whose text canon
currently holds.

The 2026-08-13 reconciliation requirement is ADDITIVE to the requirement
this change restores, not a successor to it: it governs what happens to an
`xf-session-` notebook whose session ended outside a governed ending, which
presumes the namespace `Branch-session notebooks` declares. Promoting the
ratified text supplies the premise that requirement has been standing on.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `lifecycle-notebook-projection`: gains the requirement
  `Branch-session notebooks` (five scenarios) and the amended
  `Corpus scan scope` (four scenarios), both exactly as ratified on
  2026-07-26.

## Impact

- openxFactory: `openspec/specs/lifecycle-notebook-projection/spec.md` gains
  one requirement and one scenario, and one requirement body is amended.
  Canon stops describing a projection with no session surface.
- Behavior: none. The described behavior was realized by
  `add-workbench-branch-sessions` and has been live since; this change moves
  text, not state.
- The promotion-fidelity family's two openxFactory findings are discharged
  by this change's landing — by application, which was the ruling, not by
  disposition. `add-promotion-fidelity-check` task 5.1 closes with it.
- Prevention already exists and needs nothing here: the family that found
  this is the prevention, and it is why the gap was found at all.
- Realization gate: promotion-only; `code_surface: none`, so this change
  archives on landing with no separate realization evidence.
