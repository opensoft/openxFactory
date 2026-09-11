# Tasks: add-opendox-project-header

## 1. Contracts

- [x] 1.1 Extend `gate-intent.schema.yaml` additively: `edit-project` in the
      verb enum; conditional `edit-project → target.project_id` (the field
      exists since create-project). Header note naming this change.
- [x] 1.2 Extend `gate-action-record.schema.yaml` the same way, including
      the workflow-job companion conditional.
- [x] 1.3 Conformance tests: valid intent + record for `edit-project`;
      missing companion rejected; missing `project_id` rejected.
- [x] 1.4 Contract registration at the next additive bundle cut (rides with
      create-project's 1.4). — Realized 2026-08-06 at **contract-v1.30** (release commit 6c03d78): the project-plane additive deltas to gate-intent, gate-action-record, ideation-dashboard-snapshot, and xfactory-document-catalog-snapshot ride that cut with refreshed per-file manifest digests, and the CHANGELOG credits this change by name; manifest digests verify 124/124 at the tag.

## 2. Engine + routes

- [x] 2.1 `kickoff.py`: `edit_project()` — human-only; guards in the ruled
      order (project existence, additions in the roster∪register universe,
      removals currently members, at-least-one-member floor, duplicate via
      the shared index); descriptor payload `add`/`remove` (either may be
      empty, not both); NO register mutation. `COMMISSION_TARGET_KEY`
      already maps `project_id`.
- [x] 2.2 `gate_routes.py`: `EXECUTING_VERBS` gains `edit-project` with the
      structured-refusal discipline; `cli.py`: `gate edit-project
      <project-id> [--add <repo>…] [--remove <repo>…] (--note)`; GateConsole
      delegate.

## 3. Header redesign

- [x] 3.1 Brand: "Opensoft openDox" in the brand line and `<title>`; the
      repo chip retires.
- [x] 3.2 Project dropdown (D13): "New Project" first (opens the rehomed
      create form, restoring the previous selection), then the projects,
      pending entries preserved; default = stored scope else first project.
- [x] 3.3 Repo filter (D14): icon + popover of the current project's
      members; single-select stores the key and reloads; active repository
      highlighted; unavailable members say why; "All repositories" first,
      disabled with the merged-view note (armed by
      add-project-merged-projection when it lands).
- [x] 3.4 Manage mode (D15): checkbox per register repository seeded from
      membership; apply diffs into an edit-project commission; pending
      membership changes badge until fulfilment; refusals textContent-only.
- [x] 3.5 Model tests: dropdown rows/default resolution, filter rows,
      manage-mode diffing, pending badges; engine + wire tests for
      edit-project's guards and accept path.

## 4. Verification

- [x] 4.1 Full suites green; strict validation green.
- [x] 4.2 Live browser check: the renamed header, dropdown default and New
      Project flow, filter single-select switching, manage mode
      commissioning (accept + refusal), gate-off degrade (dropdown + filter
      render read-only, New Project and manage mode absent); zero page
      errors.
      (Verified 2026-08-06, headless Chromium against gate-on + gate-off
      serves of this checkout: title + brand "Opensoft openDox", repo chip
      gone; the dropdown reads New Project… then the five register projects,
      defaulting to `core`; New Project opens the create form and restores
      the selection; the filter reads "⧩ Core Contracts" with the ARMED
      all-repos line (exit 2's derived aggregate), the member row, and
      manage members with membership-seeded checkboxes; switching projects
      re-renders the filter; gate-off disables New Project and drops manage.
      Zero console errors, page errors, and >=400 responses on both drives.
      The wire accept + refusal paths are pinned by test_edit_project.py's
      real-HTTP group.)
- [x] 4.3 First real edit-project commission by Brett, fulfilled into the
      aggregation register.
      (Realized 2026-08-06: Brett commissioned AdxFactory into project
      `openxfactory` from the filter's add dropdown at 19:35:38Z — right
      after creating the EMPTY project `xfactory` at 19:35:30Z, the D17
      create-first flow's first real use. Both fulfilled into the
      aggregation register by the fulfilling session (commit d1ea422,
      pinned schema green); both descriptors flipped dispatched ->
      delivered. Brett's second edit attempt meanwhile drew the duplicate
      guard's refusal naming the blocking descriptor — the guard's first
      real exercise.)

## 5. The dropdown-like filter (design D-h / topic D16, Brett's 2026-08-06 annotation)

- [x] 5.1 Filter popover rework: "＋ add repository…" first (inline
      candidate select over roster∪register minus members; commissions a
      single-addition edit), per-row eyeball visibility indicator (active
      repo, or any member under the project's merged view), and a two-click
      trash control commissioning the single removal; manage mode retires.
- [x] 5.2 Model: `addableRepositories` + `repositoryVisible` (manageDiff
      retires with manage mode); node tests updated.
- [x] 5.3 Live browser check re-run on the reworked popover.
- [x] 5.4 Brett's 2026-08-06 follow-up annotations: the create form becomes
      a LABELED PANEL (heading, captioned name field and member list, a
      what-this-does note, "commission project"/"cancel"), and the add-repo
      flow becomes ONE self-closing dropdown (placeholder line = the
      affordance; choosing commissions and the select closes, like the
      project selector).
- [x] 5.5 The live check exposed that explicit `display:flex` on the
      popover/panel defeated the `hidden` attribute (the filter popover
      could never close); restated `[hidden] { display:none }` for both and
      verified full open/close cycles with zero page errors.
- [x] 5.6 Brett's 2026-08-06 second annotation round: the filter box names
      its content (single member -> the repository's name; several ->
      "N Repos"); theme + settings pin to the page's top-right as chrome;
      the header-level grouping roll-up strip retires (the project dropdown
      and filter are where grouping surfaces; the pure grouping model stays
      available) — the scoped-selection delta's grouping requirement
      restated accordingly. Live-checked: labels, corner placement, settings
      panel, no roll-up row, zero page errors.
- [x] 5.7 Brett's 2026-08-06 empty-project ruling ("I think it is better if
      we allow a project to exist without a repo defined"): the register
      schema admits an empty `repositories` set (the task-2.6 minItems rule
      reversed; the negative example converts to a positive one), the
      create-project non-empty guard and the edit-project last-member floor
      are dropped, the route accepts an absent/empty list, and the create
      panel marks members optional. A project is created first and gains
      members later through edit-project. Engine/wire/UI checks green.

## 6. Queued edits (topic D18, Brett's 2026-08-07 ruling)

- [x] 6.1 Engine: `edit_project` drops the single-flight duplicate guard and
      validates against EFFECTIVE state — the register with the project's
      dispatched, undelivered commissions applied oldest-first (a pending
      create-project counts, so a just-created project can be populated
      before fulfilment). `create-project` keeps its single-flight guard.
      Same-second commissions land as distinct descriptors (stamp bump).
- [x] 6.2 Projection: `pending_edits` carries EVERY dispatched edit
      commission (not one per project), including edits queued behind a
      pending creation; the popover nets them into one badge overlay and
      the add line's candidates subtract pending additions.
- [x] 6.3 Lane: one pass delivers every queued commission oldest-first
      (the shared index's one-per-target reduction bypassed).
- [x] 6.4 Tests: queued second edit records; duplicate addition against
      pending-applied state refuses; removal of a pending addition is
      legal; edit on a pending-created project records; lane multi-edit
      pass; projection multi-row shape; add-line candidates minus pending.
- [x] 6.5 Live browser check: two successive adds from the popover with no
      refusal, the apply affordance counts both, one click lands both.
      (Verified 2026-08-07 on the scratch git fixture: repoB then repoC
      commissioned from the same open popover — the second within the same
      second, landing as a stamp-bumped distinct descriptor — both badging
      "(addition pending)"; after reload the header read "⟳ apply 2
      pending" and one click delivered both in one register-only commit,
      pushed to the bare remote. Zero page errors.)

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
Brett's "ratify both and realize them in order" of 2026-08-06, quoted on the
line and quoted again in the body of commit `8121f5f` of the same day —
'Ratified by Brett 2026-08-06 ("ratify both and realize them in order")' —
which is the commit that wrote this line. An append on a single-valued header
is mechanically impossible — `doc_health.corpus.STATUS_RE` swallows any
trailing annotation — so this is an in-place overwrite and an extension of
Brett's 2026-08-10 append ruling, named as one, and it is entered in
`docs/archive-record-discrepancies.md`.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas this delta names — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and LEAVE the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
