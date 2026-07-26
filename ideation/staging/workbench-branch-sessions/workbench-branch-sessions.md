# Staged: Workbench Branch Sessions — the branch is the unit of working state

Status: staged
Kind: architecture
Summary: Make the staging workbench the place where documents are CREATED
and EDITED, without loosening a single governance rule — by moving the
working state onto a git branch and letting the PR be the formal re-entry
into the governed doc system. The first gate write against a tile spawns
`draft/<staging-id>` and materializes a git WORKTREE for it; every gate
action is one commit, so the audit trail falls out of version control
instead of being re-invented; on-branch edits are plain commits because
THE PR REVIEW IS THE GOVERNANCE, which is exactly what the ratified
gates-happen-on-main rule already says (an unmerged transition is
exploration, not status). Branch drafts are visible ONLY inside the
workbench session — main stays the shared truth on the wheel, the funnel,
and the hosted site. The session's panels read a snapshot generated from
the worktree through the (repository, ref) seam the
[dashboard-repo-selector](../dashboard-repo-selector/dashboard-repo-selector.md)
topic defines, so no bespoke overlay machinery is invented; the tool
triangle (chat rail, canvas outline, NotebookLM) follows the branch;
"saving" is a gated `open-pr` verb that hands the work to the existing
Merge-Master ritual.
Topics: ideation-dashboard, doc-workflow, document-lifecycle, workbench, git-worktree, branch-sessions, lifecycle-projection, gate-console, merge-master
Repository context: openxFactory owns the `ideation-dashboard` capability
delta (branch sessions, the commit-per-gate-action rule, session-local
snapshots, the `open-pr` verb, draft-visibility confinement) and the
`lifecycle-notebook-projection` delta (per-session notebooks); codexFactory
realizes the worktree lifecycle, the (repository, ref) snapshot registry
shared with `dashboard-repo-selector`, branch-aware `/source`, the chat
rail's grounding set, the session-refresh actions, and the `open-pr` gate
route.
Staging ID: openxFactory:staging:workbench-branch-sessions
Source: Brett's live session decisions of 2026-07-25 and 2026-07-26 — the
2026-07-25 workbench dogfood pass that produced
`add-workbench-bullseye-and-create` (the first workbench write: gated
create-only document creation), followed by the 2026-07-26 branch-session
design round in the same thread, which decided how EDITING and multi-step
authoring reach the surface without weakening the gate model. Every claim
below is DECIDED unless it appears under "Open questions".
Target capabilities: ideation-dashboard (MODIFIED); lifecycle-notebook-projection (MODIFIED)

## Claims

1. **The branch is the unit of working state (DECIDED 2026-07-26).** The
   workbench becomes the place to CREATE and EDIT documents, and the
   formal re-entry of that work into the governed doc system is THE PR.
   Nothing about the governed system relaxes: main is still where gates
   happen, review is still where authority is exercised, and the Merge
   Master still merges. What changes is that a human working a topic gets
   somewhere legitimate to stand between "I have an idea" and "this is
   ready for review".
2. **Branch per tile, collaborative (DECIDED 2026-07-26).** The session
   branch is `draft/<staging-id>` — named for the TILE, not the actor, so
   two people working the same topic work the same branch. The FIRST gate
   write against a tile spawns the branch and materializes a git WORKTREE
   for it; the serve's main checkout NEVER switches branches. That last
   clause is the point: it dissolves the shared-checkout hazard by
   construction rather than by discipline, which is the failure mode this
   family has already been bitten by. Per-ACTOR branch variants remain a
   future option if same-tile collisions turn out to hurt in practice;
   they are not built now.
3. **One commit per gate action (DECIDED 2026-07-26).** Every gate action
   taken in a session is one commit on the session branch, so the audit
   trail FALLS OUT of version control instead of being reconstructed
   beside it. Gate records ride the branch with the documents they
   describe, which keeps a record and the artifact it attests to
   inseparable — the property the gate-action-record family wants and can
   only approximate when records and docs land through different paths.
