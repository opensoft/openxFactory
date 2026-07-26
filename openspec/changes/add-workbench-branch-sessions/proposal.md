---
code_surface: codexFactory (the branch-session lifecycle — branch creation plus git worktree materialization and teardown; session entries in the (repository, ref) snapshot registry `add-dashboard-repo-selector` lands; per-gate-action session snapshot regeneration; branch-aware `/source` confinement; the `edit-document`, `open-pr`, and abandon gate routes with CLI parity; the refresh-notebook session action and the session-notebook mode of `scripts/sync-notebooklm-books.py`; workbench session affordances and the session posture indicator; tests), openxFactory (additive `gate-action-record` growth for the three new actions, two new artifact kinds and one new target field; the `ideation-dashboard` and `lifecycle-notebook-projection` capability deltas), xFactory aggregation (the gitignored worktree-container location the session worktrees materialize into, which the notebook scan scope already excludes)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
---

# Proposal: add-workbench-branch-sessions

## Why

The workbench can now CREATE a document. It cannot EDIT one, and the human
working a topic has nowhere legitimate to stand between "I have an idea" and
"this is ready for review".

The obvious fix is the wrong one. Adding an edit verb that writes to the
served checkout's `main` would mean unreviewed edits appearing instantly on
every shared surface — the wheel, the funnel, the hosted dashboard — which is
exactly what the ratified gates-happen-on-main rule exists to prevent. The
other obvious fix, a redline round per edit, is the ceremony that already
exists for main-resident documents and it is unusable for authoring: nobody
drafts a document through a sequence of proposed-then-applied diffs.

Brett's 2026-07-26 decision takes the third path, and it loosens no rule:
**move the working state onto a git branch and let THE PULL REQUEST be the
formal re-entry into the governed doc system.** The first gate write against
a tile spawns `draft/<staging-id>` and materializes a git WORKTREE for it; the
served checkout NEVER switches branches, which dissolves the shared-checkout
hazard this family has already been bitten by — by construction rather than by
discipline. Every gate action is one commit, so the audit trail FALLS OUT of
version control instead of being reconstructed beside it, and a gate record
rides the same commit as the document it attests to. On-branch edits need no
per-edit ceremony because the PR review IS the governance — which is not a new
principle but the gates-happen-on-main rule read forwards: if an unmerged
transition is exploration and not status, then an unmerged branch is precisely
where ordinary editing is legal. Main stays the shared truth everywhere else:
branch drafts are visible ONLY inside their session.

The seam this needs already exists. `add-dashboard-repo-selector` keyed the
snapshot source on the PAIR (repository, ref) — deliberately, for this
consumer, so it would not have to be re-cut — and gave the serve ONE registry
behind that key. A session's panels read a snapshot generated from the
worktree through that same registry: no overlay machinery, no diffing layer,
no second projection path. That is why this change is sequenced strictly after
the selector rather than beside it.

## What Changes

