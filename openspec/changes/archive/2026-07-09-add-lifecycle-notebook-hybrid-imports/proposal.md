# Add Lifecycle Notebook Hybrid Imports

Status: ratified
Ratified: 2026-07-09 — record: the ratify gate recorded on the archive commit `e55724c`, "Archive add-lifecycle-notebook-hybrid-imports (ratified and realized)", whose body opens "Ratify gate approved; importer implemented in codexFactory ...; lifecycle-notebook-projection spec updated (+5 requirements)". The DATE ONLY is recorded: the gate line names no ratifier in prose, so none is claimed. The same act promoted this change's delta into `openspec/specs/lifecycle-notebook-projection/spec.md`. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The lifecycle notebook projection now gives xFactory Ideation, Working Drafts,
and Canon books, but real analysis happens in temporary hybrid notebooks that
combine a Canon release line with one brainstorm or staged topic. Those hybrids
can generate new NotebookLM sources: converted notes, web research, files, or
Drive sources. Without a ratified return path, useful source material either
stays trapped in NotebookLM or is copied back by hand with no consistent
authority, provenance, or destination rule.

The live `test-canon` experiment proved the mechanics: a note converted to a
NotebookLM source can be discovered, its content can be extracted, and it can
be written back into `ideation/brainstorm/` as L1 notebook synthesis. This
change turns that pilot into governed behavior.

## What Changes

- Extend the `lifecycle-notebook-projection` capability to cover temporary
  hybrid analysis notebooks:
  - each hybrid is scoped to exactly one Canon release line and one origin
    folder: either `ideation/brainstorm/<topic>/` or
    `ideation/staging/<topic>/`.
  - hybrids may be built by copying Canon source text plus the selected origin
    idea sources; native NotebookLM duplication may replace that copy path if
    the product later supports it.
  - hybrid output remains `L1 notebook synthesis` and cannot decide policy,
    memory, release scope, or OpenSpec approval.
- Add the source-return rule:
  - any source added to the hybrid after its seed set is importable back to
    the origin folder.
  - this includes notes converted to sources, NotebookLM research results, web
    sources, files, Drive sources, and other NotebookLM source types.
  - scratch notes remain inside NotebookLM because they are not sources.
- Define the seed-source exclusion rule:
  - the Canon, grounding, charter, and originally projected idea sources are
    baseline context and must not be imported back as new ideas.
  - the importer skips managed seed titles such as `00 [charter]`,
    `00 [hybrid charter]`, `[brainstorm]`, `[staged]`, `[draft]`,
    `[ratified]`, `[standard]`, `[spec]`, and `[grounding]`.
- Require imported material to be written into the origin folder as governed
  ideation material with source id, title, workspace reference, and
  `Authority: L1 notebook synthesis`.
- Require implementation checks to run in order before review: local
  implementation tests, owning repo validation, then OpenSpec validation.

No breaking change: existing lifecycle books remain derived and
non-curated. The new import behavior applies only to temporary analysis
notebooks when an operator supplies the origin target folder.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `lifecycle-notebook-projection`: adds governed hybrid analysis notebooks,
  new-source return imports, seed-source exclusions, provenance/authority
  requirements for imported material, and review-gate validation order.

## Impact

- openxFactory:
  - promotes the staged process in
    `ideation/staging/lifecycle-notebook-hybrids/` into the ratified
    lifecycle notebook projection workflow.
  - updates the OpenSpec `lifecycle-notebook-projection` spec and staged
    process notes to include hybrid creation, source return, and review gates.
  - keeps live NotebookLM pull output under `ideation/brainstorm/` or
    `ideation/staging/` until it moves through normal gates.
- codexFactory:
  - extends `scripts/sync-notebooklm-books.py` with a new-source import mode
    that pulls non-seed sources back to a supplied origin folder.
  - adds tests for untagged converted-note imports, added source imports,
    seed-source skipping, and source-id dedupe.
  - includes the NotebookLM importer tests in repo validation.
- NotebookLM:
  - no product API dependency beyond source listing and source content export.
  - no requirement that users rename sources; conversion/addition to the
    notebook source set is the user-facing gate.
- No runtime, credential, or customer-data impact. Imported material remains
  L1 synthesis and must be reviewed before it can influence policy,
  implementation, memory, or customer-facing output.
