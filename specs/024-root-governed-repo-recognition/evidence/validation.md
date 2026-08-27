# Validation

**Status**: record

**Recorded**: 2026-08-27 · **Feature**: `024-root-governed-repo-recognition`

## `openspec validate --all --strict`

**75 passed, 0 failed (75 items)** — including `change/split-openxwallet-repo`
after this feature ticked §9.4 and §11.1–11.3/11.5 and recorded the §11.4
finding.

## `doc-health.py --single-repo .`

| run | tree | result |
| --- | --- | --- |
| baseline | `origin/main` @ `b5fb03f3` (a detached worktree) | 5 critical, 7 error, 41 warning, 11 info |
| this branch | `024-root-governed-repo-recognition` | 5 critical, 7 error, 41 warning, 11 info |

Identical. **No new findings**, and "New regressions vs previous report: 0" in
both.

## The parity check, exercised three ways (§9.4)

A verifier that has never refused is not known to work — the same standard §3.30
applied to the consumer gate. Three scratch aggregation roots, each a real git
repository carrying (or not carrying) a `160000` gitlink at path `openXwallet`,
with openxFactory's own nested submodule initialized at the pin:

| aggregation root records | result | exit |
| --- | --- | --- |
| `63f5a1ad…` (the pinned commit) | `OK … aggregation root … agrees`, 8 digests recomputed | **0** |
| `000…001` (a different commit) | `REFUSE pin-gitlink-mismatch: … the aggregation and openxFactory disagree about which openxWallet revision the workspace consumes` | **2** |
| no gitlink at all | `REFUSE pin-member-missing: … a consumer that is supposed to carry this pin and carries no gitlink for it is not passing, it is not participating` | **2** |

Both refusals carry the wave's one fixed remediation trailer, and both codes are
in the ratified six — no new refusal vocabulary was introduced, which is D11's
whole point.

## The pin-setter regression, measured

`origin/main`'s `preserved_subblocks` run over LedgerxFactory's `stack.yaml`
shape:

```
PRE-FIX preserved the comment:   False
PRE-FIX preserved promoted_from: True
```

The block survived and the instruction protecting it did not. Post-fix both
survive, the comment still immediately precedes `promoted_from:`, and the pin is
still rewritten (twelve tests, `tests/domain_pin_setter/`).

## pytest

`python3 -m pytest tests/ -q -m "not postgres"`, the invocation the required
`pytest-suite` job uses.

### The required check: 0 failures, and the skip pin moved 20 → 21

Run `33123788199` on PR #440: **selected=7229 passed=7208 skipped=21 failures=0
errors=0**, against floors `selected>=7090` (margin 139) and `passed>=7070`
(margin 138). The job went red on ONE thing, and it was not a test:

```
::error::skipped 21, pinned exactly 20 — a directory that silently turned into
skips is exactly what this pin exists to catch. If the change is intended, move
the pin WITH the reason
```

The added skip is
`tests/domain_pin_setter/…::test_the_fixture_still_matches_the_live_ledgerx_shape`
— the fixture-drift guard on the pin-setter regression. Its twelve siblings run
everywhere off a literal fixture; this one alone compares that literal to the
LIVE LedgerxFactory `stack.yaml`, so it must stand down where no sibling checkout
exists, and CI is a lone openxFactory clone. It is a thirteenth assertion that
costs a skip, **not** a directory that turned into skips, which is the shape the
pin exists to catch. `EXPECT_SKIPPED` moved to `21` with that reason recorded at
the pin, and the stale prose above it corrected to the measured numbers (18 in a
developer worktree, 21 on a runner — a three-skip difference where the comment
still said two, and "the 17 skips" where the pin already said 20).

### A bare worktree is not a valid tree for this suite

The first local run reported 93 failures; every one is an ENVIRONMENT fact, not a
finding. `git worktree add` does not populate submodules, so `openXwallet/` was
absent and every suite reading the consumed wallet contracts refused
`pin-submodule-uninitialized` (`tests/openxwallet_pin/`, `tests/trust-anchor/`,
the pin-reachability readers). CI does the init by name before collection, which
is why the required check is the authority.

| run | result |
| --- | --- |
| local, worktree WITHOUT `openXwallet` initialized | 93 failed, 7015 passed (environment: no submodule) |
| local, same tree WITH `openXwallet` initialized | **1 failed, 7107 passed, 18 skipped**, 24:00 |
| required `pytest-suite`, run `33123788199` | **0 failures, 0 errors**, 7208 passed |

The one local failure is
`tests/hermes_runtime_contracts/test_validator_cli.py::test_release_mode_field_is_preserved_on_the_real_repository[--require-realization-realization]`
— a **subprocess timeout** in `_run_cli` on a box running two 24-minute suites
concurrently, in a module this feature does not touch, and green in CI. Recorded
rather than dismissed: a local red that CI does not reproduce is a fact about the
machine, and saying so is cheaper than leaving the next reader to re-derive it.

`wallet-validation` on PR #440: **pass** (24s).
