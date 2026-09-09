# Proposal Amendment: split-opendox-two-layer-product — FLOOR PART 2 restated as a mapping

Status: record
Kind: decision record
Decision date: 2026-09-09
Lane: openxfactory-4-opendox-extraction (formerly openxfactory-opendox)
Ruler: Brett Heap (repository owner), by click-through selection in session
`openXfactory-4`, over the § 3.2–§ 3.8 plan memo's OQ-H … OQ-Q, each option
presented with the memo's recommendation first.
Ruled: 2026-09-09T22:19:57Z, verbatim: *"**OQ-K → FLOOR PART 2 restated as a
source→destination mapping with declared multiplicity** for replicated files (a
small amendment PR to the change)."*
Ruling URL:
<https://github.com/opensoft/openxFactory/issues/656#issuecomment-5609526215>
Amends: `split-opendox-two-layer-product`, RATIFIED 2026-09-05 (record
`review/ratification-2026-09-05.md`), previously amended 2026-09-05 (repository
shape, record `review/amendment-2026-09-05-repository-shape.md`).

**THIS IS AN AMENDMENT, NOT A RE-RATIFICATION.** The packet stays ratified.
RULING OQ-1's four-part floor is not reopened: it still has four parts, part 2 is
still about tests and still refuses a silent drop, and neither of the two
single-instrument alternatives Brett rejected on the record comes back. What
moves is part 2's TEST — from a scalar equality to the mapping the ruling names.
Every edit is VISIBLE in the tree as an inline `> Amended 2026-09-09.` note in
the lifecycle's own form (`docs/document-lifecycle.md`), because a ratified
record whose text silently changed is a record nobody can cite.

## The form this amendment takes, and why

The ruling names it: *"a small amendment PR to the change"*. It is an IN-PLACE
amendment of `split-opendox-two-layer-product`, not a sibling `amend-*` change,
and not a `## MODIFIED Requirements` delta. Both alternatives were checked and
neither is available:

- **A `## MODIFIED Requirements` delta inside this change** would have to modify
  a requirement that does not exist. FLOOR PART 2 is not a promoted requirement
  and is not in any spec delta — `design.md` § D6 says so under its own heading
  *"WHY NO PROMOTED REQUIREMENT IS AUTHORED FOR THE FLOOR, stated so the omission
  is a decision and not a gap"*, and gives the reason: `release-realization`'s
  archive gate is held by two active changes, so a third writer would be an
  avoidable collision. Authoring an ADDED requirement now to have something to
  modify would create exactly that collision, to restate a floor that binds this
  change alone.
- **A sibling `amend-*` change.** Every archived precedent —
  `2026-09-03-amend-owner-layer-severity`, `2026-09-05-amend-chain-anchoring-readiness-and-durability`,
  `2026-09-05-amend-published-tip-unreadable-scenario`,
  `2026-09-05-amend-unreadable-read-sibling-scenarios`,
  `2026-09-06-amend-marker-reason-boundary`,
  `2026-09-07-amend-absent-changelog-is-an-answer`,
  `2026-09-09-amend-marker-defect-reporting` — amends a PROMOTED capability under
  `openspec/specs/` through a `## MODIFIED Requirements` delta on that capability,
  and each carries its own ratification record. There is no promoted requirement
  here to amend, so such a packet would have an empty `specs/` and would not pass
  `openspec validate --strict`. The precedent for correcting an ACTIVE, ratified,
  unarchived packet mid-flight on a #656 ruling is this packet's OWN
  2026-09-05 repository-shape amendment: inline notes at the carrier sites plus a
  `review/amendment-<date>-<topic>.md` record. That is the shape used here.

## What was false

`tasks.md` § 5.4, as ratified:

