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
- [x] 4.3 Archive on realization evidence per `release-realization`
      (`target_release: none`, so archiving follows the merged + green
      realization).
      Realization: merged as `1b964ba` (PR #163), green at
      `tests/ideation-dashboard` 2850 passed / exit 0 on 2026-08-13. Evidence
      recorded as the proposal's `Realized:` line — the gate requires it to
      EXIST, not merely to be true — and archived on 2026-08-13.
      NOTE for whoever repins the axis: `target_release: none` is not a legal
      value. `release-realization`'s "Realization axis declaration" allows only
      `implemented` or a named release; `none` belongs to `code_surface`. Five
      sibling changes carry the same mis-spelling, so it is left as-declared here
      rather than corrected under cover of an archive commit.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4 (Brett Heap, in-session,
2026-08-23): a `Ratified by:` line that names a person and a date rather than
an approving OpenSpec change is substantively the record-citing form and takes
the record-citing prefix. This line was a live CRITICAL `ratified-provenance`
finding and the respell clears it. The record that justifies this line is
Brett's 2026-08-10 instruction quoted on the line — "fix the session teardown
notebook gap" — quoted again in the body of commit `1b964ba` (PR #163) of the
same day. An append on a single-valued header is mechanically impossible —
`doc_health.corpus.STATUS_RE` swallows any trailing annotation — so this is an
in-place overwrite and an extension of Brett's 2026-08-10 append ruling, named
as one, and it is entered in `docs/archive-record-discrepancies.md`.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas this delta names — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and LEAVE the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
