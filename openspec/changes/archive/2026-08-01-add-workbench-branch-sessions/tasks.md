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
- [x] 1.6 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`, README contract index) at the next additive
      bundle cut, per `docs/contract-versioning-policy.md`
      (registration-at-realization precedent). Covers the D23 `provenance`
      growth of 1.8 as well as the 1.1/1.2 growth.
      Realized at contract-v1.26 (2026-07-30): the gate-action-record
      manifest entry (per-file sha256, covering the 1.1/1.2 session-verb
      growth and the 1.8 D23 `provenance` block), the contract-v1.26
      CHANGELOG registration, and the README contract index attribution
      landed through PR #43, published merge
      `4efa9d0e2c7d21f2abf3cd7e55f41b74afed97f9` (tree byte-identical to
      the reviewed candidate). Annotated tag object
      `bf20357d8452e7e02ff15811f1912ec691d01cfb` dereferences to that
      merge; verify-promotion and verify-tag pass. Gates at the merge SHA:
      verify-commit over the 179-entry release inventory, manifest digests
      107/107, strict family validator 0/0, OpenSpec --all --strict 57/57.
- [x] 1.7 AMENDMENT, 2026-07-27 (Brett's D23 ruling; a shipped-feature amendment
      of RATIFIED text, recorded not silent): narrow the two ratified scenarios
      that promised an agent-refusal the console-presence control cannot deliver
      — "An agent invokes the edit verb" and "An agent invokes propose" — to the
      caller that cannot demonstrate it originates from the human console this
      serve started, each stating that a process running as the identified human
      is NOT distinguished and that the distinction is deferred to the
      xForge-host identity work under D22. Narrow the same overstatement where it
      appeared in REQUIREMENT prose (`edit-document` and `open-pr`); the
      human-only AUTHORITY language stays. Record the ruling as D23 in design.md
      with the superseded wording quoted, plus a Complexity Tracking row naming
      the accepted gap and its deferral.
- [x] 1.8 Additive growth of `contracts/schemas/gate-action-record.schema.yaml`
      for the same ruling (D23 ruling 3 — tag the gateway): an OPTIONAL
      `provenance` block naming the SURFACE (`http` | `cli`) and how console
      presence was shown (`console-token` | `tty` | `declared`), with both fields
      required WITHIN the block and NO conditional requiring the block for any
      action. Commentary names this change as the growth source, the
      `create-document` / `document`-kind growths as the precedent, and states
      why no conditional may require it: records predating the growth exist in
      this corpus, and every record codexFactory PR #49's realization has already
      emitted rides a per-gate-action commit series that is FDA-traceability
      evidence under D18 — neither may be invalidated retroactively.
      The ROUTE always emits it; a codexFactory test
      pins that. Additivity proven by jsonschema probe (a record without
      `provenance` validates; one with it validates) and by the packaged
      examples, where `edit-document` carries the block and the sibling `open-pr`
      / `abandon-session` examples deliberately do not.

## 2. Branch session lifecycle (codexFactory)

- [x] 2.1 Session branch naming derived deterministically from the TILE's scope
      identity (D2): `draft/<topic-folder>` for a staged topic, scope kind + id
      for a cluster or a possible. Never the actor. Ordinals (`-2`, `-3`) are
      allocated only by D17's NEW continuation, as highest-existing-plus-one
      computed against the REMOTE so two machines cannot disagree.
      (SANCTIONED DEVIATION at realization: the scan is the UNION of the remote
      (`git ls-remote --heads`, never a fetch) and the local refs, not the remote
      alone — a strict superset. The remote half remains mandatory, and it is what
      keeps D17's two-machine property; the local half was added because a
      never-pushed abandoned branch is otherwise invisible and nothing in this
      feature pushes before `open-pr`.)
- [x] 2.1a Resume-or-new on a tile whose previous session was ABANDONED and
      whose branch survives (D17): the first gate write MUST report the
      abandoned branch and offer RESUME (re-materialize a worktree over the
      existing branch, keeping its name) or NEW (next ordinal). Offered ONLY
      while no live session holds the tile; once either choice opens a session,
      later writers JOIN it, so the prompt can never fork one tile in two.
- [x] 2.1b Refuse to open OR resume a session on a tile carrying a LIVE
      PROPOSAL (D20): an existing proposal, or a dispatched-and-undelivered
      `propose` workflow-job. The refusal names `demote` as the route back; when
      authoring is still in flight it says instead that the proposal has not
      landed yet, since there is nothing to demote. Mirror of the D15 refusal —
      the two states are mutually exclusive from both directions.
- [x] 2.2 Spawn on the FIRST gate write against a tile with no active session:
      create the branch and materialize a git WORKTREE for it. Idempotent — a
      second actor's first write JOINS the existing session (D2).
- [x] 2.3 Served-checkout immovability (D3): assert at every session entry point
      that no session operation switches, resets, or stashes the served
      checkout. A test that would move it MUST fail.
- [x] 2.4 Worktree placement in the gitignored container location the notebook
      projection's scan scope already excludes (`<repo>-worktrees/`), plus
      teardown that removes the worktree, the session's registry entry, and the
      session notebook on both endings.
- [x] 2.5 Two endings (D9): merge (teardown + DELETE the session branch +
      main-view refresh) and explicit abandon (teardown + recorded reason).
      Abandon MUST NOT delete pushed history or close a pull request — the
      asymmetry is deliberate: the merge preserved the work, the abandon did not.
- [x] 2.6 Commit-per-gate-action write path (D4): one commit carrying the
      action's documents AND its gate-action record, with the record naming the
      commit as a `commit`-kind artifact. Refuse any path that would split them.
- [x] 2.7 Refuse externally-dispatching verbs inside a session (D4/D12): a
      running workflow dispatch, a publication, a build, or a rollout invoked
      from a session refuses and reports.

## 3. Session snapshot and source resolution (codexFactory)

- [x] 3.1 Register the session as a `(repository, session-branch)` entry in the
      EXISTING snapshot registry (D6) — no overlay, no diff layer, no second
      projection path.
- [x] 3.2 Generate the session snapshot from the WORKTREE root and regenerate
      after EVERY gate action in the session, so a created or edited document
      appears in the session's bullseye, docs panel, and outline with no manual
      step.
- [x] 3.3 Refuse publication or indexing of any session snapshot — the
      selector change's non-`main` refusal already exists; confirm sessions
      exercise it rather than bypass it.
- [x] 3.4 Freshness header names the SESSION BRANCH as the active ref whenever a
      session snapshot renders (D6/D7 — draft-view ambiguity is the failure
      mode this closes).
- [x] 3.5 Branch-aware `/source` bound to the session worktree with per-entry
      confinement; a path escaping the session root REFUSES and MUST NOT fall
      back to the `main` copy. Outside a session the pass-through is unchanged.

## 4. Session gate verbs (codexFactory)

- [x] 4.1 `edit-document` route + CLI parity verb (D5): human-only,
      loopback-only, actor fail-closed, ~~agent-refused~~ **refused for any caller
      that cannot demonstrate it originates from the human console this serve
      started** (TEXT AMENDED 2026-07-27 under D23/task 1.7 — the same
      overstatement 1.7 narrowed in the ratified scenarios and requirement prose;
      a declared agent boundary is still refused outright, but a process running
      as the identified human is NOT distinguished and that distinction is
      deferred to D22's xForge-host identity work); valid ONLY inside an
      active session; rewrites an existing document in the worktree; no create,
      no delete; refuses a target outside the session root; refuses entirely
      with no active session.
- [x] 4.2 `create-document` inside a session writes into the WORKTREE instead of
      the served checkout, with its create-only semantics and every engine
      refusal unchanged.
- [x] 4.3 `open-pr` route + CLI parity verb (D8): pushes the branch, opens the
      pull request into the existing Merge-Master ritual, records the dispatch
      with the pull request as a `pull-request`-kind artifact. Cannot merge,
      approve, self-review, or bypass protection. Does NOT require the topic's
      readiness gate — neither the blocking staged-to-proposal gate nor the
      advisory recommendation gate (D21). Re-invocation updates
      and reports the existing PR rather than opening a second.
- [x] 4.4 Abandon route + CLI parity verb (D9): recorded with a reason, tears
      down session state only.
- [x] 4.5 `edit-apply` left untouched (D5): confirm by test that the
      main-resident AI-redline path is byte-identical in behaviour after this
      change. (SANCTIONED DEVIATION, D23 ruling 3 of 2026-07-27: `edit_apply`
      gained ONE keyword parameter, `provenance`, because every record-writing
      verb now tags its gateway — task 1.8's growth. The REDLINE behaviour is
      unchanged and pinned: it still rewrites the served checkout and not the
      worktree, still emits its redline artifact, still writes no `target.ref`,
      and still adds no commit to a live session branch.)
- [x] 4.6 `propose` unresolved-session refusal (D15): the existing propose route
      gains a precondition — refuse while the tile's session registry entry is
      live, naming the branch and both resolutions (merge the PR, or abandon).
      Keys on the live session, NOT on branch existence, so a branch surviving
      an abandon does not block. No new verb: the two resolutions are the
      existing `open-pr`→merge path and `abandon-session`.
- [x] 4.7 Abandoned-branch cleanup once the topic's proposal exists (D17): a
      HUMAN-invoked affordance, never automatic and never fired by the `propose`
      dispatch alone — the commissioned authoring may not have produced a
      proposal yet. Offered only for a branch whose session was abandoned.

## 5. Workbench surface (codexFactory)

- [x] 5.1 Session affordances in the workbench (edit, save, abandon, refresh
      notebook), with transport in the sibling module per the pinned renderer
      constraints (`views/staging-workbench.js` stays free of `fetch(`/`POST`).
      (DEVIATION, realization spec C10: four affordances, THREE live routes —
      `refresh-notebook` is not a gate verb, so it renders as a copyable
      descriptor in BOTH gate postures rather than as a live control, and owes no
      route and no `fetch` arithmetic. Its real invocation is 6.3's
      `sync-notebooklm-books.py --session-ref <branch>`.)
- [x] 5.2 Session posture indicator: honest about whether a branch session is
      ACTIVE, which branch it is on, and whether the view is a draft view —
      distinct from the gate-capability posture pill and from the UI-lifetime
      "workbench session" state (D14).
- [x] 5.3 Gate-capability-off rendering: every session affordance is a COPYABLE
      CLI DESCRIPTOR, never a live button; no session write reachable from the
      page.
- [x] 5.4 Renderer-bundle pins respected, never edited: the same-origin
      `fetch(` pin's file set and per-file counts are updated only as the
      arithmetic of new same-origin routes requires.

## 6. NotebookLM session notebooks (codexFactory tooling)

- [x] 6.1 `xf-session-<topic>` session-notebook mode in
      `scripts/sync-notebooklm-books.py`: sources synced FROM the session
      worktree, created on session start, RETIRED on session end (D11). The
      title MUST NOT use the `xf-wb-` prefix, and a test MUST assert that
      `workbench_orphan_sweep` leaves a live session notebook untouched.
      (TWO SANCTIONED DEVIATIONS at realization. (a) The alias is
      `xf-session-<repository>-<transformed-branch>` plus a key digest, not
      `xf-session-<topic>`: the session key is (repository, branch), so a
      topic-only alias is not injective — the same branch in two repositories, and
      a tile named `foo-2` beside tile `foo`'s ordinal-2 session, both collide.
      The `xf-session-` prefix and the never-`xf-wb-` rule are unchanged.
      (b) The AT-OPEN projection is BOUNDED — `SESSION_SOURCE_COUNT_CAP` and a
      wall-clock `SESSION_PROJECTION_BUDGET`, because the unbounded count was one
      `nlm` subprocess per governed document inside the create route (60 of 176 on
      the real corpus). The remainder is DEFERRED, not dropped: the count reaches
      the human through the D19 notice and 6.3's re-sync completes it unbounded.)
- [x] 6.2 Lifecycle books stay MAIN-ONLY: confirm by test that branch-session
      worktrees are excluded from all three books, in addition to the existing
      `<repo>-worktrees/` exclusion.
- [x] 6.3 "Refresh notebook" session action re-syncing the session notebook from
      the worktree after edits.
- [x] 6.4 Hybrid source-return imports for a session notebook write into the
      origin folder INSIDE the worktree and land on the branch, with the
      imported-file header contract and idempotency-by-source-id unchanged.
- [x] 6.5 Update `docs/lifecycle-notebook-projection.md` with the session
      notebook section (the canon books' main-only rule stated, the session
      notebook's life bound to its session, the worktree-sourced sync command,
      and the branch-landing import path).

## 7. Plane confinement

- [x] 7.1 Hosted plane exposes NONE of it (D12): no session, no ref selection,
      no session verb, no worktree, no non-`main` snapshot. A hosted request
      naming a non-`main` ref refuses.
- [x] 7.2 Record the arrival path rather than building it: a hosted session
      becomes possible by binding the intent plane's apply-lane ref (§4 of
      `add-ideation-intent-plane`) through the existing (repository, ref) seam,
      with no re-cut of the snapshot source interface.

## 8. Verification

- [x] 8.1 Lifecycle tests: first gate write spawns branch + worktree; a second
      actor joins the SAME session; the served checkout is never moved; merge
      and abandon both tear down worktree, registry entry, and notebook.
- [x] 8.2 Audit tests: each gate action is exactly ONE commit carrying documents
      and record together; the record names its commit; a split-write path
      refuses; an externally-dispatching verb refuses inside a session.
- [x] 8.3 Edit-boundary tests: `edit-document` succeeds in a session; refuses
      with no session; refuses a path outside the session root; refuses a
      delete; the main-resident `edit-apply` path is unchanged.
- [x] 8.4 Visibility tests: a session draft is absent from the wheel, the
      funnel, and the hosted snapshot; present for a second actor in the same
      session; present on shared surfaces only after merge.
- [x] 8.5 Snapshot tests: the session snapshot regenerates after every gate
      action; the freshness header names the branch; publication and indexing of
      a session snapshot refuse; no overlay path exists.
- [x] 8.6 Save tests: `open-pr` pushes, opens the PR, and records it; cannot
      merge or approve; proceeds with no fired readiness gate; a second
      invocation updates rather than duplicating; merge tears the session down,
      DELETES the session branch, and refreshes the main view.
- [x] 8.13 Proposed-tile session refusal tests (D20): a gate write on a tile
      with an existing proposal opens no session, persists nothing, and names
      `demote`; a gate write while a `propose` job is dispatched-and-undelivered
      refuses and says the proposal has not landed rather than naming demote;
      after a demotion the same tile opens a session normally; and the
      resume-or-new prompt is NOT offered on a proposed tile that still has an
      abandoned branch.
- [x] 8.11 Resume-or-new tests (D17): a first gate write on a tile with a
      surviving abandoned branch reports it and offers both continuations
      rather than choosing; RESUME re-materializes a worktree over the existing
      branch and keeps its name; NEW allocates the next ordinal computed
      against the REMOTE; a second writer arriving after the choice JOINS the
      opened session instead of seeing the prompt; and a merged (not abandoned)
      tile is reworked with NO prompt, since the merge deleted the branch.
- [x] 8.12 Abandoned-branch cleanup tests (D17): deletion is offered only once
      the topic's proposal exists, is human-invoked, and is NOT triggered by a
      `propose` dispatch whose authoring has not yet landed a proposal.
- [x] 8.10 Propose-gate tests (D15): `propose` refuses while a live session
      holds the tile, naming the branch and both resolutions, and persists
      nothing; it proceeds after the session ends by merge; it proceeds after
      the session ends by abandon EVEN IF the pushed branch still exists; the
      existing missing-topic, duplicate-dispatch, and agent-rejection refusals
      still hold.
- [x] 8.7 Notebook tests: a session notebook syncs from the worktree; NO
      lifecycle book ever contains a session source; retirement on session end;
      an import lands on the branch with the unchanged header contract; the
      workbench orphan sweep leaves a live session notebook untouched.
- [x] 8.8 Full dashboard suite green, including the renderer pins unmodified
      beyond 5.4's arithmetic, plus the boundary validator reporting no
      undeclared output path (the worktree and the session snapshot are
      declared derived/working artifacts).
- [x] 8.9 Playwright smoke (CI has no node — this is the pre-merge gate): open a
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
- [x] 9.2 Brett's live pass — the archive evidence the staged topic names: run a
      REAL session end to end. Create and edit documents on a session branch,
      watch the panels follow the worktree, use the session notebook, open the
      pull request, merge it, and find the merged documents on `main` and in the
      next published snapshot — with the served checkout never having moved and
      the wheel never having shown a draft.
      PASSED WITH FINDINGS 2026-07-31 (D10 combined pass, Brett sign-off
      2026-08-01): session `draft/consent-instrument-contract` ran real
      work end to end — create `b280542` + edits `8599f60`/`9674dc8` as
      gate-action commits (the packet went 0.458/2-blockers →
      ready/0.925/0), panels followed the worktree via the session
      snapshot, the wheel showed no draft on either plane (hosted refuses
      non-main refs outright), PR #47 merged as MERGE COMMIT `52153ce`
      preserving the series, and both documents were found on `main` and
      in the published snapshot (aggregation run `30677000612`, PR #68)
      through separate read paths — four fingerprints, HEAD/branch never
      moved. Findings: session notebook not exercised (F8 nlm CLI drift +
      dedicated-serve layout), the open-pr/abandon records land untracked
      in the served checkout (F10), and the merge-ending observation was
      environmentally blocked in the multi-session tree, resolved via the
      sanctioned abandon path (F12). Evidence:
      `add-workbench-integrated-editor-chat/evidence/d10/d-92-*`.

---

## Realization evidence (2026-07-27) — sections 2-8 ticked against merged code

**The merge.** codexFactory PR #49 (`007-workbench-branch-sessions`) merged to
`main` as **`7440bed`**, 44 commits, a MERGE COMMIT per D18 so the
per-gate-action commit series keeps its evidentiary granularity. Implementation
ran through the Speckit feature's own list
(`codexFactory/specs/007-workbench-branch-sessions/tasks.md`, 98 tasks, 97 done —
only T092, this change's 9.2, is open), not through this ledger; the boxes above
were reconciled afterwards by reading the merged tree, never by transcribing that
list. 97 Speckit tasks carry `(chg N.N)` cross-references, and each was checked
against the code and at least one test that would fail on a revert. Sections 2-8
are complete; **1.6 (contract registration at the next additive bundle cut) and
9.2 (Brett's live pass) remain open by design.**

**What the reconciliation verified, first-hand, at `7440bed`:**

- **Suite, re-run here rather than quoted.** `python3 -m pytest tests -q` →
  **2162 passed** in 267s; `tests/ideation-dashboard` → **1268 passed** in 218s.
  The build's own recorded figures at the same tip are 2150 passed / 12 skipped
  (2162 collected) and 1263 / 5 (1268 collected): the COLLECTED totals agree
  exactly and the 12 skips are the checkout-layout skips (`suite-floor.md`'s
  wave-3 correction), which run rather than skip in an aggregation checkout. Zero
  failures either way. `bash scripts/validate-docs.sh` → 894 passed,
  `doc-health self-gate ok`, `docs validation ok` (8.8).
- **Playwright smoke re-executed, not inherited** (8.9):
  `python3 specs/007-workbench-branch-sessions/playwright-smoke.py` → **36/36
  checks, zero page errors**, against a throwaway scratch checkout with
  `FakePullRequests`/`FakeNotebookAdapter`. Every clause of 8.9 is a named check:
  the create appears in the session's panels, the freshness header names
  `draft/demo-topic`, the document is absent from every wheel tile and from
  `main`'s snapshot, `open-pr` pushes and opens ONE pull request carrying D18's
  never-squash body, the merge tears the session down and deletes the branch, and
  the merged document is in `main`'s refreshed snapshot. The served checkout's
  fingerprint (branch + HEAD + porcelain minus the declared records prefix) is
  re-asserted at four points and moved only at the externally simulated
  Merge-Master merge. One accounted-for server answer (a declared 404 plus its
  `ERR_ABORTED` twin on `/source/openxFactory%40main/<created path>`, the ratified
  open-in-viewer jump meeting FR-014a) was observed exactly as declared.
- **The code behind each section**, by name:
  `scripts/ideation_dashboard/branch_session.py` (4095 lines: derivation,
  resume-or-new, liveness, the two endings, `commit_gate_action`),
  `session_git.py` (the one git seam, no amend operation, the
  served-checkout immovability guard), `session_pr.py` (a three-operation
  pull-request port with no approve/merge path), the four session routes and their
  CLI parity verbs in `gate_routes.py` / `cli.py`, `web/views/swb-session.js` (the
  only session transport — injected fetcher, so the renderer `fetch(` pin was
  satisfied UNCHANGED), and `scripts/sync-notebooklm-books.py`'s `--session-ref`
  mode. `staging-workbench.js` holds zero `fetch(` and zero `POST` (5.1).
- **Both adversarial reviews are closed.** The FIRST review's 19 confirmed
  findings were repaired across two waves (wave 1's five phases; wave 2's three
  stages, where an independent replay pass reproduced two "fixed" items as still
  broken and two as partial, and the notes were corrected in place rather than
  argued with). The SECOND, independent review (26 CONFIRMED, 2 PLAUSIBLE, 7
  critic gaps C1-C7) was cross-mapped item by item BY REPRODUCTION; wave 3 landed
  its blockers, and wave-3 stage 3 closed the tail — findings 21 and 24 plus
  B1, B2, B3, B7, B9, B10, B12, B13 — with every fix proven to FAIL on the
  pre-fix tree by reverting the hunk in a `git archive` copy and re-running the
  named test. Its stage-3 subject is worth recording: eight of the ten items were
  coverage claims that could not fail, three of them mutation-proven false. C1
  (the series unpushed and unreviewed) is closed by the merge itself.
- **D23, Brett's rulings of 2026-07-27**, all three realized: (1) the
  console-presence RESIDUAL IS ACCEPTED — a process running as the identified
  human can read the per-serve console token and act as the human; the control is
  anti-CSRF/same-origin, not authentication, and the distinction is deferred to
  D22's xForge-host identity work, so no refusal was added and no enforcement
  posture changed. (2) the ratified text IS AMENDED to what is enforced (task 1.7;
  landed openxFactory `aec57cf`/`e669b07`), and task 4.1's own "agent-refused"
  wording is narrowed above for the same reason. (3) THE GATEWAY IS TAGGED (task
  1.8): every record-writing verb now stamps `provenance: {surface,
  console_presence}` from where the fact is KNOWN — never re-derived at the
  writer, never readable from a request body (a `Provenance` type, and a mapping
  is refused by both builders), with `declared` beating `tty` so the weakest proof
  is what an auditor sees. Pinned by
  `tests/ideation-dashboard/test_gateway_provenance.py` (24 tests) plus the three
  wave-3 record-schema guards, both gateways driven for real (a live loopback
  `ThreadingHTTPServer` over `http.client`, and `cli.main`). Absent provenance
  writes the PRE-GROWTH shape byte for byte, which is why no conditional requires
  the block.

**Residuals recorded, not repaired here** (each already decided): the
console-presence gap above; `serve.py` refuses a non-console call only on the
SESSION verbs, so a pre-existing verb invoked without console presence still
succeeds and its record carries no `provenance` (deliberate — the vocabulary has
no value meaning "presence was not shown"), which leaves the landed schema
description's "…is REFUSED before a record is written" true of the session verbs
and not of the others: either the refusal widens or that sentence narrows, and
both are decisions rather than repairs; 6.1(b)'s count cap binds on the real
corpus by design; and this change still MUST NOT archive before its five
predecessors (`add-ideation-dashboard`, `add-staging-workbench`,
`add-workbench-bullseye-and-create`, `add-dashboard-repo-selector`,
`add-propose-verb`).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4's RULED extension of
2026-08-23 (Brett Heap, in-session), which widens the class to the sixteen
lines whose named change id is the DOCUMENT'S OWN. A change is not its own
approving change, and such a line passed `fam_ratified_provenance` only by
self-reference. This one emitted NO finding, so the respell is corrective
rather than a discharge and clears nothing from the census. The record that
justifies this line is Brett's approval of 2026-07-26 named on the line,
recorded by commit `6b59614` of that same 2026-07-26,
"add-workbench-branch-sessions: RATIFIED 2026-07-26", after the five-lens
adversarial review and the D16–D21 rulings the line names. An append on a
single-valued header is mechanically impossible —
`doc_health.corpus.STATUS_RE` swallows any trailing annotation — so this is an
in-place overwrite and an extension of Brett's 2026-08-10 append ruling, named
as one, and it is entered in `docs/archive-record-discrepancies.md`.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas associated with the `ideation-dashboard` capability — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and are slated for removal from the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
