# Prepared contract fragment: the codexFactory row of `contracts/policies/repository-identity.yaml`

**Feature**: `030-realize-codexfactory-repository-identity` | **Date**: 2026-09-08
**Realizes**: packet tasks **1.1, 1.2, 1.3, 1.4**
**State**: **PREPARED, NOT APPLIED.** The target file does not exist.

## Why this is a fragment and not a diff

`contracts/policies/repository-identity.yaml` is **absent from openxFactory
`main`** at `e8021fed`. Packet task 1.1 says, in as many words, *"Do not create
the file here"* — `adopt-medxsoft-repository-identity` authors it at ITS task
1.1 and registers it in `contracts/manifest.yaml` at its task 1.3, and
*"authoring it twice would produce two files claiming to be the mapping."*

That exemplar is active on `main`, `Status: draft`, and unrealized. Packet task
0.2's conditional — *"if that change is archived or withdrawn … task 1.1 changes
from 'add a row' to 'author the file'"* — does **not** fire, because it is
neither archived nor withdrawn. So the instruction stands and this row waits.

**Two independent gates hold this fragment**, and both must lift:

1. **BLOCKED** — the exemplar's task 1.1 must land the file (and its task 1.3 the
   manifest entry), or the convener must amend task 1.1 to author the file here.
2. **GATED at runbook step 1.2** — `transferred_on` records a completed act, so
   the row cannot be finished before the transfer is confirmed.

## The row, ready to apply

Appended to the exemplar's `transfers:` list, beside its two 2026-08-26 rows.
Shape mirrors `contracts/policies/layer-vocabulary.yaml`'s sibling conventions.

```yaml
  # ── opensoft/codexFactory -> codeXfactory/codexFactory ──────────────────────
  # Ratified by: adopt-codexfactory-repository-identity (2026-09-07, Brett Heap,
  # convener, verbatim "accept all [A] and ratify 763"). Canonical spelling ruled
  # by OQ-6 at 2026-09-08T03:51Z: codeXfactory/codexFactory, matching the GitHub
  # organization and repository exactly.
  - former: opensoft/codexFactory
    current: codeXfactory/codexFactory
    transferred_on: "<FILL FROM RUNBOOK STEP 1.2>"   # the date the transfer was CONFIRMED, never before
    redirect: >-
      GitHub redirects the former owner to the current one, and STOPS the moment
      `opensoft` reuses the name. It may: `opensoft` remains an active
      organization and still holds the `opensoft/xFactory` aggregation
      repository, which names this repository in eight workflow `uses:` paths.
      A frozen former spelling is therefore resolved BY LOOKUP IN THIS FILE and
      never by the provider redirect.
    owner_case: >-
      This estate compares the owner segment CASE-SENSITIVELY. GitHub does not.
      `codeXfactory` is the canonical spelling (OQ-6); `codexfactory` and
      `CodeXFactory` resolve at the provider but are not this estate's spelling
      and MUST NOT be written into governed content.
    derived_container_namespace: >-
      ghcr.io/codexfactory/codexfactory — GHCR LOWERCASES the owner segment, so
      the container namespace derived from this identity is spelled
      `codexfactory` regardless of the organization's display case. This is a
      DERIVED, TOOL-IMPOSED spelling of the SAME identity, recorded here rather
      than left for a fail-closed resolver to discover (OQ-6, ruled
      2026-09-08T03:51Z).
    redirect_does_not_cover:
      - >-
        reusable-workflow `uses:` paths — a cross-organization call to a PRIVATE
        repository's reusable workflow is not covered by any redirect and is an
        outright break (OQ-1; mitigated by Enterprise membership at access level
        `enterprise`, verified `plan=enterprise` 2026-09-07T16:41:04Z).
      - >-
        container package namespaces — `ghcr.io/<org>/...` is per-organization
        and does not redirect at all (OQ-4).
      - >-
        federated-credential subject strings — e.g.
        `repo:<owner>/<repo>:environment:<name>`; an OIDC subject is matched
        literally and no redirect applies.
```

## What the row does NOT do

- It does **not** create the file, and it does **not** add a
  `contracts/manifest.yaml` entry: task 1.4 records that the entry and its
  `consumption_rule` are the exemplar's task 1.3, and that adding a row does not
  add an entry.
- It **does** move the policy's per-file `sha256` in `contracts/manifest.yaml`,
  which is **recomputed, never hand-edited** (task 1.4).
- It does not widen, restate or reinterpret the exemplar's two existing rows.
