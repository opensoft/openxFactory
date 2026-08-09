# Tasks: add-project-visible-set

## 1. The visible-set derivation

- [x] 1.1 `composed-model.js`: `visibleSnapshot(snapshot, visible, mode)` —
      one uniform filter over every composed collection (each item carries
      `repository` by construction), `itemTail` covering namespaced ids and
      the unnamespaced keys (`staging_id`, `keyword`), intersection as a
      pure predicate (present in EVERY visible repository), trimmed
      `composed_from`, non-composed passthrough.
- [x] 1.2 `repo-selector-model.js`: `visibleRepositories(project, stored)`
      resolved against current membership (default all; stale set falls back;
      deliberate empty stays empty) and `toggleVisibility` preserving member
      order.
- [x] 1.3 Per-project view state (`storedViewState` / `storeViewState` /
      `projectViewState`) keyed by project, defensive against malformed
      storage.

## 2. The control

- [x] 2.1 The view row: union/intersection toggle (inert below two visible),
      the visible count, `all` / `none`. Degrades to the merged-view-
      unavailable note where the project has no derived aggregate.
- [x] 2.2 Member rows: the eyeball becomes the toggle where the project can
      compose (disabled when that member publishes no snapshot); the name
      solos; the trash and the pending badges keep their D15/D16/D18
      behaviour.
- [x] 2.3 The filter label states the visible count against the total.
- [x] 2.4 `app.js`: narrow the composed snapshot to the visible set BEFORE
      the cluster union, and render the freshness header from the narrowed
      snapshot.

## 3. Verification

- [x] 3.1 Node model tests: union/intersection/none/solo/ghost-id, tallies
      after narrow-then-union, trimmed members, passthrough, tails.
- [x] 3.2 Node model tests for the visible-set resolution and toggles.
- [x] 3.3 Live browser check on the real multi-repository plane: ticking a
      repository off narrows the view and the header count; the mode toggle
      switches union/intersection; `none` empties honestly; `all` restores;
      soloing serves the interactive single view.
      (Verified 2026-08-07 against the 14-repository local plane, project
      `domains`: switching to it landed on the merged view (5 of 5, 230
      documents, header "domains · 5 repos"); hiding one gave 4 of 5 / 200
      documents / "4 repos"; intersection over those four gave 8; `none`
      gave 0 of 5 and an honestly empty view; `all` restored; clicking
      AdxFactory's name soloed to 1 of 5, served ITS OWN snapshot —
      freshness header "AdxFactory @ main · 949e7d486094" — with the mode
      toggle inert. Zero console errors, page errors, and >=400 responses.)
- [x] 3.4 Brett's first real comparison session (two factories, shared mode).
      (Ruled satisfied by Brett 2026-08-09, on the Playwright acceptance
      session he commissioned against the live 13-repository local plane,
      project `domains`: hiding AdxFactory then LedgerxFactory tracked the
      header 3 then 2 repos with no reload; union over MedxFactory +
      codexFactory read 113 documents; SHARED collapsed to 4 documents /
      1 cluster — `docs/document-catalog-adoption.md` and
      `ideation/README.md`, confirmed by name in the doc list, once per
      carrier; `all` + union restored 212. OpsxFactory's row stated
      "(no published snapshot)" with its eyeball disabled. Zero console
      errors, page errors, and >=400 responses. Play-by-play report:
      "doxBench acceptance run", 2026-08-09.)

## 4. Canon correction (D18, already shipped)

- [x] 4.1 MODIFIED "Project membership editing is a recorded commission":
      the queueing rule the code has shipped since 2026-08-07, whose
      amendment landed in the `add-opendox-project-header` packet after that
      change had archived and promoted its requirements.

## 5. The shared threshold (topic D20, Brett's 2026-08-07 refinement)

- [x] 5.1 The second mode keeps identities carried by TWO OR MORE visible
      repositories rather than by every one of them, and is renamed SHARED
      throughout (constant, label, tooltip, spec, runbook) so the code stops
      claiming a set operation it no longer performs.
- [x] 5.2 Tests: a purpose-built three-member fixture separating the
      carried-by-all, carried-by-two, and single-carrier cases; the pair
      narrowing still sharpest.
- [x] 5.3 Live browser check at three or more visible repositories.
      (Verified 2026-08-07 on the 14-repository plane, project `domains`:
      union over all five gave 230 documents / 297 clusters; SHARED over
      the same five gave 15 documents and 8 CLUSTER TOPICS — where the
      strict all-of-them rule had shown 0 clusters, which is the finding
      D20 exists to surface; narrowing to a pair gave 4 documents. Zero
      console errors, page errors, and >=400 responses.)
