# Feature Specification: Root-level governed-repo recognition, the aggregation parity lane, and the pin setter's dropped comment (P4b + 9.4)

**Feature Branch**: `024-root-governed-repo-recognition`

**Created**: 2026-08-27

**Status**: Draft

**Input**: User description: "P4b root-level governed-repo recognition: widen the notebook sweep and doc-health ideation routing by an explicit allowlist of root-level neutral products, wire the aggregation root-gitlink parity check into the doc-health lane, and fix the domain pin setter dropping preserved provenance comment blocks"

**Realizes**: `openspec/changes/split-openxwallet-repo` — `tasks.md` §11 (P4b,
11.1–11.5) and task **9.4**. Governing design decision **D11** (both halves: the
parity check is a MODE of openxFactory's verifier invoked from the aggregation's
doc-health lane; P4b widens by ALLOWLIST). Council authority:
`council-systems-architect.md` **concern 4** (VALID, MEDIUM, disposition
APPLIED). The third item is a defect found by **P5a.2** in
`scripts/set-domain-openxfactory-pin.py`.

## Why this feature exists

The proposal once claimed `xf-ideation-openxwallet` would derive automatically
once the repository existed. The Systems Architect measured the tree instead and
found two code sites that say otherwise, plus the empirical proof: **there is no
`xf-ideation-openavatar` book today**, five months into the ratified openAvatar
precedent. A root-level repository derives nothing automatically because both
sites recognize only `openxFactory` and `xFactories/<Name>`.

This feature closes the recognition gap, and it does the ONE thing the concern's
disposition asks that the concern itself could not: it measures the result. That
measurement changed the acceptance (see **Clarifications** below and
`evidence/acceptance-sweep.md`).

Task 9.4 rides along because it is the other half of D11 and lands in this
repository: the aggregation's doc-health lane is a REUSABLE workflow that lives
here, so the step and the test that pins it can only be written here.

The pin-setter fix rides along because P5a.2 found it while bumping
LedgerxFactory and it is the same class of defect as the other two — tooling that
cannot see something it is supposed to preserve.

## Clarifications

### Session 2026-08-27

- Q: allowlist or rule for admitting a root-level `.gitmodules` pin? → A:
  **ALLOWLIST** (D11, ratified). The rule is one line shorter and wrong: it would
  enrol the nine `installs/*` runtime repositories as governed ideation
  repositories, each deriving its own book and each becoming
  resolvable-without-materialization. Recorded in the authority's own comment
  block, `scripts/doc_health/corpus.py`.
- Q: one shared import, or two copies pinned by test? → A: **two copies pinned by
  test**, on this repository's own established rule. `sync-notebooklm-books.py`
  is a HYPHENATED standalone that cannot be imported, and its own suite loads it
  by file path with `scripts/` absent from `sys.path`, so an import of the
  package constant would work in production and fail in the suite. The precedent
  is explicit: `doc_health.recorded_rel` is "THE SAME RULE as
  `proposal-support.py`'s `manifest_rel`, and deliberately a second copy … pinned
  to each other by test". Task 11.3's requirement ("the SAME allowlist … so the
  notebook set and the routing set cannot disagree") is discharged by the pin,
  not by the import.
- Q: does task 11.4's acceptance hold once the widening lands? → A: **NO, and the
  widening is not why.** Measured over a tree with openXwallet at `wallet-v1.1`
  initialized: neither openXwallet nor openAvatar carries a single
  `brainstorm`/`staged` document (openXwallet: 3 ratified, 2 record, 2 standard;
  openAvatar: 2 draft, 1 record). Ideation-book membership is STATUS-DERIVED ONLY
  — `split-ideation-book-per-repo`: a book exists exactly when its repo has at
  least one brainstorm/staged document. So the book's absence had TWO causes and
  this feature removes one. See `evidence/acceptance-sweep.md`; the residual
  precondition is stated there and handed to the operator.
- Q: widen the doc-health lane's submodule init to the root products? → A: **no**,
  and the reason is a property of the check: `verify_aggregation` reads the
  RECORDED gitlink through `git ls-tree HEAD` / `git ls-files -s`, which answer
  without any checkout. Widening would add openAvatar's Flutter monorepo to every
  nightly for no check that reads it. The condition under which this becomes
  false is written into the workflow comment.

## Requirements

### FR-001 — The allowlist is declared once and is an allowlist

`scripts/doc_health/corpus.py` declares `ROOT_LEVEL_GOVERNED_PRODUCTS =
("openAvatar", "openXwallet")` as the AUTHORITY, with the allowlist-not-rule
decision and the `installs/*` counter-example recorded at the declaration.

### FR-002 — Ideation routing recognizes a root-level product

`doc_health.ideation_routing._governed_repo_ids` admits every allowlisted product
alongside `openxFactory` and `xFactories/<Name>`, UNCONDITIONALLY rather than
derived from `ctx.repo_paths` (which `discover_repos` can never fill with a
root-level product). A root-level product stops being classed `external` and
stops falling under the nightly-skip / strict-materialization path. The
convention-mode `known` set is widened by the same allowlist, because a bare-name
repository id has no pattern to be accepted by, and the refusal message names the
admitted products.

### FR-003 — The notebook sweep recognizes a root-level product

`sync-notebooklm-books.py` gains `pinned_root_product_paths()` (pinned AND
present, no suffix-heuristic fallback) and `governed_repo_paths()`, and the three
sites that must agree about what a repository is — `scan()`,
`session_repositories()` and `_out_of_scope_workbench_dirs()` — all read the
latter. A pinned-but-EMPTY root product is reported with a named remediation, not
silently treated as document-free.

### FR-004 — The two allowlists cannot disagree

A test in `tests/notebooklm/` reads the authority out of `corpus.py` and asserts
equality with the sweep's copy.

### FR-005 — The aggregation parity check is invoked from the doc-health lane

`.github/workflows/doc-health-reusable.yml`'s `prepare` job runs `python3
openxFactory/scripts/verify-openxwallet-pin.py --aggregation-root .` AFTER the
governed-submodule init, guarded on openxFactory declaring the nested gitlink at
this pin (the P3→P4 ordering), unconditional within the job, and not duplicated in
`finalize`. Every part of that is pinned by a test collected by the required
`pytest-suite`.

### FR-006 — The pin setter preserves the comment that protects a block

`preserved_subblocks` carries the comment/blank run attached to a preserved
sub-block through a rewrite. Attribution rule: a run belongs to what FOLLOWS it,
so a comment above a regenerated key still goes with that key.

## Out of scope, found while here

- `scripts/set-domain-openxfactory-pin.py:18` — `TAG_RE` is written
  `r"^v[0-9]+\\.[0-9]+\\.[0-9]+…"`. In a RAW string `\\.` is an escaped backslash
  followed by any character, so the pattern matches no real tag and
  `--openxfactory-ref v1.2.3` raises `ValueError` from `infer_ref_type`. Reported,
  not fixed: it is a separate defect with its own blast radius (every caller that
  pins by tag) and belongs in its own change rather than riding a comment fix.
- `doc_health.corpus.discover_repos` still enumerates `openxFactory` plus
  `xFactories/*` only, so aggregation doc-health does not sweep a root-level
  product's OWN documents. Out of §11's scope, which is about classifying
  references INTO such a product, not about sweeping it. Named here so the next
  reader does not mistake the silence for coverage.