- OPEN a BRANCH SESSION on the first gate write against a topic-bearing tile:
  a branch named for the TILE (`draft/<staging-id>` for a staged topic; the
  scope's kind and id for a cluster or a possible) plus a git WORKTREE. Named
  for the tile and never the actor, so two humans working the same topic join
  the SAME session. The served checkout is never switched, reset, or stashed
  by any session operation. Per-ACTOR branch variants stay a future option if
  same-tile collisions hurt in practice; they are not built now.
- COMMIT ONCE PER GATE ACTION on the session branch, carrying the documents
  and the gate-action record TOGETHER, with the record naming its own commit.
  This is the property the gate-action-record family wants and can only
  approximate when records and documents land through different paths. A verb
  whose effect reaches OUTSIDE the branch — a workflow dispatch that actually
  runs, a publication, a build, a rollout — may not be performed from inside a
  session, because it would commission external action from state that is not
  yet governed.
- ADD one human-only gate verb, `edit-document`, valid ONLY inside an active
  branch session, that rewrites an existing document in the session worktree
  and commits it. No redline round per edit — the PR review is the governance.
  The gate console's `edit-apply` redline path REMAINS UNCHANGED for editing
  MAIN-RESIDENT documents outside a session: a different act, a different risk
  profile, its own ceremony kept. `create-document` keeps its create-only
  semantics and, inside a session, writes into the worktree.
- READ the session's panels from a snapshot addressed `(repository,
  session-branch)` through the registry the selector change lands, generated
  FROM the worktree and REGENERATED after every gate action, so a document
  created in the session appears in the bullseye and the docs panel seconds
  later rather than after a manual step. Session snapshots are derived,
  session-local, and never published or indexed; the freshness header names
  the session branch, so a draft view is never ambiguous.
- CONFINE draft visibility to the session. The wheel, the funnel, the pipeline
  board, the hosted dashboard, and every published projection keep rendering
  `main`. Inside the session every joining actor sees the drafts.
- RESOLVE document reads inside a session through the SAME read-only `/source`
  pass-through, bound to the session worktree and confined to its root, with
  no fallback to the `main` copy of a path that escapes — a silent fallback
  would render a stale document under a draft heading.
- ADD one human-only gate verb, `open-pr`, which IS "save": push the branch,
  open the pull request into the EXISTING Merge-Master ritual, record the
  dispatch with the pull request as a `pull-request`-kind artifact. No new
  approval path, no new authority, no bypass; the verb cannot merge or approve
  its own pull request. It does NOT require the topic's readiness gate to have
  fired (open question 3's recommendation, carried into the requirement): a
  session PR is exploration offered for review, and the readiness gate guards
  PROPOSE, not SAVE.
- END a session in exactly two ways — the pull request MERGES, or a human
  explicitly ABANDONS it — and on either ending tear down the worktree, the
  session's registry entry, and the session notebook, then refresh the main
  view. On a MERGE the session branch is ALSO deleted: the work is saved on
  `main` and the branch is residue. Abandon is a recorded action carrying a
  reason; it ends the SESSION and never deletes pushed history or closes a
  pull request on the human's behalf.
- REFUSE `propose` while the tile carries an unresolved branch session, naming
  the session and both resolutions (merge the pull request, or abandon to
  discard). Proposal ends the staging pipeline, so a tile whose drafts are
  still unmerged on a branch must be cleared first. An abandoned session is
  RESOLVED even if its pushed branch survives.
- SYNC per-session NotebookLM notebooks (`xf-session-<topic>`, a namespace
  DISJOINT from the workbench's `xf-wb-*` reference-set notebooks so the
  reference-set orphan sweep can never delete a live session's notebook) FROM
  the session WORKTREE, created on session start and retired on session end,
  with a "refresh notebook" session action after edits and hybrid
  source-return imports landing ON THE BRANCH under the unchanged imported-file
  header contract. The three canon books (`xf-ideation`, `xf-drafts`,
  `xf-canon`) stay MAIN-ONLY without exception — they ARE the lifecycle
  projection, and a projection of unmerged work is a misprojection.
- KEEP the capability LOCAL-PLANE ONLY. The hosted dashboard exposes NONE of
  it — no session, no ref selection, no session verb, no non-`main` snapshot —
  until the intent plane's apply lane (§4 of `add-ideation-intent-plane`)
  exists, because a hosted session would apply writes the hosted surface holds
  no authority to make. The seam's `ref` key is the future binding point, so
  that arrival needs no redesign. Where the gate capability is absent, every
  session affordance renders as a copyable CLI descriptor, never a live button.
- EXTEND (additive, no `contract_schema_version` bump)
  `contracts/schemas/gate-action-record.schema.yaml`: the `action` enum gains
  `edit-document`, `open-pr`, and `abandon-session`; the artifact `kind` enum
  gains `commit` and `pull-request` as first-class kinds rather than `other`
  (the precedent Brett set for `document` on 2026-07-25); `target` gains an
  optional `ref` naming the session branch; and per-action conditionals require
  `document` + `ref` + a `commit` artifact for `edit-document`, `ref` + a
  `pull-request` artifact for `open-pr`, and `ref` + a `reason` for
  `abandon-session`. No PRE-EXISTING action gains a required companion, which
  is why the commit-per-gate-action rule for `create-document` inside a session
  is a REQUIREMENT enforced at the route rather than a schema conditional.

## Impact

- Affected specs: `ideation-dashboard` — EIGHT ADDED requirements (branch
  session lifecycle; one commit per gate action; the session-scoped
  `edit-document` verb; the session snapshot addressed by (repository, session
  ref); session-confined draft visibility; branch-aware source resolution; the
  `open-pr` save verb; local-plane confinement) and THREE MODIFIED requirements.
  `Staging workbench scoped view` is modified because its "ONLY write authority
  ... MUST NOT modify or delete any existing document, in any panel, by any
  path" clause is exactly what a session edit supersedes — inside a session and
  nowhere else. `Delivery and regeneration` is modified for a subtler reason
  worth stating: its "still no per-commit regeneration" clause is TRUE of the
  publication lane and FALSE of a session, where every gate action is a commit
  AND triggers a regeneration; the modified text scopes the prohibition to
  published snapshots and states the session cadence beside it.
  `Staged-topic proposal commissioning` (of `add-propose-verb`) is modified
  because proposal ends the staging pipeline: `propose` must refuse while the
  tile carries an unresolved session, or it commissions authoring against
  drafts that are still stranded on an unmerged branch (D15). Also
  `lifecycle-notebook-projection` — ONE ADDED requirement (branch-session
  notebooks) and ONE MODIFIED (`Corpus scan scope`, whose worktree exclusion
  must now say WHICH surfaces it protects, since session notebooks are the one
  surface that deliberately reads a worktree).
- Specs deliberately NOT modified, with reasons, because each looks like a
  candidate: `Snapshot source keyed by repository and ref` (of
  `add-dashboard-repo-selector`) already declares the pair key, the one
  registry, per-entry confinement, and that non-`main` snapshots are
  session-local and never published — it was written FOR this consumer, so
  this change consumes it unedited. `Interactivity boundary` already splits
  mutation authority by actor and grants humans create AND edit authority over
  corpus documents through the dashboard; this change adds a gated route and a
  place to stand, not an authority. `Human gate console` keeps its `edit-apply`
  AI-redline path verbatim — that path is for main-resident documents and this
  change does not touch it. `Read-only document viewer` already ties content to
  "the same pinned checkout the snapshot was generated from", which for a
  session IS the worktree; per-entry confinement makes that literal rather than
  a new rule. `Snapshot projection contract` already reads "for ONE repository
  at ONE ref".
- Affected schemas: `contracts/schemas/gate-action-record.schema.yaml` only —
  three additive `action` enum values, two additive artifact `kind` values
  (`commit`, `pull-request`), one additive optional `target.ref`, and three
  per-action conditionals that constrain ONLY the new actions. No
  `contract_schema_version` bump and no existing record invalidated. NO new
  schema: a branch session deliberately carries NO session-descriptor artifact
  (design D10) — the session IS derived state (a branch, a worktree, a registry
  entry, a notebook alias derived from the tile), so it cannot drift from
  reality, and its history is the commit series.
- Delta stacking: the `ideation-dashboard` capability is NOT promoted
  (`add-ideation-dashboard` sits unarchived), so this delta stacks on it
  alongside `add-propose-verb`, `add-wheel-action-verbs`,
  `add-staging-workbench`, `add-lens-gate-verbs`,
  `add-workbench-bullseye-and-create`, and `add-dashboard-repo-selector`.
  `lifecycle-notebook-projection` IS promoted, so that delta modifies the
  promoted spec directly.
- Archive sequencing, which must be deliberate rather than discovered:
  `add-ideation-dashboard` (owns `Delivery and regeneration`),
  `add-staging-workbench` (owns `Staging workbench scoped view`),
  `add-workbench-bullseye-and-create` (last modified that requirement),
  `add-dashboard-repo-selector` (last modified `Delivery and regeneration`, and
  lands the seam this change consumes), and `add-propose-verb` (owns
  `Staged-topic proposal commissioning`, which this change MODIFIES to add the
  unresolved-session refusal) MUST ALL archive BEFORE this change.
  Archiving in any other order leaves a MODIFIED delta with nothing to modify.
- Affected code (codexFactory, realization): branch creation and git worktree
  materialization/teardown with the served checkout pinned; session entries in
  the (repository, ref) snapshot registry; per-gate-action session snapshot
  regeneration; branch-aware `/source` root binding with per-entry confinement;
  `gate_routes.py` and `gate_console.py` for `edit-document`, `open-pr`, and
  abandon, plus the commit-per-action write path that commits documents and
  record together; `cli.py` parity subcommands; `views/staging-workbench.js`
  session affordances and posture (transport in the sibling module, per the
  pinned renderer constraints); `scripts/sync-notebooklm-books.py` for the
  session-notebook mode and worktree-sourced sync; tests.
- Affected wiring (xFactory aggregation): the gitignored container location
  session worktrees materialize into — which the notebook projection's scan
  scope ALREADY excludes by name (`<repo>-worktrees/`), so this is a placement
  decision plus a `.gitignore` entry, not a new exclusion rule.
- NOT in scope: per-ACTOR session branches; a session-descriptor contract; any
  DELETE authority (no session verb removes a document); an in-panel outline
  editor; hosted sessions and anything that would let the hosted plane apply a
  write; publication or indexing of a session snapshot; relocating any gate
  verb other than `create-document` onto the branch; automatic rebase or merge
  of `main` into a session branch; and the Merge-Master ritual itself, which
  this change hands work TO and changes in no way.
- Related but NOT covered: Track C's chat rail. Topic claim 7 decides that all
  three grounding surfaces follow the branch, and this change lands two of them
  (the canvas outline via branch-aware `/source`, and NotebookLM via session
  notebooks). The chat rail's server-side grounding set is Track C's C1 — its
  own future change — and this change requires nothing of the chat layer; what
  it provides is the branch-resident working state C1 will ground on and edit.
- Compatibility: additive throughout. Every existing gate-action record stays
  valid; a pre-growth consumer reading a session record sees unrecognized
  `action` and `kind` values, which is why the growth is enumerated in the
  schema rather than left implicit. No session exists until a human performs a
  gate write, so a dashboard with no sessions behaves exactly as it does today;
  the hosted plane gains no route, no verb, and no contract change; and every
  main-resident path — the redline edit, the wheel, the funnel, the publication
  lane, the three canon notebooks — is untouched.
