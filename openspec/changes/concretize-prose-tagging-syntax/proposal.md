# Concretize Prose Tagging Syntax

## Why

The ratified `document-lifecycle` capability (change:
`add-document-lifecycle-vocabulary`) requires that prose designated for
spec conversion use "an explicit machine-readable tag" and that prose
changing promoted policy carry "an explicit supersedes marker" — but neither
artifact is defined anywhere. The abstraction was deliberate at ratification
time; it is now the blocker for the doc-health pipeline's deterministic
pass, whose tag-hygiene check (staged in
`ideation/staging/doc-health-checks/`) cannot be specified against markers
that have no syntax. The staged topic
`ideation/staging/prose-tagging/tag-syntax.md` carries the organized claims;
this change takes them through the proposal gate.

## What Changes

- Define one canonical, grep-able marker grammar under the `xspec:`
  namespace, expressed as HTML comments:
  - block-level conversion candidacy:
    `<!-- xspec:candidate target=<capability> -->` ...
    `<!-- /xspec:candidate -->`
  - inline supersedes marker:
    `<!-- xspec:supersedes spec=<capability>/<requirement-slug>
    change=<change-id> -->`
- Rule that candidacy is block-level only: no doc-level
  `Status: spec-candidate` value exists; a document's lifecycle status and
  its conversion queue stay orthogonal.
- Structural rules: candidate blocks may not nest and may not span heading
  boundaries; every open fence has a matching close fence in the same
  section.
- Marker hygiene becomes contract surface: well-formedness, target
  resolution, and structural rules are deterministic health checks; unknown
  `xspec:` directives are findings.
- Staged fragments continue to comply structurally (target capability +
  delta type in the fragment header) and need no inline markers.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `document-lifecycle`: the "Explicit delta rule" requirement is
  concretized — the abstract "explicit machine-readable tag" and "explicit
  supersedes marker" become the canonical `xspec:` marker grammar. A new
  "Prose tagging marker hygiene" requirement makes the grammar
  deterministically checkable.

## Impact

- openxFactory: `docs/document-lifecycle.md` gains the concrete marker
  syntax in its Explicit Delta Rule section, citing this change;
  `ideation/staging/prose-tagging/tag-syntax.md` moves through the proposal
  gate (references this change); the doc-health-pipeline brainstorm pointer
  updates.
- `ideation/staging/doc-health-checks/` receives a tag-hygiene rules
  fragment (grep patterns plus hygiene checks) as requirements input for
  the future doc-health checker.
- No runtime, contract schema, or credential impact. No document gains or
  loses lifecycle status; this change defines syntax only.
