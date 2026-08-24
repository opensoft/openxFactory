---
code_surface: codexFactory (a shared bullseye widget module lifted out of `views/lens.js`, the staging-workbench lens panel, a sibling workbench transport module, the `create-document` gate route + CLI parity verb, caps/fetcher threading through `mountStagingWorkbench`, tests), openxFactory (additive `gate-action-record` growth for the new action)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified: 2026-08-01 — record: the archive act, commit `ce0535d` "Archive add-workbench-bullseye-and-create (promote bullseye and create)", which applied this change's spec delta into `openspec/specs/ideation-dashboard/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. STATED PRECISELY: the register's C2 examined this record and left it headerless, finding its `origin:`-nested `approved_by`/`approved_on: 2026-07-25` pair to be permission to author and task 7.2's "Brett sign-off 2026-08-01" to be a live verification pass. Both findings stand word for word and neither is cited here. What C2 did not have is OQ-6's 2026-08-23 ruling and the phase-b derivation. The date is the archive folder's own 2026-08-01; the commit carries the 2026-07-31 authoring date. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".
---

# Proposal: add-workbench-bullseye-and-create

## Why

The staging workbench landed as the read-only foundation Brett asked for,
and dogfooding it the same day produced two findings — one a gap that is
already paid for, one the first write the surface actually needs.

FIRST, the workbench's `lens` tab shows only the flat matrix. That is not a
design choice; it is an unfinished renderer. The panel already calls the
SAME `buildLensModel` the main lens tab calls, and that call already returns
`rings`, `sectors`, and `dots` — the full match-count bullseye geometry of
D13 — computed at tile scope and then thrown away. A human working a topic
gets the tabular view of their scope and has to leave the workbench to see
the shape of it. Worse, the checked-keyword set they built to get there
resets the moment they visit `docs` or `outline` and come back, because the
panel rebuilds its `checked` set from the scope seed on every mount. The fix
is a renderer and a piece of session state, not new analysis.

SECOND, the workbench is where the human is standing when they decide a
document needs to exist. Today that decision means leaving the surface,
opening a terminal, and retyping — as `Topics:`, as `Repository context:`,
as an area path — everything the workbench already knows about the scope.
Every engine the create needs has been implemented and tested for weeks:
`authoring.create_scaffold` renders the controlled header block
(`Status`/`Kind`/`Summary`/`Topics`/`Repository context`/`Captured` plus the
`## Possible feats` seed) and writes it through
`boundary.OutputBoundary.create_document`, which is create-only — an
existing target refuses as `SOURCE_EDIT` and is never silently overwritten.
What is missing is the same last wire `add-lens-gate-verbs` just installed
for the lens plans: a gate route, a CLI parity verb, and a recorded
dispatch.

The creation gesture is not new thinking. It is the brainstorm
`ideation/brainstorm/lens-brainstorm-session-launch.md` (Brett, 2026-07-14,
using the deployed dashboard): "clicking the bullseye's center ring starts a
brainstorm session focused on the checked keyword set — a scaffolded
brainstorm doc with `Topics:` pre-filled from the checked keywords ... the
new doc's `Source:` cites the recipe ... a brainstorm born with
machine-checkable provenance about WHY it exists." That brainstorm named
three composed mechanisms; this change realizes exactly ONE of them — the
scaffolded document — from the workbench, and leaves the recipe-seeded
reference set and the scratch notebook where they are.

## What Changes

- RENDER the match-count bullseye in the workbench's `lens` panel, at tile
  scope, ABOVE the always-present flat matrix. The geometry is the geometry
  the scoped `buildLensModel` call already returns; the SVG renderer is
  lifted out of `views/lens.js` into a shared widget module both views
  consume, so there is exactly one bullseye renderer in the bundle and the
  two surfaces cannot drift. No new analysis, no new score, no new snapshot
  field — the `add-staging-workbench` constraint that the lens panel
  RE-SCOPES the existing keyword-lens derivation stands unchanged.
