# Archive Record: split-opendox-two-layer-product

Status: record
Kind: record
Archived: 2026-09-22 by openxFactory PR #1139, lane `openxfactory-4`
(display `openXfactory-4-openDox_extraction`).
Archive word: Brett Heap, in session 2026-09-22, verbatim *"land the archive when
green and keep going"*, recorded at `opensoft/openxFactory` issue #656 comment
`5769909970`. Ratified 2026-09-05, verbatim *"ratify #666"* (#656 comment
`5548470629`; record `ratification-2026-09-05.md`).

## Why a merge commit and not a squash

`scripts/validate-sequenced-after.py`'s archive-date-vs-commit arm holds that
every archived directory is named for **the UTC date of the commit that added
it**. A squash re-dates that adding commit, which reds the arm for this
directory — the failure shape already recorded at `#1076` / `#1056` and repaired
there by disposition rows. A merge commit keeps the wrapper's own act commit, so
the directory's date and its adding commit's date are the same fact. **This
pull request lands as a MERGE COMMIT on the archive day, never squashed.**

## What the archive did

The wrapper (`scripts/proposal-support.py … archive --yes`, exit 0) ran with the
pinned CLI `@fission-ai/openspec@1.12.0`, verified against its content address
over the pinned 80-package closure (`npm ci --ignore-scripts`); origin retention
passed — the declaration is unchanged since the ratifying commit `ceb6dc9ebbdc`;
`openspec validate split-opendox-two-layer-product --strict` reported
`1 passed, 0 failed` through that same binary before anything moved; and there
were no supporting docs to package, which is the majority shape for a staged
origin rather than an omission.

Spec deltas applied as ratified: **`+ 7, ~ 4, - 102, → 0`**.

| capability | act | effect |
|---|---|---|
| `corpus-adapter-seam` | **created** | 4 requirements, 11 scenarios |
| `domain-mapping-declaration` | **created** | 3 requirements, 9 scenarios |
| `domain-descendant-boundary` | modified | 2 requirements replaced |
| `neutral-product-pin` | modified | 2 requirements replaced |
| `ideation-dashboard` | **modified** | **102 of 104 requirements REMOVED** |

Capability directories **64 → 66**. The packet's own `tasks.md` § 8.4 says
63 → 65, measured at `main` `80c68da6`; the baseline moved by one when `#1133`
promoted `packet-citation-report`. The arithmetic is unchanged — two ADDs and
nothing removed — and the figure is restated here rather than left to contradict
the ledger.

## `ideation-dashboard` is REDUCED, not removed — stated because it is easy to misread

| | before | after |
|---|---|---|
| bytes | 307,705 | 15,457 |
| requirements | 104 | **2** |
| scenarios | 487 | 12 |
| directory | present | **PRESENT** |

This is the largest `## REMOVED` block ever applied at an archive in this
repository — 102 requirements, 215,683 B of delta — and the capability
**survives**, because two requirements are not in the block:

- `The doxBench chat-turn v1 envelope family is REMOVED at contract-v3.0`
- `An unrecognized chat-turn kind is refused in the SURVIVING family, never coerced into a removed one`

Both belong to `retire-doxbench-chat-turn-v1`, the one of the five § 6 changes
closed by PROMOTION rather than as re-homed, so its content is openxFactory's own
and stays. The CLI's own plan says `ideation-dashboard: update` and it is right;
anybody describing this archive as removing a capability is describing something
that did not happen.

**The two survive AS RATIFIED, and that is a recorded default rather than an
unexamined one.** The question — archive the delta as ratified, leaving the
capability with two requirements, versus amend the delta to remove all 104 — was
put to Brett and no word was given on it. Two measured facts make the default the
safe reading: the amend branch is not runnable (the pinned CLI refuses
`Spec must have at least one requirement` and will not delete a spec holding 65
lines of non-requirement content, the 2026-09-16 ERRATUM among them), and the
erratum belongs with the § 6.2 requirements it is attached to, which the ratified
shape keeps together and the amend shape strands.

## What this pull request carries beyond the wrapper's own output

