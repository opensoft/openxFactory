# Tasks: add-project-merged-projection

## 1. Project-derived aggregates (D11)

- [x] 1.1 `snapshot_registry`: derive one aggregate per register project at
      index-composition time — id/name from the project, members = the
      project's repositories the registry resolves, default ref; additive
      beside hand-declared aggregates, hand-declared winning an id
      collision.
- [x] 1.2 The index document advertises derived aggregates exactly like
      declared ones (no schema growth — `aggregates[]` already carries
      them); the composed-snapshot route resolves a derived aggregate id.
- [x] 1.3 Selector wiring: with a project scoped, the roster offers
      "all repositories in <project>" mapped to the project's aggregate;
      clearing the scope removes it.

## 2. The merged view (D9, D10)

- [x] 2.1 Wheel/canvas view-side union: composed clusters group by topic
      tail (design D-f) into one merged tile listing per-repo
      contributions; non-composed snapshots render exactly as today through
      the same path.
- [x] 2.2 Composed-view verb gating: every gate-bearing affordance hides
      when `generation.composed_from` is present; the expanded tile mounts
      the one navigation verb "open in <repo>" (store key + reload — the
      ratified selector posture).
- [x] 2.3 Composed freshness header: `N repos · composed <date>`, with the
      per-member revisions from `composed_from` reachable on demand.

## 3. Verification

- [x] 3.1 Registry tests: derived aggregates (membership, ref, collision
      rule, unresolvable member degrade); composed route resolves a project
      aggregate.
- [x] 3.2 View-model tests: topic-tail union across repos, single-repo
      passthrough, badge content; verb gating on composed vs plain
      snapshots; jump key resolution.
- [x] 3.3 Live browser check: scope a multi-repo project, select "all
      repositories", the merged wheel renders with union tiles and repo
      badges, gate verbs absent, "open in <repo>" jumps; zero page errors.
      (Verified 2026-08-06, headless Chromium against a two-repo fixture
      serve with a derived `pilots` aggregate: the composed route served
      both members; the freshness header read "pilots · 2 repos · composed
      2026-07-12"; a composed document tile's expanded row was exactly
      "▤ read" + "⤴ open in alpha" — no gate verb anywhere; the jump landed
      on "alpha @ main"; zero console errors, page errors, and >=400
      responses.)
- [x] 3.4 First real merged-view session by Brett (select a project's
      all-repos view, navigate, jump into a member repo). — PASSED
      2026-08-07: Brett served the dashboard from the real checkout,
      selected a project's all-repos merged view, navigated to a tile,
      and verified the repository attribution at the tile annotation
      ("it shows that it says the correct repo"); no findings reported.
      Walked against the promoted scenarios (read-only composed view,
      per-repo badges, the "open in <repo>" jump).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4 (Brett Heap, in-session,
2026-08-23): a `Ratified by:` line that names a person and a date rather than
an approving OpenSpec change is substantively the record-citing form and takes
the record-citing prefix. This line was a live CRITICAL `ratified-provenance`
finding and the respell clears it. The record that justifies this line is the
same 2026-08-06 "ratify both and realize them in order" that justifies its
sibling `add-opendox-project-header`, quoted on this change's own line and in
the body of the same commit `8121f5f`, which realized THIS change and wrote
both citation lines; the exit-2 decision round (topic D9–D11) is carried as
decided. An append on a single-valued header is mechanically impossible —
`doc_health.corpus.STATUS_RE` swallows any trailing annotation — so this is an
in-place overwrite and an extension of Brett's 2026-08-10 append ruling, named
as one, and it is entered in `docs/archive-record-discrepancies.md`.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas associated with the `ideation-dashboard` capability — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and are slated for removal from the bundle at `contract-v4.0` (§ 5.7; cut PR #983). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