- PERSIST the workbench's checked-keyword selection across tab switches
  within one workbench session. Opening a different scope, or closing the
  workbench, starts a fresh selection from the scope seed.
- ADD one human-only executing gate verb, `create-document`
  (`POST /actions/gate/create-document` plus a CLI parity subcommand),
  enforced at the ROUTE so the workbench button, the CLI, and a direct
  request are gated identically. It drives the EXISTING tested authoring
  engine (`authoring.create_scaffold` → `boundary.create_document`) with NO
  engine change: the controlled header block, the create-only semantics, and
  the existing-target `SOURCE_EDIT` refusal are the engine's, surfaced
  verbatim at the route. Payload:
  `{area, title, summary, topics[], repository_context?, kind?, status?,
  possible_feats[]?, source?}`, with `repository_context` defaulting from the
  served snapshot's `repository` and `status` defaulting to `brainstorm` in
  EVERY area (Brett's 2026-07-25 ruling on design open question 1 — a
  created document's tie to a staging packet is its PLACEMENT in the packet's
  folder, not its status header; a supplied status is honoured only from the
  create-legal set, so nothing is born approved). Agent actors are refused
  and reported, like every gate action.
- RECORD every create as a gate-action record — the same recorded-dispatch
  discipline as propose, dispose, and the two lens verbs — carrying the
  created document's repo-relative path.
- OFFER the create affordance per tab, seeded from what that tab knows:
  - `docs` — a button on the pane's actions row. `Topics:` seeded from the
    tile's keywords, `Repository context:` from the snapshot's repository,
    `area` = the staging topic folder for a staged scope and
    `ideation/brainstorm/` for a cluster or possible scope, `Source:` citing
    the workbench scope (kind + id).
  - `lens` — a button on the forming-set pane AND an activation of ANY
    bullseye region — the matches-ALL centre zone or any ring SECTOR —
    opening the same dialog. `Topics:` seeded from the LIVE checked keyword
    set for the button and the centre zone, and from that sector's own
    matched subset of the checked set for a sector (Brett's 2026-07-25
    ruling on design open question 2, which extended the gesture from the
    centre ring to every sector); `Source:` citing the recipe
    (checked + pinned) at the snapshot's `source_revision`. This is the
    brainstorm's centre-ring gesture, realized and widened.
  - `outline` — staged scopes only: "new fragment in this topic",
    `area` = the staging topic folder. Hidden for cluster and possible
    scopes, which have no topic folder to write into.
- KEEP the gate-off posture honest: with the gate capability absent (the
  hosted read-only image), every affordance renders as a COPYABLE CLI
  DESCRIPTOR and never as a live button — the gate bar's established
  pattern, and the hosted-dashboard reality the brainstorm itself called
  for. Loopback-only, actor fail-closed, exactly as propose and the lens
  verbs.
- OPEN the created document in the read-only viewer on success, so the human
  lands on the thing they just made rather than on a path string.
- RESTATE the workbench's posture pill: `read-only` when the gate capability
  is off, gate-bearing when the capabilities grant gate. The pill is the
  surface's honest self-description and it can no longer be a constant.
- EXTEND (additive, no `contract_schema_version` bump)
  `contracts/schemas/gate-action-record.schema.yaml`: the `action` enum gains
  `create-document`, the artifact `kind` enum gains `document` (Brett's
  2026-07-25 ruling on design open question 4 — the created document is a
  first-class artifact kind, not an `other`), and the EXISTING optional
  `target.document` field is re-commented to cover the created document path
  (it is currently described as a document within a change). Every prior
  record stays valid. This is the same additive growth `add-lens-gate-verbs`
  made for its two verbs.

## Impact

