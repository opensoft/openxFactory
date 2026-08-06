# Design: Project Merged Projection

## Context

Exit 2 of `dashboard-project-scoping` (D1: the all-repos view is a true
merged projection; D6: sequenced after exit 1). The composition substrate —
`snapshot_registry.compose_aggregate` / `compose_snapshots` — is ratified
and realized: per-repo namespaced ids, per-item repository badges,
`composed_from` freshness, degrade-on-missing-member. This change builds
the three missing pieces on top of it, each ruled by Brett in the exit-2
decision round of 2026-08-06 (topic decisions D9–D11).

## Decisions

### D9 (topic) — Cluster identity: view-side union
Composition keeps namespacing (`repo::cl-<topic>`): the ratified rule
exists so identical ids cannot corrupt each other's edges, and every
existing consumer of composed snapshots keeps its exact semantics. The
UNION lives in the wheel/canvas view model only: a composed snapshot's
clusters group by their TOPIC (the id's stable tail), rendering one tile
per topic whose membership is the per-repo contributions. The topic is the
family's global vocabulary, so this is a display grouping, not an identity
claim — drilling in shows each repository's cluster distinctly.

### D10 (topic) — Composed views are read-only plus a jump
A gate verb binds to the served checkout; a composed view has no single
checkout. Rather than mixing planes ahead of exit 3, every gate-bearing
affordance hides when the rendered snapshot is composed (the
`generation.composed_from` block is the signal — no new flag), and the
expanded tile offers exactly one navigation verb: "open in <repo>", which
stores that tile's `(repository, ref)` key and reloads — after which every
verb works as today. This is the same reload-per-switch posture the
selector already ratified.

### D11 (topic) — Project aggregates derive from the register
The serving plane derives one aggregate per register project at index-
composition time: id = the project id, display name = the project name,
members = the project's repositories that the registry can actually
resolve, at the default ref. Derived aggregates are additive beside
hand-declared ones; a name collision resolves in favour of the
hand-declared aggregate (explicit beats derived). Because derivation reads
the register projection, a create-project commission's fulfilment makes
the merged view exist with no further authoring.

### D-f — The union key is the topic tail, allow-list checked
The merged tile's grouping key is the namespaced id's tail after the
`repo::` prefix (`cl-kill-switch`), which is generator-minted from the
topic vocabulary — never free text. The view model treats an id with no
namespace prefix (a non-composed snapshot) as its own group of one, so the
same code path renders both planes.

## Risks / Trade-offs

- **A very large project composes many snapshots per selection.** The
  registry already reads members lazily and degrades on unavailable ones;
  v1 accepts the linear cost (fourteen repos today), and the selector's
  availability marking names any member that failed to load.
- **The jump verb loses view position.** Reload-per-switch is the ratified
  selector posture; a session-restoring jump would be new machinery for
  exit 3's plane, not this change.

## Open Questions

None — D9–D11 were ruled 2026-08-06; D-f is derivational.
