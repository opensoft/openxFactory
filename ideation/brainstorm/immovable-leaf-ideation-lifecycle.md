# Immovable-Leaf Ideation Lifecycle: docs never move, indexes carry the state — Brainstorm

Status: brainstorm
Kind: process
Author: Brett Heap (concept + forks); drafted with Claude (session 2026-07-22)
Origin: human
Summary: Redesigns the ideation pipeline around one principle — **a brainstorm
doc is a leaf: born in `ideation/brainstorm/`, it lives there forever and
never relocates.** All lifecycle state (status, history, cluster membership,
staging, promotion) lives in leaf metadata and in progressively refined
*index layers* that point at leaves. Movement is replaced by registration
(leaf → cluster at capture) and pinning (proposal → leaf@rev+hash at the
gate). Two cluster types: **topic clusters** (solid, direct links via
declared topics/keywords; chartered deliberately) and **possibles**
(AI-derived non-obvious connections, each shaped as a *possible proposal*
with a feat outline). Staging becomes a state plus a thin index doc — files
never move into it. Generalizes `topic-compilation-tree.md`'s
link-don't-copy instinct to the whole lifecycle.
Topics: ideation-lifecycle, document-lifecycle, brainstorm-leaves, clusters,
possibles, topic-clusters, staging, pin-manifest, provenance, attribution,
cross-reference-index, possibles-derivation, ai-generated-docs
Repository context: openxFactory (document-lifecycle spec + ideation-cross-reference index + possibles derivation lane)
Captured: 2026-07-22

## The principle

Today's lifecycle moves files: brainstorm material is selected into
`ideation/staging/<topic>/`, and at the proposal gate staged files move again
into `openspec/changes/<change-id>/supporting-docs/`, then compress into the
archive. Every move loses the doc's home, splits its identity across
locations, and makes "where is the idea now?" a filesystem question.

Inverted: **leaves never move; everything above them is an index.**

```text
leaves        ideation/brainstorm/*.md        immovable; metadata carries state
topic         chartered cluster objects        solid links (declared topics)
clusters      in the cross-reference index
possibles     AI-derived cluster objects       non-obvious links; each is a
              (possibles_register)             POSSIBLE PROPOSAL (feat outline)
staging       disposition + a thin index doc   human-worked prep; pointers only
proposal      OpenSpec change + PIN MANIFEST   (leaf path, git rev, sha256)
archive       manifest + GENERATED snapshot    copy for provenance, never a move
```

## Decided (2026-07-22)

- **The cluster gate: chartered clusters, free keywords.** Keywords stay
  free-form on leaves. A **cluster** is a deliberately created, registered
  object — name, definition, member criteria (and likely an owner). Keywords
  and the readiness lane *nominate* candidate clusters; a human charters
  them. Once chartered, new leaves auto-register by topic match. This is the
  key gate: without it clusters are keyword soup; with a heavier gate,
  capture friction kills the corpus.
- **Provenance: pin manifest + generated snapshot.** At the proposal gate the
  change records a manifest of `(leaf path, git rev, sha256)` for every
  supporting leaf; at archive a snapshot bundle is *generated* from the pins.
  Leaves never move. **Invariant: consumers of ratified content always read
  through pins, never live paths** — the leaf may keep evolving (brainstorm
  is the one place contradiction is legal); the pin freezes what was ratified.
- **Staging: a state + an index doc.** The staged topic survives as a thin
  index/summary doc (the same shape as a possible proposal, human-worked),
  but files never move into it; promotion flips dispositions and creates
  pins. New ideas raised during staging become new *leaves* in brainstorm
  that register with the cluster.
- **The derivation lane may generate leaves.** Extending
  `add-possibles-derivation-lane`: the AI worker may author new complementary
  brainstorm leaves (gap-fillers for a possible proposal), written into
  `ideation/brainstorm/` as ordinary leaves tagged `origin: ai-derived` +
  agent/worker profile + run correlation id + `disposition: pending_review`
  — the same intake pattern the register already ratified. Humans disposition
  them like any other leaf.

## Attribution (leaf metadata)

Every leaf carries its author: human leaves name the human
(`Author: <name>`); AI leaves carry `Origin: ai-derived` plus the derivation
block (worker profile, prompt-contract version, correlation id) reused from
the possibles-register kernel. This doc practices the convention on itself.

## Two cluster types, one register

The cross-reference index (`add-ideation-cross-reference-readiness`, landed)
already models both sides: topic clusters + staged topics on the solid side,
`possibles_register` on the derived side, with the dashboard as the surface
and the derivation lane (`add-possibles-derivation-lane`, in flight) filling
the possibles column. The delta this brainstorm adds:

1. Clusters become **chartered objects** with the gate above (today they are
   largely emergent from topics).
2. A possible is explicitly a **possible proposal**: its register entry
   carries a feat outline (feats, summary of how they would work, member-leaf
   pointers) — not just a connection statement.
3. **Staging and promotion stop moving files** — dispositions + pins replace
   relocation; the document-lifecycle spec's supporting-docs mechanics are
   MODIFIED accordingly.
4. Leaf **attribution metadata** becomes part of the leaf contract.

## Why (what the moves cost today)

- The 2026-07-22 staging of the Hermes content topics required synthesizing
  new primary docs partly *because* moving the 14 brainstorm sources was
  wrong — under this model the staged index would simply point at the leaves
  and their dated Decided sections.
- A leaf that feeds three proposals today must be copied or split;
  under pins it is referenced three times at three revisions.
- New docs currently get indexed nowhere until a human remembers
  (yesterday's cost-accountability leaf registered with nothing) —
  registration-at-capture closes that.

## Open questions

- **Charter authority** — who may charter a cluster (any human? the
  ideation owner? does the readiness lane's nomination need a threshold?),
  and can a chartered cluster be retired/merged (the cluster-combining GUI
  brainstorm gestures at merge mechanics)?
- **Leaf edit semantics under pins** — dated in-place edits (current
  practice) are fine for live reading; is any edit class disallowed once a
  leaf is pinned by a ratified change (e.g. deleting a section a pin cites),
  or is git rev isolation always sufficient?
- **Migration** — do existing staged topics and archived
  supporting-docs.tar.gz bundles stay as-is (two-era corpus), or backfill
  pins for the archive?
- **Registration mechanics** — is leaf→cluster registration a field on the
  leaf, an entry in the index, or both (and which is authoritative)?
- **Possible-proposal outline schema** — the exact register-entry fields for
  the feat outline (feats[], how-it-works summary, member pointers, gaps the
  AI filled with generated leaves).

## Exit path

- MODIFIED `document-lifecycle` (openxFactory): promotion mechanics — pins +
  generated snapshot replace supporting-docs moves; staging as
  state-plus-index; leaf attribution fields.
- MODIFIED `ideation-cross-reference` index kernel: chartered-cluster object
  + possible-proposal outline fields.
- Extension rider on `add-possibles-derivation-lane` (or a follow-up change):
  the generate-complementary-leaves capability with the pending-review intake.
- The lens/dashboard brainstorms (`cluster-combining-gui.md`,
  `lens-*.md`, `topic-compilation-tree.md`) consume this model as their data
  layer; `ideation-dashboard` is the working surface.
