# Tasks: 024-root-governed-repo-recognition

**Feature**: `024-root-governed-repo-recognition` · **Branch**: `024-root-governed-repo-recognition`

**Realizes**: `openspec/changes/split-openxwallet-repo` `tasks.md` §11 (11.1–11.5)
and task 9.4. Each task names the item it discharges.

## Phase 1: The allowlist and its two sites (§11.1–11.3)

- [X] T001 §11.1/11.2 authority `ROOT_LEVEL_GOVERNED_PRODUCTS = ("openAvatar",
      "openXwallet")` in `scripts/doc_health/corpus.py`, beside `discover_repos`
      and `GOVERNED_ROOTS` — the module that already owns what repositories an
      aggregation has. The allowlist-not-rule decision (D11) and the `installs/*`
      counter-example are recorded at the declaration.
- [X] T002 §11.2 `doc_health.ideation_routing._governed_repo_ids` unions the
      allowlist UNCONDITIONALLY (not from `ctx.repo_paths`, which
      `discover_repos` can never fill with a root-level product) and tolerates an
      allowlisted name in `repo_paths` without prefixing it `xFactories/`.
- [X] T003 §11.2 rider: `_known_repositories`' CONVENTION fallback widened by the
      same allowlist and `_repository_unknown_reason`'s message updated. Without
      it openxFactory's own `--single-repo` self-gate — which runs in exactly that
      mode — reports a sound reference into `openXwallet` as an unknown
      repository. A bare-name id has no pattern to be accepted by.
- [X] T004 §11.1 `sync-notebooklm-books.py`: `pinned_root_product_paths()`
      (pinned AND present; no suffix-heuristic fallback; a pinned-but-EMPTY
      product prints a named remediation instead of reading as document-free) and
      `governed_repo_paths()`.
- [X] T005 §11.1 `scan()`'s base list reads `["openxFactory",
      *governed_repo_paths(root)]`.
- [X] T006 §11.1 rider: `session_repositories()` moved to the same finder — its
      docstring CLAIMS "deliberately the same repo set `scan()` walks", and
      widening `scan()` alone would have quietly falsified it.
- [X] T007 §11.1 rider: `_out_of_scope_workbench_dirs()` likewise. The widening
      is the SAFE direction here: a workbench dir this misses is a live manifest
      the sweep cannot see, and the sweep DELETES the `xf-wb-*` notebook no live
      manifest binds.
- [X] T008 §11.3 the two allowlists pinned to each other by test
      (`tests/notebooklm/…::test_the_allowlist_matches_the_doc_health_authority`),
      on this repository's established rule for a hyphenated standalone that
      cannot be imported. See `spec.md` Clarifications for why not one import.

## Phase 2: Unit tests for the widening

- [X] T009 §11.1/11.2 six tests in `tests/doc-health/test_ideation_routing.py`:
      the admitted set, admission with no checkout in scope, no `xFactories/`
      prefix on a root product, `installs/*` never admitted, convention-mode
      recognition + the named refusal, and the authority's identity.
- [X] T010 §11.1 thirteen tests in `tests/notebooklm/test_sync_notebooklm_books.py`
      (`RootLevelGovernedProductTests`): allowlist parity, pinned+present,
      present-but-unpinned, pinned-but-absent, `installs/*` excluded, no
      `.gitmodules`, the uninitialized WARN, ordering, the derived
      `ideation-openxwallet` book with alias and title, the openAvatar twin,
      status-derived membership, `session_repositories`, workbench dirs.

## Phase 3: The aggregation parity lane (§9.4)

- [X] T011 9.4 step "Verify openXwallet root-gitlink parity" in
      `.github/workflows/doc-health-reusable.yml`'s `prepare` job, AFTER "Init
      governed submodules only", running `python3
      openxFactory/scripts/verify-openxwallet-pin.py --aggregation-root .`,
      guarded on openxFactory declaring the nested gitlink at this pin.
- [X] T012 9.4 the submodule init was deliberately NOT widened, and the reason —
      `verify_aggregation` reads the RECORDED gitlink via `ls-tree`/`ls-files`
      and needs no checkout — is written into the step, along with the condition
      that would make it false.
- [X] T013 9.4 `tests/openxwallet_pin/test_aggregation_lane_wiring.py`: eight
      tests pinning the command, the flag, the order relative to the init, the
      guard and its spoken skip, unconditionality within the job,
      non-duplication in `finalize`, and that the flag the workflow passes is a
      flag the script still has.

## Phase 4: The pin setter's dropped comment (P5a.2 finding)

- [X] T014 `preserved_subblocks` buffers comment/blank runs and flushes them when
      a preserved key follows; a trailing run inside a preserved sub-block is
      held back and attributed to the next key.
- [X] T015 `tests/domain_pin_setter/test_set_domain_openxfactory_pin.py`: twelve
      tests over LedgerxFactory's `stack.yaml` shape — the comment survives, it
      still precedes `promoted_from:`, the block survives verbatim, the pin IS
      rewritten, nothing outside `xfactory:` moves, idempotence, the attribution
      rule in three directions, and a self-skipping fixture-drift guard against
      the live sibling checkout.
- [X] T016 Regression proven empirically against `origin/main`'s function over the
      same fixture: **PRE-FIX preserved the comment: False** / preserved
      `promoted_from`: True. The defect and the fix are both measured, not
      asserted.

## Phase 5: Acceptance and validation

- [X] T017 §11.4 acceptance sweep, measured over a scratch root with openXwallet
      at `wallet-v1.1` initialized. Recorded in
      `evidence/acceptance-sweep.md`. **The headline: the widening is real (0 → 4
      openXwallet documents, 0 → 2 openAvatar) but §11.4's stated acceptance is
      NOT reachable today** — neither root product carries a single
      brainstorm/staged document, and ideation-book membership is status-derived.
      Proven both ways: no book from the real tree; the book with the exact
      required alias and title once one brainstorm document exists.
- [X] T018 §11.4 `--apply` NOT run, for three recorded reasons (no book to
      create; an apply from a scratch root would reconcile the REAL shared books
      against a partial tree; the live aggregation has no root gitlink until P4).
      `nlm notebook list` answers in this shell, so auth was not the blocker. The
      operator's ordered sequence is in `evidence/acceptance-sweep.md`.
- [X] T019 §11.5 rollback: revert. The books are DERIVED — a removed repository
      id simply stops deriving — and the parity step's guard makes its removal a
      no-op on any tree without the nested gitlink. Nothing in this change
      migrates state.
- [X] T020 `openspec validate --all --strict`: **75 passed, 0 failed**.
- [X] T021 `doc-health.py --single-repo .`: **5 critical, 7 error, 41 warning, 11
      info** — byte-identical to the `origin/main` baseline run at `b5fb03f3`.
      **No new findings.**
- [X] T022 `pytest tests/ -q -m "not postgres"` — see `evidence/validation.md`.
