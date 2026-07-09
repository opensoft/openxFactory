# Staged: Release Realization Flow (Organized From Pilot)

Status: staged
Kind: architecture
Repository context: openxFactory
Source: [openspec-speckit-release-flow brainstorm](../../brainstorm/openspec-speckit-release-flow.md)
(Brett's captured model, 2026-07-09) plus the completed pilot:
`codexFactory/openspec/changes/archive/2026-07-09-implement-doc-health-checker`
— the family's first realization-gated change (chose code-realization
archival at its proposal gate, stayed active through three failed CI runs,
archived only after the green nightly).
Target capability: new `release-realization` (delta: ADDED).

## Pilot answers to the brainstorm's open questions

1. **Early vs late decomposition** → hybrid, with a scale rule the pilot
   revealed: below multi-feat scale, the change's own tasks ARE the feats
   (the checker executed its tasks directly, no DAG); formal
   feature-decomposition engages for multi-feat changes. Early for the
   implemented target; late (from the release delta) for batched releases.
2. **Where release definitions live** → the aggregation repo (the pilot's
   "release" was the aggregation main line hosting the nightly runner; it
   is the only repo that sees every pin).
3. **Ordered deltas** → a later change modifying a requirement already
   modified by an active ratified change MUST reference it and sequence
   after it (first-ratified wins ordering).
4. **Tag vs branch** → branch while open, tag at promotion; the implemented
   target defaults to each affected repo's main line — release branches
   exist only for deliberately batched work.

## Contract surface (the change carries these)

- `code_surface:` and `target_release:` proposal front-matter; `none`
  (default) = doc-only, archives on landing (current practice codified).
- Realization archive gate: code_surface != none archives only on merge
  evidence on the implemented target (green run where a runnable surface
  exists).
- The invariant: promoted specs describe what the code does; active
  changes are approved intent not yet realized.
- Three branch kinds named: change folder (content), feat branches
  (Spec Kit), release branches (integration).
- codexFactory intake wiring: a ratified change with a code surface IS an
  approved engineering intent record for `approved-intent-intake`.

## Exit

One OpenSpec change: `add-release-realization-flow` (doc-only, ironically —
its own code_surface is none).