4. **Instant create is retained, ON the branch; on-branch edits are plain
   commits (DECIDED 2026-07-26).** The create gesture
   `add-workbench-bullseye-and-create` landed keeps working, writing into
   the session branch instead of the checkout. Editing needs NO
   per-edit ceremony — no edit-apply redline round per keystroke-batch —
   because THE PR REVIEW IS THE GOVERNANCE. This is not a new principle:
   the ratified gates-happen-on-main rule already holds that unmerged
   transitions are exploration and not status, so an unmerged branch is
   precisely the place where ordinary editing is legal. The edit-apply
   redline path REMAINS, unchanged, for main-resident documents edited
   outside a session — that is a different act with a different risk
   profile, and it keeps its ceremony.
5. **Draft visibility is session-confined (DECIDED 2026-07-26).** Branch
   drafts appear ONLY inside the workbench session that created them.
   The wheel, the funnel, the hosted site, and every other surface keep
   rendering main. A shared surface that showed someone's unmerged drafts
   would silently redefine what the team's pipeline picture means.
6. **The session snapshot rides the (repository, ref) seam (DECIDED
   2026-07-26).** The session's workbench panels read a snapshot
   generated FROM THE WORKTREE and served through the (repository, ref)
   snapshot source that `dashboard-repo-selector` defines — no bespoke
   overlay machinery, no second projection path, no diffing layer over
   the main snapshot. The session snapshot auto-regenerates after each
   gate action, so a document created in the session appears in the
   bullseye and the docs panel seconds later rather than after a manual
   step. Session snapshots are derived, session-local, and NEVER
   published (the sibling topic's claim 12).
7. **The tool triangle follows the branch (DECIDED 2026-07-26).** All
   three of the workbench's grounding surfaces bind to the session's
   worktree:
   - **Chat rail** — grounds on the WORKTREE's document set, resolved
     server-side, so the assistant reads the drafts the human is actually
     working on rather than their merged ancestors.
   - **Canvas outline** — renders branch drafts through a branch-aware
     `/source` pass-through, the same read-only route the document viewer
     already uses.
   - **NotebookLM** — the canon notebooks (`xf-ideation`, `xf-drafts`,
     `xf-canon`) stay MAIN-ONLY, without exception: they are the
     lifecycle projection and a projection of unmerged work is a
     misprojection. Per-session notebooks (`xf-wb-<topic>`) sync FROM THE
     BRANCH WORKTREE. [SUPERSEDED 2026-07-26 by the adversarial review of
     `add-workbench-branch-sessions`: the session-notebook name is now
     `xf-session-<topic>`. `xf-wb-*` is the workbench reference-set
     namespace, and its orphan sweep deletes every `xf-wb-*` notebook no
     workbench manifest binds — which a session notebook, having no
     manifest by design, never can. The original name would have had a
     live session's notebook deleted mid-session by the routine sync.
     Likewise "retired or re-pointed at main" below is now RETIRE, DECIDED by
     Brett 2026-07-26 (change design D16): the notebook never survives its
     session. Merge deletes the branch, so the worktree the notebook synced
     FROM is gone; re-pointing would also invent a notebook class the promoted
     spec does not govern, and the merged documents already project into the
     three lifecycle books. If a session's ANALYSIS should ever outlive the
     branch, the route is an explicit conversion to a §7 hybrid — a future
     change, not a silent re-point.] That is possible because NotebookLM knows uploaded
     SOURCES, not git — so this is a projection-TOOLING change only, with
     no contract consequence for the notebook family beyond declaring the
     rule. A session notebook is recreated on session start and, on
     merge, retired or re-pointed at main. The hybrid per-set import flow
     lands its imports ON THE BRANCH, where they are ordinary working
     material. A "refresh notebook" session action re-syncs after edits —
     the NLM face of the same session-refresh concept the snapshot and
     the chat rail get.
8. **"Saving" is a gated `open-pr` verb (DECIDED 2026-07-26).** The save
   gesture pushes the session branch and opens the PR, handing the work
   into the EXISTING Merge-Master ritual — no new approval path, no new
   authority, no bypass. On merge the documents become real, the nightly
   snapshot picks them up on its own schedule, and the branch, the
   worktree, and the session notebook are cleaned up. [CONFIRMED and made
   explicit 2026-07-26: the branch IS deleted at merge. Abandon still never
   deletes pushed history — the asymmetry is deliberate, since the merge
   preserved the work and the abandon did not. Brett also ruled the same day
   that `propose` REFUSES while a tile carries an unresolved session, because
   proposal ends the pipeline and a proposal must not be commissioned from
   drafts stranded on an unmerged branch.]
9. **Local plane only, until intent-plane §4 (DECIDED 2026-07-26).**
   Branch sessions are a LOCAL-PLANE capability: the hosted plane cannot
   have them until the intent plane's apply lane (§4 of
   `add-ideation-intent-plane`) exists, because a hosted session would
   need to apply writes it has no authority to make. The seam's `ref` key
   is the future binding point — a hosted session becomes possible
   without redesign the moment the apply lane can produce a ref.
