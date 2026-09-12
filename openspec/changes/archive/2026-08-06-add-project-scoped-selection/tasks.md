# Tasks: add-project-scoped-selection

## 1. Contracts

- [x] 1.1 Extend `gate-intent.schema.yaml` additively: `create-project` in
      the verb enum; `project_id` on `target`; conditional `create-project →
      target.project_id`. Header note naming this change as the growth
      source; no `contract_schema_version` bump.
- [x] 1.2 Extend `gate-action-record.schema.yaml` the same way, including
      the `artifacts contains workflow-job` companion conditional.
- [x] 1.3 Schema conformance tests: one valid intent and one valid record
      for `create-project`; a record missing its workflow-job companion
      rejected; a record without `target.project_id` rejected.
- [x] 1.4 Contract registration at the next additive bundle cut per
      `docs/contract-versioning-policy.md`. — Realized 2026-08-06 at **contract-v1.30** (release commit 6c03d78): the project-plane additive deltas to gate-intent, gate-action-record, ideation-dashboard-snapshot, and xfactory-document-catalog-snapshot ride that cut with refreshed per-file manifest digests, and the CHANGELOG credits this change by name; manifest digests verify 124/124 at the tag.

## 2. Engine + routes

- [x] 2.1 `gate_console.py`: `ACTION_CREATE_PROJECT`;
      `build_gate_action_record` grows `project_id`.
- [x] 2.2 `kickoff.py`: `create_project()` — human-only; id slugged from the
      name and collision-refused against the register projection; member
      repositories validated against the snapshot-index roster; single-parent
      refusal for a repository already in a project; duplicate refusal via
      the shared (verb, target) index (`COMMISSION_TARGET_KEY` gains
      `create-project → project_id`); `workflow-job` descriptor (workflow
      `project-register-edit`, payload name + repositories) + gate-action
      record; NO register mutation.
- [x] 2.3 `gate_routes.py`: `EXECUTING_VERBS` gains `create-project`, with
      the structured-refusal response discipline.
- [x] 2.4 `cli.py`: `gate create-project <name> --repo <id> [--repo <id>…]`
      (`--note`); GateConsole delegate mirroring the other commissions.

## 3. Selector surface

- [x] 3.1 Project picker in the repo selector: projects listed from the
      register projection; selecting one narrows the roster to member
      repositories; "(ungrouped)" repositories keep today's behaviour.
- [x] 3.2 Create-project affordance under the gate capability with the
      commission form (name + member checkboxes from the roster); refusals
      render textContent-only; the affordance retires for the session once
      commissioned.
- [x] 3.3 Pure-model tests: picker narrowing, gate off, already-commissioned,
      member-set validation surface.

## 4. Verification

- [x] 4.1 Engine + route tests green: accept path, absent member repository,
      single-parent refusal, id collision, duplicate commission, agent-path
      rejection, register untouched by commission.
- [x] 4.2 Live browser check: picker narrows the roster against the split
      register (D7 content); create-project renders under the gate capability
      and not with it off; zero page errors.
      (Verified 2026-08-06, headless Chromium against two loopback serves of
      this checkout with the D7-split register discovered one level up. Gate
      ON: the picker lists the four role projects from
      `/project-register.json`, core-scoping and clearing behave, the
      `+ project` affordance renders, and — every published repository being
      owned post-split — the form honestly reports no candidates with submit
      disabled; a wire probe returned the engine's single-parent refusal
      naming `openxFactory (in 'core')`. Gate OFF: the picker stays (selection
      is read-only) and the affordance is absent. Zero console errors,
      uncaught page errors, and >=400 responses on both drives. Multi-repo
      narrowing is pinned by the node model tests, the local serve having a
      single-entry roster.)
- [x] 4.3 First real commission by Brett recorded end-to-end and fulfilled
      into `project-register.yaml` (descriptor delivered, register edit
      validated + landed in the aggregation repo).
      (Realized 2026-08-06: Brett commissioned project `openxfactory`
      ("openXfactory", member openxFactory) from the dashboard's + project
      affordance at 14:29:28Z — descriptor + gate record under
      ideation/dashboard/gate-records/openxfactory/. The fulfilling session
      applied the edit to the aggregation register (commit 9c74556, pinned
      schema green), a legal second view over openxFactory under the D8
      multi-parent rule with `core` remaining the primary, and flipped the
      descriptor dispatched -> delivered.)

## 5. Multi-parent membership (design D-d, Brett's 2026-08-06 ruling)

- [x] 5.1 Contracts: register schema prose rules rewritten (repository
      membership multi-parent; project→group stays single-parent); snapshot
      schema gains the additive `projects` list beside the singular PRIMARY
      `project`; register validator drops `project-multi-parent-repo`.
- [x] 5.2 Adapter + generator: `ProjectRegisterAdapter.projects_of()` (full
      membership, register order, primary first); the generator stamps
      `projects` beside `project`/`project_group`.
- [x] 5.3 Engine + surface: the create-project single-parent guard dropped
      (an owned member is legal; roster guard unchanged); the affordance
      offers ALL roster repositories as candidates.
- [x] 5.4 Tests: owned-member acceptance (engine + wire), adapter
      primary/full-list resolution, validator no longer errs on shared
      membership; suites green.
- [x] 5.5 Register content: MedxFactory joins `medx-clinical` while staying
      in `domains` (aggregation-repo edit — the ruling's first beneficiary).

## 6. Pending-commission visibility (design D-e, Brett's 2026-08-06 ruling)

- [x] 6.1 `/project-register.json` gains the `pending` plane: dispatched,
      undelivered create-project commissions (name + members from the
      descriptor), deduplicated against the register's own project ids.
- [x] 6.2 Picker: pending entries render as non-selectable
      "(commissioned — pending fulfilment)" options, appended immediately on
      a same-page commission; a pending id never scopes the roster.
- [x] 6.3 Tests: node model (`buildPendingProjects` dedupe/shape/no-scope)
      + the wire round-trip (commission → pending in the projection → truth
      untouched); suites green.

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
Brett's "ratify exit 1 and realize it" of 2026-08-06, quoted on the line and
quoted again in the body of commit `db3e00c` of the same day — 'Ratified by
Brett 2026-08-06 ("ratify exit 1 and realize it")' — which is the commit that
wrote this line, with the topic's D1–D7 round carried as decided context. An
append on a single-valued header is mechanically impossible —
`doc_health.corpus.STATUS_RE` swallows any trailing annotation — so this is an
in-place overwrite and an extension of Brett's 2026-08-10 append ruling, named
as one, and it is entered in `docs/archive-record-discrepancies.md`.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas associated with the `ideation-dashboard` capability — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and are slated for removal from the bundle at `contract-v4.0` (§ 5.7; cut PR #983). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