- Affected specs: `ideation-dashboard` — three ADDED requirements (the
  workbench lens bullseye with persistent selection; the `create-document`
  gate verb; the workbench's per-tab creation affordances and seeding) and
  ONE MODIFIED requirement (`Staging workbench scoped view`, whose
  "read-only in every panel ... MUST write no document" clause is exactly
  what this change supersedes for the ONE gated verb). The
  `Human document authoring` requirement of `add-ideation-dashboard` and the
  `Interactivity boundary` requirement are NOT modified: the first already
  prescribes a human create action that scaffolds a header-compliant
  document into a chosen ideation area, and the second already grants humans
  create authority over corpus documents through the dashboard — this change
  adds a gated route to reach them, not a new authority.
- Delta stacking: the `ideation-dashboard` capability is NOT promoted
  (`add-ideation-dashboard` sits unarchived at 26/27), so this delta stacks
  on it alongside `add-propose-verb`, `add-wheel-action-verbs`,
  `add-staging-workbench`, and `add-lens-gate-verbs` — sequence the archives
  knowingly, and archive `add-staging-workbench` BEFORE this change, because
  the MODIFIED requirement restates a requirement that change ADDS.
- Affected schemas: `contracts/schemas/gate-action-record.schema.yaml`
  (additive `action` enum value + additive artifact `kind` enum value
  `document` + broadened `target.document` commentary + one per-action
  conditional requiring `target.document` and a `document`-kind artifact for
  the new action; no `schema_version` bump, no existing record invalidated).
  No new schema:
  the created document is an ordinary ideation corpus document under the
  header contract of `ideation/README.md`, and no `ideation-workbench`
  manifest is written (that is the OTHER workbench — design D5 of
  `add-staging-workbench` keeps the two senses apart).
- Affected code (codexFactory, realization): a new shared bullseye widget
  module consumed by `views/lens.js` and the workbench lens panel;
  `views/staging-workbench.js` (bullseye mount, persistent checked set,
  per-tab create affordances, posture pill) plus a NEW sibling transport
  module holding the POST (the view file is pinned free of `fetch(`,
  `"POST"`, and `XMLHttpRequest` by `test_staging_workbench.py`, and the
  set of files containing `fetch(` is pinned by `test_renderer.py`);
  `views/staging-workbench-model.js` (create-payload seeding — and it stays
  import-free for the node harness); `gate_routes.py` (the new verb beside
  propose and the lens verbs); `gate_console.py` (a `create-document` action
  constant and a record `target_id` derivation that accepts a
  document-only target); `cli.py` (the `gate create-document` parity verb
  beside the existing non-gated `create`); `app.js` (thread `caps` and the
  fetcher into `mountStagingWorkbench`, which today receives neither);
  tests.
- NOT in scope: the brainstorm's other two composed mechanisms — the
  recipe-seeded workbench reference set and the optional `xf-wb-*` scratch
  notebook in the same gesture — and the `lens-launch` action recording in
  the manifest history they imply; any EDIT or delete path (the workbench
  still never rewrites an existing document, and the engine refuses it);
  outline editing; doxBench's integrated AI editor/chat layer (then called
  Track C) and any generated content; any
  new snapshot field; a per-row "seed from this document" affordance (open
  question 3).
- Related but NOT covered: the three keyword-lens feat requests captured
  2026-07-14 stay `brainstorm`. `lens-ring-combination-explorer.md` (rings
  as a navigable lattice of keyword combinations) and
  `lens-keyword-search-and-adhoc.md` (rail typeahead + ad-hoc keywords) are
  untouched, and `lens-brainstorm-session-launch.md` is only PARTLY
  realized here — the centre-ring create slice, not the set or the notebook.
  All three remain live brainstorm material for a future
  `lens-enhancements` staging topic.
- Compatibility: additive record-schema growth only; the hosted static image
  gains no route and no live button (descriptors only), so the served plane
  needs no contract change; a pre-growth consumer reading a new record sees
  an unrecognized `action` value, which is why the growth is enumerated in
  the schema rather than left implicit.
