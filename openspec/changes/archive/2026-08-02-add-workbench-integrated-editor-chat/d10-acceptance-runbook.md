# D10 Combined Real-Corpus Acceptance Runbook — doxBench Predecessor Gates

Working evidence artifact of the OpenSpec change
`add-workbench-integrated-editor-chat`, realizing design decision **D10** and
scaffolding **task 1.3**. Non-normative: it defines no requirement, changes no
product behavior, and closes no task by existing. Per D10, each predecessor
task is checked only if its own acceptance clauses pass — "the combined run is
a scheduling optimization, not evidence laundering."

## Scope

One operator session (Brett) on the **real corpus**, against merged
codexFactory `main` **predecessor functionality only**: staging workbench,
bullseye/create, repository selector + publication, branch sessions, and the
`propose` commission. It exercises no doxBench editor/chat code and depends on
no doxBench schema, chat route, or session-created-path semantics.

Writes are ordinary governed gate actions intended to persist as real corpus
work. Sequence follows task 1.3's dependency order — **A (6.5) → B (7.2) →
C (6.2) → D (9.2) → E (4.3)** — where D's merge frees the session-free ready
topic that E requires.

Evidence lands beside this file under `evidence/d10/`. Every step records:
the action taken, the expected observation, the actual observation, the
evidence file path(s), and an explicit Pass/Fail.

## Prerequisites (record each in `evidence/d10/00-preconditions.md` before starting)

| # | Prerequisite | What to record |
|---|---|---|
| P1 | codexFactory `main` serve at a clean baseline, started with the ordinary daily-dogfood invocation; `py-bench` available for command evidence | serve HEAD sha; `git status -sb` of the serving checkout |
| P2 | Local human console: loopback serve, real checkout, resolved actor | actor; how console presence was shown |
| P3 | Hosted dashboard reachable; publication lane operational (the same `refetch` binding the green 2026-07-29 automated portion used) | hosted URL; current image tag/digest |
| P4 | Real corpus repository roster configured (all 11 selector routes) | roster list |
| P5 | One real staged topic Brett intends to work for real (drives B and D); identity of the ready topic for E | topic ids |
| P6 | `evidence/d10/` directory exists beside this runbook | — |

## Safe rollback / cleanup

- Step A is read-only by definition; prove it with before/after
  `git status -sb` of the corpus checkout.
- Steps B–E write only through existing `create-document` / `edit-document` /
  pull-request-merge / commission gate actions: one ordinary commit per
  action, reversible with `git revert <sha>`; no history rewrite, no
  force-push, no delete verb exists on any path used here.
- An unfinished Step D session is ended by the session **abandon** path,
  which tears down the branch/worktree without touching `main`.
- An aborted run keeps its partial evidence; record the remaining open
  clauses in the sign-off matrix. Cleanup never deletes evidence.

---

## Step A — `add-staging-workbench` task 6.5

> Brett's live pass on the real corpus: completeness bars are credible on
> documents he knows well; `READY_MIN_SCORE` (starting at 0.60 per his
> 2026-07-25 ruling) is calibrated against fragments he has actually taken to
> proposal; the gate's first refusals are ones he agrees with; and the
> read-only posture holds — nothing in the corpus changed by the session.

**Actions (UI unless noted):**
1. Capture `git status -sb` + HEAD of the corpus checkout (command) →
   `evidence/d10/a-65-readonly-before.txt`.
2. Open the staging workbench on the real corpus; review completeness bars on
   at least five documents Brett knows well; record each document and a
   credible/not-credible verdict.
3. Compare the readiness gate at `READY_MIN_SCORE` 0.60 against at least two
   fragments Brett actually took to proposal (should pass) and at least one he
   considers unready (should refuse).
4. Record whether each refusal encountered is one Brett agrees with.
5. Re-capture `git status -sb` + HEAD (command) →
   `evidence/d10/a-65-readonly-after.txt`.

**Expected observations:** bars credible on the named documents; 0.60 passes
the proposal-worthy fragments and refuses the unready one; refusals agreeable;
before/after checkout state byte-identical.

**Evidence:** `evidence/d10/a-65-completeness.md` (document list + verdicts),
`a-65-ready-score.md` (fragments, scores, gate outcomes),
`a-65-readonly-before.txt`, `a-65-readonly-after.txt`.

**Pass criteria:** all four clause elements individually true. **Pass/Fail:** ____

## Step B — `add-workbench-bullseye-and-create` task 7.2

> Brett's live pass: work a real staged topic in the workbench, read its scope
> in the bullseye, create the document the scope made him want, and find it
> where the dialog said — with a `Source:` line that actually re-derives the
> membership that motivated it.

**Actions (UI):**
1. Open the P5 staged topic in the workbench; read its scope in the bullseye;
   note what document the scope motivates.
2. Create that document through the existing create flow; record exactly where
   the dialog said it would land.
3. Navigate to that location and confirm the document is there.
4. Open the document's `Source:` line and confirm it re-derives the membership
   that motivated the creation (not a static copy).

**Expected observations:** creation lands where declared; `Source:` line
re-derivation matches the bullseye scope reading from action 1.

**Evidence:** `evidence/d10/b-72-creation.md` (topic, motivation, declared
location, found location, `Source:` line text, gate-action commit sha).

**Pass criteria:** every clause element true for this one real creation.
**Pass/Fail:** ____

## Step C — `add-dashboard-repo-selector` task 6.2

