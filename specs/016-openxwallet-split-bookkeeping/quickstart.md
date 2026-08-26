# Quickstart / Verification Guide: split-openxwallet-repo §1 bookkeeping

**Feature**: `016-openxwallet-split-bookkeeping` | **Date**: 2026-08-26

How a reviewer proves this feature did what §1 asked, without trusting the
author. Every check is a diff against ratified text or a counted command result.
See [data-model.md](./data-model.md) for the four edit sites and
[research.md](./research.md) for where each source text lives.

## Prerequisites

- The openxFactory feature worktree:
  `/home/brett/projects/xFactory/openxFactory-worktrees/016-openxwallet-split-bookkeeping`
  on branch `016-openxwallet-split-bookkeeping`, base `origin/main` = `5ef6d8d2`.
- The aggregation worktree:
  `/home/brett/projects/xFactory-worktrees/openxwallet-working-rule` on branch
  `change/openxwallet-working-rule`, base `origin/main`.
- `openspec` on PATH, `python3`, `gh` authenticated for `opensoft/*`.

`OX` and `AGG` below stand for those two absolute paths.

## 1. The naming record matches its ratified source (E1, E2)

```bash
# The whole diff to the record should be: one appended section, one rewritten bullet.
git -C "$OX" diff origin/main -- docs/openxdox-naming.md

# The lifecycle header must be byte-identical.
git -C "$OX" diff origin/main -- docs/openxdox-naming.md | grep -E '^[-+](Status|Ratified|Kind|Repository context|Purpose):' 
#   expected: no output
```

**Expected**: additions only at end of file (Amendment 2) plus the one
`- **Capability name:**` bullet replaced. No deletion of any other line.

Then compare against the ratified text:

```bash
# Amendment 2's source, un-blockquoted:
sed -n '236,258p' "$OX/openspec/changes/split-openxwallet-repo/proposal.md" | sed 's/^   > \?//'
# The inline pointer's ratified "after":
sed -n '264,265p' "$OX/openspec/changes/split-openxwallet-repo/proposal.md"
```

**Expected**: the record's new section says the same thing, word for word, modulo
line wrapping.

Three spot checks that catch the known traps:

```bash
# (a) The retired spelling is gone from the LIVE record body.
#     It survives twice inside Amendment 2 itself, which names it as history
#     ("`openxWallet` becomes `openXwallet`", "was genuinely a family
#     exception") — that is the ratified text, so the check is scoped to the
#     record above Amendment 2, not to the whole file.
sed -n '1,109p' "$OX/docs/openxdox-naming.md" | grep -c 'openxWallet'   # expected: 0
grep -c 'openxWallet' "$OX/docs/openxdox-naming.md"                     # expected: 2

# (b) The pointer is grammatical and singular.
grep -n 'family exception, not the rule' "$OX/docs/openxdox-naming.md"
grep -c 'spellings are the family' "$OX/docs/openxdox-naming.md"   # expected: 0

# (c) Exactly one ratification citation line in the header.
grep -cE '^(Ratified by:|Ratified:|Amended:)' "$OX/docs/openxdox-naming.md"  # expected: 1
```

## 2. The aggregation working rule (E3)

```bash
git -C "$AGG" diff origin/main --stat        # expected: CLAUDE.md | 5 +-- (one file only)
git -C "$AGG" diff origin/main -- CLAUDE.md
```

**Expected**: rule 1's two lines replaced by the proposal's four; `## Working
rules` heading and rules 2 onward untouched. Confirm against the source:

```bash
sed -n '276,279p' "$OX/openspec/changes/split-openxwallet-repo/proposal.md"
sed -n '/^## Working rules/,/^2\. Commit inside/p' "$AGG/CLAUDE.md"
```

The four substantive claims must all be present: neutral contracts may live in a
neutral `open*` product repository; openxFactory pins it **by commit and digest**;
**domain repos never author neutral contracts**; **every consumer** pins the
openxFactory version in its `stack.yaml`.

## 3. The ledger tells the truth (E4)

```bash
git -C "$OX" diff origin/main -- openspec/changes/split-openxwallet-repo/tasks.md

# Every §1 box ticked:
sed -n '/^## 1\. This change/,/^## 2\. P5a\.1/p' "$OX/openspec/changes/split-openxwallet-repo/tasks.md" | grep -c '^- \[ \]'
#   expected: 0

# No successor box ticked — count must equal the base commit's count:
for REF in origin/main HEAD; do
  git -C "$OX" show $REF:openspec/changes/split-openxwallet-repo/tasks.md \
    | sed -n '/^## 2\. P5a\.1/,$p' | grep -c '^- \[x\]'
done
#   expected: two identical numbers
```

**Expected**: task 1.1 no longer claims `Status: draft`; 1.10, 1.11 and 1.12 are
ticked; each new tick carries a trailing note naming a file and a commit or PR.
Task 1.10's note must carry the actual numbers — both commits, both finding
counts, and the one differential finding named — not the word "green" alone.

## 4. The gates

```bash
cd "$OX" && OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

**Expected**: `Totals: 77 passed, 0 failed (77 items)` — the same total as the
base commit, since this feature adds no OpenSpec item.

```bash
cd "$OX" && python3 scripts/doc-health.py --single-repo . | grep -E '^Findings:'
```

**Expected**: `Findings: 5 critical, 7 error, 41 warning, 4 info` — identical to
the base commit `5ef6d8d2`. In particular the error count must **not** rise: a
rise to 8 would mean the naming-record edit introduced a status or tag finding,
which is the specific failure task 1.11 is exposed to.

To reproduce the differential that task 1.10's evidence note records:

```bash
git -C "$OX" worktree add --detach /tmp/pre-packet 5ef6d8d2^1
cd /tmp/pre-packet && python3 scripts/doc-health.py --single-repo . | grep -E '^Findings:'
#   expected: 5 critical, 6 error, 41 warning, 4 info
```

The one-finding delta (`location-conformance`, `contested`, on
`ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md`) is
expected and is **not** remedied by this feature — see research.md § R5.

## 5. Both pull requests are open and unmerged

```bash
gh pr list -R opensoft/openxFactory --head 016-openxwallet-split-bookkeeping --state open
gh pr list -R opensoft/xFactory     --head change/openxwallet-working-rule    --state open
```

**Expected**: one open PR each, neither merged. The merge gate is human; this
feature merges nothing.

## Failure triage

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| doc-health error count 8, not 7 | a header line was added to the naming record (`Amended:` / second citation) | remove it — research.md § R2; the dated section heading carries the provenance |
| `grep -c 'spellings are the family'` returns 1 | the pointer was patched by token deletion instead of rewritten | apply the proposal's verbatim "after" sentence — research.md § R3 |
| a retired-spelling occurrence survives above Amendment 2 | the § Decision bullet was not rewritten | there is exactly one such site (line 24); rewrite that bullet. Occurrences *inside* Amendment 2 are the ratified text and must stay |
| capability ids or `xfactory_wallet_*` changed | a case-insensitive global replace ran | revert; the wire label stays lowercase by design |
| aggregation `--stat` shows more than `CLAUDE.md` | another session's work was swept in | reset and re-commit with an explicit `-- CLAUDE.md` pathspec |
| `openspec validate` total ≠ 77 | an OpenSpec artifact was touched | this feature must not add or remove OpenSpec items |
| a §2–§12 box is ticked | successor scope leaked | untick it; successors archive on their own evidence |