1. **A real `## Purpose` in each newly created capability spec.** The CLI writes
   `TBD - created by archiving change split-opendox-two-layer-product. Update
   Purpose after archive.`, and `openspec validate --all --strict` reds on it:
   measured 106 passed / 1 failed before, 105 / **3** with the placeholders left,
   and **107 / 1** once the Purposes are written — the one remaining failure
   being the pre-existing `change/add-chain-attestation`. The checker's own
   instruction is to edit the promoted spec directly, which is what this does; no
   ratified packet text moves.
2. **The corpus-ledger row**, machine-derived by
   `validate-sequenced-after.py --seed-ledger --moved-by '#1139'` — ONE row of
   222 moves, `state: active → archived` plus provenance, with `class`,
   `declares` and `prose` unchanged.
3. **The README OpenSpec Records move**, six path references repointed
   string-keyed (one of them 1,700 lines outside the records block), plus three
   sentences this archive falsifies, corrected in place.
4. **A re-aim of `tests/doc-health/test_modified_block_currency_self_gate.py`.**
   Canon's `Composed views are read-only with a repository jump` block was the
   CONTROL that test read, and the `## REMOVED` block took it. The module's own
   failure message calls corpus movement the EXPECTED cause and asks for the
   named subjects to be re-aimed in the same commit. The invariant is
   STRENGTHENED by the re-aim: a block-scoped guard could only see arrival into
   that one block; the question is now asked of ALL of canon.
5. **Four register retirements**, each on its own entry's `retires_when: … or
   the packet archives`: `scripts/target-release-register.yaml`'s
   `implementation_pending` entry and its `CLOSED_REGISTER` pair in
   `scripts/target_release.py` (20 pairs to 19), and
   `scripts/code-surface-register.yaml`'s `list-runs-into-prose` entry with its
   pair in `scripts/code_surface.py` (eight to seven). The packet's own README
   entry named the first of these in advance as *"THE LOCKSTEP PAIR THE ARCHIVE
   RETIRES"*.

## § 8.9's measurement record, in the form the box fixes

**BASELINE, fixed before the AFTER run and published first** (brett-wip
`003fc795`, before any AFTER run was taken): this pull request's OWN BASE,
`main` **`cd246a012645d1d97047cc40427f66f43440401f`**. **AFTER**: this pull
request's own head. Both trees are of the SAME KIND — a plain
`git clone --filter=blob:none` with `openDox` and `openXdox` materialized — and
doc-health is run FROM the tree it measures, never merely pointed at it.

**THE SCOPE IS NAMED FIRST**, because the two scopes do not compare: a
`--single-repo` self-gate run sees NONE of the aggregation-root dispositions
(`promotion_fidelity.py`), so a BEFORE in one scope and an AFTER in the other
would manufacture a delta out of the flag alone.

### Single-repo (`python3 scripts/doc-health.py --single-repo . --as-of 2026-09-22`)

| family | critical | error | warning | info |
|---|---|---|---|---|
| document-catalog | 0→0 | 0→0 | 0→0 | 1→1 |
| ideation-routing | 0→0 | 0→0 | 2→2 | 2→2 |
| modified-block-currency | 0→0 | 0→0 | 0→0 | 12→12 |
| **promotion-fidelity** | 0→0 | **20→17** | 0→0 | 0→0 |
| ratified-provenance | 27→27 | 0→0 | 0→0 | 0→0 |
| record-immutability | 4→4 | 0→0 | 0→0 | 0→0 |
| release-inventory-drift | 0→0 | 3→3 | 0→0 | 3→3 |
| release-tag-publication | 0→0 | 0→0 | 0→0 | 1→1 |
| staged-candidate-aging | 0→0 | 0→0 | 34→34 | 1→1 |
| staged-topic-template | 0→0 | 0→0 | 1→1 | 0→0 |
| tag-hygiene | 0→0 | 5→5 | 0→0 | 0→0 |
| **TOTAL** | **31→31** | **28→25** | **37→37** | **20→20** |

Canon share 42.1% (414,832 / 985,117) → 39.5% (371,871 / 942,156). New
regressions vs previous report: 0 at both ends. Five families skipped at both
ends and each named: `client-identity-composition`, `contract-copy-drift`,
`notebook-projection-drift`, `register-lifecycle-consistency`,
`submodule-pin-drift`.

**ENTERED 0. CHANGED SEVERITY 0. LEFT 3, each named:**

- `archive/2026-09-16-add-composed-view-authoring/specs/ideation-dashboard/spec.md` —
  *'Composed views are read-only with a repository jump' reached
  `openspec/specs/ideation-dashboard/spec.md` without 5 of its 6 ratified
  scenarios*
- `archive/2026-09-16-add-doxchat-model-intake/specs/ideation-dashboard/spec.md` —
  *'doxBench model catalog and provider boundary' … without 1 of its 12*
- `archive/2026-09-16-add-nightly-dashboard-refresh/specs/ideation-dashboard/spec.md` —
  *'Runtime snapshot fetch with baked fallback and displayed freshness' … without
  2 of its 6*

**The reason is one reason, and it is this archive's own `## REMOVED` block.**
Each of the three is a SCENARIO-COMPLETENESS finding about a title that reached
canon incompletely. The archive removes those titles from canon, so there is no
longer an incomplete promotion to report. Nothing was suppressed and no
disposition was added: the findings have no subject left.

