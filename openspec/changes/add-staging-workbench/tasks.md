# Tasks: add-staging-workbench

## 1. Contract / schema growth (openxFactory)

- [ ] 1.1 Extend `contracts/schemas/ideation-dashboard-snapshot.schema.yaml`:
      the `document` `$def` grows an OPTIONAL `completeness` object —
      `score` (number, 0..1) plus the five named signals `structure`,
      `length`, `open_markers`, `keyword_coverage`, `link_degree`, each a
      normalized 0..1 value carrying the raw count that produced it.
- [ ] 1.2 Pin the contract's invariants in the schema's own commentary: the
      definition of each signal, `open_markers` as an INVERSE signal, the
      fixed weights and fixed decimal precision as v1 constants (a tunable
      configuration is a successor, design D2), deterministic and
      reproducible from the pinned tree with NO model call (design D1), and
      informational-only — never an input to the readiness recommendation
      gate, a doc-health finding, or any console guard.
- [ ] 1.3 Keep the additive posture explicit: no `contract_schema_version`
      bump, no `additionalProperties: false`, header note naming this change
      as the growth source, and completeness OPTIONAL so a pre-growth
      snapshot stays valid (design D7).
- [ ] 1.4 Confirm no aggregate score is added to `cluster`, `possible`, or
      `staged_topic` (design D3), and that `ideation-workbench.schema.yaml`
      is untouched (design D5).
- [ ] 1.5 Validate: the delegated dashboard-contract validator
      (`scripts/validate-ideation-dashboard-contracts.py`) plus
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`; every
      packaged snapshot example still validates unchanged.
- [ ] 1.6 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`) at the next additive bundle cut, per
      `docs/contract-versioning-policy.md`.

## 2. Generator scoring (codexFactory — Speckit-side realization)

- [ ] 2.1 New deterministic scoring module beside `generator.py`: the five
      signal functions, the fixed weight constants, the fixed-precision
      rounding, and the normalized+raw output shape. Pure functions over
      already-loaded document text plus the snapshot-derived edge data — no
      I/O, no clock, no model call.
- [ ] 2.2 `structure`: expected structural elements per `Kind:` with the
      common fallback (H1 title, governance header block, at least one
      section); the expected sets are declared in ONE table, not scattered
      through the checks.
- [ ] 2.3 `length` and `open_markers`: body word count against the fixed
      saturation threshold; marker scan (`TODO`, `TBD`, `FIXME`, `??`, open-
      question headings) against the fixed saturation count, subtracted from
      1. Single pass over the already-loaded text (design: generator cost).
- [ ] 2.4 `keyword_coverage` and `link_degree`: declared `Topics:` subjects
      resolving against the snapshot's keyword vocabulary; edge degree from
      cluster document edges plus `destinations` (staged topics, changes,
      capabilities), normalized against the fixed saturation degree. Both
      read the generator's own derived maps — no second scan.
- [ ] 2.5 `generator.py` `_document_entry` emits `completeness`; excluded
      documents (`_document_exclusion_reason`) carry none, and no dangling
      score survives an exclusion.
- [ ] 2.6 Determinism tests: byte-identity across two runs on one fixture
      tree; a fixture doc gaining sections and edges scores strictly higher;
      cross-platform stability of the rounded values.
- [ ] 2.7 Non-gating test: no doc-health family, readiness path, or console
      guard reads the field (assert by absence — the scoring module has no
      importer outside the generator and its tests).

## 3. Staging workbench view (codexFactory — Speckit-side realization)

- [ ] 3.1 Pure model module: `workbenchScope(snapshot, kind, id)` deriving
      the tile's document set per kind (cluster edges; possible cited
      evidence + separately labelled inherited claiming-cluster members;
      staged-topic folder documents + documents declaring that destination),
      with stable ordering. Unit-tested from the node harness like
      `wheel-model.js`.
- [ ] 3.2 The full-screen scoped view shell with the `docs` / `lens` /
      `outline` tab set, opened at one scope and closed back to the wheel.
- [ ] 3.3 `docs` panel: one row per document with its completeness bar and
      the named signals with raw counts, rendered VERBATIM from the
      snapshot; missing completeness renders as no bar, never as zero
      (design D7).
- [ ] 3.4 `lens` panel: re-scope the EXISTING keyword-lens seed and
      edge/degree derivation to the tile's keywords/documents — reuse
      `lens-model.js` / the wheel's degree derivation, add no new
      computation and no new snapshot read.
- [ ] 3.5 `outline` panel: render the scope's outline material read-only
      through the `/source` pass-through (the viewer's route, as the
      `landed` verb does); explicit empty state when there is no outline;
      inline degraded message when the route is absent.
- [ ] 3.6 Read-only enforcement: no panel has a write path — assert against
      the boundary checker (`boundary.py`) that the view declares no output
      path, and keep the view free of any POST.

## 4. Wheel tile action (codexFactory — Speckit-side realization)

- [ ] 4.1 `views/wheel-model.js` `WHEEL_ACTIONS`: an `open workbench` row on
      `clusters`, `possibles`, and `staged` with NO `visible` predicate (a
      read-only verb, design D6); `documents` / `active` / `archived` gain
      nothing.
- [ ] 4.2 `views/wheel.js` `ACTION_MOUNTERS`: one mounter reusing the
      existing read-only nav-button chrome, wired through the app shell's
      nav callbacks (`app.js`), disabled where no nav callback is supplied.
- [ ] 4.3 Pure-model tests for `actionsFor` across all six wheels: the row
      appears on exactly the three topic-bearing wheels, with the gate
      capability both on and off.

## 5. Verification

- [ ] 5.1 Generator + view tests green, including the nightly lane's runtime
      after scoring is added (no regression in lane duration).
- [ ] 5.2 Schema conformance: a snapshot with completeness validates; a
      pre-growth snapshot still validates; a malformed completeness object
      (out-of-range value, missing signal) is rejected.
- [ ] 5.3 Live browser check on the local dashboard: the workbench opens
      from a cluster, a possible, and a staged tile with correct scope; docs
      bars match the snapshot; the lens panel is scoped; the outline renders
      for a staged topic and empty-states elsewhere; zero page errors.
- [ ] 5.4 Degraded-posture check on the served static image: the workbench
      action is offered with the gate capability off, `docs` and `lens`
      render, and `outline` reports the missing `/source` route inline.
- [ ] 5.5 Brett's live pass on the real corpus: completeness bars are
      credible on documents he knows well (the calibration input for open
      question 1), and the read-only posture holds — nothing in the corpus
      changed by the session.
