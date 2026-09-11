# Verification record: amend-merged-into-empty-tail-standing, post-merge re-run 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: amend-merged-into-empty-tail-standing — 2026-09-11, Brett Heap, "Ratify as encoded" (record `review/ratification-2026-09-11.md`)

**EVERY FIGURE IN `review/verification-2026-09-11.md` IS PRESERVED AND NOT ONE
OF THEM IS EDITED BY THIS FILE.** They are the measurement of the tree that
carried the ratification encode `7215c207` over `origin/main` `22a2ecbc`
(with `78d2c6f5` already ahead of it at capture time), and they are true of
it. **THIS IS A ONE-SHOT CAPTURE AT ITS OWN PATH**, as `document-lifecycle`
requires for a second run of a dated generator.

**`origin/main` MOVED TO `78d2c6f5` between the ratification commit and
`gh pr ready`**, and GitHub reported the pull request `CONFLICTING` (README's
`## OpenSpec Records` block: `main` had archived `state-header-window-budget`,
PR #953, removing its active row entirely, while this branch still carried
that row from before the archive). The merge was taken as its own commit,
`83dbd402` (merge of main `78d2c6f5`), resolving the one conflict by taking
`main`'s side (the row simply moved to `main`'s own archived-section entry,
already present after auto-merge) and keeping this packet's own row
unconflicted throughout; `tests/sequenced_after/corpus-ledger.yaml` auto-merged
clean, both sides kept (this packet's own row, and `state-header-window-budget`'s
flip to `archived`).

**EVERY GATE WAS RE-RUN FROM ZERO ON `83dbd402`:**

| gate | exit | result |
| --- | --- | --- |
| `openspec validate amend-merged-into-empty-tail-standing --strict` | 0 | `Change 'amend-merged-into-empty-tail-standing' is valid` |
| `proposal-support.py . verify amend-merged-into-empty-tail-standing` | 0 | `proposal support verification ok` |
| `validate-sequenced-after.py .` | 0 | `sequenced_after validation passed (40 active changes, 10 declaring the field)`, both archive-date arms passing, 12 dispositions in force |
| `validate-sequenced-after.py . --ledger-diff` | 0 | `per-change sweep ledger consistent with the corpus (200 rows)` |
| `validate-scope-globs.py .` | 0 | `scope_globs validation passed (all active changes conform)` |
| `openspec validate --all --strict` (PATH 1.2.0) | 1 | `Totals: 99 passed, 3 failed (102 items)` |
| `doc-health.py --single-repo .` | 0 | `Findings: 32 critical, 5 error, 47 warning, 15 info` |
| `pytest tests/doc-health -q` | 0 | `1689 passed, 7 warnings in 440.16s` |

**THE `--all --strict` FAILURE SET IS STILL IDENTICAL TO `origin/main`'s**, checked
against a freshly-updated `origin/main` `78d2c6f5` control worktree (`Totals: 98
passed, 3 failed (101 items)`): `change/disposition-codexfactory-declared-renames`,
`change/disposition-codexfactory-floor-relocation-retitle`, `spec/repo-boundary-governance` —
the same three names on both sides, `diff` of the two sorted lists EMPTY. The
one-item difference (102 vs 101) is this packet's own item, now passing on the
branch and absent from `main`.

**`doc-health --single-repo` IS BYTE-IDENTICAL TO A FRESH `origin/main`
`78d2c6f5` CONTROL RUN**, this time with NO residual drift: both the headline
(`32 critical, 5 error, 47 warning, 15 info`) and every severity-tagged finding
line matched exactly after normalizing the `Repo-Identity` label (`diff`
returns nothing at all, not even the small canon-share percentage drift the
first capture noted — this branch has now fully caught up to `main`'s own
latest promotion). This change is named **0** times.

**`pytest tests/doc-health -q` REPRODUCES `1689 passed, 7 warnings`**,
identical to the pre-merge capture and to the dead second author's own
pre-encode control run.

**NOTHING ABOUT THE RATIFICATION'S OWN SUBSTANCE MOVED.** `git diff --stat
546e2c97 -- openspec/changes/amend-merged-into-empty-tail-standing/specs/`
remains EMPTY on `83dbd402`; the packet's own delta, marker and scenario are
exactly what Brett Heap's word ratified, carried through two further merges
from `main` untouched.

This is the tree `gh pr ready` was called on, and the tree the bench round
after `gh pr ready` reviews.
