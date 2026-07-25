# Tasks: add-workbench-bullseye-and-create

## 1. Contract growth (openxFactory)

- [x] 1.1 `contracts/schemas/gate-action-record.schema.yaml`: the `action`
      enum gains `create-document`, with the additive posture stated in the
      schema's own commentary naming this change as the growth source (the
      `add-lens-gate-verbs` precedent, commit `0cf3864`) — every prior
      record stays valid, no `schema_version` bump.
- [x] 1.2 Same schema: broaden the EXISTING optional `target.document`
      commentary — it currently reads "document path within the change —
      e.g. the concept `edit-apply` targeted" and must also cover the
      repository-relative path a `create-document` action brought into
      existence. No type change, no new property.
- [x] 1.3 Same schema: one `allOf` conditional requiring
      `target: {required: [document]}` when `action == create-document`,
      mirroring the `propose` conditional's shape. Safe because no record
      has ever carried this action; worth having because a create record
      that does not name the created document audits nothing.
- [x] 1.4 Confirm the artifact `kind` enum is NOT grown in v1 (design D12,
      open question 4): the created document rides as an `other`-kind
      artifact with the relpath as `reference`, satisfying
      `artifacts.minItems: 1`.
- [x] 1.5 Validate: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`
      plus the delegated dashboard-contract validator; every packaged
      gate-action-record example (if any exist at realization) still
      validates unchanged.
- [ ] 1.6 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`) at the next additive bundle cut, per
      `docs/contract-versioning-policy.md`.

## 2. Shared bullseye widget (codexFactory)

- [x] 2.1 Lift the SVG bullseye renderer (`bullseye(model)` plus its `svg()`
      helper) out of `views/lens.js` into a NEW shared widget module
      consumed by BOTH the keyword-lens view and the workbench lens panel
      (design D1). Pure function of the model plus `GEOM`; `lens-model.js`
      geometry untouched.
- [x] 2.2 The widget takes an optional `onActivate` for the CENTRE-ring hit
      region (design D6): keyboard-reachable and focusable when supplied,
      wholly inert and byte-identically rendered when not — the main lens
      tab supplies none in this change.
- [x] 2.3 `views/lens.js` consumes the widget with NO signature change to
      its own callers; the existing lens tests stay green unmodified.

## 3. Workbench lens panel (codexFactory)

- [x] 3.1 `views/staging-workbench.js` lens panel mounts the shared widget
      ABOVE the always-present flat matrix, from the SAME scoped
      `buildLensModel` result it already computes (design D2/D3) — no new
      derivation, no new snapshot read, no recount of declared keyword
      counts.
- [x] 3.2 Move the checked-keyword set out of the panel's `draw()` closure
      into the workbench SHELL's scope-lifetime state (design D4): tab
      switches preserve it; opening a different scope or closing the
      workbench reseeds from `lensSeedKeywords`.
- [x] 3.3 Node-harness model tests for the seeding/reset rule; renderer
      tests that the bullseye and the matrix BOTH render, and that the
      matrix is never toggle-only.

## 4. `create-document` gate verb (codexFactory)

- [x] 4.1 `gate_routes.py`: `create-document` beside propose and the two
      lens verbs — same human-only enforcement, same loopback-only and
      actor-fail-closed posture, same refusal/record mechanics. Thin glue
      into `authoring.create_scaffold` with NO change to `authoring.py` or
      `boundary.py` (design D10).
- [x] 4.2 Payload validation/normalization at the route:
      `{area, title, summary, topics[], repository_context?, kind?,
      possible_feats[]?, source?}`, `repository_context` defaulting from the
      served snapshot's `repository`; the `Status:` default per open
      question 1's ruling (recommended: area-derived — `staged` under
      `ideation/staging/`, `brainstorm` otherwise).
- [x] 4.3 Gate-action record: action `create-document`, `target.document` =
      the created repo-relative path, one `other`-kind artifact referencing
      it. `gate_console.write_gate_action_record`'s `target_id` derivation
      must accept a document-only target — it currently reads
      `change_id or possible_id or target["topic_id"]` and would `KeyError`
      (design D10 consequence b).
- [x] 4.4 Refusal surface: an EXISTING target refuses as `SOURCE_EDIT`
      (create-only, engine-owned) with the existing document byte-identical;
      a missing required field refuses as an invalid body; an agent actor is
      rejected and reported; an unresolved actor and a non-loopback bind
      fail closed. Every refusal persists nothing.
- [x] 4.5 `cli.py gate create-document` parity subcommand beside the
      existing non-gated `create` (the propose/lens precedent) — same
      engine, same record, same refusals.

## 5. Workbench create affordances (codexFactory)

- [x] 5.1 Thread `caps` and a `fetcher` into `mountStagingWorkbench` from
      `app.js` — it receives NEITHER today (design D5 consequence);
      `app.js` already holds `caps` from the one capability probe.
