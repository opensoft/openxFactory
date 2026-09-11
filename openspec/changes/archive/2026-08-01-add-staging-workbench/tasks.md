# Tasks: add-staging-workbench

## 1. Contract / schema growth (openxFactory)

- [x] 1.1 Extend `contracts/schemas/ideation-dashboard-snapshot.schema.yaml`:
      the `document` `$def` grows an OPTIONAL `completeness` object —
      `score` (number, 0..1) plus the five named signals `structure`,
      `length`, `open_markers`, `keyword_coverage`, `link_degree`, each a
      normalized 0..1 value carrying the raw count that produced it.
- [x] 1.2 Extend the same schema: the `staged_topic` `$def` grows an
      OPTIONAL `health` object — `standing_open_items` (integer),
      `doc_score_min` / `doc_score_mean` (0..1, fixed precision),
      `blockers` (array of typed reasons, each naming its document and
      carrying its count or score), `status`
      (`ready` | `developing` | `stub`).
- [x] 1.3 Pin the contract's invariants in the schema's own commentary: the
      definition of each signal, `open_markers` as an INVERSE signal, the
      fixed weights, fixed decimal precision, and `READY_MIN_SCORE` as v1
      contract constants (tunable configurations are a successor, design
      D2), deterministic and reproducible from the pinned tree with NO
      model call (design D1), health derived from FOLDER corpus documents
      only with status derived from blockers (design D8), and the gating
      bound: the per-document score's ONE gate consumer is the
      staged-to-proposal readiness gate, through the health aggregate —
      never the readiness recommendation gate, never doc-health.
- [x] 1.4 Keep the additive posture explicit: no `contract_schema_version`
      bump, no `additionalProperties: false`, header note naming this change
      as the growth source, and both new objects OPTIONAL so a pre-growth
      snapshot stays valid (design D7).
- [x] 1.5 Confirm no aggregate is added to `cluster` or `possible` (design
      D3 — `staged_topic.health` is the one sanctioned aggregate), and that
      `ideation-workbench.schema.yaml` is untouched (design D5).
- [x] 1.6 Validate: the delegated dashboard-contract validator
      (`scripts/validate-ideation-dashboard-contracts.py`) plus
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`; every
      packaged snapshot example still validates unchanged.
- [x] 1.7 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`) at the next additive bundle cut, per
      `docs/contract-versioning-policy.md`.
      Realized at contract-v1.26 (2026-07-30): the snapshot schema's
      manifest entry (per-file sha256) landed through PR #43, published
      merge `4efa9d0e2c7d21f2abf3cd7e55f41b74afed97f9` (tree byte-identical
      to the reviewed candidate). Annotated tag object
      `bf20357d8452e7e02ff15811f1912ec691d01cfb` dereferences to that merge;
      verify-promotion and verify-tag pass. Gates at the merge SHA:
      verify-commit over the 179-entry release inventory, manifest digests
      107/107, strict family validator 0/0, OpenSpec --all --strict 57/57.

## 2. Generator scoring + health (codexFactory — Speckit-side realization)

- [x] 2.1 New deterministic scoring module beside `generator.py`: the five
      signal functions, the fixed weight constants, `READY_MIN_SCORE`, the
      fixed-precision rounding, the normalized+raw output shape, AND the
      health aggregation (`topic_health(member_docs)` → standing items,
      min/mean, blockers, status). Pure functions over already-loaded
      document text plus the snapshot-derived edge data — no I/O, no clock,
      no model call. This ONE module is imported by the generator and by
      the propose route's guard (design D9) — no second implementation.
- [x] 2.2 `structure`: expected structural elements per `Kind:` with the
      common fallback (H1 title, governance header block, at least one
      section); the expected sets are declared in ONE table, not scattered
      through the checks.
- [x] 2.3 `length` and `open_markers`: body word count against the fixed
      saturation threshold; marker scan (`TODO`, `TBD`, `FIXME`, `??`, open-
      question headings) against the fixed saturation count, subtracted from
      1. Single pass over the already-loaded text (design: generator cost).
- [x] 2.4 `keyword_coverage` and `link_degree`: declared `Topics:` subjects
      resolving against the snapshot's keyword vocabulary; edge degree from
      cluster document edges plus `destinations` (staged topics, changes,
      capabilities), normalized against the fixed saturation degree. Both
      read the generator's own derived maps — no second scan.
- [x] 2.5 `generator.py` `_document_entry` emits `completeness`; excluded
      documents (`_document_exclusion_reason`) carry none, and no dangling
      score survives an exclusion. Each `staged_topics[]` entry emits
      `health` from its FOLDER corpus documents only (design D8) —
      destination-declaring documents contribute nothing to health.
- [x] 2.6 Determinism tests: byte-identity across two runs on one fixture
      tree (documents AND staged-topic health); a fixture doc gaining
      sections and edges scores strictly higher; a fixture topic whose last
      open marker closes and whose docs cross the threshold flips to
      `ready`; an empty topic folder reports `stub`; cross-platform
      stability of the rounded values.
- [x] 2.7 Gating-bound test: no doc-health family or readiness path reads
      completeness or health; outside the generator and its tests, the
      scoring module's only importer is the propose route's guard.

## 3. Staged-to-proposal readiness gate (codexFactory — Speckit-side realization)

- [x] 3.1 The propose route in `serve.py` gains the readiness guard: import
      the scoring module, recompute the topic's health LIVE from the pinned
      checkout at request time (never the served snapshot, design D9), and
      refuse with the blockers verbatim — each document with standing open
      items and its count, each document below `READY_MIN_SCORE` with its
      score and the constant — persisting nothing, exactly like the
      existing missing-topic and duplicate refusals. The existing refusals
      and the human-only rule stand unchanged.
