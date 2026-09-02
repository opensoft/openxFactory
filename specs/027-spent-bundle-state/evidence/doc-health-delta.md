# doc-health `--single-repo`, before and after, same clock

> **A RECORD OF PR #584, AT PR #584'S HEADS — NOT THIS BRANCH'S.** Kept
> unedited because a transcript that gets rewritten stops being one. Its
> readings were taken on a branch cut from `f4fddf7c`; this branch is cut
> from `origin/main` at `47f90080`, so counts here that differ from
> [`hardening-red-first.md`](./hardening-red-first.md) differ BY THE BASE.
> That file's § D carries this branch's own gates and is the one that
> describes the code under review.

In the shape OpenSpec tasks § 4.6 used: BASE a detached worktree at
`origin/main`, HEAD this branch committed — an untracked change is invisible to
the readers, which is why the measurement is taken after the commit.

```bash
python3 scripts/doc-health.py --single-repo .
```

**RE-TAKEN AFTER `main` MOVED.** The first measurement used `f4fddf7c` as the
base; `main` then advanced to `3bcde7e2` (#585, and the archive of
`govern-sibling-added-modified-deltas`), this branch took a catch-up MERGE, and
both halves were measured again. **The delta is identical** — which is the point
of re-taking it rather than assuming.

## Headline

| | critical | error | warning | info |
|---|---|---|---|---|
| base (`3bcde7e2`, detached worktree) | 6 | 6 | 29 | 12 |
| head (`422def1a`, this branch merged) | 6 | 6 | 29 | **13** |

The base reads 6 `error` where the packet's § 4.6 read 5, and the extra one is
not this feature's: PR #577 (`2898b104`) added
`[error] release-inventory-drift docs/contract-versioning-policy.md — bytes
differ from the digest 'contract-v3.0' records` to `main` on 2026-09-02. OD-6
predicted exactly that and measured it after the fact.

## What MOVED — the ranked plan, diffed row by row

Both reports' ranked-plan rows, sorted, with the repo-identity string
normalized to `R` (the two trees necessarily have different directory names):
[`doc-health-rows-base.txt`](./doc-health-rows-base.txt) →
[`doc-health-rows-head.txt`](./doc-health-rows-head.txt).

```diff
23a24
> - severity=info family=release-inventory-drift repo=R path=contracts/CHANGELOG.md rule="bytes differ from the digest 'contract-v3.0' records (editorial member — expected between cuts)" action="cut a release through the bundle realization order; …"
```

**EXACTLY ONE NEW ROW, AND IT IS THE PREDICTED ONE.** `contracts/CHANGELOG.md`
is one of the three EDITORIAL members, so its between-cuts drift is an `info`
the family itself labels *expected between cuts* — which is what made the
changelog the only release member a between-cuts disposition could be written
to at all (OD-1, OD-6). It clears on its own when the next cut re-baselines the
inventory (OpenSpec tasks § 3.2 — no action, recorded so a reader does not go
looking for one).

**NOTHING ELSE MOVED.** No finding changed family, no severity moved, no census,
word count, canon-share figure or catalog record moved.

## The three zeroes, checked rather than assumed

* **`family-enumeration`: `No findings.`** This feature adds NO family and
  moves no count, so the family-count sentences in `docs/doc-health.md` are
  untouched and that gate stays silent. Verbatim from the head report:

  ```text
  ### family-enumeration

  No findings.
  ```

* **`modified-block-currency`**: `scenario-title completeness: 0` (the arm
  carrying that family's gate) and the carriage ledger unchanged at `8` — both
  identical to base.

* **`release-tag-publication` at head still reports the `error`**, and that is
  CORRECT rather than a defect: the family reads the changelog at the PUBLISHED
  TIP, and the published tip carries no declaration until this PR is squashed.
  **The finding-class change is a MERGE-TIME event, not a branch-time one** —
  measured post-merge in [`post-merge-proof.md`](./post-merge-proof.md), where
  the same run answers one `info` on the inventory path instead.

**So the honest statement of what this branch moves in a doc-health report is:
+1 `info` (CHANGELOG, editorial, expected between cuts) and nothing else. The
`error` → `info` conversion lands at the squash.**
