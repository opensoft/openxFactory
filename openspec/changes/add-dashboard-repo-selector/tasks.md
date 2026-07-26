# Tasks: add-dashboard-repo-selector

## 1. Contract (openxFactory)

- [ ] 1.1 NEW `contracts/schemas/ideation-dashboard-snapshot-index.schema.yaml`
      (`kind: ideation-dashboard-snapshot-index`, `schema_version`), the thin
      locator of design D3: one entry per (repository, ref) carrying
      `repository`, `ref`, the snapshot location, `source_revision`, and the
      generated-at stamp derived from that revision (never the wall clock,
      matching the snapshot schema's determinism commentary). Additive/
      forward-compatible posture in the file's own commentary (consumers
      ignore unknown properties, no `additionalProperties: false`), and an
      explicit statement of what the index MUST NOT carry — no document,
      cluster, possible, keyword, or funnel data. The
      `ideation-dashboard-snapshot` schema is NOT grown (D3).
- [ ] 1.2 Validator-side rule the shape cannot express, stated in the schema
      commentary and enforced in
      `scripts/validate-ideation-dashboard-contracts.py`: every
      (repository, ref) pair is UNIQUE within one index.
- [ ] 1.3 Register the new schema in that validator's `SCHEMA_FILENAMES` and
      `KIND_TO_SCHEMA` (the `gate-intent.schema.yaml` precedent, tasks
      2.1-2.3 of `add-ideation-intent-plane`), so the packaged-example sweep
      and the repo-tree scan pick it up automatically.
- [ ] 1.4 Packaged examples under `examples/ideation-dashboard/`: a valid
      index spanning at least three repositories (one of them a sparse
      install repo) at `ref: main`, and negatives under `negative/` —
      `snapshot-index-duplicate-repo-ref` (the uniqueness rule) and
      `snapshot-index-carries-projection-data` (the locator-not-projection
      rule) — each naming the rule it violates.
- [ ] 1.5 Validate: `OPENSPEC_TELEMETRY=0 openspec validate
      add-dashboard-repo-selector --strict` and `--all --strict`, plus
      `python3 scripts/validate-ideation-dashboard-contracts.py . --strict`
      green (0 errors, 0 warnings) with the new examples included.
- [ ] 1.6 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`, README contract index) at the next additive
      bundle cut, per `docs/contract-versioning-policy.md`
      (registration-at-realization precedent).

## 2. Snapshot source seam and registry (codexFactory)

- [ ] 2.1 Address snapshots by the (repository, ref) PAIR throughout the
      serving layer, with `ref` defaulting to `main` when a caller names
      none (design D4). ONE registry keyed by the pair; every renderer
      route, both refresh bindings, and the index reader go through it —
      no second path convention anywhere.
- [ ] 2.2 Per-entry source confinement: reading a document through a
      (repository, ref) entry MUST NOT escape that entry's own root
      (multi-root confinement, extending the existing single-root check).
- [ ] 2.3 Refuse publication of any non-`main` snapshot and refuse its
      entry into a published index — the session-local rule that keeps
      `add-workbench-branch-sessions` honest before it exists.
- [ ] 2.4 Fix the `serve.py` relative-import quirk (design D12) so POST
      routes no longer require module invocation; keep the module-invocation
      path working so the documented live-serve command does not break.

## 3. Selector, freshness, and runtime fetch (codexFactory)

- [ ] 3.1 Nightly/publication generator iterates the project register,
      emitting one snapshot per registered repository plus the index (the
      generator already takes `--repository` + `--project-register` and
      needed zero changes in the 2026-07-25 domain drive — this is the
      loop, not a redesign).
- [ ] 3.2 Repository selector in the renderer bundle, roster from the index
      (register-derived), switching the active snapshot; sparse stations
      render explicit empty states naming what is absent (design D10); an
      indexed-but-unregistered repository renders ungrouped (D9).
- [ ] 3.3 Serving-side runtime fetch of the index + active snapshot into the
      registry from the declared data source (design D5 — the fetch is
      server-side so the bundle keeps its grep-proven same-origin
      boundary; topology, in-process versus init container plus periodic
      sidecar, is realization's call). The data source is CONFIGURATION, so
      open question 1's ratification changes a fetcher and no contract.
- [ ] 3.4 Baked snapshot demoted to first-boot/offline fallback with a
      stale banner naming its generated-at (design D6); the degradation is
      never silent, and the fallback path is exercised by a test that makes
      the source unreachable.
- [ ] 3.5 Freshness header — `repo @ ref · source_revision short SHA ·
      generated-at` — on every plane (design D11).
- [ ] 3.6 Refresh affordance, two bindings (design D7): served = re-fetch
      index + active snapshot then re-render (read-only, derived cache
      only); local = POST regenerate against the served checkout then
      re-render, loopback-only, no restart. A failed refresh leaves the
      previously rendered snapshot in place and reports inline. Posture of
      the local route per open question 3's ruling (recommendation:
      ungated, stated explicitly rather than inherited).
- [ ] 3.7 Renderer-bundle pins respected, never edited:
      `tests/ideation-dashboard/test_renderer.py` bans `https?://` and
      every network primitive bundle-wide and pins each `fetch(` to a
      same-origin backend route with per-file counts — the new fetches are
      same-origin by construction (3.3), and the pin's file set + counts are
      updated only as the arithmetic of new same-origin routes requires.

