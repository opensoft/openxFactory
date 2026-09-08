---
code_surface: none — this change's whole diff is governance text: one spec delta restating two already-promoted requirements with their count phrase corrected, this proposal, its tasks, its origin declaration, the promotion of that delta into `openspec/specs/lifecycle-notebook-projection/spec.md`, five sentences in the `Status: standard` workflow doc plus one header line recording the amendment, and one README record row. No script, workflow, schema, contract, test, or runtime artifact moves, in this repository or any other. Nothing under `contracts/` changes, so no bundle is cut and no digest set moves. The sync implementation already behaves as the corrected text describes — it has since 2026-08-10.
target_release: promotion-only — the corrected text reaching canon IS the release; archives on landing (`code_surface: none`), per `release-realization`'s doc-only default rather than the merge-plus-green gate.
Status: ratified
Ratified: 2026-08-24 by Brett — in-session, verbatim: "commission the successor change reconciling the lifecycle-books count". The ruling was given on the residual that PR #317's closing comment flagged in the same words ("the stale 'three lifecycle books' count … a small successor change reconciling the count is the lawful fix"), which is the record this citation stands on: `openspec/changes/archive/2026-08-25-apply-branch-sessions-deltas/proposal.md` is the packet that carried the stale count into canon faithfully and deliberately declined to correct it. No approving OpenSpec change exists to name — the amending act IS this change — so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing the three-way floor on two axes: approver (`by Brett`) and date (`2026-08-24`).
Proposed: 2026-08-24
Origin: the residual recorded in PR #317's closing comment (2026-08-25T02:34:50Z), and the two faithful promotions that left it standing — `openspec/changes/archive/2026-08-25-apply-branch-sessions-deltas/` and the closed duplicate it superseded.
---

# Proposal: reconcile-lifecycle-books-count

## Why

**Canon counts the lifecycle books, and the count has been wrong since
2026-08-10.** The promoted `lifecycle-notebook-projection` spec says "the
three LIFECYCLE BOOKS" in `Corpus scan scope` and "one of the three lifecycle
books" in `Branch-session notebooks`. The `Status: standard` workflow doc
`docs/lifecycle-notebook-projection.md` says it five more times. There are not
three lifecycle books and there have not been for two weeks.

**What made it stale.** The archived `split-ideation-book-per-repo` (ratified
2026-08-10, after the shared Ideation book hit the platform's 300-source cap
mid-sync) replaced the single shared Ideation book with **one Ideation book
per governed repository** — title family `xFactory Ideation — <RepoName>`,
alias family `xf-ideation-<repo-slug>` — beside the shared Working Drafts and
Canon books, and retired the legacy shared book and its `xf-ideation` alias
outright. Its own delta says so: "one Ideation book per governed
repository … the shared Working Drafts book, and … the shared Canon book".
The family is `2 + N`, where N is the number of governed repositories carrying
ideation membership, and N moves whenever the family gains or loses a
repository. A fixed count cannot describe it.

That change's Impact section is explicit that it made "no changes to hybrid
notebooks, imports, drafts/canon membership, or scan scope" — which is why the
count in `Corpus scan scope` was never in its diff. The staleness is
collateral: the split changed what the book family IS without touching the
requirement that counts it.

