# Ring Combination Explorer for the Keyword Lens — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Feat request against the realized keyword lens — clicking ring k lists the checked keywords' combinations taken k at a time as tiles (ring 2 → all pairs, ring 3 → all triples), each tile showing its doc membership; clicking a combination tile focuses the view on exactly that keyword subset and offers the brainstorm-launch gesture there — turning the bullseye into a navigable lattice of keyword intersections, where EMPTY combinations read as unexplored-idea signals.
Topics: feat-request, ideation-dashboard, keyword-lens, doc-management, doc-workflow
Repository context: openxFactory (capability owner; realization would be a codexFactory delta)
Captured: 2026-07-14
Origin: Brett, 2026-07-14, using the deployed dashboard.

Brainstorm — contradiction and half-formed options are legal here.

## The request

Today ring k shows the docs that match exactly k of the checked keywords,
sectored by WHICH subset matched. Brett's extension: make the rings
navigable by combination —

1. Click **ring 2** → a list of the checked keywords' combinations taken
   TWO at a time (all pairs), each as a tile with its member docs/count.
2. Click **ring 3** → the same list re-cut as triples. Ring k → k-at-a-time.
3. Click a **combination tile** → a focused view of exactly that keyword
   subset (its docs, its clusters) — and brainstorm from there (the
   brainstorm-launch gesture from the sibling feat request, scoped to the
   combination).

This generalizes the existing subset sectors into a first-class
combination lattice — the bullseye becomes the map, the combination list
the index, the focused view the room.

## Design notes

- **Pure derivation.** Combinations and their memberships derive entirely
  from `documents[].topics` × the checked set — renderer-side, pure,
  node-testable in the lens-model pattern. No schema change, no new fetch.
- **Explosion control.** C(n,k) grows fast (10 checked → 120 triples).
  Controls: only enumerate combinations of the CHECKED set (bounded by the
  user); sort by member count descending; collapse empty combinations
  behind a toggle; cap rendered tiles with an explicit "showing top N of
  M" (no silent truncation).
- **Empty combinations are signal, not noise.** A pair of keywords with
  ZERO docs is a gap in the corpus — possibly an unexplored idea niche.
  Render empties (when toggled on) in the gap-prompt idiom from the
  canvas: "no doc connects `keycloak` × `doc-workflow` — start the
  brainstorm that does?" This makes the lattice a generative surface, not
  just a filter: the empty cell IS the feat-request generator.
- **Focused combination view.** Reuses existing pieces: the matrix
  filtered to the combination, member doc cards with summaries, the
  cluster-canvas lineage strip where the combination coincides with a
  cluster, and the brainstorm-launch gesture with Topics pre-filled to
  exactly the combination.
- **Membership semantics choice**: does a combination tile count docs
  matching AT LEAST that subset (supersets included) or EXACTLY it? At
  least = more useful for exploration; exactly = matches the ring's
  current match-count semantics. Leaning: at-least, with the exact count
  shown secondary ("14 docs, 3 exactly").

## Open questions

- Ring-click vs a mode: does clicking ring k REPLACE the bullseye with the
  list (drill-in + breadcrumb back), or open a side panel keeping the
  bullseye visible? Leaning side panel (the bullseye is the map — do not
  lose it).
- Do combination views deep-link (hash-route) so a combination can be
  shared/bookmarked? Cheap and valuable on the hosted dashboard.
- Does an empty-combination brainstorm-launch pre-fill BOTH keywords into
  Topics even though no doc carries them together yet? (Yes — that is the
  point — but confirm the tag-vocabulary implications with the cataloging
  registry.)

## Possible feats

- Ring-click combination list (k-at-a-time tiles, member counts, sort +
  cap with explicit truncation note).
- Empty-combination gap prompts as brainstorm invitations.
- Focused combination view (filtered matrix + member cards + launch
  gesture with pre-filled Topics).
- Hash-route deep links for combinations on the hosted dashboard.
- At-least/exactly membership toggle.

## Exit

Clusters with the other lens feat requests; picked possibles go to one
staged `lens-enhancements` topic and realize as a MODIFIED
`ideation-dashboard` OpenSpec delta with a codexFactory feature.