- [x] 5.2 NEW sibling transport module holding the create POST, using the
      `const doFetch = fetcher || fetch` spelling. `staging-workbench.js`
      stays free of `fetch(`, `"POST"`, and `XMLHttpRequest`;
      `staging-workbench-model.js` stays import-free. Both are PINNED by
      `test_staging_workbench.py`, and the `fetch(`-bearing file set is
      pinned by `test_renderer.py` (design D5) — realize inside those pins,
      never by editing them.
- [x] 5.3 Create-payload seeding in the PURE model module (design D7): the
      per-tab area / topics / repository-context / source rules, including
      the recipe citation at the snapshot's `source_revision`. Unit-tested
      from the node harness for all three tabs and all three scope kinds.
- [x] 5.4 The `docs` tab affordance: a pane actions-row button opening the
      dialog with every seeded value editable.
- [x] 5.5 The `lens` tab affordances: a forming-set pane button AND the
      bullseye centre-ring gesture (per open question 2's ruling; recommended
      YES plus the button) opening the SAME dialog with the LIVE checked set
      as topics.
- [x] 5.6 The `outline` tab affordance: staged scopes only ("new fragment in
      this topic", area = the staging topic folder), HIDDEN — not disabled —
      for cluster and possible scopes.
- [x] 5.7 Gate-off posture (design D8): every affordance renders as a
      COPYABLE CLI DESCRIPTOR carrying the seeded values, never a live
      button, with no write reachable from the page.
- [x] 5.8 On success open the created document in the read-only viewer
      (the same `onOpenDoc` path the `docs` rows already use).
- [x] 5.9 The posture pill becomes capability-derived (design D9):
      `read-only` with the gate off — byte-identical to what the hosted
      image shows today — the gate-bearing posture with the actor when on.

## 6. Verification

- [x] 6.1 Route + CLI tests: a create lands the document and its record;
      the existing-target refusal leaves the prior document byte-identical;
      invalid bodies, agent path, unresolved actor, and non-loopback bind
      all refuse and persist nothing; the record validates against the
      grown schema.
- [x] 6.2 Full dashboard suite green, INCLUDING the two pinning tests
      unmodified (`test_staging_workbench.py`'s no-transport assertions,
      `test_renderer.py`'s `fetch(`-file-set pin) and the existing lens
      tests after the widget lift.
- [x] 6.3 Playwright smoke: open the workbench on a cluster, a possible,
      and a staged topic; the bullseye renders at scope with the matrix
      below; check keywords, switch tabs, return, and find the selection
      intact; create from `docs`, from the forming-set button, and from the
      centre ring; the created document opens in the viewer; the `outline`
      affordance is absent on cluster/possible scopes; zero page errors.
- [ ] 6.4 Degraded-posture check on the served static image: the pill reads
      `read-only`, every create affordance is a copyable CLI descriptor, no
      live button exists, and the bullseye + matrix still render from the
      snapshot alone.
- [x] 6.5 Boundary check: the boundary validator still reports no
      undeclared output path, and `create_document`'s deliberate
      allowlist-independence (design D10 consequence a) is asserted as
      intended behaviour rather than silently relied on.

## Realization notes (codexFactory PR #46, 2026-07-25)

Recorded deviations from the design, all additive and reasoned:

- D10's "no change to `authoring.py`" was relaxed: honouring Q1's
  area-derived `Status:` and the `Source:` citation WITHOUT post-editing
  the created file required `authoring.status_for_area()` plus `status`/
  `source` passthrough on `create_scaffold` and one optional `Source:`
  line in `render_scaffold` (emitted only when supplied — a sourceless
  scaffold is byte-identical to before). `CREATABLE_STATUSES =
  (brainstorm, staged, draft)` guards against a document born `ratified`.
  `boundary.py` untouched.
- The route payload accepts an optional `status` (validated against
  `CREATABLE_STATUSES`, defaulting area-derived) because the dialog keeps
  the field editable per Q1's recommendation.
- `topics` is required non-empty at the route (an empty `Topics:` header
  would violate the ideation header contract the engine's agent path
  already enforces).
- The "dialog" is an inline disclosure panel, not a nested modal (the
  workbench overlay owns document-level Escape; the panel stops
  propagation and closes itself).
- The workbench lens tab has no forming-set pane, so the lens button
  lives on a new one-line forming row stating what the checked set
  matches.
- Suite 479 passed (+34); Playwright smoke on a scratch checkout covered
  6.3's full script (screenshots in the session scratchpad); the smoke
  caught and fixed a real bug — the lens affordance initially mounted
  without the live checked set (empty `Topics:` seed), now
  regression-pinned.

## 7. Dogfood

- [ ] 7.1 Brett's rulings on open questions 1-4 recorded in this change
      before the seeding defaults and the artifact-kind decision are frozen
      at realization.
- [ ] 7.2 Brett's live pass: work a real staged topic in the workbench,
      read its scope in the bullseye, create the document the scope made him
      want, and find it where the dialog said — with a `Source:` line that
      actually re-derives the membership that motivated it.
