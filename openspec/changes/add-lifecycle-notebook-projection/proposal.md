# Add Lifecycle Notebook Projection

## Why

The document lifecycle taxonomy (promoted by `add-document-lifecycle-vocabulary`)
made every governance doc's state machine-readable. A working pilot now
projects those states into NotebookLM notebooks (Ideation / Working Drafts /
Canon) so the prose corpus can be interrogated, visualized, and synthesized —
but the pilot ran ahead of governance: the sync script, book definitions,
charter text, and chat framing exist in `codexFactory` with no ratified
contract behind them. Without one, notebook membership and authority framing
are implementation accidents that the next editor may silently change,
recreating the status-drift problem the taxonomy just eliminated.

`docs/notebooklm-source-workspaces.md` already governs NotebookLM authority
(L0–L5 levels, workspace ownership); it does not cover lifecycle-derived
notebooks or their sync discipline.

## What Changes

- Define the lifecycle notebook projection contract: which books exist, how
  membership derives from `Status:` headers, exclusions, grounding sources,
  title prefixes, charter, and chat framing.
- Require that lifecycle notebooks are always derived, never hand-curated,
  and that stage transitions move sources between books.
- Bind the projection to the existing source-authority model: all lifecycle
  notebook output is L1 synthesis; only `[standard]`/`[spec]` sources
  describe the running system.
- Document the full NotebookLM workflow in a ratified openxFactory doc and
  regularize the existing codexFactory sync implementation against it.

## Capabilities

### New Capabilities

- `lifecycle-notebook-projection`: derived NotebookLM books over the
  governance corpus, their membership rules, authority framing, and sync
  implementation ownership.

### Modified Capabilities

- None. (`document-lifecycle` is unchanged; this capability consumes its
  states. The source-workspaces authority model is referenced, not altered.)

## Impact

- openxFactory: new `docs/lifecycle-notebook-projection.md` workflow doc
  (ratified by this change); README index link; relation note in
  `docs/notebooklm-source-workspaces.md`.
- codexFactory: `scripts/sync-notebooklm-books.py` is regularized as the
  reference implementation — its book definitions, charter, prefixes, and
  chat prompt become conformance to this contract rather than ad hoc choices.
- NotebookLM: three notebooks (`xFactory — Ideation`, `xFactory — Working
  Drafts`, `xFactory — Canon`) become governed workspaces registered per the
  source-workspaces record model.
- No runtime, contract schema, or credential impact. Notebook content is
  L1 synthesis and never feeds gates.
