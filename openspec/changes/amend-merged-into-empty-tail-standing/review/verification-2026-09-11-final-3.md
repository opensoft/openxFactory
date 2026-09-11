# Verification record: amend-merged-into-empty-tail-standing, merge note 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: amend-merged-into-empty-tail-standing — 2026-09-11, Brett Heap, "Ratify as encoded" (record `review/ratification-2026-09-11.md`)

**THIS IS A SHORT ADDENDUM, NOT A FULL RE-RUN.** `review/verification-2026-09-11-final-2.md`
measured `a8235295` and is NOT edited (committed captures are never edited —
lane hard limit, #887 `e65aed15` precedent). Between that capture's commit
(`3db8762c`) and this one, `origin/main` advanced again, `34bb5c71` →
`ac688c40` (PR #960, `amend-register-act-5b-projection-proof`, ratified), and
the branch went CONFLICTING. This file records the merge that resolved it
and re-verifies the two corpus-wide gates that merge touches.

## 0. The merge

Merge commit `596eb05f`, merging `origin/main` `ac688c40` into `3db8762c`.
`git diff --stat 34bb5c71 ac688c40` shows PR #960 added ONLY its own packet
directory (`openspec/changes/amend-register-act-5b-projection-proof/`), one
README `## OpenSpec Records` row, and one `tests/sequenced_after/corpus-ledger.yaml`
row — nothing under this packet's own directory, `openspec/specs/doc-health/spec.md`,
or the predicate/test files this packet cites. The merge's only conflict was
README's active-list section (two independent list entries adjacent to each
other); resolved by keeping BOTH this packet's row and PR #960's row, in
list order. `tests/sequenced_after/corpus-ledger.yaml` auto-merged cleanly,
keeping every packet's row (verified: `amend-merged-into-empty-tail-standing`,
`amend-register-act-5b-projection-proof` and
`honour-grandfather-dispositions-in-ratified-provenance` rows all present).
`.openspec.yaml` diff against `7215c207` remains EMPTY; the packet's own
delta (`git diff --stat 546e2c97 -- .../specs/`) remains EMPTY.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-merged-into-empty-tail-standing --strict`

```
Change 'amend-merged-into-empty-tail-standing' is valid
```

Exit code 0.

## 2. `python3 scripts/validate-sequenced-after.py . --ledger-diff`, on the merged tree

```
sequenced_after corpus sweep
----------------------------
change ids (41 active + 161 archived): 202
co-modified at requirement granularity (each would owe a declaration): 148
sole modifiers (each would declare `sequenced_after: []`): 54
ACTIVE changes: co-modified / sole: 25 / 16
declaring `sequenced_after:`: 27
declaring an explicit `[]` root claim: 8
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (202 rows).
```

Exit code 0. (Active-change count rose 40 → 41 and ledger rows 201 → 202,
entirely from PR #960's own landing — one active change, one ledger row,
neither this packet's.) `python3 scripts/validate-sequenced-after.py .`
(without `--ledger-diff`) also passed: `sequenced_after validation passed
(41 active changes, 11 declaring the field)`, exit 0.

## 3. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

Exit code 0.

## 4. What is NOT re-run here, and why

`--all --strict` on both binaries, `doc-health --single-repo` and
`pytest tests/doc-health -q` are NOT re-run in this addendum: PR #960's own
diff (§ 0, above) touches only bookkeeping rows this packet does not read,
and `review/verification-2026-09-11-final-2.md` already certified all four
of those gates clean on `a8235295`, with failure-sets/finding-sets identical
to `origin/main` by name. This addendum's own § 2 and § 3 are the two gates
the orchestrator asked re-verified on the merged tree; nothing else moved.

## 5. Independent review

No new review thread opened between `3db8762c` and `596eb05f` as of this
writing. The two threads on `review/verification-2026-09-11-final.md`
(`PRRT_kwDOTAvnrs6hefH9`, `PRRT_kwDOTAvnrs6hfKTQ`) and the one on
`review/verification-2026-09-11-final-2.md` (`PRRT_kwDOTAvnrs6hgLKF`, a
stale review that landed after the PR body had already been corrected) were
resolved before this merge; see the PR body and `review/verification-2026-09-11-final-2.md`
§ 9.

**THIS LANE ENCODES AND FREEZES; IT DOES NOT MERGE OR LAND.** The Rule 6
LANDING/LANDED post belongs to the landing lane, on Brett Heap's standing word
"land each when green."
