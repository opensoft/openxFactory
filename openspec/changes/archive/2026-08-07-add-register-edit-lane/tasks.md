# Tasks: add-register-edit-lane

## 1. The lane

- [x] 1.1 `register_edit_lane.py`: scan dispatched `project-register-edit`
      descriptors (both project verbs); surgical block edits on the register
      (create appends a project; edit adds/removes members inside the
      project's block; comments preserved); pinned-schema validation BEFORE
      writing; structured `delivered_at`/`delivered_by` stamps on the flip;
      refuse-and-report for stale commissions.
- [x] 1.2 Git half: commit ONLY `project-register.yaml` (explicit pathspec)
      and push with pull-rebase-retry; any git failure leaves the file
      edited, the descriptor dispatched, and reports.
- [x] 1.3 CLI: `python3 -m ideation_dashboard.register_edit_lane
      --repo-root . [--watch --interval N] [--no-git]`.

## 2. The button

- [x] 2.1 `POST /actions/apply-register-edits`: loopback-only, gate-actor
      required; runs the lane once, returns the report.
- [x] 2.2 Header affordance: "⟳ apply N pending" whenever the projection
      carries pending items under the gate capability; reloads on success.

## 3. Verification

- [x] 3.1 Lane tests: create/add/remove applied on a comment-bearing fixture
      register (including the empty-list form), validation refusal, stale
      commission refusal, delivered stamps, git-off mode.
- [x] 3.2 Wire test: commission → apply route → register updated, descriptor
      delivered, report shape; refused off-loopback.
- [x] 3.3 Live browser check: the button appears with a pending commission,
      applies it, and the projection's truth plane reflects the edit; zero
      page errors.
      (Verified 2026-08-06 on a scratch git fixture — bare remote + clone +
      register + fixture corpus: the filter's add dropdown commissioned
      repoB into core; after reload the header read "⟳ apply 1 pending";
      the click ran the lane in the serve — the register gained repoB, the
      register-only commit landed AND pushed to the remote, the shell
      reloaded, and the button retired with nothing pending. Zero console
      errors, page errors, and >=400 responses.)
- [x] 3.4 Runbook: the watcher's run line beside the serve.
- [x] 3.5 First unattended fulfilment observed (Brett commissions; the
      watcher or button delivers with no terminal session involved).
      (Observed 2026-08-07: Brett commissioned AdxFactory into `xfactory`
      from the dashboard at 01:30:23Z; the polling watcher delivered it at
      01:31:13Z — descriptor stamped `delivered_by: register-edit-lane`,
      register-only commit dd1179e pushed to the aggregation's origin/main —
      with no terminal session involved.)

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
Brett's 2026-08-06 instruction quoted on the line — "we need to automate that
step 2. we need an update button plus a job that watches" — echoed in the body
of commit `23c0f6c` of the same day, "Ratified change realizing Brett's
'automate step 2' directive". An append on a single-valued header is
mechanically impossible — `doc_health.corpus.STATUS_RE` swallows any trailing
annotation — so this is an in-place overwrite and an extension of Brett's
2026-08-10 append ruling, named as one, and it is entered in
`docs/archive-record-discrepancies.md`.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas associated with the `ideation-dashboard` capability — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and are slated for removal from the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
