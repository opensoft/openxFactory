# Staged: Hybrid Canon Analysis Notebooks

Status: staged
Kind: process
Repository context: openxFactory
Source: live `test-canon` NotebookLM copy test, 2026-07-08.
Target capability: follow-on OpenSpec delta to `lifecycle-notebook-projection`
(delta: MODIFIED) if this process becomes canon.

## Purpose

Define the implementable process for creating one temporary NotebookLM hybrid
per idea analysis. A hybrid notebook combines one release-scoped Canon
notebook with exactly one brainstorm target or one organized staging folder,
so NotebookLM chat and Studio tools can reason about the idea against the
running system without mutating the canonical lifecycle notebooks.

## Decision

Create a separate hybrid NotebookLM notebook for each analysis target.

Do not add brainstorm or staged material directly to `xFactory - Canon`.
Do not use a single long-lived "all comparisons" notebook. The unit of work is
the tuple:

```text
hybrid = one canon release line + one idea target
```

The idea target is one of:

- a brainstorm file or folder under `ideation/brainstorm/`
- an organized staging folder under `ideation/staging/<topic>/`

The hybrid's output is always `L1 notebook synthesis` under the
NotebookLM Source Workspaces authority model. It may identify conflicts,
questions, candidate deltas, and implementation risks. It does not decide
policy, memory, release scope, or OpenSpec approval.

## Naming

Use a title that names both sides of the tuple:

```text
xFactory - Hybrid - <canon-release> - brainstorm/<topic>
xFactory - Hybrid - <canon-release> - staging/<topic>
```

Examples:

```text
xFactory - Hybrid - current - brainstorm/openspec-speckit-release-flow
xFactory - Hybrid - support/a - staging/doc-health-checks
```

If the Canon notebook is release-line scoped, use the same release slug the
Canon notebook uses, such as `support/a`, `release/b`, or `v1.4.x`. If the
current single Canon notebook is used, use `current`.

## Source Set

Each hybrid contains these source groups:

1. **Hybrid charter**: a pasted text source named
   `00 [hybrid charter] Read me first`. It names the Canon release, the idea
   target, and the L1 authority rule.
2. **Copied Canon source set**: every source from the selected Canon notebook,
   copied with its existing title preserved.
3. **Idea source set**:
   - brainstorm analysis: the selected `ideation/brainstorm/` file or every
     Markdown file in the selected brainstorm folder
   - organized analysis: every Markdown file in the selected
     `ideation/staging/<topic>/` folder

Idea source titles keep their epistemic prefix:

```text
[brainstorm] <repo>: <topic-or-path>
[staged] <repo>: <topic-or-path>
```

Do not include unrelated sibling brainstorms or staged topics. If two ideas
must be compared together, create a separate hybrid whose idea target is an
explicit comparison folder.

## Build Procedure

1. Choose the Canon release line that represents the running system being
   analyzed.
2. Create a new NotebookLM notebook with the naming convention above.
3. Add the hybrid charter as the first source.
4. Copy the Canon source set into the hybrid:
   - preferred future path: use NotebookLM duplicate/copy if the product adds
     it
   - current path: read each Canon source's indexed text and re-add it to the
     hybrid as a text source with the same title
5. Add the idea source set from the repository ref being analyzed.
6. Verify source count:

```text
expected = 1 hybrid charter + canon source count + idea source count
```

7. Run a baseline query:

```text
Using only your sources, what is the running-system canon for this topic?
Separate canon claims from idea claims and cite source titles.
```

8. Run an impact query:

```text
Using only your sources, what would the idea change, contradict, or leave
unresolved relative to the Canon release in this notebook?
```

9. Store any useful NotebookLM output as evidence only. If the output drives
   further work, move the human-reviewed conclusions into staging or an
   OpenSpec proposal with source references.

## Notebook-Originated Source Return Path

NotebookLM material returns to the repository by source membership, not by
manual title tagging.

- **Scratch notes** stay inside NotebookLM because they are notes, not sources.
  They are not imported into the repository and are not part of the governed
  lifecycle.
- **Imported material** is any new source in the analysis notebook. This
  includes notes that a human converted to sources, sources discovered through
  NotebookLM research, web sources, files, Drive sources, and any other source
  type NotebookLM exposes.

The origin folder determines where imported material returns:

```text
analysis notebook created from ideation/brainstorm/<topic>/
  -> import new sources to ideation/brainstorm/<topic>/

analysis notebook created from ideation/staging/<topic>/
  -> import new sources to ideation/staging/<topic>/
```

The codexFactory sync implementation imports those new sources with:

```bash
python3 xFactories/codexFactory/scripts/sync-notebooklm-books.py . \
  --import-new-sources "<hybrid-notebook-id-or-alias>" \
  --target-path "openxFactory/ideation/brainstorm/<topic>"

python3 xFactories/codexFactory/scripts/sync-notebooklm-books.py . \
  --import-new-sources "<hybrid-notebook-id-or-alias>" \
  --target-path "openxFactory/ideation/brainstorm/<topic>" \
  --apply
```

