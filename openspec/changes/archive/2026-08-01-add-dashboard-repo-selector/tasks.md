# Tasks: add-dashboard-repo-selector

## 1. Contract (openxFactory)

- [x] 1.1 NEW `contracts/schemas/ideation-dashboard-snapshot-index.schema.yaml`
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
- [x] 1.2 Validator-side rule the shape cannot express, stated in the schema
      commentary and enforced in
      `scripts/validate-ideation-dashboard-contracts.py`: every
      (repository, ref) pair is UNIQUE within one index.
- [x] 1.3 Register the new schema in that validator's `SCHEMA_FILENAMES` and
      `KIND_TO_SCHEMA` (the `gate-intent.schema.yaml` precedent, tasks
      2.1-2.3 of `add-ideation-intent-plane`), so the packaged-example sweep
      and the repo-tree scan pick it up automatically.
- [x] 1.4 Packaged examples under `examples/ideation-dashboard/`: a valid
      index spanning at least three repositories (one of them a sparse
      install repo) at `ref: main`, and negatives under `negative/` —
      `snapshot-index-duplicate-repo-ref` (the uniqueness rule) and
      `snapshot-index-carries-projection-data` (the locator-not-projection
      rule) — each naming the rule it violates.
- [x] 1.5 Validate: `OPENSPEC_TELEMETRY=0 openspec validate
      add-dashboard-repo-selector --strict` and `--all --strict`, plus
      `python3 scripts/validate-ideation-dashboard-contracts.py . --strict`
      green (0 errors, 0 warnings) with the new examples included.
- [x] 1.6 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`, README contract index) at the next additive
      bundle cut, per `docs/contract-versioning-policy.md`
      (registration-at-realization precedent).
      Realized at contract-v1.26 (2026-07-30): the snapshot-index manifest
      entry (per-file sha256), the contract-v1.26 CHANGELOG registration,
      and the new README contract index row landed through PR #43,
      published merge `4efa9d0e2c7d21f2abf3cd7e55f41b74afed97f9` (tree
      byte-identical to the reviewed candidate). Annotated tag object
      `bf20357d8452e7e02ff15811f1912ec691d01cfb` dereferences to that merge;
      verify-promotion and verify-tag pass. Gates at the merge SHA:
      verify-commit over the 179-entry release inventory, manifest digests
      107/107, strict family validator 0/0, OpenSpec --all --strict 57/57.

## 2. Snapshot source seam and registry (codexFactory)

- [x] 2.1 Address snapshots by the (repository, ref) PAIR throughout the
      serving layer, with `ref` defaulting to `main` when a caller names
      none (design D4). ONE registry keyed by the pair; every renderer
      route, both refresh bindings, and the index reader go through it —
      no second path convention anywhere.
- [x] 2.2 Per-entry source confinement: reading a document through a
      (repository, ref) entry MUST NOT escape that entry's own root
      (multi-root confinement, extending the existing single-root check).
- [x] 2.3 Refuse publication of any non-`main` snapshot and refuse its
      entry into a published index — the session-local rule that keeps
      `add-workbench-branch-sessions` honest before it exists.
- [x] 2.4 Fix the `serve.py` relative-import quirk (design D12) so POST
      routes no longer require module invocation; keep the module-invocation
      path working so the documented live-serve command does not break.

## 3. Selector, freshness, and runtime fetch (codexFactory)

- [x] 3.1 Nightly/publication generator iterates the project register,
      emitting one snapshot per registered repository plus the index (the
      generator already takes `--repository` + `--project-register` and
      needed zero changes in the 2026-07-25 domain drive — this is the
      loop, not a redesign).
- [x] 3.2 Repository selector in the renderer bundle, roster from the index
      (register-derived), switching the active snapshot; sparse stations
      render explicit empty states naming what is absent (design D10); an
      indexed-but-unregistered repository renders ungrouped (D9).
- [x] 3.3 Serving-side runtime fetch of the index + active snapshot into the
      registry from the declared data source (design D5 — the fetch is
      server-side so the bundle keeps its grep-proven same-origin
      boundary; topology, in-process versus init container plus periodic
      sidecar, is realization's call). The data source is CONFIGURATION, so
      open question 1's ratification changes a fetcher and no contract.
      RULED 2026-07-26: the hosted binding is the aggregation repo's RAW
      FILES (raw GitHub URLs for `health/ideation-dashboard/`), with the
      read-only token supplied as deploy-time config (an environment/secret
      NAME) — never a credential in a repository and never reachable from the
      browser.
- [x] 3.4 Baked snapshot demoted to first-boot/offline fallback with a
      stale banner naming its generated-at (design D6); the degradation is
      never silent, and the fallback path is exercised by a test that makes
      the source unreachable.
- [x] 3.5 Freshness header — `repo @ ref · source_revision short SHA ·
      generated-at` — on every plane (design D11).
- [x] 3.6 Refresh affordance, two bindings (design D7): served = re-fetch
      index + active snapshot then re-render (read-only, derived cache
      only); local = POST regenerate against the served checkout then
      re-render, loopback-only, no restart. A failed refresh leaves the
      previously rendered snapshot in place and reports inline. Posture of
      the local route RULED 2026-07-26: UNGATED and loopback-only (the
      `open-workbench` precedent), stated explicitly at the requirement and
      at the route rather than inherited.
- [x] 3.7 Renderer-bundle pins respected, never edited:
      `tests/ideation-dashboard/test_renderer.py` bans `https?://` and
      every network primitive bundle-wide and pins each `fetch(` to a
      same-origin backend route with per-file counts — the new fetches are
      same-origin by construction (3.3), and the pin's file set + counts are
      updated only as the arithmetic of new same-origin routes requires.
