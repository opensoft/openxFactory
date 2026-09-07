# Verification record: amend-absent-changelog-is-an-answer, 2026-09-07

Status: record
Kind: report
Captured: 2026-09-07, in lane `openxfactory-1`, on branch
`change/amend-absent-changelog-is-an-answer` (openxFactory PR #753).

**This record is CAPTURED AT MERGE, not at first push, and EVERY NUMBER BELOW WAS
RE-DERIVED PRE-CAPTURE** — on the tree this record sits in, at `origin/main`
**`7f7ce75a`**, the head this branch's FOURTH and last catch-up merge took, and
with the ratification encoded. Every figure below was taken twice — once at
`origin/main` `64aad02e`, in the encode commit, and again on the merged tree
after `07869a37` — and **not one of them moved**; the second column is what
stands here. `record-immutability` forbids editing a
`Status: record` document AFTER capture; capture is the merge of the pull request
that establishes it, and nothing is merged yet. A commit cannot write its own
hash into its own tree, so the ratification commit is named by its subject and
its position on the branch rather than by a hash.

**NOTHING THE PULL REQUEST BODY CARRIED AT `5f0154e6` IS TAKEN ON TRUST.** Every
figure was re-run in the ratification encode, on the merged tree, and the body is
refreshed to match.

**THE ONE THING THIS RECORD DOES NOT QUOTE, AND WHY.** `doc-health`'s report
prints corpus WORD totals as well as findings. Those totals are computed over
`GOVERNED_ROOTS` (`contracts`, `docs`, `examples`, `ideation`, `templates`) plus
promoted specs, so `openspec/changes/` — this packet, its delta, and the two
records this commit adds — moves none of them by construction; the lifecycle
families still READ those files, through `LIFECYCLE_SCAN`
(`openspec/changes/**/proposal.md` and `openspec/changes/**/review/*.md`), which
is the scope that matters here. What is quoted is the FINDING set.

## 1. `validate-openspec-cli-pin.py --change amend-absent-changelog-is-an-answer --strict --no-cache`

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact; integrity sha512-oFE2Lj7WVSc87nSi… verified
-> openspec validate amend-absent-changelog-is-an-answer --strict --json
Totals: 1 passed, 0 failed (1 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
```

## 2. THE PINNED 1.12 ENTRYPOINT OVER THE WHOLE CORPUS, EXACTLY AS `openspec-cli-pin-gate.yml` RUNS IT

`python3 scripts/validate-openspec-cli-pin.py --all --no-cache`:

```
Totals: 97 passed, 2 failed (99 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures.
THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

**NEITHER DISPOSITIONED FINDING IS THIS CHANGE'S**, and no third appears. Both
are `#677`'s standing dispositions — 1.12's scenario-currency check is
MARKER-BLIND, so it refuses two landed `Merged into` renames that canon's own
worked example defines, and Brett Heap accepted them on *"take exit 2"*.

**AND THAT IS THE PREDICTION THIS RUN CONFIRMS.** 1.12 refuses a `## MODIFIED`
block that OMITS a SCENARIO the current spec still has. This block **omits none
and retitles none** — it carries all 30 promoted titles and replaces TWO BULLETS
inside one scenario — so it adds **no undispositioned failure**.

## 3. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (39 active changes, 4 declaring the field).
```

`python3 scripts/validate-sequenced-after.py . --ledger-diff`:

```
declaring an explicit `[]` root claim: 0
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 2 hop(s), from add-per-change-sweep-ledger

per-change sweep ledger consistent with the corpus (180 rows).
```

**RATIFICATION MOVES NO ROW.** A row's derived keys are `state`, `class`,
`declares`, `depth` and `prose`; none of them reads a lifecycle status, so a
`draft` → `ratified` transition is invisible to the ledger by construction. This
change's row stands exactly as `6ec99c8c` seeded it —

```
amend-absent-changelog-is-an-answer: {state: active, class: co-modifier,
                                      declares: absent, prose: false,
                                      moved_by: "#753", moved_on: "2026-09-07"}
```

`class: co-modifier` because the `## MODIFIED` block writes `doc-health`
§ *Release-tag publication*, a key `add-release-tag-publication-check`,
`declare-spent-bundle-state`, `add-release-tag-gate`,
`amend-published-tip-unreadable-scenario` and
`amend-unreadable-read-sibling-scenarios` already write; **all five are
ARCHIVED**, so no partner flips and no MOVEMENT LOG entry is owed. **ROWS MOVED
BY THE RATIFICATION COMMIT: ZERO.**

## 4. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

## 5. THE ORIGIN-RETENTION GATE, ON THE ACTIVE DIRECTORY

`python3 scripts/proposal-support.py . verify amend-absent-changelog-is-an-answer`:

```
proposal support verification ok
```

**THE TWO `--archive-gate` ARMS ARE RUN AGAINST THE RATIFICATION COMMIT ITSELF,
WHICH IS WHY THEIR OUTPUT REACHES THIS FILE ONE COMMIT LATER.** Both take
`--ratified-ref`, and the ref they need is the commit that carries this record —
a commit cannot write the result of a check run against its own hash into its own
tree. They are run the moment that commit exists, and their output is appended
here in a FOLLOW-UP commit touching `review/` files only, which leaves the
RATIFYING commit exactly where it is: the gate resolves it as the FIRST commit
whose `proposal.md` declares `Status: ratified`, and a later records-only commit
never becomes that one.

```
$ python3 scripts/validate-sequenced-after.py . \
    --archive-gate openspec/changes/amend-absent-changelog-is-an-answer \
    --ratified-ref 58654e34
sequenced_after retention gate passed (declaration unchanged since ratification).
exit=0
```

```
$ python3 scripts/validate-scope-globs.py . \
    --archive-gate openspec/changes/amend-absent-changelog-is-an-answer \
    --ratified-ref 58654e34
scope_globs scope-retention gate passed (scope unchanged since ratification).
exit=0
```

**BOTH ARMS: RETAINED**, and re-run RETAINED a second time on the merged tree
after `07869a37`. `58654e34` is the ratification commit — verified to be
the FIRST commit on this branch whose `proposal.md` declares `Status: ratified`,
which is exactly the commit the gate resolves on its own at archive time. This
paragraph and the two blocks above it are the whole of the follow-up records
commit; it touches `review/` files only, so it moves neither the ratified bytes
nor the commit the gate resolves.

**THE STATUS FLIP AND THE APPROVAL PAIR MUST MOVE IN ONE COMMIT, AND THEY DO.**
The gate resolves the RATIFYING COMMIT as the FIRST commit whose `proposal.md`
declares `Status: ratified`, and compares the origin declaration there with the
one being archived. So `.openspec.yaml`'s approval pair is added in the same
commit as the flip, and that is the last time the file is edited.

## 6. `python3 scripts/doc-health.py --single-repo .` — TWO CONTROLS, NOT ONE

Measured against controls minutes apart on the same clock — a temporary worktree
of `origin/main` `7f7ce75a` INSIDE this clone, removed afterwards — not against a
stale baseline.

| | critical | error | warning | info |
| --- | --- | --- | --- | --- |
| `origin/main` `7f7ce75a` (worktree control) | 9 | 8 | 58 | 13 |
| this branch, BEFORE the ratification was encoded | 9 | 8 | 58 | 13 |
| this branch, AFTER it was encoded | 9 | 8 | 58 | 13 |

All three read `9 critical, 8 error, 58 warning, 13 info` (88 findings), with
`New regressions vs previous report: 0`.

- **Against `origin/main`:** a line-by-line diff of the two reports is **EMPTY**
  once the checkout's own directory-name token is normalized.
- **Against the pre-ratification branch:** the diff of the FINDING lines is
  **EMPTY** — the status flip, the citation lines, the approval pair, the
  README row and both new record files together add **not one finding**.
- **The families that could have spoken about this transition say nothing:**
  `doc-health` names `amend-absent-changelog-is-an-answer`
  **ZERO** times in the whole report — no `ratified-provenance` finding,
  no `proposal-origin` finding, no `duplicate-packet` finding.

**AND THE RATIFICATION IS INSIDE THAT READING, MADE TO FIRE AND THEN CLEARED
RATHER THAN ASSUMED AWAY.** `proposal-origin`'s class 7 reports an ERROR for *"a
proposal declaring `Status: ratified` while its origin still carries drafting
provenance and asserts no approval"*. With `Status: ratified` set and the
approval pair REMOVED from `.openspec.yaml`, `--family proposal-origin` reported
exactly that and nothing else:

```
Findings: 0 critical, 1 error, 0 warning, 0 info.
- [error] openspec/changes/amend-absent-changelog-is-an-answer — proposal declares
  `Status: ratified` while its origin asserts no approval — approval MUST appear
  when the status claims it
```

Restoring `approved_by` + `approved_on` BESIDE the retained
`proposed_by`/`proposed_on` — `kind`, `id` and `reason` unmoved, the
addition-not-rewrite shape `add-drafted-proposal-origin` defined — clears it:

```
Findings: 0 critical, 0 error, 0 warning, 0 info.
```

and the restored file is byte-identical to the one this commit carries.

**AND `ratified-provenance` IS PROBED THE SAME WAY**, because the family counts
citation lines and a count of one cannot be told from a family that never read
the document. A SECOND `Ratified:` line added to `proposal.md`'s header window:

```
Findings: 6 critical, 0 error, 0 warning, 0 info.      (5 on origin/main, none this packet's)
- [critical] openspec/changes/amend-absent-changelog-is-an-answer/proposal.md —
  carries 2 ratification citation lines, not one
  action="keep exactly one: Ratified by: where an approving OpenSpec change
  exists, Ratified: where none does"   class="auto-fixable"
```

Removed again:

```
Findings: 5 critical, 0 error, 0 warning, 0 info.
(the same five `origin/main` carries — add-sequenced-after-substrate,
add-structured-scope-substrate, mirror-floor-regeneration-automation and the
archived mirror-floor-addition-grace pair — and NOT ONE of them is this packet's)
```

### `--family release-tag-publication`, both sides

```
control (origin/main 7f7ce75a): Findings: 0 critical, 0 error, 0 warning, 1 info
branch                        : Findings: 0 critical, 0 error, 0 warning, 1 info
```

The identical single finding both sides — the `contract-v2.6` SPENT record on
`contracts/releases/contract-v2.6.digests.yaml`. **This repository never reaches
the amended arm**: it carries a readable `contracts/CHANGELOG.md` at its
published tip.

### `--family modified-block-currency`, and the marker probe both ways

```
control (origin/main 7f7ce75a): Findings: 0 critical, 0 error, 0 warning, 8 info
branch                        : Findings: 0 critical, 0 error, 0 warning, 8 info
```

Zero alone cannot be distinguished from a block the family never read, so it was
probed. **The second marker (the `AND` bullet's) disabled:**

```
Findings: 0 critical, 0 error, 0 warning, 9 info
- [info] openspec/changes/amend-absent-changelog-is-an-answer/specs/doc-health/spec.md
  — active MODIFIED block for 'Release-tag publication' does not carry 1 of the
  232 body units and scenario bullets openspec/specs/doc-health/spec.md currently
  states for it — a divergence this arm CANNOT distinguish from a deliberate
  rewording, and does not claim to: [bullet] '**AND** where the commit IS held,
  the skip MUST SAY THAT and MUST state the presence — naming the held commit and
  the read that returned not…'
  action="restate the requirement as canon currently states it, or declare the
  deletion with a `Removed from canon by` marker"  class="contested"
```

**Restored:** `Findings: 0 critical, 0 error, 0 warning, 8 info` — silent again,
and the delta byte-identical to the one this commit carries.

**So the block raises ZERO carriage findings from its own family while genuinely
being read by it.**

## 7. The self-reference discharge — both markers, one name each, no span in the reason

Both markers this block carries, parsed through `parse_marker` on the ratified
tree:

```
marker paragraphs found: 2
--- marker 1 ---
  Marker('removed', 'amend-absent-changelog-is-an-answer',
         ['**THEN** the family MUST report a skip naming that read, and MUST NOT treat the absence of a declaration it could not look for as the absence of a declaration'])
  names: 1     reason chars: 388     reason contains a backtick code span: False
--- marker 2 ---
  Marker('removed', 'amend-absent-changelog-is-an-answer',
         ["**AND** where the commit IS held, the skip MUST SAY THAT and MUST state the presence — naming the held commit and the read that returned nothing at it, and NOT asserting a file absence the held commit does not establish — because a tip this checkout holds is an ANSWER rather than a read that failed, and reporting it in the unfetched case's words sends a reader to look for a fetch defect that does not exist"])
  names: 1     reason chars: 496     reason contains a backtick code span: False
```

With no code span in either reason, the RETIRED grammar (the reason is everything
after the LAST span's following ` — `) and the AMENDED one (the names are the
spans closing before the FIRST ` — ` outside a span) derive the SAME single name
and the SAME reason from each. **This is a constraint on amendment markers
generally while both grammars are in the estate** (`design.md` D4).

## 8. THE D6 SHIM TABLE — SIX STATES, BOTH SIDES

One shim declaring `contract-v2.0`, its tip HELD (`present_commits`), its tag
absent (an ANSWER, `(None, None)`, not an unlistable `None`), its first-parent
walk declaring the bundle throughout so the distance arm reaches its error band.
The runs differ in ONE seam answer and in nothing else.

| the shim's `contracts/CHANGELOG.md` | at `origin/main` `7f7ce75a` | on this branch |
| --- | --- | --- |
| absent — per-path `None` at a HELD tip, tree LISTS NO SUCH PATH | ONE `Skip` (held words), nothing graded | ONE `error` on `contracts/manifest.yaml` naming the untagged bundle, PLUS one `info` on `contracts/CHANGELOG.md` recording the read |
| present and EMPTY | ONE `error` on `contracts/manifest.yaml` | unchanged — the same ONE `error` |
| below the enforcement floor, no changelog | `[]` | `[]` |
| held tip, tree LISTS AN ENTRY at the path, blob absent | ONE `Skip`, in the HELD words | ONE `Skip`, naming the entry and the failed read |
| held tip, tree UNLISTABLE at that path | ONE `Skip`, in the HELD words | ONE `Skip`, saying UNESTABLISHED, and saying the tip is held |
| tip NOT held, no changelog | ONE `Skip` — and it says *"WHICH THIS CLONE HOLDS"*, asserting the opposite of its own condition | ONE `Skip` saying the clone does NOT hold the tip and that a bounded fetch was attempted |

`origin/main` has ONE arm and gives all four held/unheld states ONE answer; the
branch's four distinct answers are the whole of what this packet does to the
read.

**The error's words, both sides, byte for byte:**

```
contract-v2.0 is declared and has no published annotated tag more than 5
first-parent landings after the commit that declared it — under the versioning
policy it is NOT PUBLISHED, and its presence in the manifest is not a release
```

**The `info` this packet adds, verbatim:**

```
contracts/CHANGELOG.md yielded nothing at the published tip tip, WHICH THIS CLONE
HOLDS — the commit is held in this store and no readable contracts/CHANGELOG.md
blob is reachable at it, and the tree at that commit LISTS NO SUCH PATH, so this
is neither an unfetched commit nor a listed entry whose blob did not come back,
and NO SPENT DECLARATION EXISTS at contracts/CHANGELOG.md to be read; the bundles
in scope (contract-v2.0) are graded with no declarations, exactly as at an empty
changelog, rather than skipped past
```

**The two skips a HELD tip still emits, verbatim:**

```
alphaFactory: contracts/CHANGELOG.md could not be read at the published tip tip,
WHICH THIS CLONE HOLDS AND WHOSE TREE CARRIES THAT PATH — the tree at that commit
LISTS AN ENTRY at that path and no readable blob came back for it, which is a READ
THAT FAILED rather than an absent document; a SPENT declaration for contract-v2.0
could not be looked for, which is not the same fact as there being none
```

```
alphaFactory: contracts/CHANGELOG.md could not be read at the published tip tip,
WHICH THIS CLONE HOLDS, and the tree at that commit could not be listed either,
so whether the document is absent or merely unreadable is UNESTABLISHED; a SPENT
declaration for contract-v2.0 could not be looked for, which is not the same fact
as there being none
```

## 9. `python3 -m pytest tests/doc-health -q`

```
1593 passed, 7 warnings in 278.47s (0:04:38)
```

`tests/doc-health/test_release_tag_publication.py` alone: **152 passed**, against
**146 passed** measured in the `origin/main` `7f7ce75a` worktree control on the
same clock — six ADDED and one CONVERTED.

**A STATUS FLIP ADDS NO TEST**, and the count is identical before and after the
ratification was encoded.

### THE MUTATION PROBE ON ALL THREE GUARDS, re-run on the ratified tree

| the mutation | the result |
| --- | --- |
| revert the held-tip split to `if changelog is None:` | **5 failed, 147 passed** |
| disable D3a's tree consultation (`if False:`) | **3 failed, 149 passed** |
| drop `and in_scope` from D3a's tree consultation | **1 failed, 151 passed** |
| all three restored | **152 passed** |

The third row is why a test was ADDED in the fix round: before it, that mutation
left ALL 151 tests green. After each probe the module was restored from a
byte-copy and `git status` reported the working tree clean.

## 10. The branch's merge history

**THREE merges from `main` stand on this branch**, and the ratification encode
took no fourth, `origin/main` having not moved past `64aad02e`:

| merge | took `origin/main` | note |
| --- | --- | --- |
| `787130fb` | `44d8fbaf` | ONE conflict, `README.md`, where both sides added a row at the top of *Active changes*; BOTH rows kept, neither edited. Its own message says *"No conflict"* and carries git's `# Conflicts:` block below its trailers — the message is wrong and the content is right, and history is not rewritten for it |
| `2f8f93d0` | `d52e6b88` | UNDOCUMENTED: git's bare default merge message, no `Lane:` trailer, no body. It brought only `main`'s own commits and touched nothing of this packet |
| `5f0154e6` | `64aad02e` | No conflict; the six paths `main` moved are `openspec/changes/add-chain-attestation/tasks.md`, three validator scripts and two files under `tests/sequenced_after/`, none of which this branch edits |
| `07869a37` | `7f7ce75a` | Taken AFTER the ratification was encoded. No conflict: `main` added the Apache-2.0 `LICENSE`, a four-line `## License` section at the END of `README.md` — several thousand lines below the OpenSpec Records block this branch edits — and split `scripts/ideation_dashboard/serve.py` with its tests. Nothing under `scripts/doc_health/` or `tests/doc-health/` moved. Written message and `Lane:` trailer, unlike `2f8f93d0` |

**No ledger row moved and no partner flipped in any of the four.** **AND THE
FOURTH IS WHY THIS FILE IS THE ONLY THING THE FOLLOW-UP COMMITS TOUCH**: when
`main` moves after the encode, the branch takes the merge and every number here
is re-derived, in a SEPARATE commit touching `review/` files only, so the
RATIFYING commit — `58654e34`, the first commit whose `proposal.md` declares
`Status: ratified` — never moves. If `main` moves again before this pull request
lands, that is done a third time, before capture.

## 11. Independent review

**Codex: ONE round** (`6ec99c8c`, 13:13:17Z), **one P2**, taken in full — the
tree consultation of `design.md` D3a. Thread replied to and **resolved**.
**Copilot: SEVEN rounds by head** — `6ec99c8c` (13:10:45Z), `48ecf6f4`
(13:15:39Z), `72153d23` (13:26:47Z), `787130fb` (13:32:05Z), `446b4720`
(14:53:16Z), `5f0154e6` (14:58:35Z), `7313b45c` (15:13:34Z) — of which rounds 1,
2 and 5 carried comments; all were taken or dispositioned and **every thread is
resolved**. **Sourcery** is the private-repo upsell stub (13:07:38Z). Three
adversarial review lenses returned **MERGEABLE_AFTER_FIXES** with eleven
findings; all eleven were folded across `4e237311`, `446b4720` and `7313b45c`,
two of them as DISCLOSURES with named successors, and a re-verification over
`7313b45c` returned **READY_TO_ENCODE**. The full disposition is
`ratification-2026-09-07.md` § 5.
