# Staged: Prose Tagging Syntax

Status: staged
Kind: reference
Repository context: openxFactory
Source: [doc-health-pipeline brainstorm](../../brainstorm/doc-health-pipeline.md)
Target capability: `document-lifecycle` (delta: MODIFIED — concretize the
"explicit machine-readable tag" and "explicit supersedes marker" the ratified
requirements reference abstractly)
Proposed by: [concretize-prose-tagging-syntax](../../../openspec/changes/concretize-prose-tagging-syntax/proposal.md)
— this topic has passed the proposal gate; the change carries the spec delta.

## Claims

1. Conversion is opt-in via explicit tags; only tagged prose is queued.
   Doc-level: `Status: spec-candidate` is NOT used — candidacy is block-level
   only, so a doc's lifecycle status and its conversion queue stay orthogonal.
2. Block-level candidate tag:
   `<!-- xspec:candidate target=<capability> -->` ... `<!-- /xspec:candidate -->`
3. Supersedes marker (satisfies the Explicit Delta Rule inline, pending an
   OpenSpec change):
   `<!-- xspec:supersedes spec=<capability>/<requirement-slug> change=<change-id-when-known> -->`
4. Markers are contract surface: one canonical grep-able syntax, validated by
   the doc-health deterministic pass (marker targets must resolve).
5. Staged fragments comply structurally (target capability + delta type in
   the fragment header) and need no inline markers.

## Open questions

Both resolved at the proposal gate — see
[design.md](../../../openspec/changes/concretize-prose-tagging-syntax/design.md)
of the proposing change:

- HTML comments vs visible Markdown syntax → **HTML comments** (markers are
  machine contract surface, not reader content; gate reviewers work in
  source; the doc-health report is the rendered-view inventory).
- Nesting / heading-spanning of `xspec:candidate` blocks → **neither** (one
  block, one target, one section-anchored extraction unit; keeps hygiene a
  plain line scan).

## Exit

One OpenSpec change delta to `document-lifecycle` ratifying the syntax:
[concretize-prose-tagging-syntax](../../../openspec/changes/concretize-prose-tagging-syntax/proposal.md)
(created 2026-07-08). Implementation of enforcement lands with the
doc-health checker — hygiene rules handed to
[../doc-health-checks/tag-hygiene-rules.md](../doc-health-checks/tag-hygiene-rules.md).