**Why two later changes carried the stale count forward on purpose.** The
count reached the promoted spec on 2026-08-25 through
`apply-branch-sessions-deltas`, which promoted text ratified 2026-07-26 —
before the split — byte-for-byte, and said in terms that byte-fidelity was the
whole point: "Not a rewrite, not a re-derivation, not a reconciliation with
anything learned since 2026-07-26. Any improvement to that text is a separate
change with its own ratification." A parallel session's independent packet
(PR #317) derived the identical text from the identical source and was closed
as the duplicate. Neither declined the correction by oversight. Editing
ratified text inside a promotion change is precisely the defect the
promotion-fidelity family exists to catch, and the codex PR #85 discipline
both packets followed forbids it. The lawful fix is the successor change with
its own ratification. This is that change.

**What a reader of canon is told today.** That the projection has exactly
three books — so a reader counting them finds five, or nine, and cannot tell
whether the corpus grew past its contract or the contract was never updated.
The main-only rule, the workspace-record rule, the hybrid and session
exclusions, and the shared-quota note all key off "the three books", so the
wrong number is load-bearing in five separate rules at once.

## What Changes

- **The fixed count leaves the two promoted requirements.** In
  `Corpus scan scope`, "The three LIFECYCLE BOOKS' projection" becomes "The
  LIFECYCLE BOOKS' projection — one Ideation book per governed repository,
  plus the shared Working Drafts and Canon books —", naming the topology the
  requirement's scope depends on rather than a number that will restale on the
  next split. In `Branch-session notebooks`, "one of the three lifecycle
  books" becomes "one of the lifecycle books": that sentence states
  non-membership, so it needs no enumeration at all and gains none.
- **The wording is derived, not invented.** Every phrase above is
  `split-ideation-book-per-repo`'s own ratified vocabulary — "one Ideation
  book per governed repository", "the shared Working Drafts book", "the shared
  Canon book" — reused verbatim. This change ratifies no new topology; it
  makes two requirements say the topology that was ratified on 2026-08-10.
- **Nothing else in either requirement moves.** Both bodies are the promoted
  text byte-for-byte apart from the substitutions above, and every scenario is
  restated unchanged: `Corpus scan scope` keeps its four,
  `Branch-session notebooks` keeps its five. Measured, not asserted — the
  block hashes are in `tasks.md` §2.
- **The workflow doc's five instances are corrected consistently**
  (`docs/lifecycle-notebook-projection.md` §1 main-only rule, §7 hybrid
  exclusion, §9 session-notebook exclusion, §9 shared-quota note, §10
  workspace records). Each becomes "the lifecycle books"; none gains an
  enumeration, because §1's book table two paragraphs above already states the
  topology and §11 already says "3+N books". The doc records this change on an
  `Amended by:` header line, the convention `split-ideation-book-per-repo` set
  on this same doc.
- **Nothing outside those two files.** No requirement is added or removed, no
  scenario changes, no other capability is touched, and no code, workflow,
  contract, or test changes.

## Not in scope

Three further instances of the phrase exist in this repository and are
deliberately left alone:

- `README.md`'s archived-change record row for `apply-branch-sessions-deltas`
  quotes the 2026-07-26 amendment's own words. It is a `record`: an accurate
  historical statement of what that delta said when it was ratified, and
  editing it would falsify the record this change's own history rests on.
- `scripts/sync-notebooklm-books.py`, `scripts/ideation_dashboard/branch_session.py`,
  and their tests carry the phrase in comments and one operator message. They
  are code surface; this change declares `code_surface: none` and will not
  quietly acquire one. They are reported as owed follow-up work, not fixed
  here.
- `ideation/staging/` fragments and archived change packets carry it as
  authored history. Staging fragments are rewritten when their topic is next
  worked; archived packets are immutable.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `lifecycle-notebook-projection`: the `Corpus scan scope` and
  `Branch-session notebooks` requirements stop asserting a fixed count of
  lifecycle books and state the per-repository-Ideation-plus-shared-pair
  topology ratified by `split-ideation-book-per-repo`.

## Impact

- openxFactory: two requirement bodies in
  `openspec/specs/lifecycle-notebook-projection/spec.md`; five sentences and
  one header line in `docs/lifecycle-notebook-projection.md`; one README
  record row.
- Behavior: none. The sync has projected per-repository Ideation books since
  `split-ideation-book-per-repo` was realized on 2026-08-10; this change moves
  text, not state.
- Promotion fidelity: this change becomes the latest archived writer of both
  requirements, so the family measures IT against canon from the moment it
  archives. It must read — and does read — zero findings for openxFactory.
- Realization gate: promotion-only; `code_surface: none`, so this change
  archives on landing with no separate realization evidence.
