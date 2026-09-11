# Tasks: add-propose-verb

## 1. Contracts (openxFactory)

- [x] 1.1 Extend `gate-intent.schema.yaml`: `propose` in the verb enum,
      `topic_id` on target, conditional `propose → target.topic_id`.
- [x] 1.2 Extend `gate-action-record.schema.yaml`: `propose` in the action
      enum, `topic_id` on target, conditionals `propose → target.topic_id`
      and `propose → artifacts contains workflow-job`.
- [x] 1.3 Validate: schema validators + `openspec validate --all --strict`.

## 2. Engine (codexFactory)

- [x] 2.1 `kickoff.py`: `propose()` dispatch — human-only, staging-topic
      existence guard, duplicate-commission refusal, `workflow-job`
      descriptor (workflow `proposal-authoring`, `topic_id` target) +
      gate-action record.
- [x] 2.2 `gate_console.py`: `ACTION_PROPOSE`, `build_gate_action_record`
      grows `topic_id`; `GateConsole.propose` delegate.
- [x] 2.3 `cli.py`: `gate propose <topic-id>` (+ `--outline`, `--workflow`,
      `--note`).
- [x] 2.4 `gate_routes.py`: `propose` joins `EXECUTING_VERBS`; loopback
      route with the dispose-possible response discipline.

## 3. Dashboard affordance (codexFactory)

- [x] 3.1 Wheel: focused staged tile mounts a "▶ draft proposal" button in
      the badge rail under the same capability gate as the dispose tray;
      refusals land in the refusal panel; success decorates the tile
      (session-local overlay, snapshot untouched).

## 4. Verification

- [x] 4.1 Engine + route tests (accept, missing topic, duplicate
      commission, agent-path rejection) green.
- [x] 4.2 Live browser check on the local dashboard (button renders on a
      staged focus under gate capability, actor resolved; zero page errors).
- [x] 4.3 First real commission by Brett recorded end-to-end (descriptor +
      record in the checkout).
      PASSED 2026-08-01 (D10 combined pass Step E, Brett sign-off same
      day): `▶ draft proposal` on the merged, session-free, honestly-ready
      `consent-instrument-contract` (live health 0.925 / 0 blockers)
      commissioned workflow `proposal-authoring` — descriptor
      `ideation/dashboard/gate-records/consent-instrument-contract/propose-20260801T012134Z.workflow-job.yaml`
      and gate-action record
      `propose-20260801T012134Z.gate-action.yaml` (`actor: brettheap`),
      both landed on `main` by this governance commit (the verb records
      without committing — F10). The first click's FR-023 refusal over the
      then-live session is preserved as evidence of the guard working.
      The commissioned change is `add-consent-instrument` (DTN-016 exit).
      Evidence:
      `add-workbench-integrated-editor-chat/evidence/d10/e-43-commission.md`.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 4 and 5, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting exactly those two lines recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `583bd6e` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

**Why this reverses no finding.** The 2026-08-22 register ruling C2 examined this record and left it headerless, and its finding is re-verified here and stands word for word: "Nothing. Its front matter, its whole directory, its created and archive commits, and its README row name no ratifier and no ratification date." Nothing on this record has been re-read into meaning it did not have. What C2 did not have is OQ-6's later ruling and the phase-b derivation, which make the archive ACT — not any approval on the packet — the citable record. Task 4.3's Brett sign-off is a verification pass and is not cited.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas this delta names — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and LEAVE the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
