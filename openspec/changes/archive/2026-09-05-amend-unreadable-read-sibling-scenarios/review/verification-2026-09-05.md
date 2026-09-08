# Verification record: amend-unreadable-read-sibling-scenarios, 2026-09-05

Status: record
Kind: report
Captured: 2026-09-05, in lane `openxfactory-1` (session `5e783e4d`), on branch
`change/amend-unreadable-read-sibling-scenarios` (openxFactory PR #688).

**This record is CAPTURED AT MERGE, not at first push, and EVERY NUMBER BELOW WAS
RE-DERIVED PRE-CAPTURE** — on the tree this record sits in, after this branch's
SECOND merge from `main` (taking `origin/main` `9b1888bb`: #693's restored origin
declaration, #694's pinned-CLI archive path, #684 and #696) and after the
adversarial review was folded. `record-immutability` forbids editing a
`Status: record` document AFTER capture; capture is the merge of the pull request
that establishes it, and nothing is merged yet. A commit cannot write its own hash
into its own tree, so the ratification commit is named by its subject and its
position on the branch rather than by a hash.

**None of the numbers the pull request body first carried survives unchecked.**
They were taken at an older tree, before two merges from `main` and before the
fold; every one is re-derived here and the body is refreshed to match.

**If `main` moves again before this pull request lands**, the branch takes another
merge and every number here is re-derived a second time, with § 8 extended to say
so, before capture.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-unreadable-read-sibling-scenarios --strict`

```
Change 'amend-unreadable-read-sibling-scenarios' is valid
```

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`

```
Totals: 95 passed, 0 failed (95 items)
```

**AND THE READING THAT GOES WITH IT, because this line disagrees with the one the
pull request body first carried.** The body reported *92 passed, 2 failed (94
items)*. Two things moved. **The item count** is 95 because `main` brought its own
change directories in the two merges — neither is this packet's. **The failure
count is 0 here because THIS INVOCATION IS THE `PATH` CLI, which in this session
is `@fission-ai/openspec` 1.2.0**, and 1.2.0 has no scenario-currency check. The
two failures belong to the PINNED 1.12 entrypoint and are reported under § 3,
which is what CI actually runs. The two lines are not in conflict; they are two
CLI versions, and both are recorded rather than the flattering one alone.

## 3. THE PINNED 1.12 ENTRYPOINT, EXACTLY AS `openspec-cli-pin-gate.yml` RUNS IT

`python3 scripts/validate-openspec-cli-pin.py --all --no-cache`:

```
Totals: 93 passed, 2 failed (95 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied)
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content
address; every target validated --strict with 0 UNDISPOSITIONED failures.
```

**NEITHER FINDING IS THIS CHANGE'S**, and no third appears. Both are `#677`'s
standing dispositions — 1.12's scenario-currency check is MARKER-BLIND, so it
refuses two landed `Merged into` renames that canon's own worked example defines,
and Brett accepted them on *"take exit 2"*.

**AND THAT IS THE PREDICTION THIS RUN CONFIRMS.** 1.12 refuses a `## MODIFIED`
block that OMITS a SCENARIO the current spec still has. This block **omits none
and retitles none**: it carries all 30 promoted titles and replaces a `WHEN`
BULLET inside one of them, which that check cannot see. The bullet replacement is
declared to the in-house `modified-block-currency` family by the reserved
`Removed from canon by` marker instead (§ 7). Had the amendment retitled the
scenario, this run would have produced a THIRD refusal and the packet would have
owed a disposition — a governed edit, and not this lane's to write.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (36 active changes, 2 declaring the field).
```

## 5. `python3 scripts/validate-sequenced-after.py . --ledger-diff`

```
per-change sweep ledger consistent with the corpus (174 rows).
```

**RATIFICATION MOVES NO ROW, AND NEITHER DID THE MERGE.** A row's derived keys
are `state`, `class`, `declares`, `depth` and `prose`; none of them reads a
lifecycle status, so a `draft` → `ratified` transition is invisible to the ledger
by construction. The merge from `main` auto-merged the ledger with no conflict and
no re-seed: this change's row stands exactly as `04c2a97b` seeded it, with the
real pull request number —

```
amend-unreadable-read-sibling-scenarios: {state: active, class: co-modifier,
                                          declares: absent, prose: false,
                                          moved_by: "#688", moved_on: "2026-09-05"}
```

`class: co-modifier` because the `## MODIFIED` block writes `doc-health`
§ *Release-tag publication*, a key `add-release-tag-publication-check`,
`declare-spent-bundle-state`, `add-release-tag-gate` and
`amend-published-tip-unreadable-scenario` already write; **all four are ARCHIVED**
and were co-modifiers before this change, so **no partner flips and no MOVEMENT
LOG entry is owed**. **ROWS MOVED BY THIS PULL REQUEST: ONE — this change's own,
and it was seeded, not moved.**

## 6. `python3 -m pytest tests/doc-health tests/sequenced_after -q`

```
1739 passed
```

`tests/doc-health/test_release_tag_publication.py` alone: **146 passed**
(145 → 146). The four `tests/sequenced_after/test_sweep.py` failures the pull
request body first reported were the documented pre-seed state — *"missing row:
amend-unreadable-read-sibling-scenarios is in the corpus and has no ledger row"* —
and the row was seeded in `04c2a97b`. **There is no failing test at this head.**

**WHAT THE ONE ADDED TEST PINS.** `test_an_absent_changelog_says_the_tip_is_held_rather_than_unfetched`
asserts the two new fragments as fresh literals and asserts NEGATIVELY on two
counts: against the manifest arm's *"a bounded fetch of exactly that commit was
attempted and did not obtain it"*, so two skips that are only positively pinned
cannot drift into each other's words; and against the OVER-CLAIMING form
*"carries no contracts/CHANGELOG.md"*, which the fold added. It also declares its
precondition rather than assuming it — `present_commits={"tip"}` with
`fetch_calls == []` asserted — so the held-tip words are pinned over a double
that actually holds the tip and holds it without a round trip (Copilot round 2).
The existing changelog test is UNCHANGED and still passes: all three of its
literals are still carried.

## 7. `python3 scripts/doc-health.py --single-repo .` — SAME-CLOCK CONTROL

Measured against a control run minutes apart, not against a stale baseline: this
report ages by the calendar. The control is a worktree at `origin/main`
`9b1888bb` — the `main` this branch has merged — and the two runs are minutes
apart on the same clock.

| | critical | error | warning | info |
| --- | --- | --- | --- | --- |
| `main` `9b1888bb` | 8 | 7 | 30 | 13 |
| branch | 8 | 7 | 30 | 13 |

Both read `8 critical, 7 error, 30 warning, 13 info`, with `New regressions vs
previous report: 0`. A line-by-line diff of the two reports is **EMPTY** once the
checkout's own directory name is normalized — the only lines that differ raw are
the ones that PRINT that name (`Repo-Identity:`, the scope line, the
validator-entrypoint line, and the `<repo>:` prefix each finding carries).

**AND THE RATIFICATION IS INSIDE THAT READING.** The status transition is not
free to `doc-health`: `proposal-origin`'s class 7 reports an ERROR for *"a
proposal declaring `Status: ratified` while its origin still carries drafting
provenance and asserts no approval"*. **It was made to fire and then cleared,
rather than assumed away.** With `Status: ratified` set and `.openspec.yaml`
untouched, `--family proposal-origin` reported exactly that finding against this
change; adding `approved_by` + `approved_on` BESIDE the retained
`proposed_by`/`proposed_on` — `kind` and `id` unmoved, which is the
addition-not-rewrite shape `add-drafted-proposal-origin` defined for this
transition — clears it. That is why the ratification commit touches
`.openspec.yaml`, and it is the last time that file is edited.

**THE `modified-block-currency` PROBE, BOTH WAYS, ON THE FOLDED TREE.** The
family naming this change zero times cannot be distinguished from a block it
never read, so it was probed and fired both times:

- **marker removed** → *"does not carry **1** of the 222 body units and scenario
  bullets"*, naming exactly the retired changelog `WHEN` — one unit dropped, and
  the marker is what declares it;
- **a promoted scenario title mutated** → *"omits 1 of the **30** scenarios …
  'The published tag is lightweight rather than annotated'"*;
- **restored** → names this change zero times again.

## 8. The branch's merge history

**TWO merges from `main`.**

1. `3bb41b63` took `76434aac` (#680, `implement-omniworker-install-repo`), which
   had collided with this branch's README row at the same insertion point.
   Resolved by keeping BOTH, this branch's first.
2. The merge carried in this pull request took `9b1888bb` — #693 (the restored
   archived origin declaration of `amend-published-tip-unreadable-scenario`),
   #694 (`proposal-support` archiving through the pinned OpenSpec CLI rather than
   PATH), #684 and #696. **Every hunk auto-merged**: README kept `main`'s side and
   this packet's Active row, and the corpus ledger kept both this change's row and
   #685's archived row for the predecessor. No row moved and no partner flipped.

## 9. The two behaviours measured on shims, and the control that makes each real

**THE THIRD FACT (§ 4 of the ratification record, P3), reproduced on real git.**
In a store built by copying a repository and deleting one loose blob object,
`git cat-file -e <sha>^{commit}` and `^{tree}` both report HELD while
`git cat-file --batch` answers `<commit>:contracts/CHANGELOG.md missing` — the
per-path None `blobs_at` turns into this arm. So "the commit is held" does not
license "the commit carries no such file", and the skip now says only what the
read gives it.

**THE SUPPRESSION (§ 4, P2), measured with its own control.** A shim with the tag
ABSENT and no changelog blob at a held tip returns one `Skip`; the SAME shim with
an EMPTY `contracts/CHANGELOG.md` returns one `error`. **The control is the same
pair run against `origin/main` `9b1888bb` in a second worktree: identical
answers.** So the behaviour is pre-existing, this packet does not introduce it,
and this packet does not fix it — it is carried as a named carve-out and an owed
successor (`design.md` D6, `tasks.md` § 6).

## 10. Independent review

**Codex REFUSED twice** on usage limits (17:55Z and 18:20Z) — **no Codex round
ran**. **Sourcery** is the private-repo upsell stub. **Copilot ran twice**: round
1 on the pre-merge head was 🟢 Approval recommended; round 2 on `3bb41b63` was
🟡 Changes recommended and was RIGHT — the new test asserted held-tip wording
without setting the `FakeGit` object-store precondition — and it is fixed in the
fold commit. The full disposition is `ratification-2026-09-05.md` § 5.