- [x] 3.2 Guard tests: standing open marker → refusal naming the document
      and count; closed questions but an under-threshold document → refusal
      citing score vs constant; ready topic → the commission proceeds
      (descriptor + gate-action record, as add-propose-verb realized);
      refusal persists nothing; agent path still rejected.
- [x] 3.3 Staleness test: a fixture where the snapshot says `ready` but the
      checkout has since gained a standing marker → the route refuses,
      citing the marker the snapshot has not seen.

## 4. Staging workbench view (codexFactory — Speckit-side realization)

- [x] 4.1 Pure model module: `workbenchScope(snapshot, kind, id)` deriving
      the tile's document set per kind (cluster edges; possible cited
      evidence + separately labelled inherited claiming-cluster members;
      staged-topic folder documents + documents declaring that destination),
      with stable ordering. Unit-tested from the node harness like
      `wheel-model.js`.
- [x] 4.2 The full-screen scoped view shell with the `docs` / `lens` /
      `outline` tab set, opened at one scope and closed back to the wheel.
- [x] 4.3 `docs` panel: one row per document with its completeness bar and
      the named signals with raw counts, rendered VERBATIM from the
      snapshot; missing completeness renders as no bar, never as zero
      (design D7).
- [x] 4.4 `lens` panel: re-scope the EXISTING keyword-lens seed and
      edge/degree derivation to the tile's keywords/documents — reuse
      `lens-model.js` / the wheel's degree derivation, add no new
      computation and no new snapshot read.
- [x] 4.5 `outline` panel: render the scope's outline material read-only
      through the `/source` pass-through (the viewer's route, as the
      `landed` verb does); explicit empty state when there is no outline;
      inline degraded message when the route is absent.
- [x] 4.6 Read-only enforcement: no panel has a write path — assert against
      the boundary checker (`boundary.py`) that the view declares no output
      path, and keep the view free of any POST.

## 5. Wheel tile action + staged health display (codexFactory — Speckit-side realization)

- [x] 5.1 `views/wheel-model.js` `WHEEL_ACTIONS`: an `open workbench` row on
      `clusters`, `possibles`, and `staged` with NO `visible` predicate (a
      read-only verb, design D6); `documents` / `active` / `archived` gain
      nothing.
- [x] 5.2 `views/wheel.js` `ACTION_MOUNTERS`: one mounter reusing the
      existing read-only nav-button chrome, wired through the app shell's
      nav callbacks (`app.js`), disabled where no nav callback is supplied.
- [x] 5.3 Staged tile health chrome (design D10): the FOCUSED tile face
      carries a compact tri-state indicator from the snapshot's
      `health.status`; the EXPANDED tile renders the full health block —
      status, standing open items per document, score min/mean, blockers —
      VERBATIM from the snapshot; resting drum faces stay unadorned; a
      pre-growth snapshot renders no indicator and no block, and the
      renderer never computes health itself.
- [x] 5.4 Pure-model tests: `actionsFor` across all six wheels (the
      workbench row appears on exactly the three topic-bearing wheels, gate
      capability on and off); health chrome model for ready / developing /
      stub / absent-health fixtures.

## 6. Verification

- [x] 6.1 Generator + view tests green, including the nightly lane's runtime
      after scoring is added (no regression in lane duration).
- [x] 6.2 Schema conformance: a snapshot with completeness and health
      validates; a pre-growth snapshot still validates; a malformed
      completeness or health object (out-of-range value, missing signal,
      unknown status) is rejected.
- [x] 6.3 Live browser check on the local dashboard: the workbench opens
      from a cluster, a possible, and a staged tile with correct scope; docs
      bars match the snapshot; the lens panel is scoped; the outline renders
      for a staged topic and empty-states elsewhere; the staged tile shows
      the compact indicator at focus and the full health block at expand;
      a propose on a blocked topic surfaces the refusal with its named
      blockers; zero page errors.
- [x] 6.4 Degraded-posture check on the served static image: the workbench
      action is offered with the gate capability off, `docs` and `lens`
      render, `outline` reports the missing `/source` route inline, and a
      pre-growth snapshot shows no health chrome.
- [x] 6.5 Brett's live pass on the real corpus: completeness bars are
      credible on documents he knows well; `READY_MIN_SCORE` (starting at
      0.60 per his 2026-07-25 ruling) is calibrated against fragments he
      has actually taken to proposal; the gate's first refusals are ones
      he agrees with; and the read-only posture holds — nothing in the
      corpus changed by the session.
      PASSED WITH FINDINGS 2026-07-31 (D10 combined pass, Brett sign-off
      2026-08-01): bars credible 5/5 across 0.4–0.74; refusals endorsed on
      two specimens (repo-selector remainder 0.4, consent-instrument 0.458,
      both judged accurate); read-only proven byte-identical. The
      taken-to-proposal should-pass cell is structurally untestable
      (partial promotion moves exactly those fragments out of staging) and
      yielded calibration findings F2/F3 instead — the 0.60 threshold is
      affirmed; the scorer's severity-blind open-question counting is the
      V2 work. Evidence: `add-workbench-integrated-editor-chat/evidence/d10/`
      (`a-65-*`, `session-findings.md`, `signoff-matrix.md`).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 4 and 5, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting exactly those two lines recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `849f026` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

**Why this reverses no finding.** C2 of `docs/archive-record-discrepancies.md` examined this record on 2026-08-22 and left it headerless, finding the `origin:`-nested `approved_by`/`approved_on: 2026-07-25` pair to record permission to author without a staging source, and task 6.5's Brett sign-off to be task acceptance. Both findings stand word for word and NEITHER is cited here. What C2 did not have is OQ-6's later ruling and the phase-b derivation, which make the archive act the citable record.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas associated with the `ideation-dashboard` capability — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and are slated for removal from the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
