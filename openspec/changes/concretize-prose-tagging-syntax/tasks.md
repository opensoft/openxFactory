# Tasks: Concretize Prose Tagging Syntax

## 1. Canonical Document

- [ ] 1.1 Update the "The Explicit Delta Rule" section of
      `docs/document-lifecycle.md` with the concrete `xspec:` marker
      grammar (candidate fences and supersedes marker), the block-level-only
      candidacy rule, and the structural rules (no nesting, no
      heading-spanning), citing this change.

## 2. Ideation Pointers (staged -> proposed gate)

- [ ] 2.1 Update `ideation/staging/prose-tagging/tag-syntax.md`: reference
      this change as its proposal, and record the resolved open questions
      (HTML comments; no nesting or heading-spanning) pointing at this
      change's `design.md`.
- [ ] 2.2 Update the prose-tagging pointer line in
      `ideation/brainstorm/doc-health-pipeline.md` to reference this change,
      and note that the doc-level `Status: spec-candidate` idea was dropped
      at the proposal gate.

## 3. Doc-Health Handoff

- [ ] 3.1 Add `ideation/staging/doc-health-checks/tag-hygiene-rules.md`
      (companion to `status-check-rules.md`): the grep contract
      (`grep -rn 'xspec:' --include='*.md'`), the canonical grammar, and
      the hygiene checks the deterministic pass MUST implement
      (well-formedness, target resolution, fence structure, `change=`
      aging), sourced from this change.

## 4. Validation

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate
      concretize-prose-tagging-syntax --strict` and
      `openspec validate --all --strict` pass from the openxFactory root.
- [ ] 4.2 Grep-verify: every `xspec:` occurrence in the repo parses against
      the canonical grammar, and no `Status:` header anywhere uses
      `spec-candidate`.
