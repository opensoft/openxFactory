# doc-health `--single-repo`, before and after, same clock

In the shape OpenSpec tasks § 4.6 used: BASE a detached worktree at
`f4fddf7c` (this branch's base and `main`'s tip), HEAD this branch committed —
an untracked change is invisible to the readers, which is why the measurement
is taken after the commit.

```bash
python3 scripts/doc-health.py --single-repo .
```

## Headline

| | critical | error | warning | info |
|---|---|---|---|---|
| base (`f4fddf7c`, detached worktree) | 6 | 6 | 29 | 12 |
| head (this branch) | 6 | 6 | 29 | **13** |

Head's own headline line, verbatim:

```text
Findings: 6 critical, 6 error, 29 warning, 13 info. New regressions vs previous report: 0.
```

**The base reads 6 `error` where the packet's § 4.6 read 5**, and the extra one
is not this feature's: PR #577 (`2898b104`) added
`[error] release-inventory-drift docs/contract-versioning-policy.md — bytes
differ from the digest 'contract-v3.0' records` to `main` on 2026-09-02. The
packet predicted exactly that in OD-6 and measured it after the fact.

## What MOVED — the ranked plan, diffed row by row

Both reports' ranked-plan rows, sorted, with the repo-identity string
normalized to `R` (the two trees necessarily have different directory names):
[`doc-health-rows-base.txt`](./doc-health-rows-base.txt) →
[`doc-health-rows-head.txt`](./doc-health-rows-head.txt), 53 rows → 54 rows.

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
  CORRECT rather than a defect:

  ```text
  ### release-tag-publication

  - [error] …:contracts/manifest.yaml — contract-v2.6 was cut and SUPERSEDED
    without ever being published: …
  ```

  The family reads the changelog at the PUBLISHED TIP, and the published tip is
  `f4fddf7c`, which carries no declaration. **The finding-class change is a
  MERGE-TIME event, not a branch-time one** — measured post-merge in
  [`post-merge-proof.md`](./post-merge-proof.md), where the same run answers
  one `info` on the inventory path instead.

**So the honest statement of what this branch moves in a doc-health report is:
+1 `info` (CHANGELOG, editorial, expected between cuts) and nothing else. The
`error` → `info` conversion lands at the squash.**
