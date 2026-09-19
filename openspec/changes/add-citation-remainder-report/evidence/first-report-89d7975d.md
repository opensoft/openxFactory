# The first reading the shipped report produced, at `main` `89d7975d`

**Subject:** openxFactory issue #1053, `add-citation-remainder-report` § 2.3 — the
first measurement the report itself produces, set beside § 1.9's
hand-instrumented reading of the same tree at the same commit.
**Tree measured:** `opensoft/openxFactory` at
`89d7975d9e042ae6987131633bc0dd91226ea6f2` (`main` at 2026-09-18T20:03:40Z, the
merge commit of realization slice R2, PR #1111), in a dedicated detached
worktree, working tree clean, nothing committed. The reading DECLARES its own
tree state beside its own head, which is what makes it a point in D6's series
rather than a number: `tree_unmodified_at_head: true`, `tree_state: the tracked
content read stands UNMODIFIED at this head`.
**Instrument:** `scripts/report-citation-remainder.py`, landed by realization
slice R1 (PR #1100, merge `83166366d499d58b5e8801e0bb17e346c73fc8e6`), run as
`python3 scripts/report-citation-remainder.py . --json`, **exit 0**. No
refinement is passed — no `--include` and no `--exclude` — and `--all`,
`--tokens` and `--history` are all off: this is the report's own default
reading, the remainder grouped by IDENTITY, with the history probe D2 made
opt-in left off because § 2.3 asks for a reading of a TREE and not of a history.
**Control:** `measure.py`, the hand instrument § 1.9 measured with, run over the
same worktree at the same commit with `--no-history`, its PRIMARY `issue-native`
block. The resolver both instruments load is the same file and not merely the
same name: `scripts/packet_reference.py` is byte-identical at
`b1df95ee80633339907c9e661164a783885a5d30` and at this head, so the resolver is
not a variable anywhere below.
**AND THE SAME READING WAS TAKEN INDEPENDENTLY, BY THE NIGHTLY R2 WIRED, AND
THE TWO AGREE IN EVERY BLOCK BUT THE CHECKOUT PATH.** `opensoft/xFactory`
`doc-health-nightly` run `35415908738` uploaded `citation-remainder-2026-09-19`
in the small hours of 2026-09-19; § 5 sets the two documents side by side.
**THE `--json` DUMP AND THE ITEMIZED TABLE ARE NOT COMMITTED AND ARE NOT IN
THIS PULL REQUEST.** This file carries COUNTS, tables and prose. The dump, the
itemized per-identity table, the all-token dump and both control runs stand in
the repository `opensoft/brett-wip` at
`handoffs/xFactory/attachments/openxfactory-1-2026-09-13/1053/`, cited by
repository and repo-relative path exactly as § 1.9 cites its own 1.5 MB dump.
**§ 6 states why that is a DECISION and not an omission**, and § 7 is the
measurement that proves this file took it.
**Lane:** openxfactory-1 (openXfactory-1), writer `realize-R3`, session 393ade52.

---

## 0. The headline figures

| | at this head |
| --- | ---: |
| **INCLUSIVE remainder** (every flagged entry held in) | **86 TOKENS** |
| **remainder IDENTITIES** (the same population, labelled by identity) | **57** |
| **FILTERED remainder** (every entry carrying the cross-repository flag removed) | **47 TOKENS / 30 IDENTITIES** |
| `AMBIGUOUS` | **0** |

**THE FIGURES ARE PINNED TO THE RUN THAT PRODUCED THEM**, in R1's own words'
spirit: they are a reading of a MOVING corpus and not a property of this packet.
A later run at a later head will print different numbers and none of them makes
this one wrong; what this file fixes is the FIRST point of the series, the one
every later point is compared against.

---

## 1. The population, and the arithmetic that closes over it

| term | at this head |
| --- | ---: |
| tracked entries | 5,536 |
| tracked ENTRIES in scope | 2,993 |
| FILES read | 2,989 |
| skipped, not a file (gitlinks) | 4 |
| skipped, link leaving the root | 0 |
| skipped, undecodable | 0 |

`2,993 = 2,989 + 4 + 0 + 0`, and the report says so in its own output
(`arithmetic_closes: true`) rather than leaving a reader to add it up. Three
default exclusions are in force, each for a stated reason: the ARCHIVED corpus
(frozen record, whose citations may not be repaired), `tests/` (fixtures,
carrying synthetic ids and deliberately-absent files) and `specs/` (Spec Kit
feats, citing illustratively). Four output paths are excluded structurally, the
two `health/` spellings and the two bare-root ones a local redirect lands on;
none of them exists in this tree, and no refinement named one, because no
refinement was passed.

### Tokens and outcomes

| outcome | tokens |
| --- | ---: |
| distinct tokens | **620** |
| RESOLVED (of which 79 resolved somewhere other than the path they were spelled as) | 528 |
| DANGLING, identity half | 80 |
| DANGLING, file half | 6 |
| AMBIGUOUS | 0 |
| NOT A PACKET REFERENCE | 6 |

`528 + 80 + 6 + 0 + 6 = 620`.

### The raw-path-absent arithmetic, in tokens

`169 raw-path-absent = 79 repaired by the identity rule + 80 identity half + 6
file half + 0 ambiguous + 4 not a packet reference`; **165** of those under
choice (2), which holds NOT-A-PACKET-REFERENCE out of the remainder population;
and `165 − 79 = 86`, the INCLUSIVE remainder. The remainder's own arithmetic
row closes the same way: `86 inclusive = 47 filtered + 39 REMAINDER ENTRIES
carrying the cross-repository flag`. The corpus-wide flagged figure at this
head is **83 tokens** — a larger and a DIFFERENT quantity, never the
arithmetic row's term, which is the distinction the requirement fixes and the
report prints in those words.

### Classes, counted in tokens

| class | tokens |
| --- | ---: |
| `truncated` | 5 |
| `punctuation-stripped` | 0 |
| `fixture-path` | 19 |
| `unclassified` | 62 |

`5 + 0 + 19 + 62 = 86`. `unclassified` is the majority and that is D4 working
as ruled: the classifier decides only what a machine can decide from the tree,
and INTENT — *never-existed* against *synthetic*, *self-referential*, the two
file-half repair classes — is a hand read no instrument asserts.

---

## 2. Three readings of one tree, and which one this is

The report prints **86** where this packet's own published headline reads
**82**, and BOTH ARE RIGHT. Two different things separate them and they are
worth keeping apart, because only one of them is methodology:

| reading | distinct tokens | INCLUSIVE remainder | who takes it |
| --- | ---: | ---: | --- |
| `issue-native` — normalization BEFORE deduplication, NOT-A-PACKET-REFERENCE held OUTSIDE the remainder, the cross-repository flag set by ANY qualified occurrence | 620 (619 by § 1.9's instrument, § 4) | **86** | **the SHIPPED REPORT**, because these are the three choices the delta FIXES |
| the prose regex as written, `DANGLING` + `AMBIGUOUS` only | 636 | 90 | `design.md` D0(iv) and § 1.1's own tick |
| `literal` — the prose regex, remainder = raw-absent minus repaired | 636 | 96 | `measure.py`'s carried alternative |

Two identities re-derived here rather than quoted: `636 − 619 = 17` raw
spellings absorbed by normalize-before-dedup, and `96 − 6 = 90`, the six
NOT-A-PACKET-REFERENCE tokens the literal reading holds INSIDE its remainder
and choice (2) holds outside it.

**SO THE GAP A READER SHOULD WEIGH IS 86 AGAINST 90 AT ONE COMMIT, AND NOT 86
AGAINST 82.** The published 82 was measured at an earlier head; at THIS head
the very same middle reading gives 90. The three fixed choices account for
`90 − 86 = 4` tokens here; everything else between 82 and 90 is CORPUS
MOVEMENT, which is what the second half of § 4 is for. § 2.3's check is
against § 1.9's `issue-native` figures, which is the first row of this table
and not D0's headline.

---

## 3. The reproduction gate: the shipped report beside § 1.9's instrument, at this commit

Both readings taken at `89d7975d`, in the same worktree, minutes apart.

| figure | § 1.9's instrument | the shipped report | |
| --- | ---: | ---: | --- |
| tracked entries | 5,536 | 5,536 | ✓ |
| tracked ENTRIES in scope | 2,993 | 2,993 | ✓ |
| distinct tokens | 619 | 620 | **+1, recorded — § 4** |
| tokens with no raw path, choice (2) applied | 165 | 165 | ✓ |
| repaired by the identity rule | 79 | 79 | ✓ |
| `DANGLING` identity half | 80 | 80 | ✓ |
| `DANGLING` file half | 6 | 6 | ✓ |
| `AMBIGUOUS` | 0 | 0 | ✓ |
| **INCLUSIVE remainder, TOKENS** | **86** | **86** | **✓** |
| NOT A PACKET REFERENCE | 5 | 6 | **+1, the same one token** |

**THE GATE IS THE INCLUSIVE READING AND IT AGREES EXACTLY.** § 2.3's contract
is that the two must agree or the report is not the instrument this packet
measured with; on every term of the remainder arithmetic they do, to the token.

**THE ONE FIGURE-PAIR THAT MOVES IS A SINGLE TOKEN, IDENTIFIED RATHER THAN
ESTIMATED.** The two token sets were differenced: the report holds exactly one
token the hand instrument does not, `openspec/changes/archive/..`, and the hand
instrument holds none the report does not. The hand instrument folds that
spelling onto the archive prefix by stripping a dot off a `..` segment; the
report refuses to, because rewriting a path that walks UP into a citation OF
what it walks up from is inventing the citation. The token's outcome is
NOT-A-PACKET-REFERENCE with its raw path PRESENT, so it stands outside the
remainder population twice over and **the remainder is unmoved at 86 either
way**. This is the divergence R1 recorded at § 2.1 (Copilot
`PRRT_kwDOTAvnrs6jsy7w` on PR #1100), re-found here independently at a
different head and in the same direction: distinct tokens +1,
NOT-A-PACKET-REFERENCE +1, remainder Δ 0.

**AND TWO ROWS ARE NOT COMPARED, DELIBERATELY.** The hand instrument's
this-tree-only reading sets aside 23 tokens over all tokens (22 of the
raw-absent) and leaves a remainder of 64; the report's FILTERED reading removes
39 flagged remainder entries and leaves 47. These are two different rules and
not two answers to one question: the report's is D3(c)'s FIXED rule — the
citing line plus the three lines above it, five named signals — and the hand
instrument's is the wide decoration reading § 1.3 states. The packet already
measured the distance between them rather than discovering it here: D3(c)
records the mechanical flag catching 13 of the 14 hand-found cross-repository
tokens with 2 false positives among the other 43. The INCLUSIVE reading is the
one § 2.3 gates on precisely because it holds every flagged entry in and so
does not depend on that rule at all.

---

## 4. The instrument is the one § 1.9 measured with, proved at `b1df95ee`

The comparison above is taken at a head § 1.9 never saw, so it cannot by itself
say the report would have reproduced § 1.9. That is a separate, checkable claim
and it was checked: the shipped report was run over a detached worktree at
`b1df95ee80633339907c9e661164a783885a5d30`, the tree § 1.9 measured, with that
commit's own resolver.

| figure | § 1.9 published @ `b1df95ee` | the shipped report @ `b1df95ee` | |
| --- | ---: | ---: | --- |
| distinct tokens | 571 | 572 | **+1, the same one token** |
| raw path absent | 151 | 151 | ✓ |
| resolve by identity | 73 | 73 | ✓ |
| **remainder** | **78** | **78** (72 identity half, 6 file half) | **✓** |
| `AMBIGUOUS` | 0 | 0 | ✓ |
| NOT A PACKET REFERENCE | 4 | 5 | **+1, the same one token** |
| tracked ENTRIES in scope | — | 2,973 | R1's record: 2,973 |
| FILES read | — | 2,969 | R1's record: 2,969 |

This reproduces R1's § 2.1 record independently, figure for figure, including
both halves of the recorded `..` divergence. So the movement from **78** at
`b1df95ee` to **86** here is CORPUS movement measured by one unchanged
instrument, and not a change of instrument.

---

## 5. The nightly's own reading: D6's series has its first point

The same reading was taken, independently and on a machine nobody in this lane
touched, by the wiring R2 landed.

| | |
| --- | --- |
| caller | `opensoft/xFactory`, `doc-health-nightly` (the reusable suite's artifacts belong to the CALLER) |
| run | `35415908738`, event `schedule`, started 2026-09-19T02:31:31Z |
| aggregation commit | `e7af336fcf0256d21688fe26e341a4781a9f4f50` |
| the `openxFactory` GITLINK that run read the report from | `89d7975d9e042ae6987131633bc0dd91226ea6f2` — this file's own head |
| the reading step | *Citation remainder report (advisory — add-citation-remainder-report § 2.2)*, **success**, 02:52:02Z, no `::warning::` emitted on any of its three failure paths |
| the upload step | *Upload citation remainder report*, **success**, `if-no-files-found: error`, `retention-days: 90` |
| artifact | `citation-remainder-2026-09-19`, id `10575838648`, 10,682 bytes zipped, expires 2026-12-18T02:31:31Z |
| the run's OVERALL conclusion | `failure`, at a later and unrelated step (§ 5.1) |

**THE NIGHTLY'S READING AND THIS ONE ARE THE SAME READING.** The artifact was
fetched and compared block by block against the local run: `head`,
`tree_unmodified_at_head`, `tree_state`, `reading`, `population`, `counts`,
`grouping`, `listed` and the 57 listed identities are all EQUAL. The single
field that differs is `root`, the absolute path of the checkout each run read —
a fact about where the tree stood, not about the tree. The nightly's own
`head` is `89d7975d…` because the aggregation initializes its submodules at the
RECORDED GITLINK, and that gitlink moved to this commit in `opensoft/xFactory`
PR #467 (merge `d9a0c2b6e4fa82911af443d463cb167e35797bac`, 2026-09-18T20:19:14Z)
— which is the act that made the first producing night possible and is
invisible from the artifact alone.

### 5.1 Why a `failure` conclusion is not a fact about this reading

The run died at *Open regression issue*, 75 seconds after the artifact was
finalized, on `GraphQL: Body is too long (maximum is 65536 characters)
(createIssue)` — the nightly's regression-issue body outgrowing GitHub's limit,
which is openxFactory #1118 and has a fix in flight. The reading step is
`if: always()` and ran to `success` before it; the upload ran to `success`
after it. The step took its SUCCESS branch, which is a measurement and not an
inference: all three `::warning::` lines in the log stand inside the runner's
echo of the step's own script between its `##[group]` and `##[endgroup]`
markers, and the step emitted NOTHING of its own between that `##[endgroup]`
and the next step's group — so the report ran, the reading was read back, and
the tree-state gate passed.

---

## 6. What this file does not carry, and why that is a decision

**IT CARRIES FIGURES AND NOT THE ITEMIZED REMAINDER.** This directory is INSIDE
the scanned population. The report's own itemized table writes one citation
token per remainder line and a `cited at <path>:<line>` line under it for every
occurrence — so committing it here would be the largest single act of
self-counting this packet could perform, which is the mechanism D5 exists to
refuse, and D0(iv) states the governing fact in one line: *the tokens a packet
adds are the ones it QUOTES*. § 1.9 already measured the cost of a single
quoted token at +1 remainder.

There is a second and harder reason, in the delta's own text. The requirement
*The reported population is derived from a stated recipe* carries the scenario
*The report's own output is committed into the corpus*, whose THENs are that
the committed report's path MUST be excluded from the file population AND that
the exclusion MUST be in force in the same change that first commits it.
Committing the dump or the itemized table here would FIRE that antecedent and
pull the output-path exclusion — code — into a slice the plan sized as
documents. Carrying counts instead leaves the antecedent unfired, which is
§ 7's measurement.

**THIS IS THE RECOMMENDATION THE REALIZATION PLAN'S Q3 AUTHORIZES ITS AUTHOR TO
TAKE, TAKEN, WITH CONFIRMATION OUTSTANDING.** The lawful alternative — commit
the itemized list and land the exclusion in the same pull request — was not
taken here and remains open to a ruling.

What stands in `opensoft/brett-wip` at
`handoffs/xFactory/attachments/openxfactory-1-2026-09-13/1053/`, by
repo-relative path: the reading's own `--json` dump; the itemized human table;
the all-token dump the § 3 difference was taken from; the hand instrument's run
at the same head, its stdout and its JSON; the independent prose-regex recount;
the shipped report's run over the `b1df95ee` tree; the nightly artifact as
fetched; and the merge-base/head pair § 7 measures.

---

## 7. The mint check: committing this file moved no remainder

The check R1's § 2.1 record established, run again for this file, in two clean
detached worktrees rather than by restoring a dirty tree: the shipped report at
this branch's MERGE BASE, where this file does not exist, and at this branch's
HEAD, where it is tracked and therefore read.

| figure | at the merge base | at this branch's head |
| --- | ---: | ---: |
| distinct tokens | 619 | 619 |
| INCLUSIVE remainder, TOKENS | 86 | 86 |
| remainder IDENTITIES | 57 | 57 |
| FILTERED remainder, TOKENS | 47 | 47 |
| FILES read | 2,978 | 2,979 |

**Δ = 0 on every figure but `FILES read`, which moves by exactly one file — and
that one file is this one.** A note that had quoted what it should have
described would have moved the first four rows; this one describes shapes and
quotes only tokens that resolve. The exact shas, and the same check's output
verbatim, are in the pull request that lands this file.

---

## 8. What this reading does not claim

* **It realizes no requirement.** All five are R1's, realized by the report and
  its unit tests. What this reading adds is a DIFFERENT KIND of evidence — a
  live reading of the real corpus where R1's is a fixture corpus built in a
  temporary tree — for six scenarios it does not claim as newly passed:
  *The report is taken over a corpus*; *The tree read is not clean at the head
  printed* (the CLEAN half only — the modified branch is R1's fixtures and
  R2's step, and is not exercised here); *No identity in the corpus is claimed
  by two packets* (the `AMBIGUOUS` row printed as zero rather than omitted);
  *A reading is compared against an earlier reading* (§ 3 and § 4, each stating
  the pattern and the three fixed choices it applied); *The report's own output
  is committed into the corpus* (satisfied by CONSTRUCTION, the antecedent
  never firing, which § 7 measures rather than asserts); and *The report finds a
  remainder* (a non-empty remainder, exit 0).
* **It is not a gate.** The report is advisory by ruling and by construction;
  nothing in this reading fails anything, and promoting the report to a gate is
  a separate act on a separate word.
* **It does not repair a citation.** Not one of the 86 is touched; § 4.3 of the
  task list records that as residue named and not taken.
* **It does not classify intent.** 62 of the 86 are `unclassified` and stay so.
