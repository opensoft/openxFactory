# Brainstorm Session Launch from the Keyword Lens — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Feat request against the realized keyword lens — clicking the bullseye's center ring starts a brainstorm session focused on the checked keyword set: a scaffolded brainstorm doc with Topics pre-filled from the checked keywords, a workbench reference set of the matching docs, and optionally a scratch notebook — composing three already-landed mechanisms (authoring scaffold, workbench manifest, xf-wb notebooks) behind one gesture.
Topics: feat-request, ideation-dashboard, keyword-lens, workbench, doc-management, doc-workflow
Repository context: openxFactory (capability owner; realization would be a codexFactory delta)
Captured: 2026-07-14
Origin: Brett, 2026-07-14, using the deployed dashboard.

Brainstorm — contradiction and half-formed options are legal here.

## The request

The center ring holds the docs matching ALL checked keywords — the
tightest expression of "the thing I am currently thinking about." Clicking
it should START A BRAINSTORM SESSION focused on that keyword set, not just
show the docs.

## What "start a session" means — composed from landed parts

Nearly everything needed already shipped in the realization:

1. **The doc**: the authoring create action (D7) scaffolds a
   header-compliant brainstorm doc — `Topics:` pre-filled with the CHECKED
   KEYWORDS, `## Possible feats` seeded, opened in the human's editor.
   Today the scaffold takes manual inputs; the feat pre-fills them from
   lens state.
2. **The reference set**: a workbench manifest, recipe-seeded from the
   checked/pinned keywords (the recipe engine + `build_workbench_from_recipe`
   exist) — the session's reading list is the center ring's members plus
   the outer rings as context.
3. **The notebook (optional)**: bind an `xf-wb-<topic>` scratch notebook
   over the set for semantic interrogation while writing; dies with the
   manifest via the orphan sweep.

So the feat is one lens gesture wiring three existing engines plus the
session framing: the new doc's `Source:` cites the recipe (checked/pinned
keywords + the member docs at that snapshot revision) — a brainstorm born
with machine-checkable provenance about WHY it exists.

## Interaction sketch

- Click the center ring (or a "start brainstorm" button on the forming-set
  pane) → a small confirm card: proposed doc title, the Topics line
  (editable), which of set/notebook to create → CREATE opens the editor.
- Hosted-dashboard reality: the web surface is read-only — like the gate
  bar, the gesture emits the CLI descriptor
  (`cli.py create ... --topics <checked> --workbench <recipe>`) until a
  write-enabled authenticated host phase exists (Keycloak brainstorm is
  the prerequisite chain). Locally via generate-and-open it executes.
- The AI-assisted variant (seed-to-spec expanding the session's seed into
  a structured draft) stays a follow-on tied to the generation-engine
  lane — same boundary as every AI assist: pending-review, never direct.

## Open questions

- Does the session doc default to `ideation/brainstorm/` of the scanned
  repo (openxFactory in v1) or ask? Multi-repo dashboards make this a
  real choice (D10 grouping could scope it).
- Should launching from the center ring auto-record a `lens-launch`
  action in the workbench manifest history (auditable session origin)?
  Leaning yes — the action vocabulary is additive.
- Title/topic-slug derivation from N checked keywords (join? ask?).

## Possible feats

- Center-ring (and forming-set) brainstorm-launch gesture: scaffold doc
  with Topics = checked keywords + Source citing the recipe.
- Recipe-seeded workbench set + optional scratch notebook in the same
  gesture.
- CLI descriptor emission on the hosted read-only surface (parity with
  the gate bar).
- `lens-launch` action recording in the manifest history (additive).
- (follow-on) AI seed-to-spec expansion of the launched session, pending
  review, via the generation-engine lane.

## Exit

Clusters with the other lens feat requests; picked possibles go to one
staged `lens-enhancements` topic and realize as a MODIFIED
`ideation-dashboard` OpenSpec delta with a codexFactory feature.
