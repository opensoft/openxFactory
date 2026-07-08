# Tasks: Add Lifecycle Notebook Projection

## 1. Workflow Documentation

- [ ] 1.1 Write `docs/lifecycle-notebook-projection.md` — the full NotebookLM
      workflow: the three books, projection table, exclusions, grounding set,
      title prefixes, charter text, chat framing, sync cadence and manifest,
      stage-transition behavior, and operator runbook (auth, dry-run, apply,
      artifact generation). Status: ratified, citing this change.
- [ ] 1.2 Link the doc from the README documentation index.
- [ ] 1.3 Add a relation note in `docs/notebooklm-source-workspaces.md`
      pointing to the projection doc for lifecycle-derived workspaces.

## 2. Regularize The Pilot Implementation

- [ ] 2.1 Update `codexFactory/scripts/sync-notebooklm-books.py` docstring to
      cite this capability as the contract it conforms to, and align any
      drifted constants (books, prefixes, charter, chat prompt) with the doc.
- [ ] 2.2 Commit the script in codexFactory (it currently exists uncommitted)
      and sync the aggregation pin.
- [ ] 2.3 Register the three notebooks as `external_source_workspace` records
      (source-workspaces model §6) under `openxFactory/examples/` or a
      workspace registry location chosen in 1.1.

## 3. Validation

- [ ] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes.
- [ ] 3.2 Run the sync dry-run twice after a no-op: second run reports zero
      adds/deletes (idempotence proof).
- [ ] 3.3 Move one doc between states, run sync, verify the source moved
      books, then restore (stage-transition proof).
