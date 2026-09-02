# Test counts

## The family's own file

| | tests | result |
|---|---|---|
| `f4fddf7c` (base) | 19 | **18 passed, 1 failed** |
| this branch | **51** | **50 passed, 1 failed** |

`+32`: **fourteen** reader tests that need no repository, **fifteen** ladder
scenarios over real git fixtures, **three** report-integration proofs. All
**13** new scenarios of the amended requirement are covered, each with the
positive control the file's own convention requires.

**The failing test is the SAME test in both rows, for the same reason**, and it
is not edited: `test_this_repository_reads_zero_and_the_probe_can_fire` reads
the LIVE remote `main`'s changelog via `git ls-remote origin refs/heads/main`.
See [`post-merge-proof.md`](./post-merge-proof.md) for it passing once that
changelog carries the declaration.

## `tests/doc-health`

```text
FAILED tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire
1 failed, 1415 passed, 7 warnings in 462.80s (0:07:42)
```

An earlier run of the same directory, taken before the three self-review tests
were added (see [`red-log.md`](./red-log.md)), read:

```text
1 failed, 1412 passed, 7 warnings in 486.77s (0:08:06)
```

The single failure is the self-gate above. Nothing else in the twenty-three
families moved.

## `tests/sequenced_after`

```text
118 passed in 3.07s
```

Plus `python3 scripts/validate-sequenced-after.py .` →
`sequenced_after validation passed (32 active changes, 1 declaring the field)`.
**No pin moved.**

## The full suite

Run locally at this head and, authoritatively, by the `pytest-suite` gate in
CI. The gate pins SKIPPED exactly and SELECTED/PASSED as floors, so the +32
tests raise the floors and red nothing. **CI is the authority**; the local
number is recorded for comparison only, and the run id and the FAILED line from
the gate on the final head are cited in the PR conversation.

**The expected CI result is `1 failed`** — the self-gate, byte-identical to
`main`'s single failure since `ff9ed815` — **and it goes green at the squash.**
