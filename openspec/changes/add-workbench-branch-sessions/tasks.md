# Tasks: add-workbench-branch-sessions

Sequencing precondition: `add-dashboard-repo-selector` MUST have landed the
(repository, ref) seam and the snapshot registry before section 3 begins
(topic claim 11 — strict, not a preference). Nothing here duplicates that
registry.

## 1. Contract (openxFactory)

- [x] 1.1 Additive growth of `contracts/schemas/gate-action-record.schema.yaml`
      (design D13; no `contract_schema_version` bump, no existing record
      invalidated): `action` enum gains `edit-document`, `open-pr`, and
      `abandon-session`; the artifact `kind` enum gains `commit` and
      `pull-request` as first-class kinds (the `document` precedent of
      2026-07-25, not `other`); `target` gains an OPTIONAL `ref` naming the
      session branch. Commentary states each addition's owning change and why
      the growth is safe.
- [x] 1.2 Three per-action conditionals in the same file, constraining ONLY the
      new actions: `edit-document` requires `target.document` + `target.ref` and
      an artifact of kind `commit`; `open-pr` requires `target.ref` and an
      artifact of kind `pull-request`; `abandon-session` requires `target.ref`
      and `reason`. State in the commentary why the commit-per-gate-action rule
      is NOT a conditional on `create-document` (D13 — it would narrow a
      pre-existing action whose non-session use produces no commit), and why
      `target.ref` therefore stays optional.
- [x] 1.3 Packaged examples under `examples/`: a valid `edit-document` record
      (document + ref + commit artifact), a valid `open-pr` record
      (ref + pull-request artifact), a valid `abandon-session` record with a
      reason, and negatives naming the rule they violate —
      `gate-action-edit-document-no-commit-artifact`,
      `gate-action-open-pr-no-pull-request-artifact`,
      `gate-action-abandon-session-unreasoned`, and
      `gate-action-edit-document-no-ref`.
- [x] 1.4 NO new schema (D10): confirm at review that no session-descriptor
      artifact was introduced — a session stays derived from its branch, its
      worktree, its registry entry, and its tile-derived notebook alias.
      (Confirmed at realization review: codexFactory feature 007 T089 evidence
      shows no session-descriptor artifact and no new schema — the contract
      growth here is additive on `gate-action-record` alone.)
- [x] 1.5 Validate: `OPENSPEC_TELEMETRY=0 openspec validate
      add-workbench-branch-sessions --strict` and `--all --strict`, plus the
      repo's contract validators green (0 errors, 0 warnings) with the new
      examples included.
