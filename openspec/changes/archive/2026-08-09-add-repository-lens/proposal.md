---
code_surface: openxFactory (dashboard runtime — composed-model repository-vocabulary projection + drill-in scoping, the lens tab's vocabulary switch and drill-in pane, app shell scope/banner wiring, styles; tests)
target_release: none
Status: ratified
Ratified: Brett's 2026-08-07 observation and instruction (topic `dashboard-project-scoping` D21) — "our repo selector is now very similar to the lens function but for documents in repos vs keywords in documents. figure out how to make a lense widget for this repo selector where the repos would be our selector checkboxes instead of keywords. we can then make a drill in dashboard that looks at that set of documents only" — with the three realization choices answered the same day (vocabulary toggle inside the Lens tab; the filter keeps its own control and the lens is the deep view; drill-in is a scoped view with no new persistence)
---

# Proposal: add-repository-lens

## Why

Brett noticed that the repository filter and the keyword lens are the same
mechanism wearing different words, and he is right in a way the code can
prove: `buildLensModel` reads a snapshot in exactly two places — the
vocabulary with counts, and which terms a document carries. Everything
downstream (the bullseye rings and sectors, the label-collision geometry,
the co-occurrence hints, the matrix) is vocabulary-agnostic.

Reading the repository plane through that lens also answers a question the
filter's two modes could only gesture at. The filter says union or shared;
the lens says HOW shared — a ring per carrier count, a sector per exact
repository combination. On the real five-factory `domains` project that
distribution is the finding: 215 document identities in exactly one
repository, one in two, one in three, two in all five. A factory family
that is almost entirely domain-specific over a two-document neutral core,
which is precisely the question the domain-neutralization candidate
register exists to ask.

And once a region of that bullseye is a named set of documents, "show me
only those" is the obvious next gesture — the bullseye already carries an
activation contract for exactly this, currently unused by the lens tab.

## What Changes

- ADD a REPOSITORY VOCABULARY for the lens: `repositoryVocabulary()`
  re-expresses a composed snapshot in the shape the lens already reads —
  vocabulary terms are member repositories, "documents" are cross-repository
  document IDENTITIES, and a document "carries" a repository when that
  repository has that identity. The lens engine is not modified at all.
- ADD a vocabulary switch to the Lens tab, offered only on a composed view
  (a single-repository view has no member set to lens over). The keyword
  lens is untouched in behaviour and appearance.
- The repository rail's ticks ARE the visible set: the lens opens on the
  current set and writes changes through, so the filter popover and the
  lens always agree. The lens redraws locally rather than reloading — it
  holds the whole aggregate, so any subset is a pure re-derivation.
- ADD the DRILL-IN: activating the bullseye's centre or a sector — from the
  hit region or from the labelled drill-in pane beside it — scopes the whole
  shell to that region's documents, with a banner naming the scope and
  clearing it.
- The scope is a DOCUMENT SET; every other plane keeps only what references
  it (a cluster on an edge into the set, a change or staged topic on a file
  path, a keyword while a kept document still declares it).

## Impact

No contract growth: no schema, no route, no gate verb. The projection and
the scoping are pure view derivations over data the composition already
carries, and both degrade to null/no-op off a composed snapshot. The
keyword lens keeps its persistence affordances; a repository set is a view,
not a set to save, so the repository vocabulary shows the drill-in pane
where the keyword lens shows its forming/persistence pane — saving a
repository recipe (workbench manifest, add-as-cluster) is deliberately out
of scope for this pass and would be a successor change with real gate-verb
growth.