10. **One piece of new server plumbing (DECIDED 2026-07-26).** The serve
    grows a snapshot REGISTRY keyed (repository, ref). That is the whole
    server-side addition, and it is SHARED with `dashboard-repo-selector`
    rather than duplicated — which is why the sequencing below is strict
    rather than a preference.
11. **Sequencing (DECIDED 2026-07-26).** `add-dashboard-repo-selector`
    defines the (repository, ref) seam and STRICTLY PRECEDES
    `add-workbench-branch-sessions`, which consumes it. Both stack on the
    still-unpromoted `ideation-dashboard` capability, alongside
    `add-staging-workbench`, `add-lens-gate-verbs`, and
    `add-workbench-bullseye-and-create` — the archive order has to be
    sequenced knowingly, not discovered at archive time.

## Open questions

1. **Branch-name collision handling.** `draft/<staging-id>` is stable by
   design, so a staging id worked again after its first branch merged
   collides with the merged (or still-present) name. Reuse the name after
   deletion, suffix a session ordinal, or refuse and require the human to
   name the continuation.
2. **Session-notebook quota behavior.** Per-session `xf-session-<topic>`
   notebooks (renamed 2026-07-26, see claim 7) are created and retired per
   session; what happens when the
   NotebookLM account's notebook quota is reached mid-session (refuse the
   session, degrade to no notebook, or evict the oldest retired one) is
   undecided.
3. **Whether commit-per-gate-action needs squash-on-PR.** One commit per
   gate action is what makes the audit trail free, but it also means a
   long session opens a PR with many small commits. Whether the PR
   squashes (losing the per-action granularity in main's history while
   keeping it in the PR record) or merges the series intact is open.

## Exit path

One openxFactory change, `add-workbench-branch-sessions` (`code_surface`:
codexFactory for the worktree lifecycle, the shared snapshot registry,
branch-aware `/source`, the chat-rail grounding set, the session-refresh
actions and the `open-pr` gate route; openxFactory for the
`ideation-dashboard` and `lifecycle-notebook-projection` deltas), raised
AFTER `add-dashboard-repo-selector` has landed the (repository, ref) seam.
It archives on merged + green realization evidence including a real
session: create and edit documents on a session branch, watch the panels
follow the worktree, open the PR, and find the merged documents on main
and in the next nightly snapshot.

Related work: the sibling topic
[dashboard-repo-selector](../dashboard-repo-selector/dashboard-repo-selector.md)
owns the seam this topic consumes;
[add-workbench-bullseye-and-create](../../../openspec/changes/add-workbench-bullseye-and-create/proposal.md)
is the change that landed the workbench's first write (the gated
create-only document creation and the lens/bullseye create gestures) and
whose create verb these sessions relocate onto the branch; Track C — the
workbench's AI chat layer, locked in
`ideation/brainstorm/ideation-dashboard.md` — is what claim 7's chat rail
belongs to, and the branch is the working state that layer will edit.
