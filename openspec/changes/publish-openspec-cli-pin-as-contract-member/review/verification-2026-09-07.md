# Verification record: publish-openspec-cli-pin-as-contract-member, 2026-09-07

Status: record
Kind: report
Captured: 2026-09-07, in lane `openxfactory-1`, on branch
`change/publish-openspec-cli-pin-as-contract-member` (openxFactory PR #757).

**This record is CAPTURED AT MERGE, not at first push, and EVERY NUMBER BELOW
WAS RE-DERIVED PRE-CAPTURE** — on the tree this record sits in, at `origin/main`
**`f756a91f`**, the head this branch's THIRD and last catch-up merge (`ee657e30`)
took, and with the ratification encoded. `record-immutability` forbids editing a
`Status: record` document AFTER capture; capture is the merge of the pull
request that establishes it, and nothing is merged yet. A commit cannot write
its own hash into its own tree, so the ratification commit is named by its
subject and its position on the branch rather than by a hash, and the two
`--archive-gate` runs that take it as `--ratified-ref` are appended in a
follow-up commit touching `review/` files only.

**NOTHING THE PULL REQUEST BODY CARRIED AT `8eb5dc8f` IS TAKEN ON TRUST.** Every
figure was re-run on the merged tree in the ratification encode, and the body is
refreshed to match. Figures that MOVED because `main` moved are marked.

**THE ONE THING THIS RECORD DOES NOT QUOTE, AND WHY.** `doc-health` prints
corpus WORD totals as well as findings. Those totals are computed over
`GOVERNED_ROOTS` plus promoted specs, so `openspec/changes/` — this packet, its
delta and these two records — moves none of them by construction; the lifecycle
families still READ those files, through `LIFECYCLE_SCAN`
(`openspec/changes/**/proposal.md` and `openspec/changes/**/review/*.md`), which
is the scope that matters here. What is quoted is the FINDING set.

## 1. `validate-openspec-cli-pin.py --change publish-openspec-cli-pin-as-contract-member --strict --no-cache`

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact; integrity sha512-oFE2Lj7WVSc87nSi… verified
-> openspec validate publish-openspec-cli-pin-as-contract-member --strict --json
Totals: 1 passed, 0 failed (1 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
exit=0
```

Run twice: on the merged tree before the ratification was encoded, and again
after. Identical both times.

## 2. THE PINNED 1.12 ENTRYPOINT OVER THE WHOLE CORPUS, EXACTLY AS `openspec-cli-pin-gate.yml` RUNS IT

`python3 scripts/validate-openspec-cli-pin.py --all --no-cache`:

```
Totals: 98 passed, 2 failed (100 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures.
THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
exit=0
```

**NEITHER DISPOSITIONED FINDING IS THIS CHANGE'S**, and no third appears. Both
are `#677`'s standing dispositions — 1.12's scenario-currency check is
MARKER-BLIND and refuses two landed `Merged into` renames that canon's own
worked example defines — accepted by Brett Heap on *"take exit 2"*, 2026-09-05.
**THE ITEM COUNT MOVED AND THIS BRANCH DID NOT MOVE IT**: 99 items at the
fix-round head, **100** here, because `main` landed `#753`'s
`amend-absent-changelog-is-an-answer`. The passed/failed SPLIT is unchanged in
kind: 2 failed, both dispositioned, both somebody else's.

**AND THIS PACKET ADDS NO UNDISPOSITIONED FAILURE BY CONSTRUCTION.** 1.12
refuses a `## MODIFIED` block that omits a scenario the current spec still has.
This delta writes **no `## MODIFIED` block at all** (`design.md` D4) — two ADDED
requirements, seven scenarios and three — so it has no such block to fail on.

## 3. Release membership, before and after the diff

`scripts/hermes_runtime_validation/release.py::release_membership`, run on this
branch and on a control worktree of `origin/main` `f756a91f` placed OUTSIDE this
clone:

```
release_membership(origin/main f756a91f control)   -> 283
release_membership(this branch, with the diff)     -> 283
contracts/openspec-cli-pin.yaml    in membership   -> False  (both readings)
contracts/manifest.yaml            in membership   -> True   (editorial)
contracts/README.md                in membership   -> True   (editorial)
contracts/releases/contract-v3.4.digests.yaml      -> 283 entries
```

**283 → 283**, the pin absent from both, and the declared bundle and the derived
membership agree at this commit. This is R2's own obligation on a registering
author, discharged in the packet that writes it.

## 4. `python3 scripts/validate-manifest-digests.py`

```
OK contracts/manifest.yaml: 188 per-file digest(s) verify
exit=0
```

Unchanged in count: the new row carries no `sha256` (`design.md` D2), so the
digest-bearing set is the same set it was.

## 5. `sequenced_after` and the corpus ledger

```
python3 scripts/validate-sequenced-after.py .
sequenced_after validation passed (40 active changes, 5 declaring the field).   exit=0

python3 scripts/validate-sequenced-after.py . --ledger-diff
DEEPEST DECLARED CHAIN RESOLVED: 2 hop(s), from add-per-change-sweep-ledger
per-change sweep ledger consistent with the corpus (181 rows).                  exit=0
```

**MOVED BECAUSE `main` MOVED, NOT BECAUSE THIS BRANCH DID**: 39 active changes
and 180 ledger rows at the fix-round head, **40 and 181** here, `main` having
landed `#753`.

**RATIFICATION MOVES NO ROW.** A row's derived keys are `state`, `class`,
`declares`, `depth` and `prose`; none of them reads a lifecycle status, so a
`draft` → `ratified` transition is invisible to the ledger by construction. This
change's row stands exactly as `36cd4fb6` seeded it:

```
publish-openspec-cli-pin-as-contract-member: {state: active, class: sole,
                                              declares: [add-openspec-cli-pin],
                                              depth: 1, prose: false,
                                              moved_by: "#757", moved_on: "2026-09-07"}
```

`class: sole` because both requirement titles are new, so no partner row flips
and no MOVEMENT LOG entry is owed. **ROWS MOVED BY THE RATIFICATION COMMIT:
ZERO.**

**AND ONE ENTRY REMAINS UNWRITEABLE, RE-MEASURED RATHER THAN QUOTED.** This
packet also stands behind `bump-openspec-cli-pin-to-1.12`, and that entry cannot
be declared:

```
sequenced_after of publish-openspec-cli-pin-as-contract-member entry
'bump-openspec-cli-pin-to-1.12' has change-id half 'bump-openspec-cli-pin-to-1.12',
which does not match ^[a-z0-9][a-z0-9-]*$
```

Found by writing the declaration and reading the refusal. Recorded as an owed
successor at `tasks.md` § 5.6 with three honest exits, none taken here.

## 6. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).                     exit=0
```

## 7. THE ORIGIN-RETENTION GATE, ON THE ACTIVE DIRECTORY

```
python3 scripts/proposal-support.py . verify publish-openspec-cli-pin-as-contract-member
proposal support verification ok                                                exit=0
```

**THE TWO `--archive-gate` ARMS ARE RUN AGAINST THE RATIFICATION COMMIT ITSELF,
WHICH IS WHY THEIR OUTPUT REACHES THIS FILE ONE COMMIT LATER.** Both take
`--ratified-ref`, and the ref they need is the commit that carries this record —
a commit cannot write the result of a check run against its own hash into its
own tree. They are run the moment that commit exists, and their output is
appended here in a FOLLOW-UP commit touching `review/` files only, which leaves
the RATIFYING commit exactly where it is: the gate resolves it as the FIRST
commit whose `proposal.md` declares `Status: ratified`, and a later records-only
commit never becomes that one.

**THE STATUS FLIP AND THE APPROVAL PAIR MOVE IN ONE COMMIT, AND THEY DO HERE.**
The gate resolves the RATIFYING COMMIT as the first commit declaring
`Status: ratified` and compares the origin declaration there with the one being
archived, so `.openspec.yaml`'s approval pair is added in the same commit as the
flip, and that is the last time the file is edited.

## 8. `python3 scripts/validate-release-tag-gate.py . --base origin/main --head HEAD --repo-name openxFactory`

```
## release-tag-gate
release surface touched by this pull request (1 path(s)):
  - contracts/manifest.yaml
declared bundle: contract-v3.4 at the base f756a91f9 -> contract-v3.4 at the head <ratification commit>
  [info] contract-v2.6 is declared SPENT: it was cut, has no published annotated
  tag, and contract-v3.0 — itself cut, itself published and strictly later —
  superseded it. … RULED BY Brett Heap, 2026-09-02
the release-tag obligation holds over the merge tree: no error, no warning
exit=0
```

**No error and no warning.** The one `[info]` is the repository's PRE-EXISTING
`contract-v2.6` SPENT record, untouched by this packet and reported identically
on `origin/main`. `contract-v3.4` is published — an annotated tag object peeling
to commit `807a4f47` — and this packet does not touch `contract_bundle_version`,
so neither `gate-findings` nor `gate-version-reuse` has a condition to fire on.
Run with the tool's own default base as well, which compares the two most recent
commits rather than the pull request's base and therefore reports *"no release
surface change"*; the run quoted above is the one that matches what CI asks.

## 9. `python3 scripts/doc-health.py --single-repo .` — TWO CONTROLS, NOT ONE

Measured against a control minutes apart on the same clock — a worktree of
`origin/main` `f756a91f` placed **OUTSIDE** this clone, as the `modified-block-currency`
self-gate's resolver requires, and removed afterwards.

| | critical | error | warning | info |
| --- | --- | --- | --- | --- |
| `origin/main` `f756a91f` (worktree control, outside the clone) | 9 | 8 | 58 | 13 |
| this branch, BEFORE the ratification was encoded | 9 | 8 | 58 | 15 |
| this branch, AFTER it was encoded | 9 | 8 | 58 | 15 |

All three report `New regressions vs previous report: 0`.

- **Against the pre-ratification branch:** the two normalized reports are
  **BYTE-IDENTICAL** (`md5sum` equal). The status flip, the three citation
  lines, the approval pair, the README row and BOTH new record files together
  add **not one finding** and move not one number.
- **Against `origin/main`:** the whole difference is **+2 `info` and one changed
  `info`**, and every one of the three is named below. **ZERO new `critical`,
  ZERO new `error`, ZERO new `warning`.**

| the difference | severity | why it is expected |
| --- | --- | --- |
| `release-inventory-drift` on `contracts/manifest.yaml` — *"bytes differ from the digest `contract-v3.4` records (editorial member — expected between cuts)"* | `info` | **THIS IS THE A-DEFER READING, CONFIRMED BY THE FAMILY ITSELF.** The manifest is one of the three EDITORIAL members; `release-surface-integrity` declares its movement between cuts an expected bounded state, and the family grades it `info` rather than `error` for exactly that reason. |
| `release-inventory-drift` on `contracts/README.md` — same words | `info` | the second editorial member this packet edits, same reason. |
| `staged-candidate-aging` — *"draft age distribution days: min=**0** max=61 n=75"* (control: `min=1`) | `info`, class `contested` | a trend datum whose own action string is *"trend data — no action required"*. |

**AND ONE STANDING `error` NAMED SO IT IS NOT MISREAD AS THIS PACKET'S.**
`release-inventory-drift` reports `severity=error` on
`docs/contract-versioning-policy.md` — *"bytes differ from the digest
`contract-v3.4` records"*. That file is a NORMATIVE member (`release.py`
`NORMATIVE_DOCS`), not one of the three editorial members, so its drift grades
`error` rather than `info`. It is **pre-existing and identical on `origin/main`,
byte for byte in both reports**; this packet does not touch that file, and
A-defer neither creates nor discharges it.

### The families that could have spoken about this transition

`doc-health` names `publish-openspec-cli-pin-as-contract-member` **ZERO** times
in the whole report, on either side — no `ratified-provenance` finding, no
`proposal-origin` finding, no `duplicate-packet` finding, no
`modified-block-currency` finding.

```
--family proposal-origin        : Findings: 0 critical, 0 error, 0 warning, 0 info
--family ratified-provenance    : Findings: 5 critical, 0 error, 0 warning, 0 info
--family duplicate-packet       : Findings: 0 critical, 0 error, 0 warning, 0 info
```

The five `ratified-provenance` criticals are the five `origin/main` already
carries — `add-sequenced-after-substrate`, `add-structured-scope-substrate`,
`mirror-floor-regeneration-automation` and the archived
`mirror-floor-addition-grace` pair — and **NOT ONE of them is this packet's**.

**AND ZERO IS PROBED RATHER THAN ASSUMED, BOTH WAYS**, because a count of zero
cannot be told from a family that never read the document.

**`proposal-origin`, made to fire and then cleared.** With `Status: ratified`
set and the approval pair REMOVED from `.openspec.yaml`, `--family
proposal-origin` reported exactly one finding and nothing else:

```
Findings: 0 critical, 1 error, 0 warning, 0 info.
- [error] openspec/changes/publish-openspec-cli-pin-as-contract-member — proposal declares
  `Status: ratified` while its origin asserts no approval — approval MUST appear
  when the status claims it
  class="contested"
```

Restoring `approved_by` + `approved_on` BESIDE the retained
`proposed_by`/`proposed_on` — `kind`, `id` and `reason` unmoved, the
addition-not-rewrite shape `add-drafted-proposal-origin` defined — clears it:

```
Findings: 0 critical, 0 error, 0 warning, 0 info.
```

and the restored file is **byte-identical** (`cmp -s`) to the one this commit
carries.

**`ratified-provenance`, probed the same way**, because the family counts
citation lines. A SECOND citation line added to `proposal.md`'s header window:

```
Findings: 6 critical, 0 error, 0 warning, 0 info.
- [critical] openspec/changes/publish-openspec-cli-pin-as-contract-member/proposal.md —
  carries 2 ratification citation lines, not one
  action="keep exactly one: Ratified by: where an approving OpenSpec change
  exists, Ratified: where none does"   class="auto-fixable"
```

Removed again:

```
Findings: 5 critical, 0 error, 0 warning, 0 info.
```

and the restored file is **byte-identical** to the one this commit carries. So
the packet carries EXACTLY ONE citation line per document — `Ratified:` in
`proposal.md`'s front matter, `Ratified by:` in `design.md` and `tasks.md` —
and the family genuinely reads it.

## 10. Test suites

```
python3 -m pytest tests/doc-health tests/sequenced_after tests/scope_globs tests/proposal-support -q
1923 passed, 7 warnings, 2 subtests passed                                      exit=0
```

**THE HEADLINE NUMBER MOVED AND THE BRANCH DID NOT MOVE IT.** The fix-round head
quoted **1917**; the count here is **1923**, and the `origin/main` `f756a91f`
control worktree — **placed OUTSIDE this clone** — reports **1923 passed, 7
warnings, 2 subtests passed** on the same clock. **The same number, so this
branch adds ZERO tests**, which is what a packet realizing in two editorial
files should do, and a status flip adds none either: the count is identical
before and after the ratification was encoded.

```
python3 -m pytest tests/manifest_digests tests/hermes_runtime_contracts/test_release_inventory.py \
                 tests/doc-health/test_release_tag_gate.py tests/doc-health/test_release_inventory.py -q
131 passed                                                                      exit=0

python3 -m pytest tests/sequenced_after tests/scope_globs -q
262 passed                                                                      exit=0

python3 -m pytest tests/intent-compliance/test_release_boundary.py tests/credential_contracts -q
261 passed                                                                      exit=0

python3 -m pytest tests/sequenced_after -q
177 passed                                                                      exit=0

python3 -m pytest tests/intent-compliance -q
288 passed                                                                      exit=0
```

**AND ONE MEASUREMENT ARTIFACT, RECORDED SO NOBODY RE-DERIVES IT AS A `main`
REGRESSION.** Running the four-suite command in an `origin/main` worktree placed
INSIDE this clone fails one case —
`test_modified_block_currency_self_gate.py::test_the_resolver_fails_on_a_checkout_it_cannot_confirm_and_never_walks_up`
— because the test asserts the resolver REFUSES `ROOT.parent`, and a nested
worktree's parent IS a real openxFactory checkout, so the resolver correctly
resolves it. **Every control in this record was taken from a worktree OUTSIDE
the clone**, which is why the numbers above compare.

## 11. THE PINNED-CHECKOUT RECIPE, REPRODUCED AGAINST A FOREIGN ROOT

The recipe `contracts/README.md` now publishes is not asserted; it was RUN, from
this checkout standing in for a consumer's pinned `openxFactory` tree, against a
scratch repository standing in for the consumer, with **nothing copied into the
consumer's tree**:

```
$ OPENXFACTORY_ROOT=<this checkout>
$ python3 "$OPENXFACTORY_ROOT/scripts/validate-openspec-cli-pin.py" --repo <foreign root> --all --strict
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
-> …/bin/openspec validate --all --strict --json  (in <foreign root>)
Totals: 1 passed, 0 failed (1 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
exit=0
```

**AND THE FIRST ATTEMPT REFUSED, WHICH IS THE MORE USEFUL HALF OF THE
REPRODUCTION.** Before the scratch repository declared a `remote.origin.url`,
the same command returned:

```
REFUSE pin-repo-unidentified: <foreign root> declares no `remote.origin.url`, so this
run cannot say WHICH repository's tree it is validating. The pin declares dispositions,
and a disposition is scoped to one repository — applying them all would suppress
findings in a tree they were never written about, and applying none would refuse this
run for exceptions that are simply out of scope. Neither guess is taken
```

So a consumer wiring the published recipe gets a NAMED refusal rather than a
silent misapplication of another repository's dispositions — the fail-closed
behaviour R1's precondition clause requires of a gate that meets an absence.

## 12. The branch's merge history

**THREE merges from `main` stand on this branch**, and the ratification encode
took no fourth:

| merge | took `origin/main` | note |
| --- | --- | --- |
| `e318e0e7` | `64aad02e` | no conflict |
| `85adc0f3` | `5e4d960c` | no conflict; `main` had landed the Apache-2.0 `LICENSE` (PR #762), which is why the licence-count refusal's `license` side moved |
| `ee657e30` | `f756a91f` | taken BEFORE the ratification was encoded. **No conflict.** The 32 paths `main` moved include `README.md`, where both sides had added a row to the *Active changes* block and git kept BOTH (this packet's row and `amend-absent-changelog-is-an-answer`'s), and `tests/sequenced_after/corpus-ledger.yaml`, where both sides added a row and git kept both. Nothing else `main` moved is a path this packet edits — `contracts/manifest.yaml` and `contracts/README.md` were untouched on the `main` side |

**No ledger row moved and no partner flipped in any of the three.** **AND THE
THIRD IS WHY THIS FILE IS THE ONLY THING A FOLLOW-UP COMMIT TOUCHES**: when
`main` moves after the encode, the branch takes the merge and every number here
is re-derived in a SEPARATE commit touching `review/` files only, so the
RATIFYING commit — the first commit whose `proposal.md` declares
`Status: ratified` — never moves.

## 13. Independent review, at the ratified head

**Codex: ONE round, one P1, TAKEN INTO CANON** — the published instructions named
a verb the entrypoint rejects. Thread replied to and **resolved**.
**Copilot: FOUR inline threads across the rounds by head** — two on the
section-title citation in `contracts/README.md` and `contracts/manifest.yaml`,
and two in bench round 3 finding the archive-verb claim still standing in those
same two carriers — **all taken, all resolved**. **Sourcery** is the private-repo
upsell stub. **ZERO threads are open**, measured through the GraphQL
`reviewThreads` set rather than by reading the timeline.

**Three adversarial review lenses** on the pushed head returned
MERGEABLE_AFTER_FIXES with two MAJORs and eight smaller corrections; all were
taken in `2d195187` and `8eb5dc8f`, and a re-verification pass over `8eb5dc8f`
returned **READY_TO_ENCODE**. The ratified baseline is the folded text.
