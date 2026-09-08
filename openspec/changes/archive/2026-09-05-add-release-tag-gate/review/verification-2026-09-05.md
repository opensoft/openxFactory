# Verification record: add-release-tag-gate, 2026-09-05

Status: record
Kind: report
Captured: 2026-09-05, in the ratification lane `openxfactory-max001`
(session `5e783e4d`), on branch `change/add-release-tag-gate`
(openxFactory PR #668).

**This record is CAPTURED AT MERGE, not at first push, and every number below
was RE-DERIVED PRE-CAPTURE** — on the tree this record sits in, at the
ratification commit, after the branch's ONE merge from `main` (`35a41c34`,
taking `74993389` / PR #667). `record-immutability` forbids editing a
`Status: record` document AFTER capture; capture is the merge of the pull
request that establishes it, and nothing is merged yet. A commit cannot write
its own hash into its own tree, so the ratification commit is named by its
subject and its position on the branch rather than by a hash. § 8 lists the
merge history and what it moved.

**If `main` moves again before this pull request lands**, the branch takes
another merge and every number here is re-derived a second time, with § 8
extended to say so, before capture.

**The branch's base is `74993389`.** `main` has since advanced to `3d7b8f3b`
(#670) WITHOUT conflict — the pull request reads `MERGEABLE` — so no further
merge was taken and the readings below describe the branch tree as it stands.

## 1. `openspec validate add-release-tag-gate --strict`

```
Change 'add-release-tag-gate' is valid
```

## 2. `openspec validate --all --strict`

```
Totals: 91 passed, 0 failed (91 items)
```

91 and not 90: `add-openspec-cli-pin` arrived with #667 in the branch's merge
and brings the `neutral-product-pin` capability's item with it.

## 3. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (33 active changes, 2 declaring the field).
```

## 4. `python3 scripts/validate-sequenced-after.py . --ledger-diff`

```
per-change sweep ledger consistent with the corpus (167 rows).
```

**RATIFICATION MOVES NO ROW, and this run is the evidence.** A row's derived
keys are `state`, `class`, `declares`, `depth` and `prose`; none of them reads a
lifecycle status, so a `draft` → `ratified` transition is invisible to the
ledger by construction. The count stands at the 167 it reached when #667's own
row arrived in the merge — this change's row was seeded at 166 in PR #668 and
has not moved since:

```
add-release-tag-gate: {state: active, class: co-modifier, declares: absent,
                       prose: false, moved_by: "#668", moved_on: "2026-09-04"}
```

`class: co-modifier` because the `## MODIFIED` block writes
`doc-health` § *Release-tag publication*, a key `add-release-tag-publication-check`
and `declare-spent-bundle-state` already write; both were co-modifiers before
this change, so **no partner row flips and no MOVEMENT LOG entry is owed** — the
diff states everything.

## 5. `python3 -m pytest tests/doc-health tests/sequenced_after -q`

```
1738 passed, 7 warnings in 325.63s (0:05:25)
```

Of these, **24 are the gate's own** in `tests/doc-health/test_release_tag_gate.py`
— the short-circuit with its positive control, the path classification, the
clean cut with its recorded obligation, the stale bundle, the in-window
release-surface edit, the misplaced tag, version reuse, pre-publication, the
below-floor bundle, four fail-closed refusals (two driven by fault injection at
the git seam so the refusal table is an EQUALITY rather than a subset), the two
rename cases, the retired pin's own absence, the workflow-command escaping and
its unreachability, the closed refusal set, and the workflow's wiring.

## 6. `python3 scripts/doc-health.py --single-repo .` — SAME-CLOCK CONTROL

**Measured against a control run minutes apart, not against a stale baseline.**
This report AGES BY THE CALENDAR: an earlier before/after in this packet was
taken hours apart and reported three `warning`s as movement this change caused,
when they were staged topics and routing records crossing a 30-day threshold on
their own. The control here is a worktree at the branch's own base
`74993389` — this branch minus this branch's changes — run beside it.

| | critical | error | warning | info |
| --- | --- | --- | --- | --- |
| base `74993389` | 6 | 5 | 30 | 13 |
| branch (this tree) | 6 | **6** | 30 | 13 |

A line-by-line diff of the two reports, with the checkout-name prefix
normalized, differs by **EXACTLY ONE finding**:

```
> - [error] docs/contract-versioning-policy.md — bytes differ from the digest 'contract-v3.4' records
```

That is the `release-inventory-drift` `error` this packet accepts knowingly:
the policy document is a DIGESTED MEMBER of the published `contract-v3.4` bundle
and is not one of the three EDITORIAL members, so naming the gate in its
§ Bundle Realization Order is drift the governing scenario calls a **defect**.
It is cleared by the next cut re-digesting the member; hand-editing a published
bundle's inventory is forbidden. `ratification-2026-09-05.md` § 7 carries the
reasoning and the precedents.

**THE BASE'S OWN ERROR COUNT MOVED, AND NOT BY THIS PACKET.** An earlier
control against `9420472e` read 4 errors; `74993389` reads 5. The added one is
`add-openspec-cli-pin/review/ratification-2026-09-04.md — missing status
header`, which arrived with #667. It is present in BOTH columns above and is
therefore not this change's, but it is named here so the shift in the base
figure is not read as drift in this measurement.

**THE TWO RECORD FILES THIS COMMIT ADDS RAISE NO FINDING.** Both carry
`Status: record` and `Kind: report`, and the branch column above was re-derived
with BOTH present. `ratified-provenance` does not fire: `proposal.md`,
`design.md` and `tasks.md` each carry `Status: ratified` against **exactly one**
citation line — the front-matter `Ratified:` for the proposal, the
`Ratified by:` header for the other two — which is the one-total rule that
family enforces across front-matter and body together.

## 7. `actionlint .github/workflows/release-tag-gate.yml`

```
(no output, exit 0)
```

## 8. The branch's merge history, and the gate's own run

**ONE merge from `main`**, and it exists because of a failure worth recording:
`35a41c34` took `74993389` (#667, `add-openspec-cli-pin`). Before it, main's
landing had left this pull request `CONFLICTING` — both changes insert a row at
the same point in README's *Active changes:* block — and **a conflicting pull
request has no merge ref, so GitHub cannot compute the tree `on: pull_request`
workflows run against and silently does not fire them.** After the fix-round
push only `merge-master-approval` and the Copilot review ran; closing and
reopening the pull request did not help. **An absent check reads a great deal
like a passing one**, which is the reason this is in the record rather than in
a session note. The merge resolved by keeping BOTH README rows.

**The gate's own first proof** — this pull request touches no release-surface
path, so `release-tag-gate` must short-circuit green while changing the
machinery that decides it:

| head | run | job | result |
| --- | --- | --- | --- |
| `57a009c9` | **`33933031517`** | `101215392876` | **pass, 8s** |

Its log: `no release surface change: none of the … changed path(s) … is
contracts/manifest.yaml or under contracts/releases/`, and
`Complete job name: release-tag-gate` — the check surfaces under the literal
token a ruleset pins.

**All NINE checks were green on `57a009c9`** — `pytest-suite` (23m32s,
`selected=9638 passed=9617 skipped=21 failures=0 errors=0`, the skip pin holding
exactly), `release-tag-gate`, `openspec-cli-pin`, `clearing-dispatch-gate`,
`lane-line`, `merge-master-approval`, `openreposhape-pin`,
`signed-execution-chain-gate`, `wallet-validation`. The ratification commit
carrying this record re-runs them; its result is on the pull request.

## 9. Replay against real history, with its honest limit

`python3 scripts/validate-release-tag-gate.py . --head 807a4f47` — the
`contract-v3.4` cut, PR #653 — exits **0**, reporting the bundle PRE-PUBLISHED
because its tag now peels to that very commit. **That is a different arm from
the one a live cut takes** (distance-zero silence plus the `TAG OWED` record),
and naming it is the difference between evidence and a coincidence.

`--head 16b85614` (PR #636) also exits 0 **today**, and that is a limit of
replay rather than a result: the family reads LIVE published refs and
`contract-v3.3`'s tag exists now. When that pull request was open it did not,
and the gate would have refused it. That condition is asserted on synthetic
trees instead, where the refs are under the test's control.