- [x] 3.8 PASSIVE FRESHNESS HINT (RULED 2026-07-26, open question 2): the
      page polls the THIN index in the background (~5 minutes) and shows a
      "newer data available" badge when the index's freshness beats the
      loaded snapshot's; the viewer clicks refresh and the page NEVER
      auto-reloads. The serving side answers those polls from a short-lived
      index peek, so N viewers cost the data source at most one index read
      per cache window. Additive to the freshness header (3.5) — the header
      states what IS rendered, the badge advertises what EXISTS.

## 4. Aggregation wiring (xFactory)

- [x] 4.1 Project-register instance grows the repositories to be offered
      (the selector's roster; adding a repository stays a register edit plus
      a lane run — no code and no image change, design D9).
      Realized in xFactory's `project-register.yaml`; the live hosted selector
      offered all 11 registered repositories during the 2026-07-29 dogfood,
      including the sparse stations.
- [x] 4.2 Declare the published data source's layout under
      `health/ideation-dashboard/` — per-repository snapshot filenames keyed
      by (repository, ref) plus the index — and publish both from the lane
      (design D2, RULED 2026-07-26: those raw files ARE the hosted data
      source, so this layout is the fetcher's contract).
      Realized and documented in
      `health/ideation-dashboard/README.md`; the live provenance validator
      fetched all 11 indexed snapshots from that layout successfully.
- [x] 4.3 `workflow_dispatch` on the nightly snapshot workflow (design D8),
      changing nothing else about the lane: same generator, same artifacts,
      same commit posture as a scheduled run.
      Realized in `.github/workflows/doc-health-nightly.yml` and exercised by
      workflow run `30503605213`.
- [x] 4.4 Open question 1 RULED raw files (2026-07-26): provision the
      read-only, narrowly-scoped fetch credential for the serving side and
      record it through the ordinary credential-contracts path — never a raw
      credential in any repository, and never reachable from the browser. The
      serving side takes the token from a named environment variable only
      (`--data-source-token-env`), so this task is a deployment/credential
      action, not a code change.
      Realized through the deployed Key Vault/CSI reference-only credential
      path; validation exercised the hosted fetch without exposing the secret
      value to the browser, repository, or evidence log.

## 5. Verification

- [x] 5.1 Registry + seam tests: a ref-less request resolves to `main`; two
      refs of one repository serve independently; confinement holds per
      entry; a non-`main` publication attempt refuses.
- [x] 5.2 Index tests: a new index entry makes a repository selectable with
      no bundle change; an unfetchable entry reports that repository
      unavailable while the active view keeps rendering; the duplicate-pair
      and projection-data negatives fail validation.
- [x] 5.3 Fetch/fallback tests: reachable source renders fetched data with
      the freshness header; unreachable source renders the baked fallback
      WITH the stale banner; a snapshot published after the image was built
      is reflected with no rebuild.
- [x] 5.4 Refresh tests: served refresh re-fetches and writes only the
      derived cache; local regenerate re-runs the generator with no server
      restart and writes only the derived snapshot; every build/rollout/
      publication path from the surface refuses; a failed refresh preserves
      the prior view.
- [x] 5.5 Full dashboard suite green (baseline 485 + 5 skipped as of
      codexFactory PR #46), including the renderer pins unmodified beyond
      3.7's arithmetic.
- [x] 5.6 Playwright smoke (CI has no node — this is the pre-merge gate):
      select each registered repository including a sparse one; confirm the
      freshness header against the served snapshot's `source_revision`;
      click refresh and see a newly published document appear; kill the
      data source and confirm the fallback plus stale banner; local
      regenerate after a commit shows the new document with no restart;
      zero page errors throughout.
- [x] 5.7 Boundary check: the boundary validator reports no undeclared
      output path (the derived snapshot cache and the regenerated snapshot
      are declared derived artifacts), and the served plane exercises no
      write authority.

## 6. Dogfood

- [x] 6.1 Brett's rulings on the three open questions recorded in this
      change before realization freezes them: (1) the data source, (2) the
      index polling cadence, (3) whether the local regenerate is gated.
      RULED 2026-07-26 (all three, binding) and recorded in design.md's Open
      Questions plus D2/D7 and in tasks 3.3/3.6/3.8/4.4 above: (1)
      aggregation-repo RAW FILES with a deploy-time read-only token; (2) a
      PASSIVE "newer data available" badge on a ~5-minute index poll, never
      an auto-reload; (3) the local regenerate is UNGATED and loopback-only.
- [x] 6.2 Brett's live pass: reproduce the motivating incident deliberately
      — land a document on `main`, dispatch the publication lane, click
      refresh on the hosted dashboard, and find the document — with no
      image rebake anywhere in the sequence; then drive the selector across
      Medx/Adx/Ledgerx and confirm the sparse wheels read as honest rather
      than broken.
      Passed 2026-07-29/30: openxFactory PR #40 landed
      `docs/doxbench-runtime-refresh-dogfood.md` as `f5c5a8b`; the publication
      source revision was the later descendant `3e01ee8`. xFactory workflow
      run `30503605213` published all 11 repositories, publication PR #47
      head `4dcd9c4` merged as `ffcb943`, and the hosted `refetch` refresh
      returned `ok: true`. The refreshed snapshot-backed document view
      contained the marker, while the deployment retained image digest
      `sha256:b602380e6f07ddc7d4eff7a7e1680fc37082e274f2cd947085898329ecdb02c3`
      and pod UID `c99d5139-218a-4e30-b320-8a97c480e0ff` (created
      `2026-07-30T00:10:51Z`, zero restarts). The selector had already passed
      across all 11 repositories, including Medx/Adx/Ledgerx and sparse
      repositories with explicit honest empty states. The separately governed
      `/source` pass-through remains bound to the served checkout and does not
      expose this post-image file; that known plane boundary is not used as
      evidence for this task. The governing distinction is preserved in
      `docs/doxbench-runtime-refresh-dogfood-erratum.md` while the original
      dogfood evidence record remains immutable.
      DELIBERATE HUMAN OBSERVATION COMPLETED 2026-07-31/08-01 (the final
      dogfood step this note left open; D10 combined pass Step C, Brett
      sign-off PASS 2026-08-01): a distinct marker
      (`docs/d10-hosted-refresh-marker.md`, PR #46 → `ae3f9c7`) landed on
      `main`, pointer-sync `2bf51fd` + dispatched lane run `30672928437`
      published it (rolling PR xFactory#65), Brett clicked refresh on the
      hosted dashboard and FOUND the marker, and the image digest was
      byte-identical before and after
      (`sha256:b602380e…`, pod spot-reschedule within the same ReplicaSet
      noted). Selector sweep verbatim: "Medx populated fine, Adx and
      Ledgerx sparse but honest, nothing looked broken." Evidence:
      `add-workbench-integrated-editor-chat/evidence/d10/c-62-*`.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4's RULED extension of
2026-08-23 (Brett Heap, in-session), which widens the class to the sixteen
lines whose named change id is the DOCUMENT'S OWN. A change is not its own
approving change, and such a line passed `fam_ratified_provenance` only by
self-reference. This one emitted NO finding, so the respell is corrective
rather than a discharge and clears nothing from the census. The record that
justifies this line is Brett's approval of 2026-07-29 named on the line,
recorded by commit `c14cecc` of that same 2026-07-29, "Record ratification of
add-dashboard-repo-selector", on the three binding rulings of 2026-07-26 the
line quotes. An append on a single-valued header is mechanically impossible —
`doc_health.corpus.STATUS_RE` swallows any trailing annotation — so this is an
in-place overwrite and an extension of Brett's 2026-08-10 append ruling, named
as one, and it is entered in `docs/archive-record-discrepancies.md`.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas this delta names — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and LEAVE the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
