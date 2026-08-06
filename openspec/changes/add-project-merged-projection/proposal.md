---
code_surface: openxFactory (dashboard runtime — snapshot_registry project-aggregate derivation, selector/app wiring for the all-repos selection, wheel/canvas view-side cluster union, composed-view read-only plane + open-in-repo jump, composed freshness header; tests)
target_release: none
Status: draft
---

# Proposal: add-project-merged-projection

## Why

Brett's D1 ruling on `dashboard-project-scoping` (2026-08-06): "all repos
in a project" is a TRUE MERGED VIEW — one wheel, funnel, and count set
spanning every member repository. Exit 1 (`add-project-scoped-selection`,
realized) deliberately shipped the filtered interim: a project narrows the
selector, one snapshot at a time.

The heavy machinery already exists and is ratified: the snapshot registry
composes an aggregate's member snapshots into one snapshot-shaped document
with per-repo namespaced ids (`repo::id`, so identical cluster ids cannot
corrupt each other's edges), per-item `repository` badges, and a
`composed_from` generation block carrying every member's revision — and the
app shell already resolves composed items back to their member `(repository,
ref)` for source reads. What is missing is exactly three things, ruled in
the exit-2 decision round (topic decisions D9–D11): project-derived
aggregates, the merged view's cluster-identity rendering rule, and the
composed view's interactivity posture.

## What Changes

- ADD register-derived project aggregates (D11): the serving plane derives
  one aggregate per register project — members are the project's
  repositories present in the registry at the default ref — and the index
  advertises them beside any hand-declared aggregates. A commissioned
  project yields its merged view the moment its fulfilment lands; no
  hand-declared upkeep.
- ADD the all-repos selection: with a project scoped, the selector offers
  "all repositories in <project>" — the project's derived aggregate — and
  selecting it renders the composed snapshot through every existing view.
- ADD the view-side cluster union (D9): the wheel and canvas render
  same-TOPIC clusters from different repositories as ONE merged tile whose
  membership lists each repository's contribution; composition keeps its
  ratified per-repo namespacing untouched, so edges stay correct and every
  other consumer sees exactly what it sees today.
- ADD the composed-view interactivity posture (D10): on a composed
  snapshot every gate verb hides; expanded tiles offer one navigation verb,
  "open in <repo>", which switches the active snapshot to that tile's
  repository. Per-tile binding stays exit 3.
- ADD the composed freshness header: `N repos · composed <date>` with the
  per-member revisions reachable on demand (the `composed_from` block the
  registry already stamps).

## Non-Goals

- Any change to the ratified composition rule (namespacing, degrade-on-
  missing-member) or the snapshot/index contracts — no schema growth.
- Gate actions on composed tiles beyond the jump (exit 3,
  `add-project-tile-repository-binding`).
- Hosted-plane changes; the publication lane's hand-declared aggregates
  keep working unchanged.

## Impact

- Dashboard runtime only: registry aggregate derivation, selector/app
  wiring, wheel/canvas union rendering, verb gating on composed views.
- No contract release; no domain-repo or aggregation-repo change.
