## Context

The public entry point `scripts/sync-notebooklm-books.py` currently combines
provider invocation, corpus discovery, lifecycle reconciliation, source import,
workbench cleanup, session synchronization, session sweeping, hosting-profile
enforcement, parity reporting, and CLI orchestration. Its primary test module
loads the hyphenated script dynamically and covers those same concerns in one
file. The behavioral suite is green, but the two files exceed the repository's
module-size discipline and hide type and lint defects at important boundaries.

The extraction must preserve the existing executable path and flags because
operator documentation and automation call that surface directly. It must also
preserve the optional dashboard integration's current lazy-loading and failure
semantics, and it must keep profile binding fail-closed across every `nlm`
subprocess invocation.

## Goals / Non-Goals

**Goals:**

- Make provider rows, manifest state, profile state, and session adapters
  explicit typed boundaries.
- Split production and tests by responsibility with an acyclic dependency
  direction and focused files.
- Preserve CLI behavior and direct helper compatibility during extraction.
- Establish one reproducible scoped command that enforces Ruff,
  basedpyright, and the repository programming checker.
- End with zero findings on the scoped NotebookLM sync surface.

**Non-Goals:**

- Changing any lifecycle projection requirement or provider mutation policy.
- Adding a new third-party runtime dependency.
- Automating NotebookLM authentication, sharing, or migration acts.
- Expanding quality enforcement to unrelated Python surfaces with known debt.
- Refactoring `scripts/ideation_dashboard/` beyond typed adapter boundaries.

## Decisions

### 1. Keep the executable as a compatibility wrapper

`scripts/sync-notebooklm-books.py` remains the public entry point and owns
argument parsing, mode precedence, manifest flush orchestration, and exit
semantics. Implementation moves under `scripts/notebooklm_sync/`. During the
split, the wrapper re-exports helpers currently imported by tests.

Alternative considered: replace the script with `python -m notebooklm_sync`.
Rejected because it would change documented and automated invocation paths.

### 2. Extract in dependency order

The package uses this direction:

```text
constants/models
  -> nlm_client, corpus
  -> imports, lifecycle, hosting
  -> workbench_sweep, sessions, session_sweep, parity
  -> CLI wrapper
```

Shared records live in `models.py`; corpus discovery never imports provider
code; `nlm_client.py` is the sole subprocess/profile-state owner. Session Git
commit logic lives with sessions, while import planning consumes only typed
session ports and shared records. This prevents the current conceptual
imports/sessions seam from becoming a module cycle.

Alternative considered: one package module per current function cluster with
cross-imports as needed. Rejected because it would preserve hidden state and
create import cycles.

### 3. Parse untrusted JSON once

The `nlm` boundary returns a closed JSON value union. Provider notebook and
source rows are parsed into typed records before business logic consumes them.
Internal code does not carry raw unparameterized dictionaries. Invalid
required fields fail at the provider boundary with an explicit error.

Alternative considered: annotate existing dictionaries broadly. Rejected
because it retains unknown-member propagation and permits malformed rows to
reach mutation logic.

### 4. Keep process profile state in one typed owner

Profile binding and config cache state move to `nlm_client.py` with lowercase
mutable names and an explicit reset hook used by tests. Every provider command
re-checks the bound profile. Hosting enforcement binds before any provider
operation, including parity and cleanup modes.

Alternative considered: pass profile through every function. Rejected for this
change because it would widen nearly every public helper signature and increase
behavioral risk without improving the external contract.

### 5. Split tests along production responsibilities

The monolithic test module becomes focused source-import, lifecycle, session,
session-import, session-sweep, and hosting modules. A non-collectable support
module owns the dynamic wrapper loader and immutable builders. Hosting-only
helpers remain separate, and mutable fakes are created per test. No test module
imports another `test_*.py` module.

Both pytest collection and `unittest discover` remain supported. The suite must
retain at least the pre-split collected tests and subtests; a count decrease is
a failure requiring explanation, not an accepted cleanup.

### 6. Gate only the declared surface

A checked-in command runs Ruff and basedpyright over the wrapper, extracted
package, and NotebookLM tests, then runs the repository programming checker on
the same declared paths. It does not baseline or suppress existing findings.
The gate is introduced only after the scoped surface is clean, so its standing
baseline is zero.

## Risks / Trade-offs