For organized pre-feature work, point `--target-path` at the staged topic:

```bash
python3 xFactories/codexFactory/scripts/sync-notebooklm-books.py . \
  --import-new-sources "<hybrid-notebook-id-or-alias>" \
  --target-path "openxFactory/ideation/staging/<topic>" \
  --apply
```

Dry-run lists the target files. `--apply` writes imported source material to:

```text
openxFactory/ideation/brainstorm/<topic>/notebooklm-ideas-YYYY-MM-DD.md
openxFactory/ideation/staging/<topic>/notebooklm-ideas-YYYY-MM-DD.md
```

Each imported file declares `Status: brainstorm` or `Status: staged`, records
the NotebookLM source id and source title, and carries `Authority: L1 notebook
synthesis`. Re-running the importer skips source ids that are already present
in ideation files.

The importer skips managed seed sources from the original hybrid build:
`00 [charter]`, `[brainstorm]`, `[staged]`, `[draft]`, `[ratified]`,
`[standard]`, `[spec]`, and `[grounding]`. Everything else that appears as a
NotebookLM source is treated as new source material for the origin folder.

## Current Product Constraint

The live `test-canon` test proved that a NotebookLM notebook created from
copied Canon source text can be queried successfully and can cite those copied
sources. It did not prove that NotebookLM has a native notebook duplicate
operation.

Until NotebookLM exposes native notebook duplication or notebook-as-source,
hybrids are copy-like derived notebooks:

- source text can be copied from Canon and re-added to the hybrid
- original NotebookLM source IDs, source type, and freshness metadata are not
  preserved
- copied sources become text sources in the hybrid
- the repository and release tag remain the durable source of truth

This is acceptable for temporary idea analysis. It is not acceptable as the
canonical Canon sync mechanism.

## Record Keeping

Track active hybrids as external source workspace records when their outputs
are used outside ad hoc chat. The record may live beside the staged topic or
in a local operator register until the process is ratified.

Recommended record shape:

```yaml
kind: external_source_workspace
schema_version: 1
id: workspace-xfactory-hybrid-<canon-release-slug>-<topic-slug>
provider: notebooklm
provider_notebook_id: <notebooklm-id>
owner_layer: domain_hermes
scope:
  domain_id: xfactory
  client_id: null
  customer_id: null
purpose: hybrid analysis of <idea-target> against Canon <canon-release>
default_authority_level: L1_notebook_synthesis
created_at: "<iso-8601>"
base_canon:
  title: "xFactory - Canon - <canon-release>"
  release_ref: "<branch-or-tag>"
  provider_notebook_id: <canon-notebooklm-id>
idea_target:
  status: brainstorm | staged
  repo: openxFactory
  path: ideation/<brainstorm-or-staging>/<topic>
retention:
  disposition: temporary_analysis
  delete_or_refresh_when:
    - canon release changes
    - idea source set changes materially
    - analysis has been moved into an OpenSpec proposal or rejected
```

## Refresh And Retirement

Hybrids are derived state. Rebuild rather than patch them when either side of
the tuple changes materially:

- Canon branch, tag, or source set changes
- the brainstorm file/folder is rewritten
- the staged topic adds, removes, or retitles Markdown sources
- the analysis shifts to a different release line

Retire the hybrid after the idea is rejected, deferred, or promoted into an
OpenSpec proposal. Keep only the reviewed conclusions and the workspace record
needed to trace any NotebookLM-derived claims.

## Ready For Review Gate

Changes to this process or to its codexFactory implementation are ready for
proposal review only after the checks run in this order:

1. Implement or edit the affected docs and tooling.
2. Run local implementation tests for the touched tooling.
3. Run the owning repo's validation suite.
4. Run OpenSpec validation for the affected proposal/spec corpus.
5. Mark the proposal/change ready for review only if all prior checks pass.

For the current NotebookLM importer, the concrete sequence is:

```bash
cd xFactories/codexFactory
python3 -m unittest discover -s tests/notebooklm -q
bash scripts/validate-docs.sh

cd ../../openxFactory
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

OpenSpec validation checks proposal/spec structure. It does not replace
implementation tests for importer behavior or repo validation for generated
artifacts, schemas, and self-gates.

## Exit

If this process becomes standard, ratify it through an OpenSpec change against
`lifecycle-notebook-projection`. That change should decide:

- whether hybrid workspace records are committed or kept as local derived
  state
- whether codexFactory owns a script for building hybrids
- whether hybrid cleanup is manual, time-based, or tied to proposal/archive
  gates
- whether release-scoped Canon notebooks are required before hybrid creation
