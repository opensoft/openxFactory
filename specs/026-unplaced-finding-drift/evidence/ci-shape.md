# CI shape — the suite run from a clean extraction, not from the worktree (T040)

A worktree carries untracked files, a shared object store and a `.git` FILE
rather than a directory. A test that reads the repository can pass here and fail
in CI for reasons that have nothing to do with the change. So the suite was run
against a clean extraction of exactly what is committed:

```bash
TREE=$(git write-tree)                 # the staged tree, i.e. what will land
git archive $TREE | tar -x -C <scratch>/cishape
cd <scratch>/cishape && git init -q .
python3 -m pytest tests/doc-health -q
```

## Result

```text
7 failed, 1211 passed, 9 skipped, 5 warnings in 62.30s
```

## The seven failures are the extraction's, not this feature's — measured

The SAME extraction was taken of the BRANCH POINT `86b7ca3f` (the module
untouched) and run the same way:

```text
7 failed, 1199 passed, 9 skipped, 5 warnings in 66.46s
```

**The same seven tests, by name, in both runs:**

| test | why a history-less extraction fails it |
|---|---|
| `test_ideation_readiness.py::test_derivation_reproduces_the_real_bootstrap_clusters` | derives from committed history |
| `test_modified_block_currency_fixtures.py::test_the_reconstructed_fixtures_are_the_history_they_claim[351]` | `git show bcfc26a0…` — the commit does not exist in a fresh `git init` |
| `…[329]` | `git show d5f447e8…`, same reason |
| `test_pin_reachability.py::test_the_declared_loss_in_this_repository_cites_a_committed_record` | resolves refs |
| `test_pin_reachability.py::test_this_repository_resolves_the_main_half_of_the_ref_set` | resolves refs |
| `test_pin_reachability.py::test_the_resolver_this_probe_shares_with_the_readiness_proof_agrees` | resolves refs |
| `test_readiness_proof_resolution.py::test_the_landed_index_pins_a_revision_this_repository_can_resolve` | resolves a revision |

Every one needs REAL GIT HISTORY, which a `git init` over an extracted tree does
not have and which CI's clone does. **1199 → 1211 is +12, exactly this feature's
twelve new tests**, and not one of them — nor any pin this feature moved — is
among the failures.

**No new test of this feature is environment-sensitive.** The behavioural tests
read fixture trees under `tests/doc-health/fixtures/`, which the extraction
carries; the two that read the real tree (`_real_ctx()` in
`test_a_run_the_map_places_entirely_emits_no_additional_finding` and the
`test_every_finding_carries_its_class_s_band_and_action` pass, plus the
self-gate's fourth probe) read the checked-out tree through the family's own
readers and need no git at all. All pass in the extraction.

## What was NOT done, and why

`pytest tests` over the whole repository was never run from the worktree. The
suite outside `tests/doc-health` is not this feature's subject, and a whole-tree
run from a worktree is precisely the shape that produces environment failures a
reader then has to triage.