- [Risk] Moving profile state breaks fail-closed drift detection. → Keep one
  state owner and run profile-drift tests after its extraction.
- [Risk] Eager dashboard imports make lifecycle-only modes unavailable. → Keep
  optional adapters lazy and test imports without dashboard execution.
- [Risk] Session import extraction changes branch/worktree ownership. → Keep
  lock, branch assertion, explicit staging, and `commit(only=...)` in one
  session module and preserve focused tests.
- [Risk] Test splitting accidentally reduces discovery. → Compare pytest
  collection and run both pytest and unittest discovery.
- [Risk] Mechanical lint changes alter exception behavior. → Fix broad-catch
  findings only after boundary-specific tests establish intended degradation or
  refusal semantics.
- [Trade-off] Compatibility re-exports keep the wrapper wider than a pure CLI
  facade. They are retained to avoid an unrelated public-helper break and may
  be removed only by a later governed change.

## Migration Plan

1. Add the scoped gate command in report mode and record its exact failing
   baseline without suppressions.
2. Extract constants/models and the provider boundary while retaining wrapper
   re-exports; run focused tests after each stateful seam.
3. Extract corpus, imports, lifecycle, hosting/parity, workbench, sessions, and
   session sweep in dependency order.
4. Split the test module without changing test bodies except for imports,
   shared support, and type-safe fakes.
5. Resolve remaining typed and lint findings, then enable the zero-finding gate.
6. Run full NotebookLM, doc-health, and strict OpenSpec validation plus manual
   CLI `--help`, dry-run, and invalid-input probes.

Rollback is commit-by-commit: each extraction preserves wrapper imports and can
be reverted independently without data migration.

## Open Questions

None. Observable behavior remains governed by the existing
`lifecycle-notebook-projection` capability; this change governs only the code
quality and compatibility evidence around its implementation.

## Recovery amendment, 2026-10-03

Use current main as the compatibility baseline. Preserve ID-keyed readiness
polling and settled rename checks, digest equality before stray adoption,
governed root-product discovery and title disambiguation, workspace record
updates, the common hosting declaration order, and session host registration
and scope checks. Extend the original package boundaries where needed to
retain focused modules. Preserve both snapshots' meaningful hermetic test
scenarios; collection counts alone do not establish equivalent coverage.

The original programming checker is recoverable from local oh-my-opencode
history (blob `4270ef321d4303ce90ed5afefe2460944458e9b6`). Use it through
`PROGRAMMING_CHECKER` when the normal installation is unavailable. Do not skip
it or substitute a permissive checker. Speckit owns current realization tasks.


### Recovery wiring and evidence (2026-10-03)

The historical executable remains `scripts/sync-notebooklm-books.py`; it is a
relative symlink to `scripts/sync_notebooklm_books.py`, the normally named Python
module. The quality command resolves that alias and checks the same implementation
with every rule enabled. Neither a naming suppression nor a second wrapper copy
is introduced. Public imports, command arguments and executable behavior remain
covered through the historical path.

The scoped command pins Ruff 0.16.10 and basedpyright 1.40.1. Its configuration
includes only the declared surface. An explicitly named missing programming
checker refuses immediately. The recovered original checker remains an external
tool, with its Git blob identity and verification procedure recorded in
`realization-evidence.md`.

Shared test helpers use the repository namespace package. Guarded unittest now
adds that repository root and performs the same optional-leg host registration as
pytest before discovery. Both runners retain the existing provider refusal guards.
The required pytest workflow supplies pinned uv tooling for the type-gate
regression and moves its exact skipped count from six to four: the two stale
pre-shed NotebookLM module probes now run against the pinned packages. No other
stand-down or named required verdict is removed.

The full-suite compatibility audit additionally preserves the retained carve
entry point and its 137-method floor. That file contains typed scenario
forwarders; focused non-collectable case modules hold the unchanged assertion
bodies and setup. Each scenario is collected once by both supported runners.
Literal callback bindings preserve the manifest retirement audit while keeping
the public loader patchable. The sweep fixture reads the neutral output boundary
through a checked save protocol, without type or size exemptions.

The per-change sweep ledger requires an actual moving PR reference. Keep its
update pending until that PR exists. Publication can expose the verified code
commit first, then submit the already prepared governance packet and seed its
ledger with the real PR number before final exact-head review and landing. The
recorded pre-push baseline gate still requires its owner decision; this order
does not authorize bypassing it or any required final check.
