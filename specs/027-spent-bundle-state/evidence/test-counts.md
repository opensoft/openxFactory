# Test counts

## CORRECTION, 2026-09-02 (lane openxfactory-1d), and it is against this file

**THE `69` IN THE TABLE BELOW IS WRONG.** PR #584's family-file count at its
final head `8106f204` was **66** — 65 passed plus 1 deselected — not the 69 that
this file and that PR's round-5 comment published. The error was arithmetic on a
running total across five rounds rather than a re-count of the collected file,
and it is corrected here rather than silently edited out of the row, because a
number nobody re-counted is exactly the class of claim this estate's own
"claim-outrunning-machinery" lesson names. The rest of the table's readings
stand.

For the RE-SCOPED branch's own counts — `main`'s 46, this branch's 73, both
re-counted from a collected run rather than accumulated — see
[`hardening-red-first.md`](./hardening-red-first.md) § C.

## The family's own file

| | tests | result |
|---|---|---|
| `f4fddf7c` (the packet's merge, this branch's base) | 19 | **18 passed, 1 failed** |
| PR #584, final head `8106f204` | **66** (published as 69; see § CORRECTION) | **65 passed, 1 deselected** |

`+50` tests across five review rounds. The failing test is the SAME test in
both rows, for the same reason, and it is not edited:
`test_this_repository_reads_zero_and_the_probe_can_fire` reads the LIVE remote
`main`'s changelog via `git ls-remote origin refs/heads/main`. See
[`post-merge-proof.md`](./post-merge-proof.md) for it passing once that
changelog carries the declaration.

## `tests/doc-health`

At `95c11696` (before the last two rounds of fixes):

```text
FAILED tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire
1 failed, 1420 passed, 7 warnings in 470.50s (0:07:50)
```

Earlier, at `09e28b3d`: `1 failed, 1415 passed`. Earlier still, before the
self-review round: `1 failed, 1412 passed`. Every run: **the same single
failure**, and nothing else in the twenty-three families moved.

### ONE RUN IS RECORDED AS A FALSE GREEN, BECAUSE IT WAS ONE

A run of `tests/doc-health` at `32c215e1` read **`1430 passed`, zero
failures** — including the self-gate. **That was not the declaration working.**
`origin/main` had advanced to `3bcde7e2` under this branch and the checkout had
not fetched it, so `blobs_at` could not read `contracts/manifest.yaml` at that
tip and the family returned the SKIP the self-gate explicitly tolerates:

> A SKIP IS NOT A DEFECT AND IS NOT ASSERTED AWAY. This family reads the
> PUBLISHED refs, so its answer depends on whether the checkout has fetched the
> tip — an environment fact, not a corpus fact.

With the tip fetched and `main` merged, the family reads the real changelog
again and the self-gate fails exactly as it should. **Recorded rather than
banked**: a green that comes from an unfetched commit is the #338 conflation
wearing the other hat, and this family's own guards exist because of it. It is
also the reason the post-merge claim is proved against a bare repository whose
`main` really does carry the declaration, rather than against a checkout whose
`origin` happens not to have moved.

## `tests/sequenced_after`

```text
118 passed
```

Plus `python3 scripts/validate-sequenced-after.py .` →
`sequenced_after validation passed (31 active changes, 1 declaring the field)`.
**No pin moved by this PR.** The reading fell 32 → 31 when `main` archived
`govern-sibling-added-modified-deltas`; that pin move is `main`'s, taken as-is
by the catch-up merge.

## The full suite

`pytest-suite` in CI is the authority. It pins SKIPPED exactly and
SELECTED/PASSED as floors, so the added tests raise the floors and red nothing.

Measured on `09e28b3d`, run **33641746085**:

```text
FAILED tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire
1 failed, 8652 passed, 21 skipped, 338 deselected, 9 warnings, 46 subtests passed in 1211.49s (0:20:11)
```

`main`'s own run at `f4fddf7c` reads `1 failed, 8620 passed, 21 skipped, 338
deselected` — **the same single failure**, `skipped` identical at the
exactly-pinned 21, and `passed` +32 for the tests that head added. The run id
and failure line for the FINAL head are cited in the PR conversation.
