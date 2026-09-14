# Verification record: amend-register-act-5b-projection-proof, ratified tree 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: amend-register-act-5b-projection-proof — 2026-09-11T13:09:12Z, Brett Heap, "accept all A on 960" (record `review/ratification-2026-09-11.md`)

**THIS FILE'S SUBJECT IS THE GATE RUN, NOT THE RATIFICATION**, which is why it
keeps `Status: record` while `review/ratification-2026-09-11.md` carries
`Status: ratified`. `document-lifecycle`'s *A review record records a
ratification* governs that file; the sibling scenario *A review record is not
about a ratification* governs this one.

**IT IS A ONE-SHOT CAPTURE.** This is the packet's first and only gate
capture after ratification; a later re-run writes `verification-<later
date>.md` beside it rather than rewriting this one.

**EVERY FIGURE BELOW WAS TAKEN TWICE IN THE SAME WORKTREE** — once on the
pre-encode tree (head `69a57fa2`, PR #960's own head, the tree all ten CI
checks ran green against) and once on the ratified tree (this commit) — so
each command's own before/after comparison is a direct measurement, not a
recollection of an earlier session's numbers.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| branch | `change/amend-register-act-5b-projection-proof` |
| PR #960 head the ten CI checks ran green against | `69a57fa2780dd1b4725d4ab4f04e4b98230dcd03` |
| worktree | `~/projects/xFactory/openxFactory-worktrees/amend-5b` |
| merge-from-`main` owed at encode time | none — `git diff --stat 38c076d1..origin/main` (2 new commits, `contracts/manifest.yaml` + `contracts/policies/repository-identity.yaml`) has ZERO overlap with this packet's touched paths (`README.md`, `openspec/changes/amend-register-act-5b-projection-proof/**`, `tests/sequenced_after/corpus-ledger.yaml`); `gh pr view 960` reported `mergeable: MERGEABLE` throughout |
| CLI on `PATH` | `openspec` **1.2.0** |
| pinned CLI | `@fission-ai/openspec@1.12.0`, the required gate's entrypoint |

**`git diff --stat -- openspec/changes/amend-register-act-5b-projection-proof/specs/`
between `69a57fa2` and the ratification commit is EMPTY (0 files).** All
seven OQs were ruled at their RECOMMENDED option, so the delta moved no byte
— the claim in `proposal.md` § Rulings, verified here rather than asserted.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-register-act-5b-projection-proof --strict`

```
$ OPENSPEC_TELEMETRY=0 openspec validate amend-register-act-5b-projection-proof --strict
Change 'amend-register-act-5b-projection-proof' is valid
```

**exit 0**, both before and after the encode.

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the 1.2.0 binary on `PATH`

Pre-encode (head `69a57fa2`):

```
Totals: 99 passed, 2 failed (101 items)
✗ change/disposition-codexfactory-declared-renames
✗ change/disposition-codexfactory-floor-relocation-retitle
```

Post-encode (ratification commit):

```
Totals: 99 passed, 2 failed (101 items)
✗ change/disposition-codexfactory-declared-renames
✗ change/disposition-codexfactory-floor-relocation-retitle
```

**exit 1 both times, expected rather than a regression — the same 2 failures,
byte-for-byte, before and after.** Both are the codexFactory disposition
findings this packet does not touch. **NO REGRESSION.**

## 3. `python3 scripts/validate-openspec-cli-pin.py --all` — the pinned 1.12.0, the required gate

Pre- and post-encode output is **byte-identical** (`diff` of the two captures
is empty): exit 0, `Totals: 99 passed, 2 failed (101 items)` folded into `OK
openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content
address; every target validated --strict with 0 UNDISPOSITIONED failures`,
with the same 2 accepted exceptions named both times
(`add-chain-attestation` / `signed-execution-chain/spec.md`,
`add-composed-view-authoring` / `ideation-dashboard/spec.md`, both accepted
by Brett Heap 2026-09-05 "take exit 2"). **NO REGRESSION.**

## 4. `python3 scripts/validate-sequenced-after.py .`

Pre- and post-encode:

```
sequenced_after validation passed (39 active changes, 9 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (... 12 disposition(s) in force, enforcement error).
```

**exit 0 both times, identical.** This packet's own row was seeded at
authoring time (state `active`) and does not move at ratification — only at
archive, per `tasks.md` § 5.1.

## 5. `python3 scripts/validate-sequenced-after.py . --ledger-diff`

Pre- and post-encode: **`per-change sweep ledger consistent with the corpus
(200 rows)`**, exit 0, identical both times. `declaring sequenced_after:`
count (25, corpus-wide) and `DEEPEST DECLARED CHAIN RESOLVED` (4 hops, from
`admit-review-lane-repin-to-merge-approval-envelope`) unchanged.

## 6. `python3 scripts/doc-health.py --single-repo . --fail-on error`

| | critical | error | warning | info |
| --- | --- | --- | --- | --- |
| pre-encode | 32 | 5 | 47 | 15 |
| post-encode | 32 | 5 | 47 | 15 |

**exit 1 both times — expected, unrelated to this packet** (the 5 `error`
severity findings are pre-existing corpus residue, none naming this
change). `diff` of the two runs' `severity=` finding lines, sorted, is
**EMPTY** — not one finding line moved, added or dropped, including none
naming the two new `review/*.md` files this encode adds. **NO REGRESSION.**

## 7. Summary

All six commands `tasks.md` § 6.1 names were run before and after the
ratification encode, in the same worktree, on the same tree modulo the
encode's own bookkeeping diff. **Every figure is identical pre- and
post-encode**, which is the direct proof that ruling all seven OQs at their
RECOMMENDED option moved no delta byte and regressed no gate. The two
`--all --strict` / `doc-health` failure sets that stay red
(`disposition-codexfactory-declared-renames`,
`disposition-codexfactory-floor-relocation-retitle`; the 5 doc-health
`error`-severity findings) are pre-existing corpus residue this packet does
not touch and is not the cited change for.

## 8. Provenance of this record

Written in the ratification commit itself, in the worktree
`~/projects/xFactory/openxFactory-worktrees/amend-5b`, by lane
`hermes-wallet-exercise`. Every path in this file is repo-relative.
