# doc-health `--single-repo`, before and after, same clock

Status: record
Kind: evidence

Measurement shape: BASE is a detached worktree at `origin/main`, HEAD is this
branch COMMITTED — an untracked change is invisible to the readers, which is why
the reading is taken after the commit.

```bash
python3 scripts/doc-health.py --single-repo .
```

## Headline

| | critical | error | warning | info |
| --- | --- | --- | --- | --- |
| base (`e4ff4fb3`, detached worktree) | 6 | 4 | 27 | 16 |
| head (this branch, before the catch-up merge) | 6 | 4 | 27 | 16 |
| base (`bc1bd4ee`, RE-TAKEN after `main` moved 23 commits) | 6 | 4 | 27 | 14 |
| head (`f24ff113`, this branch MERGED) | 6 | 4 | 27 | 14 |

**RE-TAKEN AFTER `main` MOVED, rather than assumed to still hold.** `main`
advanced from `e4ff4fb3` to `bc1bd4ee` (23 commits, including the archives of
`add-consumer-identity-namespace` and `create-medxchart-overlay-boundary`), this
branch took a catch-up merge, and BOTH halves were measured again. Two `info`
findings dropped on both sides at once — they were `modified-block-currency`
findings on the two changes that archived — so the base moved and **the delta is
identical: still zero.** Which is the point of re-taking it.

## The delta

**ZERO.** Not merely equal counts — the finding SETS are identical. Compared
family-by-family, path-by-path, with the repo label normalised (the worktree
directory name differs and the finding is otherwise the same):

```bash
diff <(grep -oE 'severity=[a-z]+ family=[a-z-]+ repo=[^ ]+ path=[^ ]+' base.txt \
        | sed 's/repo=[^ ]*/repo=R/' | sort) \
     <(grep -oE 'severity=[a-z]+ family=[a-z-]+ repo=[^ ]+ path=[^ ]+' head.txt \
        | sed 's/repo=[^ ]*/repo=R/' | sort)
# (no output)
```

Six new schema files, fifteen new example files, fifty-two new fixtures, two new
documentation surfaces and a new Speckit feature, and the corpus's health
findings do not move. The pre-existing `release-inventory-drift` info finding on
`contracts/manifest.yaml` ("bytes differ from the digest `contract-v3.3`
records (editorial member — expected between cuts)") is present on BOTH sides:
this feature adds six rows to that file, and the finding was already standing
before it because the manifest is an editorial member between cuts.