- [ ] 1.6 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`, README contract index) at the next additive
      bundle cut, per `docs/contract-versioning-policy.md`
      (registration-at-realization precedent).

## 2. Branch session lifecycle (codexFactory)

- [ ] 2.1 Session branch naming derived deterministically from the TILE's scope
      identity (D2): `draft/<topic-folder>` for a staged topic, scope kind + id
      for a cluster or a possible. Never the actor. Ordinals (`-2`, `-3`) are
      allocated only by D17's NEW continuation, as highest-existing-plus-one
      computed against the REMOTE so two machines cannot disagree.
- [ ] 2.1a Resume-or-new on a tile whose previous session was ABANDONED and
      whose branch survives (D17): the first gate write MUST report the
      abandoned branch and offer RESUME (re-materialize a worktree over the
      existing branch, keeping its name) or NEW (next ordinal). Offered ONLY
      while no live session holds the tile; once either choice opens a session,
      later writers JOIN it, so the prompt can never fork one tile in two.
- [ ] 2.1b Refuse to open OR resume a session on a tile carrying a LIVE
      PROPOSAL (D20): an existing proposal, or a dispatched-and-undelivered
      `propose` workflow-job. The refusal names `demote` as the route back; when
      authoring is still in flight it says instead that the proposal has not
      landed yet, since there is nothing to demote. Mirror of the D15 refusal —
      the two states are mutually exclusive from both directions.
- [ ] 2.2 Spawn on the FIRST gate write against a tile with no active session:
      create the branch and materialize a git WORKTREE for it. Idempotent — a
      second actor's first write JOINS the existing session (D2).
- [ ] 2.3 Served-checkout immovability (D3): assert at every session entry point
      that no session operation switches, resets, or stashes the served
      checkout. A test that would move it MUST fail.
- [ ] 2.4 Worktree placement in the gitignored container location the notebook
      projection's scan scope already excludes (`<repo>-worktrees/`), plus
      teardown that removes the worktree, the session's registry entry, and the
      session notebook on both endings.
- [ ] 2.5 Two endings (D9): merge (teardown + DELETE the session branch +
      main-view refresh) and explicit abandon (teardown + recorded reason).
      Abandon MUST NOT delete pushed history or close a pull request — the
      asymmetry is deliberate: the merge preserved the work, the abandon did not.
- [ ] 2.6 Commit-per-gate-action write path (D4): one commit carrying the
      action's documents AND its gate-action record, with the record naming the
      commit as a `commit`-kind artifact. Refuse any path that would split them.
- [ ] 2.7 Refuse externally-dispatching verbs inside a session (D4/D12): a
      running workflow dispatch, a publication, a build, or a rollout invoked
      from a session refuses and reports.

## 3. Session snapshot and source resolution (codexFactory)

- [ ] 3.1 Register the session as a `(repository, session-branch)` entry in the
      EXISTING snapshot registry (D6) — no overlay, no diff layer, no second
      projection path.
- [ ] 3.2 Generate the session snapshot from the WORKTREE root and regenerate
      after EVERY gate action in the session, so a created or edited document
      appears in the session's bullseye, docs panel, and outline with no manual
      step.
- [ ] 3.3 Refuse publication or indexing of any session snapshot — the
      selector change's non-`main` refusal already exists; confirm sessions
      exercise it rather than bypass it.
- [ ] 3.4 Freshness header names the SESSION BRANCH as the active ref whenever a
      session snapshot renders (D6/D7 — draft-view ambiguity is the failure
      mode this closes).
- [ ] 3.5 Branch-aware `/source` bound to the session worktree with per-entry
      confinement; a path escaping the session root REFUSES and MUST NOT fall
      back to the `main` copy. Outside a session the pass-through is unchanged.

## 4. Session gate verbs (codexFactory)

- [ ] 4.1 `edit-document` route + CLI parity verb (D5): human-only,
      loopback-only, actor fail-closed, agent-refused; valid ONLY inside an
      active session; rewrites an existing document in the worktree; no create,
      no delete; refuses a target outside the session root; refuses entirely
      with no active session.
- [ ] 4.2 `create-document` inside a session writes into the WORKTREE instead of
      the served checkout, with its create-only semantics and every engine
      refusal unchanged.
- [ ] 4.3 `open-pr` route + CLI parity verb (D8): pushes the branch, opens the
      pull request into the existing Merge-Master ritual, records the dispatch
      with the pull request as a `pull-request`-kind artifact. Cannot merge,
      approve, self-review, or bypass protection. Does NOT require the topic's
      readiness gate — neither the blocking staged-to-proposal gate nor the
      advisory recommendation gate (D21). Re-invocation updates
      and reports the existing PR rather than opening a second.
- [ ] 4.4 Abandon route + CLI parity verb (D9): recorded with a reason, tears
      down session state only.
- [ ] 4.5 `edit-apply` left untouched (D5): confirm by test that the
      main-resident AI-redline path is byte-identical in behaviour after this
      change.
- [ ] 4.6 `propose` unresolved-session refusal (D15): the existing propose route
      gains a precondition — refuse while the tile's session registry entry is
      live, naming the branch and both resolutions (merge the PR, or abandon).
      Keys on the live session, NOT on branch existence, so a branch surviving
      an abandon does not block. No new verb: the two resolutions are the
      existing `open-pr`→merge path and `abandon-session`.
- [ ] 4.7 Abandoned-branch cleanup once the topic's proposal exists (D17): a
      HUMAN-invoked affordance, never automatic and never fired by the `propose`
      dispatch alone — the commissioned authoring may not have produced a
      proposal yet. Offered only for a branch whose session was abandoned.

## 5. Workbench surface (codexFactory)

- [ ] 5.1 Session affordances in the workbench (edit, save, abandon, refresh
      notebook), with transport in the sibling module per the pinned renderer
      constraints (`views/staging-workbench.js` stays free of `fetch(`/`POST`).
- [ ] 5.2 Session posture indicator: honest about whether a branch session is
      ACTIVE, which branch it is on, and whether the view is a draft view —
      distinct from the gate-capability posture pill and from the UI-lifetime
      "workbench session" state (D14).
- [ ] 5.3 Gate-capability-off rendering: every session affordance is a COPYABLE
      CLI DESCRIPTOR, never a live button; no session write reachable from the
      page.
- [ ] 5.4 Renderer-bundle pins respected, never edited: the same-origin
      `fetch(` pin's file set and per-file counts are updated only as the
      arithmetic of new same-origin routes requires.

## 6. NotebookLM session notebooks (codexFactory tooling)

- [ ] 6.1 `xf-session-<topic>` session-notebook mode in
      `scripts/sync-notebooklm-books.py`: sources synced FROM the session
      worktree, created on session start, RETIRED on session end (D11). The
      title MUST NOT use the `xf-wb-` prefix, and a test MUST assert that
      `workbench_orphan_sweep` leaves a live session notebook untouched.
- [ ] 6.2 Lifecycle books stay MAIN-ONLY: confirm by test that branch-session
      worktrees are excluded from all three books, in addition to the existing
      `<repo>-worktrees/` exclusion.
- [ ] 6.3 "Refresh notebook" session action re-syncing the session notebook from
      the worktree after edits.
- [ ] 6.4 Hybrid source-return imports for a session notebook write into the
      origin folder INSIDE the worktree and land on the branch, with the
      imported-file header contract and idempotency-by-source-id unchanged.
- [x] 6.5 Update `docs/lifecycle-notebook-projection.md` with the session
      notebook section (the canon books' main-only rule stated, the session
      notebook's life bound to its session, the worktree-sourced sync command,
      and the branch-landing import path).

## 7. Plane confinement

- [ ] 7.1 Hosted plane exposes NONE of it (D12): no session, no ref selection,
      no session verb, no worktree, no non-`main` snapshot. A hosted request
      naming a non-`main` ref refuses.
- [ ] 7.2 Record the arrival path rather than building it: a hosted session
      becomes possible by binding the intent plane's apply-lane ref (§4 of
      `add-ideation-intent-plane`) through the existing (repository, ref) seam,
      with no re-cut of the snapshot source interface.

## 8. Verification

- [ ] 8.1 Lifecycle tests: first gate write spawns branch + worktree; a second
      actor joins the SAME session; the served checkout is never moved; merge
      and abandon both tear down worktree, registry entry, and notebook.
- [ ] 8.2 Audit tests: each gate action is exactly ONE commit carrying documents
      and record together; the record names its commit; a split-write path
      refuses; an externally-dispatching verb refuses inside a session.
- [ ] 8.3 Edit-boundary tests: `edit-document` succeeds in a session; refuses
      with no session; refuses a path outside the session root; refuses a
      delete; the main-resident `edit-apply` path is unchanged.
- [ ] 8.4 Visibility tests: a session draft is absent from the wheel, the
      funnel, and the hosted snapshot; present for a second actor in the same
      session; present on shared surfaces only after merge.
- [ ] 8.5 Snapshot tests: the session snapshot regenerates after every gate
      action; the freshness header names the branch; publication and indexing of
      a session snapshot refuse; no overlay path exists.
- [ ] 8.6 Save tests: `open-pr` pushes, opens the PR, and records it; cannot
      merge or approve; proceeds with no fired readiness gate; a second
      invocation updates rather than duplicating; merge tears the session down,
      DELETES the session branch, and refreshes the main view.
- [ ] 8.13 Proposed-tile session refusal tests (D20): a gate write on a tile
      with an existing proposal opens no session, persists nothing, and names
      `demote`; a gate write while a `propose` job is dispatched-and-undelivered
      refuses and says the proposal has not landed rather than naming demote;
      after a demotion the same tile opens a session normally; and the
      resume-or-new prompt is NOT offered on a proposed tile that still has an
      abandoned branch.
- [ ] 8.11 Resume-or-new tests (D17): a first gate write on a tile with a
      surviving abandoned branch reports it and offers both continuations
      rather than choosing; RESUME re-materializes a worktree over the existing
      branch and keeps its name; NEW allocates the next ordinal computed
      against the REMOTE; a second writer arriving after the choice JOINS the
      opened session instead of seeing the prompt; and a merged (not abandoned)
      tile is reworked with NO prompt, since the merge deleted the branch.
- [ ] 8.12 Abandoned-branch cleanup tests (D17): deletion is offered only once
      the topic's proposal exists, is human-invoked, and is NOT triggered by a
      `propose` dispatch whose authoring has not yet landed a proposal.
- [ ] 8.10 Propose-gate tests (D15): `propose` refuses while a live session
      holds the tile, naming the branch and both resolutions, and persists
      nothing; it proceeds after the session ends by merge; it proceeds after
      the session ends by abandon EVEN IF the pushed branch still exists; the
      existing missing-topic, duplicate-dispatch, and agent-rejection refusals
      still hold.
- [ ] 8.7 Notebook tests: a session notebook syncs from the worktree; NO
      lifecycle book ever contains a session source; retirement on session end;
      an import lands on the branch with the unchanged header contract; the
      workbench orphan sweep leaves a live session notebook untouched.
- [ ] 8.8 Full dashboard suite green, including the renderer pins unmodified
      beyond 5.4's arithmetic, plus the boundary validator reporting no
      undeclared output path (the worktree and the session snapshot are
      declared derived/working artifacts).
- [ ] 8.9 Playwright smoke (CI has no node — this is the pre-merge gate): open a
      tile, create a document, watch it appear in the session's panels, edit it,
      confirm the freshness header names the branch, confirm the wheel does NOT
      show it, save via `open-pr`, then confirm the merged document on `main` and
      the session torn down. Zero page errors throughout.

## 9. Dogfood

- [x] 9.1 Brett's rulings on ALL SIX open questions recorded before
      realization can freeze them — DONE 2026-07-26, the change carries no
      parked decision: D16 the session notebook is retired and never
      re-pointed; D17 resume-or-new on rework, the abandoned branch deletable
      once the proposal exists; D18 merge commit, never squash, because the
      gate-action commit series is FDA traceability evidence; D19 a full
      notebook quota degrades the session rather than blocking it; D20 a tile is
      a work surface OR a proposal, `demote` being the route back; D21 `open-pr`
      consults NO readiness signal.
- [ ] 9.2 Brett's live pass — the archive evidence the staged topic names: run a
      REAL session end to end. Create and edit documents on a session branch,
      watch the panels follow the worktree, use the session notebook, open the
      pull request, merge it, and find the merged documents on `main` and in the
      next published snapshot — with the served checkout never having moved and
      the wheel never having shown a draft.
