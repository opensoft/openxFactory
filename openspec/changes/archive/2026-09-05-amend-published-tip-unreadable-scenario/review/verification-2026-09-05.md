# Verification record: amend-published-tip-unreadable-scenario, 2026-09-05

Status: record
Kind: report
Captured: 2026-09-05, in lane `openxfactory-1` (session `5e783e4d`), on branch
`change/amend-published-tip-unreadable-scenario` (openxFactory PR #678).

**This record is CAPTURED AT MERGE, not at first push, and every number below
was RE-DERIVED PRE-CAPTURE** — on the tree this record sits in, after the
branch's ONE merge from `main` (`61d6c8e4`, taking `92005d70` / PR #677).
`record-immutability` forbids editing a `Status: record` document AFTER capture;
capture is the merge of the pull request that establishes it, and nothing is
merged yet. A commit cannot write its own hash into its own tree, so the
ratification commit is named by its subject and its position on the branch
rather than by a hash.

**If `main` moves again before this pull request lands**, the branch takes
another merge and every number here is re-derived a second time, with § 8
extended to say so, before capture.

## 1. `openspec validate amend-published-tip-unreadable-scenario --strict`

```
Change 'amend-published-tip-unreadable-scenario' is valid
```

## 2. `openspec validate --all --strict`

```
Totals: 94 passed, 0 failed (94 items)
```

**94 and not the 92 this branch read before its merge**: `#677` brought its own
change directory and the `neutral-product-pin` item that goes with it. Neither
is this packet's, and the count is recorded at the tree this record sits in
rather than at the one it was authored on.

## 3. THE SAME VALIDATION THROUGH THE PINNED CLI, WHICH IS WHAT CI NOW RUNS

`#677` landed in this branch's merge and made the fleet's OpenSpec CLI a
CONTENT-ADDRESSED pin at **1.12.0**, with
`scripts/validate-openspec-cli-pin.py` as the one entrypoint through which
strict validation runs. `python3 scripts/validate-openspec-cli-pin.py --all
--no-cache`, exactly as `openspec-cli-pin-gate.yml` invokes it:

```
Totals: 92 passed, 2 failed (94 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied)
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content
address; every target validated --strict with 0 UNDISPOSITIONED failures.
```

**NEITHER FINDING IS THIS CHANGE'S.** Both are the pre-existing dispositions
`#677` carries — 1.12's scenario-currency check is MARKER-BLIND, so it refuses
two landed `Merged into` renames that canon's own worked example defines, and
Brett accepted them on *"take exit 2"*. This packet adds no third.

**AND THAT IS THE PREDICTION THIS RUN CONFIRMS.** 1.12 refuses a `## MODIFIED`
block that omits a SCENARIO the current spec still has. This block **omits no
scenario**: it carries all 30 promoted titles and replaces a `WHEN` BULLET
inside one of them. A bullet replacement is invisible to that check and is
declared to the in-house `modified-block-currency` family by the reserved
`Removed from canon by` marker instead (§ 6). Had the amendment retitled the
scenario rather than reworded its bullet, this run would have produced a THIRD
refusal and the packet would have owed a disposition — which is a governed edit
and not this lane's to write.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (33 active changes, 1 declaring the field).
```

## 5. `python3 scripts/validate-sequenced-after.py . --ledger-diff`

```
per-change sweep ledger consistent with the corpus (172 rows).
```

**RATIFICATION MOVES NO ROW, and this run is the evidence.** A row's derived
keys are `state`, `class`, `declares`, `depth` and `prose`; none of them reads a
lifecycle status, so a `draft` → `ratified` transition is invisible to the
ledger by construction. The count is 172 because the merge brought #677's row,
not because anything of this packet's moved: `main` carries 171 rows and this
branch 172, and the single difference is this change's own row, unmoved since
#678 seeded it —

```
amend-published-tip-unreadable-scenario: {state: active, class: co-modifier,
                                          declares: absent, prose: false,
                                          moved_by: "#678", moved_on: "2026-09-05"}
```

`class: co-modifier` because the `## MODIFIED` block writes `doc-health` §
*Release-tag publication*, a key `add-release-tag-publication-check`,
`declare-spent-bundle-state` and `add-release-tag-gate` already write; all three
are ARCHIVED and were co-modifiers before this change, so **no partner flips and
no MOVEMENT LOG entry is owed**.

## 6. `python3 -m pytest tests/doc-health tests/sequenced_after -q`

```
1738 passed, 7 warnings
```

**UNCHANGED, WHICH IS THE POINT.** `code_surface: none`: no test asserts the old
scenario prose — checked before authoring, the only occurrence of "commonest
cause" outside canon is a code COMMENT — and the suite already pins the two skip
texts apart from each other as fresh literals (`_UNFETCHED_WORDS` +
`_FETCH_TRIED_WORDS` against `_PRESENT_WORDS` + `_ANSWERED_WORDS`, over a
`_StoreGit` fake that can express "the commit is not here").

## 7. `python3 scripts/doc-health.py --single-repo .` — SAME-CLOCK CONTROL

Measured against a control run minutes apart, not against a stale baseline: this
report ages by the calendar. **The control is a worktree at `92005d70` — the
`main` this branch has merged — and NOT at the branch's original base
`ceb6dc9e`.** Taking it at the base would have compared this branch against a
tree two landings behind it and charged this packet with other people's
findings, which is exactly what a pre-merge reading of it did: at `ceb6dc9e`
both columns read `6 critical`, and at `92005d70` both read `8`.

| | critical | error | warning | info |
| --- | --- | --- | --- | --- |
| `main` `92005d70` | 8 | 6 | 30 | 13 |
| branch | 8 | 6 | 30 | 13 |

A line-by-line diff of the two reports, with the checkout-name prefix
normalized, is **EMPTY** — as a prose change over an active delta should be.

**THE TWO ADDED `critical`s ARE MAIN'S AND ARE NAMED HERE RATHER THAN ABSORBED.**
They are `mirror-floor-addition-grace/proposal.md` and that packet's
`review/ratification-2026-09-05.md`, both *"ratified header carries no citation
in either sanctioned spelling"* — a change that landed on `main` as PR **#676**
from another lane. They appear in BOTH columns above, this branch touches
neither file (`git diff --name-only origin/main..HEAD` lists only this packet's
own files, `README.md` and the ledger), and **this lane does not fix another
lane's packet in a ratification commit**. Recorded so the count movement is not
read as drift in this measurement.

**THE `modified-block-currency` PROBE, BOTH WAYS.** The family naming this
change zero times cannot be distinguished from a block it never read, so it was
probed and fired both times:

- **marker removed** → *"does not carry **1** of the 214 body units and scenario
  bullets"* — exactly ONE unit is dropped, and the marker is what declares it;
- **a promoted scenario title mutated** → *"omits 1 of the **30** scenarios …
  'The published tag is lightweight rather than annotated'"*;
- **restored** → silent again.

## 8. The branch's merge history

**ONE merge from `main`**: `61d6c8e4` took `92005d70` (#677,
`bump-openspec-cli-pin-to-1.12`), which had left this pull request's README row
colliding with its own at the same insertion point. Resolved by keeping BOTH,
this branch's first. That merge is also what makes § 3's reading possible: the
pinned-CLI entrypoint did not exist on this branch's base.

## 9. Independent review

**Codex REFUSED** on usage limits — no Codex round ran. **Sourcery** is the
private-repo upsell stub. **Copilot ran twice**: round 1 caught `tasks.md` 3.6
ticked while the ledger carried no row for this change (fixed, `3fdcd95b`) and
the lane casing against corpus precedent (fixed, `cd71ff12`); **round 2 on the
fixed head: 🟢 Approval recommended, 0 new comments.** The full disposition is
`ratification-2026-09-05.md` § 5.
