# Tasks: add-session-notebook-reconciliation

## 1. The derivation, pure and testable

- [x] 1.1 `live_session_aliases(root, *, repository=None)` — every LIVE session's
      own `notebook_alias`, across the workspace's session repositories, built on
      the EXISTING `session_repositories` + `branch_session.live_session_worktree`
      joint signal. No second liveness rule.
- [x] 1.2 Enumeration failure is a REFUSAL, not an empty set: the function
      reports per-repository failures alongside the aliases it did resolve, so
      the caller can fail closed rather than infer death from silence.
- [x] 1.3 `classify_session_notebooks(titles, aliases, slugs)` — pure, returning
      each `xf-session-` title as `live` / `dead` / `out-of-scope`; a title whose
      repository segment is not one of this workspace's slugs is out of scope.
      Non-session titles are never classified at all.
- [x] 1.4 Enumeration covers EVERY WORKTREE of each session repository, not only
      its canonical checkout — a session container is keyed on the checkout the
      session was opened FROM. Added after task 4.1's live dry run found the gap.

## 2. The mode

- [x] 2.1 `--session-sweep` on `sync-notebooklm-books.py`, report-only, listing
      each dead notebook with the source count a retirement would discard, each
      live one it left alone, and each out-of-scope one.
- [x] 2.2 `--apply` retires the dead set through `branch_session.retire_session_notebook`
      — never a scratch delete — and reports the adapter's own verdict per
      notebook.
- [x] 2.3 Any per-repository enumeration failure refuses the whole run, names the
      repository and reason, exits nonzero, and retires nothing.
- [x] 2.4 An adapter exposing no `retire` refuses loudly under `--apply`.
- [x] 2.5 Flag composition: `--session-sweep` is mutually exclusive with
      `--session-ref` (one names a branch, the other reconciles a namespace), and
      the usage line documents the fourth mode.

## 3. Coverage

- [x] 3.1 The classifier: live untouched, dead detected, out-of-scope excluded,
      non-session titles ignored, and the lossy-alias case (a branch whose
      `draft/` prefix and case differ from its alias) resolving correctly
      FORWARD.
- [x] 3.2 The fail-closed refusal: one unreadable repository refuses the run and
      retires nothing, asserted against a fake adapter that records every call.
- [x] 3.3 Report-only default performs no retirement, proven by the same
      recording adapter.
- [x] 3.4 `--apply` retires exactly the dead set and reports each verdict; an
      adapter without `retire` refuses.
- [x] 3.5 A live session's notebook is never retired even when its repository
      also carries dead ones.

## 4. Evidence and exit

- [x] 4.1 A recorded dry run against the live account from the workspace root:
      the report names the live sessions it left alone and any orphan it found,
      and mutates nothing. RUN 2026-08-10 — and it EARNED ITS PLACE: the first
      run reported both of Brett's LIVE sessions as dead (a session container is
      keyed on the checkout it was opened from, and both were opened from a
      FEATURE worktree the enumeration never asked). Fail-closed could not fire —
      "no sessions in this checkout" is a legitimate answer — so the enumeration
      was completed across every worktree git lists for the repository. Second
      run: `2 live session(s); no orphans`, both KEEP. Regression pinned in
      `test_a_session_opened_from_a_feature_worktree_is_seen_as_live` against a
      real repository with a real linked worktree.
- [x] 4.2 Runbook note: which mode cleans up after a hand teardown, and that the
      targeted route still refuses a dead branch by design — session runbook
      §4a, including the run-from-the-workspace-root rule task 4.1 earned.
- [ ] 4.3 Archive on realization evidence per `release-realization`
      (`target_release: none`, so archiving follows the merged + green
      realization).
