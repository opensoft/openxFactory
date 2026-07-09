# Tasks: Add Lifecycle Notebook Hybrid Imports

## 1. Contract Documentation

- [ ] 1.1 Update `docs/lifecycle-notebook-projection.md` to define hybrid
      analysis notebooks: one Canon release line plus one brainstorm or
      staged origin folder.
- [ ] 1.2 Add the source-return workflow: any non-seed NotebookLM source in a
      hybrid returns to the origin folder; scratch notes remain in
      NotebookLM until converted to sources.
- [ ] 1.3 Document seed-source exclusions and imported entry provenance:
      source workspace, source id, source title, L1 authority, and origin
      lifecycle status.
- [ ] 1.4 Link or promote the staged
      `ideation/staging/lifecycle-notebook-hybrids/` process as the source
      of this ratified workflow.

## 2. codexFactory Implementation

- [ ] 2.1 Extend `scripts/sync-notebooklm-books.py` with a dry-run-by-default
      import mode that accepts a hybrid notebook id/alias and an origin
      `--target-path`.
- [ ] 2.2 Ensure the importer skips managed seed sources:
      `00 [charter]`, `[brainstorm]`, `[staged]`, `[draft]`, `[ratified]`,
      `[standard]`, `[spec]`, and `[grounding]`.
- [ ] 2.3 Ensure the importer writes imported material under the supplied
      brainstorm/staged origin folder with `Status`, `Kind`, workspace,
      source id, source title, and `Authority: L1 notebook synthesis`.
- [ ] 2.4 Ensure imports are idempotent by NotebookLM source id.
- [ ] 2.5 Keep any explicit `[export:*]` title path as compatibility only;
      the primary path imports all non-seed sources from the origin-scoped
      hybrid.

## 3. Tests And Validation

- [ ] 3.1 Add unit tests for untagged converted-note sources importing to a
      brainstorm origin.
- [ ] 3.2 Add unit tests for added non-note sources, such as web/research
      sources, importing to a staged origin.
- [ ] 3.3 Add tests proving seed sources are skipped and already imported
      source ids are not duplicated.
- [ ] 3.4 Include NotebookLM importer tests in codexFactory repo validation.
- [ ] 3.5 Run local implementation tests before repo validation.
- [ ] 3.6 Run codexFactory repo validation before OpenSpec validation.
- [ ] 3.7 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` from
      the openxFactory root.

## 4. Live Acceptance Evidence

- [ ] 4.1 Use a live hybrid/test notebook to convert a NotebookLM note into a
      source, pull it back to the origin brainstorm folder, and record the
      source id/title in the imported file.
- [ ] 4.2 Add or discover a non-note source in a hybrid notebook and verify
      the importer writes it to the same origin folder.
