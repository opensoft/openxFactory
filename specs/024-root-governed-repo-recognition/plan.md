# Implementation Plan: 024-root-governed-repo-recognition

**Feature**: `024-root-governed-repo-recognition` · **Spec**: `spec.md`

**Realizes**: `split-openxwallet-repo` `tasks.md` §11 (P4b) + task 9.4; design
**D11**; council `council-systems-architect.md` concern 4.

## Approach

Three independent defects, one pull request, because all three are openxFactory's
and two of them (11.1, 11.2) are required by task 11.3 to land together.

### 1. The allowlist (FR-001, FR-004)

Authority in `scripts/doc_health/corpus.py` — the module that already owns "what
repositories does this aggregation have" (`discover_repos`, `GOVERNED_ROOTS`).
`ideation_routing.py` imports it in-package (`from .corpus import …`, no cycle:
`corpus` imports only `.lines`). `sync-notebooklm-books.py` carries a deliberate
second copy, pinned by test — the repository's established rule for a hyphenated
standalone (see `spec.md` Clarifications).

### 2. The two widened sites (FR-002, FR-003)

`_governed_repo_ids` unions the allowlist unconditionally. The sweep grows two
functions rather than one so the "pinned AND present" discipline and the
three-site agreement are separately nameable, and the three call sites that had
`pinned_factory_paths(root)` inline move to `governed_repo_paths(root)` — one of
which (`session_repositories`) had the agreement written into its docstring as a
claim, and widening `scan()` alone would have falsified it.

`_known_repositories`' convention fallback is widened too, one line, because a
bare-name id has no pattern to be accepted by and openxFactory's own
`--single-repo` self-gate runs in exactly that mode.

### 3. The lane wiring (FR-005)

A step in `prepare` after the init, guarded exactly as the init is guarded, and a
test that pins the command, the flag, the order, the guard, the unconditionality
and the non-duplication — plus that the flag the workflow passes is a flag the
script still has, so a pinned invocation cannot outlive its option.

### 4. The pin setter (FR-006)

`preserved_subblocks` buffers comment/blank runs and flushes them when a
preserved key follows. A trailing run inside a preserved sub-block is held back
rather than swallowed, so it is attributed to the next key.

## What was deliberately NOT done

- **The submodule init was not widened.** `verify_aggregation` reads the RECORDED
  gitlink and needs no checkout; widening adds openAvatar's Flutter monorepo to
  every nightly for no reader. The condition that makes this false is in the
  workflow comment.
- **`discover_repos` was not widened.** Out of §11's scope (see `spec.md`).
- **`TAG_RE` was not fixed.** Reported (see `spec.md`).
- **`--apply` was not run.** See `evidence/acceptance-sweep.md` for why the
  scan derives no `ideation-openxwallet` book to create, and why an apply from a
  scratch root would reconcile the REAL shared books against a partial tree.

## Validation

`openspec validate --all --strict`; `doc-health.py --single-repo .` against an
origin/main baseline run; the full `pytest tests/ -q -m "not postgres"` suite;
and a measured before/after sweep over a tree with openXwallet initialized.
Results in `evidence/`.