## 4. Aggregation wiring (xFactory)

- [ ] 4.1 Project-register instance grows the repositories to be offered
      (the selector's roster; adding a repository stays a register edit plus
      a lane run — no code and no image change, design D9).
- [ ] 4.2 Declare the published data source's layout under
      `health/ideation-dashboard/` — per-repository snapshot filenames keyed
      by (repository, ref) plus the index — and publish both from the lane
      (design D2, pending open question 1's ratification).
- [ ] 4.3 `workflow_dispatch` on the nightly snapshot workflow (design D8),
      changing nothing else about the lane: same generator, same artifacts,
      same commit posture as a scheduled run.
- [ ] 4.4 If open question 1 ratifies raw files: provision the read-only,
      narrowly-scoped fetch credential for the serving side and record it
      through the ordinary credential-contracts path — never a raw
      credential in any repository, and never reachable from the browser.

## 5. Verification

- [ ] 5.1 Registry + seam tests: a ref-less request resolves to `main`; two
      refs of one repository serve independently; confinement holds per
      entry; a non-`main` publication attempt refuses.
- [ ] 5.2 Index tests: a new index entry makes a repository selectable with
      no bundle change; an unfetchable entry reports that repository
      unavailable while the active view keeps rendering; the duplicate-pair
      and projection-data negatives fail validation.
- [ ] 5.3 Fetch/fallback tests: reachable source renders fetched data with
      the freshness header; unreachable source renders the baked fallback
      WITH the stale banner; a snapshot published after the image was built
      is reflected with no rebuild.
- [ ] 5.4 Refresh tests: served refresh re-fetches and writes only the
      derived cache; local regenerate re-runs the generator with no server
      restart and writes only the derived snapshot; every build/rollout/
      publication path from the surface refuses; a failed refresh preserves
      the prior view.
- [ ] 5.5 Full dashboard suite green (baseline 485 + 5 skipped as of
      codexFactory PR #46), including the renderer pins unmodified beyond
      3.7's arithmetic.
- [ ] 5.6 Playwright smoke (CI has no node — this is the pre-merge gate):
      select each registered repository including a sparse one; confirm the
      freshness header against the served snapshot's `source_revision`;
      click refresh and see a newly published document appear; kill the
      data source and confirm the fallback plus stale banner; local
      regenerate after a commit shows the new document with no restart;
      zero page errors throughout.
- [ ] 5.7 Boundary check: the boundary validator reports no undeclared
      output path (the derived snapshot cache and the regenerated snapshot
      are declared derived artifacts), and the served plane exercises no
      write authority.

## 6. Dogfood

- [ ] 6.1 Brett's rulings on the three open questions recorded in this
      change before realization freezes them: (1) the data source, (2) the
      index polling cadence, (3) whether the local regenerate is gated.
- [ ] 6.2 Brett's live pass: reproduce the motivating incident deliberately
      — land a document on `main`, dispatch the publication lane, click
      refresh on the hosted dashboard, and find the document — with no
      image rebake anywhere in the sequence; then drive the selector across
      Medx/Adx/Ledgerx and confirm the sparse wheels read as honest rather
      than broken.
