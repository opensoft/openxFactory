# Design: Lifecycle Notebook Hybrid Imports

## Decision 1: The origin folder routes all imports

The operator supplies the origin folder when importing new sources from a
hybrid notebook. That folder is the notebook's purpose and the destination for
all new sources:

```text
ideation/brainstorm/<topic>/ -> Status: brainstorm
ideation/staging/<topic>/    -> Status: staged
```

This avoids relying on NotebookLM source titles for routing. In real use,
NotebookLM often names converted notes or discovered sources itself. Requiring
manual retitling would make the workflow fragile and would turn source naming
into a hidden gate. The explicit `--target-path` is the gate: it says which
analysis object this notebook represents.

## Decision 2: Source membership, not notes, is the return boundary

NotebookLM notes are useful scratch space, but they are not imported. A note
enters xFactory only after a human converts it to a NotebookLM source. Sources
added through research, web URLs, files, Drive, or other NotebookLM mechanisms
are already sources and therefore eligible.

This rule gives operators a simple mental model:

```text
inside NotebookLM note pane = scratch
inside NotebookLM source set = pull back to the origin folder
```

All imported material is still L1 notebook synthesis unless independently
verified and promoted through the normal lifecycle.

## Decision 3: Skip seed sources by managed title prefixes

Hybrid notebooks are built with a seed set: the copied Canon release line,
grounding context, charter, and the origin idea sources. Those sources are
context, not new material. The importer skips the managed source titles used by
the lifecycle projection:

```text
00 [charter]
00 [hybrid charter]
[brainstorm]
[staged]
[draft]
[ratified]
[standard]
[spec]
[grounding]
```

Everything else in the NotebookLM source set is treated as new source material.
This is intentionally broad so web research and converted notes do not need a
special title convention.

## Decision 4: Source ids provide idempotence

Every imported entry records the NotebookLM source id. Subsequent imports scan
existing ideation files for those ids and skip already imported sources. The
importer appends new entries to the dated `notebooklm-ideas-YYYY-MM-DD.md`
file under the origin folder.

This keeps the import command repeatable and avoids creating a sidecar state
file that would drift from the repository. If a NotebookLM source is edited or
recreated with a new source id, it imports as a new entry; the human reviewer
then decides whether to merge, supersede, or discard the earlier entry.

## Decision 5: Imported material is governed ideation, not canon

Imported source material is written as:

```text
Status: brainstorm | staged
Kind: reference
Authority: L1 notebook synthesis
Source workspace: <notebook id or alias>
NotebookLM source id: <source id>
NotebookLM source title: <source title>
```

It does not become `ratified` or `standard` by import. The normal gates still
apply: brainstorm material can be organized into staging, staging can become
an OpenSpec proposal, and only approved/promoted OpenSpec artifacts can become
canon.

## Decision 6: Keep explicit export tags as compatibility, not the main path

The implementation may continue to support `[export:brainstorm]` and
`[export:staged]` title tags as a compatibility path, but the ratified workflow
does not require them. The primary operator path is `--import-new-sources` with
an explicit origin `--target-path`.

## Decision 7: Review readiness requires implementation tests before OpenSpec

OpenSpec validation proves proposal/spec shape, not importer behavior. Changes
to hybrid imports are ready for review only after:

1. local implementation tests for the touched tooling pass;
2. the owning repo's validation suite passes;
3. OpenSpec validation passes.

This ordering catches broken importer behavior before treating the proposal as
ready.