> **FLOOR PART 2 (RULED OQ-1) — test counts that must SUM across the three
> repositories.** 3,927 `def test_` leave — 52% of this repository's 7,612.
> openDox + openXdox + the `openxFactory` remainder (which now includes the
> adapter's own tests, per RULING DQ-1) SHALL equal the pre-split count, pinned
> by test the way `pytest-suite.yml` already pins the collection triple.

`design.md` § D6 (2) states the same test as *"SHALL SUM to the pre-split
count"*, and `proposal.md`'s RULED OQ-1 item 2 as *"Test counts that must SUM
across the three repositories"*.

It is false twice over, and the first way is by design:

1. **REPLICAS.** The manifest that landed as FLOOR PART 1 (`docs/opendox-carve-manifest.yaml`,
   PR #865, 454 rows) carries **18** rows dispositioned
   `not_moved / replicated_at_destination` — a replica at each destination and the
   original retained at `openxFactory`, *"never a shared module across a
   repository boundary with no pin"* (manifest header). Three of them are test
   modules and they carry **30 `def test_`** between them. § 3.7 (FLOOR PART 3)
   requires **EVERY destination** to pass the neutral conformance corpus — openDox,
   openXdox's adapter implementation, and `openxFactory`'s own adapter — so each of
   those three files has **three** post-split homes, not one. The post-split sum
   therefore EXCEEDS the pre-split count by exactly 60, on the first run, forever.
   An equality test that fails by construction gets "fixed" by deleting replicas,
   which would break FLOOR PART 3 to satisfy FLOOR PART 2. That is the wrong
   repair, and it is the reason the ruling restates the test rather than the
   numbers.
2. **THE SCALARS ARE STALE, AND SCALARS ALWAYS WILL BE.** `3,927 def test_ across
   125 files` and `7,612` were measured at `origin/main` `a858e5b0` on 2026-09-04.
   Measured at the named carve commit `b075fd91` (2026-09-09):
   `tests/ideation-dashboard/` is **4,169** `def test_` across **140** `.py`
   files and the repository holds **8,731**. Nothing was lost and nothing is
   wrong — the tree grew, as it will keep doing until the carve. A floor written
   as a scalar equality against a number in a ratified document is re-falsified
   by every merge; a floor written as a mapping over the manifest is re-evaluated
   from the manifest and stays true.

## What replaces it

FLOOR PART 2 becomes a source→destination MAPPING with DECLARED MULTIPLICITY.
The full restated text is what now stands at `design.md` § D6 (2) and
`tasks.md` § 5.4; its four clauses are:

- **(a) TOTAL COVERAGE — no test is lost.** Every file in the manifest's declared
  surface that carries at least one `def test_` has at least ONE post-split home,
  named by its own row. A file with tests and no home is a LOST TEST and the
  carve REFUSES. This is the intent of the ratified rule, unchanged and now
  stated directly rather than inferred from an arithmetic identity.
- **(b) DECLARED MULTIPLICITY.** A row dispositioned
  `not_moved / replicated_at_destination` DECLARES the set of repositories its
  replica lands in, including the retained `openxFactory` copy; its multiplicity
  `m` is the size of that set. Multiplicity is DECLARED IN THE ROW, never
  inferred at arrival — an undeclared replica set makes the check uncomputable,
  which is a refusal and not a pass.
- **(c) THE SUM CHECK, OVER DECLARED MULTIPLICITIES.**
  `Σ(destinations) = source_count + Σ(replicated rows) (m − 1) × row_test_count`.
  Every term is read from the manifest at the carve commit; nothing is estimated
  and no number is transcribed into prose where it can go stale.
- **(d) PINNED BY TEST**, at each destination and in `openxFactory`, the way
  `pytest-suite.yml` already pins this repository's collection triple. Unchanged.

## The arithmetic, with the landed manifest's real numbers

Measured 2026-09-09 in a detached worktree at `origin/main` `17167481` (the
commit that landed PR #865), counting `def test_` — the packet's own idiom — over
each row's blob at `carve_commit b075fd91dc8fced8e1373825ba80220c33536bae`:

| manifest rows | `.py` rows with tests | `def test_` |
| --- | ---: | ---: |
| `→ opendox_code` | 40 | 1,098 |
| `→ openxdox_code` | 71 | 2,315 |
| `not_moved / stays_openxfactory_adapter` | 28 | 813 |
| `not_moved / stays_openxfactory_governance` | 4 | 155 |
| `not_moved / replicated_at_destination` | 3 | 30 |
| **source total (the declared surface)** | **146** | **4,411** |

The three replicated test modules and their multiplicity, fixed by § 3.7's own
"every destination" and here DECLARED rather than inferred:

| replicated row | `def test_` | homes | `m` |
| --- | ---: | --- | ---: |
| `tests/corpus-adapter/test_conformance.py` | 20 | openxFactory (retained) · openDox-code · openXdox-code | 3 |
| `tests/corpus-adapter/test_interface_closure.py` | 6 | openxFactory (retained) · openDox-code · openXdox-code | 3 |
| `tests/corpus-adapter/test_no_home_vocabulary.py` | 4 | openxFactory (retained) · openDox-code · openXdox-code | 3 |

Post-split homes:

| destination | carved | replica | total |
| --- | ---: | ---: | ---: |
| openDox-code | 1,098 | 30 | **1,128** |
| openXdox-code | 2,315 | 30 | **2,345** |
| `openxFactory` remainder (adapter + governance + retained replicas) | 968 | 30 | **998** |
| **Σ destinations** | | | **4,471** |

The check:

```
Σ(destinations)  = source_count + Σ (m − 1) × row_test_count
       4,471     =    4,411     +      (3 − 1) × 30
       4,471     =    4,411     +           60          ✔
```

The ratified equality reads `4,471 = 4,411` and fails by exactly 60 — which is
`Σ(m − 1) × row_test_count`, the term it does not have. The restated check
passes on the same tree with nothing deleted.

Two currency notes, so a later reader is not surprised:

- The ruling and the plan memo say **17** replicated rows and *"~60"*. The
  manifest that LANDED carries **18**: the eighteenth is
  `scripts/corpus_adapter.py`, added by the #865 fix round as OQ-Q's repair
  (author's disposition `replicated_at_destination`; the re-verifier recommends
  accept; still being clarified with Brett at the time of this record). It carries
  **zero** `def test_`, so the arithmetic above is identical under either
  disposition, and this amendment does not decide OQ-Q.
- The memo's split of the 4,411 (*"3,426 leave — openXdox 2,315 / openDox 1,111,
  985 stay"*) was measured against #865 BEFORE its fix round. Against the LANDED
  manifest the total is the same 4,411 and the split is 3,413 leaving (openXdox
  2,315 / openDox 1,098) with 998 staying. This record's table is the landed one
  and is what the check should be re-run against.

## What this amendment does NOT move

- **RULING OQ-1 is not reopened.** Four parts, not three and not five. Parts 1, 3
  and 4 are untouched, as are the two rejected single-instrument alternatives and
  the sentence that neither substitutes for another.
- **No promoted requirement is authored, modified or removed.** `openspec/specs/`
  is not touched by this pull request, and no spec delta in this change gains,
  loses or re-titles a requirement or a scenario.
- **The Migration blocks in `specs/ideation-dashboard/spec.md`.** 87 of that
  file's 102 `**Migration**:` blocks summarise the floor as *"test counts that
  must SUM across the three repositories"* (the other 15 are RULING DQ-1's
  stay-home requirements and never mention the floor). That phrase names no
  quantity to be equal to — counts DO sum, and under the restatement they sum to
  `source_count + Σ(m − 1) × row_test_count` — so it is not falsified by OQ-K and
  is left byte-identical deliberately, rather than swept across 87 sites for a
  sentence that is still true. The 2026-09-05 repository-shape amendment set the
  same precedent in its own words: *"No spec delta file is touched by this
  amendment."*
- **The manifest is not edited here.** Clause (b) puts one obligation on FLOOR
  PART 1 — the replicated rows owe a declared destination set — and § 5.4a carries
  it as the input part 2 reads, with § 5.4's own enumeration standing as the
  declaration until that manifest edit lands. `docs/opendox-carve-manifest.yaml` is outside this
  change's own files and moves in its own pull request.
- **The `3,927` / `7,612` figures** are kept where they describe THE SHED as
  measured on 2026-09-04 (`proposal.md` `code_surface:`, `design.md` § D2). They
  are removed only from the FLOOR's own TEST, which is the one place a stale
  scalar was load-bearing.

## What changed, file by file

| file | before | after |
| --- | --- | --- |
| `proposal.md` header | `Ratified:` + one `Amended:` line | a SECOND `Amended:` line naming RULING OQ-K, the verbatim word, the comment id and this record. `Status:`, `Ratified:` and the 2026-09-05 line are UNTOUCHED |
| `proposal.md` § *The eleven acts* item 12 | *"test counts that must SUM across the three repositories"* inside the four-part list | the same list with part 2 named as the MAPPING, carrying an inline amendment clause that quotes what it first said and points at § RULED OQ-1 item 2 and `design.md` § D6 (2). The other three parts and both rejected alternatives are byte-identical |
| `proposal.md` § RULED OQ-1 item 2 | *"Test counts that must SUM across the three repositories — 3,927 `def test_` leave, 52% of this repository's 7,612"* | the mapping, the declared-multiplicity rule, the sum check, the measured arithmetic against the landed manifest, and an `AMENDED 2026-09-09` note carrying the original sentence verbatim |
| `design.md` header | one `Amended:` line | a SECOND naming OQ-K, with the sentence that RULING OQ-1 is not reopened and the floor still has four parts |
| `design.md` R-index, row `OQ-1` | *"test counts that SUM"* | the same clause plus **restated 2026-09-09 by RULING OQ-K**, the comment id, and *"the part unchanged and only its test moved"*. The row's other four clauses and its `D6` pointer do not move |
| `design.md` § D6 (2) | one paragraph stating the equality | the restated part in four clauses (a) total coverage, (b) declared multiplicity, (c) the sum check over declared multiplicities, (d) pinned by test — followed by an inline `> Amended 2026-09-09.` note carrying the original paragraph verbatim and both reasons it was false. §§ D6 (1), (3), (4), the closed edit-class list and the *"WHY NO PROMOTED REQUIREMENT IS AUTHORED"* paragraph are byte-identical |
| `tasks.md` § 5.4 | the ratified equality item | the four clauses, the measured arithmetic, and the inline amendment note. Clause (b) carries the one obligation this amendment puts on FLOOR PART 1 — a replicated row declares its repository set — and names FLOOR PART 1's own successor pull request as where the manifest's row grammar gains the field |
| `tasks.md` § 8.2 (the archive gate's floor evidence) | *"the collection counts SUMMING across the three repositories"* | the mapping closing on § 5.4's ledger, with the identity, and an inline amendment clause quoting what it first said. The other three evidence lines and the *"None of these is 'the tests passed'"* sentence do not move |
| `README.md` OpenSpec Records row | the 2026-09-05 amendment note | that note, plus this amendment with the verbatim word, the timestamp, this record's path and the one-sentence reason. No other row moves |
| `review/amendment-2026-09-09-floor-part-2-mapping.md` | — | this file |

**Nine sites, four files plus this record.** Every one of them is inside the
change's own directory except the README row, which the 2026-09-05 amendment's
own form requires (*"the change's OpenSpec Records row"*). Nothing under
`contracts/`, `.github/`, `scripts/`, `openspec/specs/` or `docs/` is touched —
including `docs/opendox-carve-manifest.yaml`, which this amendment reads and does
not edit.

## Verification, from this session's own runs at the final tree

- **The arithmetic was measured twice, independently**, by two authors working
  from the landed manifest at `origin/main` `17167481`, counting `def test_` over
  each row's blob at `carve_commit b075fd91`. Both runs returned the same
  figures — 4,411 source; 1,098 / 2,315 / 968 + 30; three replicated test modules
  carrying 30 at `m = 3`; 4,471 across the destinations — and the tables above are
  what both produced. The measurement is a five-line loop over the manifest's own
  `rows:` and is re-runnable from any checkout carrying `carve_commit`.
- `python3 scripts/validate-openspec-cli-pin.py --change split-opendox-two-layer-product`
  and `--all` — strict validation through the pinned CLI entrypoint, the only
  route this repository permits.
- `python3 scripts/proposal-support.py . verify`.
- `python3 scripts/doc-health.py --single-repo .`, compared against the same run
  on the base commit: no new finding.
