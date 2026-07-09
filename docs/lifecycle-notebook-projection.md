# Lifecycle Notebook Projection

Status: standard
Kind: process
Backed by: [openspec/specs/lifecycle-notebook-projection/spec.md](../openspec/specs/lifecycle-notebook-projection/spec.md) (promoted from the archived add-lifecycle-notebook-projection change)
Repository context: openxFactory
Purpose: define the full NotebookLM workflow for the governance corpus — how
document lifecycle states project into derived notebooks, how those notebooks
are framed against the running system, and how the sync is operated.

Authority model: [NotebookLM Source Workspaces](notebooklm-source-workspaces.md).
Lifecycle states: [Document Lifecycle](document-lifecycle.md).
Reference implementation: `codexFactory/scripts/sync-notebooklm-books.py`.

## 1. The Books

Three NotebookLM notebooks project the family's governance corpus by
lifecycle state. Membership is always derived from `Status:` headers —
never hand-curated.

| Book | Statuses projected | Answers questions like |
| --- | --- | --- |
| `xFactory — Ideation` | `brainstorm`, `staged` | What are we considering? How do ideas differ from the system today? |
| `xFactory — Working Drafts` | `draft` | What is the intended design? Where do drafts conflict? |
| `xFactory — Canon` | `ratified`, `standard`, promoted `openspec/specs/*/spec.md` | What is governed today? What would this idea change? |

Excluded by design: `record` (immutable evidence), `superseded`, `retired`.
Scope: `openxFactory/` and `xFactories/*/`, skipping `.git`, `installs/`
(nested submodules), and `openspec/changes/` (change artifacts have their own
lifecycle; promoted specs are included from `openspec/specs/`).

## 2. Source Titles

Titles are the authority signal chat sees on every citation:

```text
[<status>] <repo>: <file stem>          e.g. [draft] MedxFactory: care-organization-hermes
[spec] openxFactory: <capability>        promoted capability specs
[grounding] openxFactory: <stem>         grounding set (section 3)
00 [charter] Read me first               workspace charter (section 4)
```

Title rule for ambiguous stems: when the file stem is `README` (or otherwise
non-unique within a repo), the title uses `<parent-dir>/<stem>` — e.g.
`[ratified] AdxFactory: ideation/README`.

## 3. Grounding Set

Every book carries these three docs under `[grounding]` titles regardless of
their own lifecycle state, so chat can compare any idea against the system's
shape:

- `docs/document-lifecycle.md`
- `docs/terminology-and-repo-topology.md`
- `docs/architecture.md`

A grounding doc also appears in its own state's book under its `[status]`
title; the duplication is intentional.

## 4. Charter And Chat Framing

Each book's first source is a charter (`00 [charter] Read me first`) stating:
the book is a derived projection; what each title prefix means; and that per
the source-workspaces model all notebook output is **L1 notebook synthesis**
— it may raise claims but never decides policy, memory, gates, or
customer-facing output.

Each book's chat is configured (`nlm chat configure <book> --goal custom`)
with the running-system framing: `[brainstorm]`/`[staged]` are ideas on top
of the running system, `[standard]`/`[spec]`/`[ratified]` describe the system
as governed, `[draft]` is intended but unratified; answers must label each
claim's origin and describe conflicts as proposed change from current, never
as fact.

Charter text and chat prompt are contract surface: they live in the reference
implementation as constants and change only through an OpenSpec delta to the
`lifecycle-notebook-projection` capability.

## 5. Sync Behavior

The sync reconciles desired state (repo scan) against actual state (notebook
source list), matched by title:

- **Add**: repo doc projected to a book it is not in.
- **Delete**: managed source (title starts `[` or is the charter) present in
  a book but no longer projected there — including hand-added strays.
- **Update**: repo content changed (SHA-256 tracked in the manifest) →
  delete + re-add.
- **Stage transition**: a status change is a delete from the old book plus an
  add to the new one on the next sync.

Operational properties: dry-run by default (`--apply` to execute); idempotent
(a no-op resync reports zero changes); rate-limited ~2s per source operation;
manifest at `<workspace-root>/.claude/nlm-sync-manifest.json` (intentional
local derived state — not committed; safe to delete, next apply rebuilds it).

## 6. Operator Runbook

```bash
# 1. Authenticate (host shell with a browser; ~20 min session lifetime).
#    Credentials land in ~/.notebooklm-mcp-cli/, shared with containers
#    that mount the same home. WSL without a Linux browser: nlm login --wsl.
nlm login

# 2. Preview, then apply, from the workspace root.
python3 xFactories/codexFactory/scripts/sync-notebooklm-books.py . 
python3 xFactories/codexFactory/scripts/sync-notebooklm-books.py . --apply

# 3. Books are aliased: xf-ideation, xf-drafts, xf-canon (tags: xfactory,lifecycle).
nlm source list xf-canon
nlm notebook query xf-canon "What owns gate structure?"
nlm cross query "Where do drafts contradict canon?" --tags "xfactory"

# 4. Artifacts (async on Google's side).
nlm mindmap create xf-ideation --confirm
nlm report create xf-canon --format "Briefing Doc" --confirm
nlm studio status xf-canon
```

Cadence: manual after meaningful doc changes for now; intended to run from
the nightly doc-health action once that pipeline is implemented (see
`ideation/staging/doc-health-pipeline/`).

## 7. Workspace Records

The three books are registered as `external_source_workspace` records in
[examples/lifecycle-notebook-workspaces.yaml](../examples/lifecycle-notebook-workspaces.yaml),
per the source-workspaces record model.

## 8. Known Limitations

- NotebookLM source-count limits apply per notebook; the Working Drafts book
  is the largest and should be watched as the corpus grows (split by repo if
  it approaches the plan's cap).
- nlm sessions expire in ~20 minutes; CI use needs an auth strategy before
  the nightly integration.
- Matching is title-based; retitling rules (section 2) therefore cause a
  delete + re-add cycle on the affected sources.
- Notebook synthesis can be stale between syncs; the repo is always the
  system of record.