The canon-share fall is the same event seen from the other side: the removed
requirements were canon words, and canon and governance words fall by the
identical 42,961.

### Aggregation (`--repo-root`, with `health/` from `opensoft/xFactory` `cfe27de3`)

| | critical | error | warning | info |
|---|---|---|---|---|
| BEFORE | 16 | **949** | 3300 | 33 |
| AFTER | 16 | **951** | 3300 | 33 |

Only `document-catalog` moves, 941 → 943 errors. **ENTERED 2, LEFT 0, CHANGED
SEVERITY 0:**

```
+ [error] document-catalog openspec/specs/corpus-adapter-seam/spec.md
          [coverage] document has no catalog entry
+ [error] document-catalog openspec/specs/domain-mapping-declaration/spec.md
          [coverage] document has no catalog entry
```

Both are the two capabilities this archive promoted, both are
`class="auto-fixable"`, and the remedy is **NOT in this repository**: the catalog
baseline lives at the aggregation root (`health/document-catalog/baseline/`), so
the mechanical catalog pass for these two documents belongs to the xFactory sync
that follows this landing, not to this pull request. Recorded here so the two
errors are not read as unexplained.

`promotion-fidelity` contributes ZERO findings in aggregation mode at BOTH ends —
the aggregation's dispositions suppress the family entirely — which is precisely
why the single-repo scope above is where its 20 → 17 movement is visible, and why
the two scopes are reported separately rather than netted.

## The disposition rows this archive makes inert

Of the four rows in the aggregation's `health/dispositions.yaml` naming a
`specs/ideation-dashboard/spec.md` delta, exactly **one** goes to zero matches
here: `add-composed-view-authoring`. Its finding is the first of the three that
LEFT above. The other three keep at least one matching finding.

**No gate reds on it.** `promotion_fidelity.load_dispositions()` builds a
suppression set consumed only by `disposed()`; there is no reverse pass and no
stale-entry arm exists for this record. The row simply goes inert. Its removal
belongs to the aggregation-root sync PR, after this landing — until the archive
is on `main`, the finding is live and removing the row would un-suppress a real
error. A second row, `retire-doxbench-chat-turn-v1` (#473), never matched at all:
it was written on the premise that the promoted spec disappears wholesale, and
its two disposed titles are exactly the two requirements that SURVIVE.

Registered and not taken: giving `health/dispositions.yaml` the stale-entry arm
that `validate-openspec-cli-pin.py` already has, so a spent row is reported
rather than inert.

## What this archive does NOT close

§§ 5.6 and 8.4 archive in the house's reserved `[~]` DEFERRED form on RULED
**R-B** (#656 comment `5728607038`), which inverted their written order because
both of R-B's remaining clauses take this archive's own merge sha as their input,
so neither can be performed before this landing. § 7.3 and § 7.4 keep their own
`[~]`. The ledger closes at **68 `[x]` / 0 `[ ]` / 4 `[~]` of 72**.
