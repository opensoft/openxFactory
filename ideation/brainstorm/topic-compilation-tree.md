# Topic Compilation Tree — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Supporting documents relate to features one-to-many, so packets should LINK to docs in a general home instead of copying them — and for each topic we want a generated, tree-structured compilation doc: a one-line-summary index that opens to per-passage abstracts, each linked to the full source doc.
Topics: ideation-tooling, doc-management, doc-workflow, supporting-docs, possibles-register, document-cataloging, ideation-dashboard
Repository context: openxFactory
Captured: 2026-07-19 (Brett, live session — prompted by the
add-possibles-derivation-lane packet showing no supporting docs while the
idea's substance sits scattered across other docs)

## The problem (verbatim intent)

The possibles idea has real brainstorm substance, but it lives as passages
inside OTHER topics' docs (`ideation-dashboard.md`, 37 mentions;
`cluster-combining-gui.md`, 16; three lens docs in passing). The packet
folder shows nothing because the supporting-doc model assumes docs belong
to ONE packet. Brett, 2026-07-19:

> if we have docs that mention a feat, then those should be part of the
> folder and support packet. but those docs are also part of other
> packets. this is a 1 to many relationship. since this is usually the
> case, we need to put the docs in some general folder and link to them
> from the staging folder. on top of this we want to compile all the
> passages into a single long doc with those links as a sort of index.
> in fact we want an index that is built, then we take abstracts and make
> the expanded doc. This can be one doc with tree structure. so it has a
> oneline summary index. that opens to abstract and is linked to the full
> doc.

## Two coupled proposals

### 1. Link, don't copy — shared supporting docs

Documents live in ONE general home (they already do: `ideation/brainstorm/`,
`docs/`). Staging folders and change packets REFERENCE them — passage-level
where possible — instead of copying. A doc mentioning N features supports N
packets without duplication or drift. The supporting-doc manifest gains a
`linked` kind alongside the current copied kind (`origin_path` already
records provenance for copies; a link entry records target + passage
anchor + why-relevant).

### 2. The compilation tree — a built topic digest

Per topic, a GENERATED doc with three levels:

```text
Level 1  index    — one line per passage/source (scannable table of the
                    whole idea-space; each line links down)
Level 2  abstract — a paragraph per passage: what this passage contributes
                    to THIS topic (not a summary of the source doc)
Level 3  source   — deep link to the full doc at the passage anchor
```

Build order matters (Brett): the INDEX is built first from passage
discovery; abstracts are then written per index row; the expanded doc is
the assembly. One doc, tree-structured, collapsible in the dashboard
(summary line → opens abstract → links out to the source viewer).

## What already exists to build on (do not reinvent)

- **Passage discovery** is the possibles-derivation problem in miniature:
  finding that a doc passage relates to a topic IS deriving a possible
  (doc→topic edge, class `inferred`). The derive-possibles worker lane
  (`add-possibles-derivation-lane`, sections 3-5 unbuilt) and this
  compilation index could share one discovery pass.
- **Abstract generation** is cataloger-shaped work: the document-cataloging
  capability (contract-v1.11) already runs a bounded tool-less worker over
  the corpus producing per-doc records — extend per-passage, with the
  model-worker contract lessons (no machine-precision transcription; the
  worker proposes, deterministic tooling anchors).
- **Anchoring**: document-lifecycle's prose-tagging markers give passages
  durable ids that survive edits better than line numbers; heading-path
  anchors are the fallback.
- **Rendering**: the dashboard's source viewer + lens views already do
  reference-set assembly; the compilation tree is a lens made durable —
  and the tree's edge data (passage→topic, classed
  indexed|inferred|synthesized) is EXACTLY the materialized cross-class
  edge contract the WHEEL realization requires.
- **NotebookLM projection**: a compilation doc per topic is an ideal
  notebook source — one doc that carries the whole idea-space with
  provenance.

## Open questions

1. Generated vs curated: is the compilation doc a pure build artifact
   (regenerated, never hand-edited — like the snapshot) or does it accept
   human curation (abstract edits, ordering) that survives rebuilds?
   Leaning: index level pure-generated; abstract level human-editable with
   worker proposals `pending_review`, like the possibles register.
2. Where does it live: committed under the topic's staging folder (it IS
   the staging organization step, mechanized) or under `health/` as a
   derived artifact? Staging-folder placement makes it the natural bridge
   from brainstorm to staged.
3. Does the `linked` supporting-doc kind need an origin-contract delta
   (the proposal-origin work is active — coordinate, don't collide)?
4. Passage granularity: heading-section, paragraph, or marker-delimited?
5. Does the compilation replace the copied support bundle at archive time,
   or does archive still compress copies for durability (links rot;
   archives should not)?

## Exit path

Organize into a staging topic once the shape settles; the passage-discovery
half likely lands as scope in (or beside) `add-possibles-derivation-lane`;
the compilation-tree rendering is dashboard work (post-v5 candidate); the
`linked` supporting-doc kind is a document-lifecycle/origin-contract delta.
