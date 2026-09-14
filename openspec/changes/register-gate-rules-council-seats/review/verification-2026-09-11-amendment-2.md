# Verification record: register-gate-rules-council-seats, Amendment 2 ratified tree 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: register-gate-rules-council-seats — Amendment 2 ratified
2026-09-11T17:08:42Z, Brett Heap, "accept all A on 971, merge slice 3 when
green" (record `review/ratification-2026-09-11-amendment-2.md`)

**THIS FILE'S SUBJECT IS THE GATE RUN, NOT THE RATIFICATION**, which is why it
keeps `Status: record` while `review/ratification-2026-09-11-amendment-2.md`
carries `Status: ratified`. `document-lifecycle`'s *A review record records a
ratification* governs that file; the sibling scenario *A review record is not
about a ratification* governs this one.

**IT IS A ONE-SHOT CAPTURE.** A later re-run writes
`verification-<later date>.md` beside it rather than rewriting this one.

**EVERY FIGURE BELOW WAS TAKEN TWICE, ON TWO TREES, IN TWO WORKTREES OF THE SAME
REPOSITORY** — once on `origin/main` at `ce5c054e` (the pre-encode baseline, in
the throwaway worktree `~/projects/xFactory/openxFactory-worktrees/dh-baseline-qgrc4`)
and once on the ratified tree (this commit, in
`~/projects/xFactory/openxFactory-worktrees/ratify-q-grc-4`) — so each command's
before/after comparison is a direct measurement rather than a recollection.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| branch | `change/register-gate-rules-council-seats-ratify-q-grc-4` |
| pre-encode baseline | `ce5c054e` — `origin/main` at encode time |
| the amendment's own landing | PR [#971](https://github.com/opensoft/openxFactory/pull/971), head `1d49368b`, merge commit `3402d93a`, merged 2026-09-11T16:49:55Z |
| catch-up merge owed at encode time | **taken, and it is in the history rather than asserted**: the encode was authored over `3402d93a` and REBASED onto `ce5c054e` (24 commits, 416 files, including contract-v4.0's BREAKING removal of the five ideation-dashboard schemas). `git diff --stat 3402d93a..ce5c054e -- README.md openspec/changes/register-gate-rules-council-seats/` reports `README.md` ONLY — the packet's own directory is untouched by all 24 — and the rebase applied with NO conflict |
| CLI on `PATH` | `openspec` **1.2.0** |
| pinned CLI | `@fission-ai/openspec@1.12.0`, the required gate's entrypoint |
| doc-health `Repo-Identity` | differs by worktree directory name (`dh-baseline-qgrc4` vs `ratify-q-grc-4`); normalised out of the finding-line comparison in § 6 and out of nothing else |

**`git diff --stat 3402d93a -- openspec/changes/register-gate-rules-council-seats/specs/`
at this commit is EMPTY (0 files).** All five OQs were ruled at their RECOMMENDED
option, so the delta moved no byte — the claim `proposal.md` § AMENDMENT —
2026-09-11 and the amendment record § 9 both make, verified here rather than
asserted.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate register-gate-rules-council-seats --strict`

```
Change 'register-gate-rules-council-seats' is valid
```

**exit 0**, both before and after the encode.

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the 1.2.0 binary on `PATH`

Pre-encode (`ce5c054e`) and post-encode (this commit), byte-identical:

```
Totals: 100 passed, 2 failed (102 items)
✗ change/disposition-codexfactory-declared-renames
✗ change/disposition-codexfactory-floor-relocation-retitle
```

**exit 1 both times, expected rather than a regression** — the same two
codexFactory disposition findings this packet does not touch, and the same pair
#960's ratification recorded eight hours earlier at a smaller item count.
**NO REGRESSION.**

## 3. `python3 scripts/validate-openspec-cli-pin.py --all` — the pinned 1.12.0, the required gate

**exit 0** both times, with the same tail both times:

```
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content
address; every target validated --strict with 0 UNDISPOSITIONED failures.
THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

The two accepted exceptions are `add-chain-attestation` and
`add-composed-view-authoring`, both accepted by Brett Heap 2026-09-05,
*"take exit 2"*. **NO REGRESSION.**

## 4. `python3 scripts/validate-sequenced-after.py .`

Pre- and post-encode, identical:

```
sequenced_after validation passed (40 active changes, 10 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (... 12 disposition(s) in force, enforcement error).
```

**exit 0 both times.** This packet's own ledger row was seeded at authoring time
(`state: active`, `class: sole`, `moved_by: "#717"`) and does not move at an
amendment ratification — only at archive, per `tasks.md` § 5.1.

## 5. `python3 scripts/validate-sequenced-after.py . --ledger-diff`

Pre- and post-encode: **`per-change sweep ledger consistent with the corpus
(203 rows)`**, exit 0, identical both times. `DEEPEST DECLARED CHAIN RESOLVED`
(4 hops, from `admit-review-lane-repin-to-merge-approval-envelope`) unchanged.

## 6. `python3 scripts/doc-health.py --single-repo . --fail-on error`

| | critical | error | warning | info | finding lines |
| --- | --- | --- | --- | --- | --- |
| pre-encode (`ce5c054e`) | 32 | 9 | 52 | 14 | 107 |
| post-encode (this commit) | 32 | 9 | 52 | 14 | 107 |

**exit 1 both times — expected, and unrelated to this packet.** `diff` of the
two runs' `severity=` finding lines, sorted, with the `repo=` identity token
normalised, is **EMPTY**: not one finding line moved, was added or was dropped.
**`grep -c register-gate-rules-council-seats` over the post-encode finding lines
returns 0** — no finding names this packet, and none of the three files this
encode adds or re-headers produced one:

- the NEW `review/ratification-2026-09-11-amendment-2.md` satisfies the
  `ratified-provenance` family's ratification-record arm on both limbs
  (`Status: ratified`, plus one citation in the record-citing `Ratified:`
  spelling naming an approver, a date AND a resolvable record path);
- the NEW `review/verification-2026-09-11-amendment-2.md` is not a ratification
  record by either recognizer (its name does not open `ratification-`, its H1
  does not open `# Proposal Ratification:`), so `Status: record` is what the
  taxonomy asks of it and it owes no citation;
- the amendment record keeps `Status: record` and gains one ADDED
  `Ratification:` header line, which is not a sanctioned citation prefix and
  cannot be read as one.

**NO REGRESSION.**

## 7. Summary

All six commands were run before and after the ratification encode, in two
worktrees of the same repository, on the same base commit. **Every figure is
identical**, which is the direct proof that ruling all five OQs at their
RECOMMENDED option moved no delta byte and regressed no gate. The failure sets
that stay red (`disposition-codexfactory-declared-renames`,
`disposition-codexfactory-floor-relocation-retitle` under `--all --strict`; the
9 `error`-severity doc-health findings) are pre-existing corpus residue this
packet does not touch and is not the cited change for.

**WHAT THIS RECORD DOES NOT CLAIM.** It does not claim the pull request's own
required checks — `lane-line`, `openspec-cli-pin`, `pytest-suite`,
`release-tag-gate`, `signed-execution-chain-gate`, `wallet-validation` — have
run; those run on GitHub against the pushed head and are recorded on the pull
request, not here. It does not claim anything is realized: no key is minted, no
seat is bound, no grant, register or roster byte moves, and C2 stays PARKED.

## 8. Provenance of this record

Written in the ratification commit itself, in the worktree
`~/projects/xFactory/openxFactory-worktrees/ratify-q-grc-4`, by lane
`hermes-wallet-exercise` (window `codeXfactory-2`). Every REPOSITORY path in
this file is repo-relative; the worktree paths — here and in § 0's provenance
table — are LOCAL provenance, named as such, in the form
`amend-register-act-5b-projection-proof/review/verification-2026-09-11.md` (the
#960 precedent) uses for the same disclosure. They are recorded rather than
elided because a before/after measurement whose two trees cannot be located is
not reproducible.