> Brett's live pass: reproduce the motivating incident deliberately — land a
> document on `main`, dispatch the publication lane, click refresh on the
> hosted dashboard, and find the document — with no image rebake anywhere in
> the sequence; then drive the selector across Medx/Adx/Ledgerx and confirm
> the sparse wheels read as honest rather than broken.

Note: the 2026-07-29 **automated** live portion is already green in the owning
ledger (hosted `refetch` without rebuild; 11/11 selector routes; populated
Medx/Adx/Ledgerx; five sparse installs honest-empty). This step is the
remaining **deliberate human observation**. It MUST use a distinct document
landed on `main` through an ordinary governed path as part of this step —
not Step B's creation, which is still unmerged at this point in the
A→B→C→D→E sequence.

**Actions:**
1. Record the hosted image tag/digest (must not change during this step) →
   `evidence/d10/c-62-image-before.txt`.
2. Land a distinct document on `main` (ordinary governed path; record the
   commit sha) — not Step B's still-unmerged creation.
3. Dispatch the publication lane (the P3 binding).
4. Click refresh on the hosted dashboard; find the document.
5. Re-record the hosted image tag/digest → `c-62-image-after.txt`; confirm
   identical (no rebake).
6. Drive the selector across Medx / Adx / Ledgerx; record whether each sparse
   wheel reads as honest-empty rather than broken.

**Expected observations:** document visible on hosted after refresh; image
digest unchanged; three selector targets honest.

**Evidence:** `evidence/d10/c-62-publication.md` (commit sha, lane dispatch
record, refresh observation), `c-62-image-before.txt`, `c-62-image-after.txt`,
`c-62-selector-sweep.md`.

**Pass criteria:** full incident reproduction with no rebake + honest sparse
wheels. **Pass/Fail:** ____

## Step D — `add-workbench-branch-sessions` task 9.2

> Brett's live pass — the archive evidence the staged topic names: run a REAL
> session end to end. Create and edit documents on a session branch, watch the
> panels follow the worktree, use the session notebook, open the pull request,
> merge it, and find the merged documents on `main` and in the next published
> snapshot — with the served checkout never having moved and the wheel never
> having shown a draft.

**Actions:**
1. Capture the served checkout fingerprint (branch + HEAD + porcelain)
   before starting → `evidence/d10/d-92-fingerprint-1.txt`.
2. On the P5 staged topic, start/join a branch session; create one document
   and edit one existing document on the session branch (record both
   gate-action commit shas).
3. Confirm the panels follow the worktree (created/edited content visible in
   session panels; wheel shows no draft) and use the session notebook; capture
   fingerprint → `d-92-fingerprint-2.txt`.
4. Open the pull request (record URL; body carries the never-squash series).
5. Merge it; capture fingerprint → `d-92-fingerprint-3.txt`.
6. Find both merged documents on `main` and in the next published snapshot
   through a separate `main`/publication read path (published snapshot,
   hosted read, or an independent clone — never by moving the served
   checkout); capture final fingerprint → `d-92-fingerprint-4.txt`.

**Expected observations:** panels track the worktree throughout; wheel never
shows a draft; all four fingerprints show branch, HEAD, and porcelain
unchanged throughout — including across the PR merge; merged documents
present on `main` and in the next published snapshot, verified through a
separate `main`/publication read path, never by moving the served checkout.

**Evidence:** `evidence/d10/d-92-session.md` (session branch, commit shas, PR
URL, merge sha, snapshot id, panel/notebook/wheel observations), four
fingerprint files.

**Pass criteria:** every clause element observed on this one real session.
**Pass/Fail:** ____

## Step E — `add-propose-verb` task 4.3

> First real commission by Brett recorded end-to-end (descriptor + record in
> the checkout).

Precondition: Step D merged, leaving the P5 ready topic **session-free**
(task 1.3's "merged/session-free ready topic").

**Actions:**
1. Run the first real `propose` commission from that ready topic.
2. Locate the resulting descriptor and its gate-action record in the checkout;
   record both paths and the commit sha.

**Expected observations:** descriptor and record present end-to-end in the
checkout, attributable to this commission.

**Evidence:** `evidence/d10/e-43-commission.md` (topic, descriptor path,
record path, commit sha).

**Pass criteria:** descriptor + record both present and correct.
**Pass/Fail:** ____

---

## Sign-off matrix

Checking the owning-ledger boxes (and doxBench task 1.3) happens in a separate
governance commit after this evidence is reviewed — never during the run.

| Predecessor task | All clause elements pass | Evidence refs | Pass/Fail | Brett sign-off (date) |
|---|---|---|---|---|
| `add-staging-workbench` 6.5 | ☐ | `a-65-*` | ____ | ____ |
| `add-workbench-bullseye-and-create` 7.2 | ☐ | `b-72-*` | ____ | ____ |
| `add-dashboard-repo-selector` 6.2 | ☐ | `c-62-*` | ____ | ____ |
| `add-workbench-branch-sessions` 9.2 | ☐ | `d-92-*` | ____ | ____ |
| `add-propose-verb` 4.3 | ☐ | `e-43-*` | ____ | ____ |

## One-session feasibility

Estimated 1.5–2 hours sequentially: A ≈ 20 min, B ≈ 15 min, C ≈ 15 min
(publication lane latency dominates), D ≈ 30–40 min, E ≈ 10 min, plus
evidence capture. Feasible in one sitting provided P3 (hosted + publication
lane) is confirmed operational before starting; if P3 is down, run A/B/D/E
and leave C open rather than blocking the session.
