# T092 Re-run — Notebook-Half Acceptance Evidence

Status: brainstorm
Kind: note
Repository context: openxFactory

## What this records

The 2026-08-04 re-run of codexFactory `specs/007-workbench-branch-sessions`
T092 (SC-009), agent-driven on Brett's commission against a dedicated serve
checkout pinned at published `origin/main` b9c5dc3a3d21. The ratified 2026-07-31
D10 combined pass (Brett sign-off 2026-08-01) accepted the feature with finding
F8 open: the session notebook was never exercised, because the `nlm` CLI had
drifted and the dedicated-serve layout hid the session worktree from the
notebook sync's repository walk. This session exists to close that half while
re-walking every other SC-009 clause.

## The pass, in this session's own terms

- The serve is a loopback `generate-and-open` on a dedicated clone whose
  workspace root carries `openxFactory/` at the exact name the sync's
  `session_repositories()` walk requires — the F8 layout lesson applied.
- This document was CREATED through the workbench's own create verb, which
  opened `draft/workbench-branch-sessions` (create commit 945ce0697284).
- The at-open notebook create degraded EXACTLY as F8 recorded: the adapter
  speaks `nlm notebook create <alias> --json` and the installed CLI has no
  such option, so the session opened fully usable with no notebook (D19,
  FR-042). The drift is therefore still live in the adapter and is re-filed
  by this run rather than silently patched around.
- The notebook (xf-session-openxfactory-workbench-branch-sessions-kd9b2acae0586) was then created and populated through the FR-040
  route the refusal itself names —
  `sync-notebooklm-books.py <workspace-root> --session-ref
  draft/workbench-branch-sessions --apply` — which is the daily-proven `nlm`
  surface; it was re-synced after this rewrite, and a real `nlm` query was
  answered from the session's own sources before the save. The op lists and
  the query answer live in the evidence bundle beside the codexFactory T092
  tick.
- The document was then REWRITTEN to this text through the session bar's
  rewrite verb — one more gate-action commit on the branch.
- The save, the merge-commit landing, and the reconciling second save follow
  runbook §6; their fingerprints (PR number, merge sha, snapshot) are recorded
  in the codexFactory T092 tick, which this document necessarily predates.

## Why it lives in this topic

`ideation/staging/workbench-branch-sessions/` is the staged topic that owns
this feature's ideation material; the acceptance run's own record is exactly
the kind of dated fragment the topic exists to hold.
