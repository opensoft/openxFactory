# Staged: Prose Tagging Syntax

Status: staged
Kind: reference
Repository context: openxFactory
Source: [doc-health-pipeline brainstorm](../../brainstorm/doc-health-pipeline.md)
Target capability: `document-lifecycle` (delta: MODIFIED — concretize the
"explicit machine-readable tag" and "explicit supersedes marker" the ratified
requirements reference abstractly)

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

- HTML comments vs visible Markdown syntax (comments are invisible in
  rendered views — is that a feature or a hazard for reviewers?).
- Whether `xspec:candidate` blocks may nest or span headings.

## Exit

One OpenSpec change delta to `document-lifecycle` ratifying the syntax;
implementation lands with the doc-health checker.
