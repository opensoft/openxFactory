# Implementation Plan: The consent instrument grows a re-derivable custody record, and the bundle is cut on it

**Branch**: `033-add-consent-custody-rederivation-record`
**Spec**: `specs/033-add-consent-custody-rederivation-record/spec.md`
**Clarifications**: `specs/033-add-consent-custody-rederivation-record/clarify-questions.md`
(round 1 ruled 2026-09-09 after cross-model adversarial review; Q2's exit-code
NUMBER parked for Brett Heap)
**Lane**: opsXfactory-1

## Summary

Realize §§ 0–5 of `add-consent-custody-rederivation-record`: grow
`contracts/schemas/consent-instrument.schema.yaml` by ONE closed top-level
sibling array and a `contract_schema_version` bump; grow
`scripts/validate-consent-instruments.py` by the chain's INTERNAL legs, a
rewritten-pin refusal, a `path_only` digest-equality refusal, an extended
blob-shape walk and a THIRD OUTCOME (`custody-content-class-withheld`) with its
own exit status; grow the packaged corpus by positives, negatives and a third
WITHHELD bucket; then cut `contract-v3.5` in the SAME pull request. Bookkeeping
boxes whose acts are already performed are ticked with evidence; boxes owned by
the lane or the operator or the consumer take dated NOT-OWED lines.

## Technical Context

**Language/Runtime**: Python 3 (`pyyaml`, `jsonschema>=4.18`,
`rfc3339-validator`), YAML contracts, Markdown governance docs.
**Primary surfaces**: `contracts/schemas/consent-instrument.schema.yaml`;
`scripts/validate-consent-instruments.py` (862 lines);
`examples/consent-instrument/` (+ `negative/`, + a NEW `withheld/`);
`contracts/manifest.yaml`; `contracts/CHANGELOG.md`;
`contracts/releases/contract-v3.5.digests.yaml`; `contracts/README.md`;
`README.md`; a NEW `tests/consent_instruments/`.
**Test command CI runs**: `python3 -m pytest tests/ -q -m "not postgres"`
(`.github/workflows/pytest-suite.yml:462`).
**Pinned OpenSpec CLI**: `scripts/validate-openspec-cli-pin.py`
(`@fission-ai/openspec@1.12.0`), `OPENSPEC_TELEMETRY=0`. PATH's 1.2.0 is never
used.
**Repository**: single-repo shape; feature worked in a linked worktree at
`../openxFactory-worktrees/033-add-consent-custody-rederivation-record`.

## Constitution Check

| Rule | How this plan satisfies it |
| --- | --- |
| OpenSpec governs, Speckit implements | The packet is ratified; this feature writes no requirement and edits no ratified prose. |
| Ratified prose frozen | `proposal.md`, `design.md`, `.openspec.yaml` and the delta are untouched except ONE additive dated realization note after `proposal.md`'s `Lane:` line, permitted by architect ruling Q10. |
| Every YAML carries `schema_version` + `kind` | The grown schema keeps both; new fixtures carry both. |
| Neutral contracts live here; consumers pin | No consumer file is written. § 6 stays the consumer's. |
| Tick only what is done | A box is ticked in the same commit as its evidence, or in neither. |
| No host-absolute paths in committed files | Every path written is repo-relative. |
| Lane discipline | `Lane: opsXfactory-1` on every commit; no PR, no comment, no merge, no tag from this seat. |

## Project Structure

### Documentation (this feature)

```text
specs/033-add-consent-custody-rederivation-record/
├── spec.md                  # what and why
├── clarify-questions.md     # 12 questions + inline answers + A1/A2
├── plan.md                  # this file
├── research.md              # the measurements the plan stands on
├── tasks.md                 # the executable task graph
├── checklists/              # no-arg maximum-coverage set
└── evidence/                # gate transcripts, doc-health report pair
```

### Repository files this feature writes

```text
contracts/schemas/consent-instrument.schema.yaml   # § 2
scripts/validate-consent-instruments.py            # § 3
examples/consent-instrument/*.example.yaml         # § 4 positives
examples/consent-instrument/negative/*.yaml        # § 4 negatives
examples/consent-instrument/withheld/*.yaml        # § 4 THIRD bucket (new dir)
examples/consent-instrument/README.md              # § 4.9
contracts/README.md                                # clarify A1
tests/consent_instruments/                         # new package (Q7)
contracts/manifest.yaml                            # § 5.2 (three edits, one commit)
contracts/CHANGELOG.md                             # § 5.3
contracts/releases/contract-v3.5.digests.yaml      # § 5.2, BUILT not hand-edited
README.md                                          # three amended sites (Q8)
openspec/changes/add-consent-custody-rederivation-record/tasks.md      # notes
openspec/changes/add-consent-custody-rederivation-record/proposal.md   # ONE note
openspec/changes/add-consent-custody-rederivation-record/evidence/realization-2026-09-09.md
```

## Phase 0 — Research (measurements, not options)

Recorded in `research.md`. Every figure was taken on this branch, not carried
forward from the packet. The load-bearing ones:

- The next additive minor is `contract-v3.5`, free on all three surfaces.
- The consent schema is NOT a release-inventory member.
- `contracts/` carries 4 additions and 14 modifications since `contract-v3.4`,
  none of them this session's.
- The packaged corpus is 6 valid + 7 negative; three separate documents state
  `5 + 5`.
- No caller anywhere reads `validate-consent-instruments.py`'s exit code.
- PR #774 carries no approving GitHub review.

## Phase 1 — Design decisions, all taken from the architect's ruled answers

Nothing below is this plan's invention; each cites its answer.

1. **ONE pull request carries §§ 2–5** (Q1a) — § *Version Identity* requires the
   manifest and changelog to move atomically with the contract files.
2. **WITHHELD gets a new exit status behind a single named constant** (Q2),
   provisionally `3`, docstring vocabulary extended in this script only, the
   packaged withheld fixture exempt, the NUMBER parked for Brett Heap.
3. **A third fixture directory** `examples/consent-instrument/withheld/` with a
   fail-closed-both-ways `EXPECTED_WITHHELD_OUTCOMES` table (Q3a).
4. **Only `contract_schema_version` moves** (Q4).
5. **No split of the manifest edit** (Q5a) — digest, bundle version and the
   appended `consumption_rule` paragraph all ride the § 5.2 candidate commit;
   § 2's commit leaves the digest stale on purpose and says so.
6. **The CHANGELOG names the whole bundle** (Q6).
7. **`tests/consent_instruments/`**, with both a fixture and a parametrized
   pytest for the walk, and both a source-level ban and a runtime patch over all
   three buckets for the no-git absence (Q7).
8. **Three README sites amended in the `3b530009` form**, two of them awaiting
   the lane's substrate note (Q8).
9. **Nine new *Named cases* bullets and a third table column** (Q9).
10. **All seven finding codes verbatim** (Q10).
11. **§ 5.4 ticks on local gate runs against the exact candidate** (Q11).
12. **The blob walk covers the whole entry minus the two digests** (Q12).
13. **`contracts/README.md:102` is corrected as an ADDITIONAL act** (A1).
14. **A2's cross-repo consequence is RECORDED, never armed.**

## THE LANDING CONTRACT (ruled at Q1, recorded here because `plan.md` is where it belongs)

1. **§§ 2–5 land in ONE pull request.** The manifest, the changelog, the digest
   inventory and the contract files are one atomic release surface.
2. **`contract-v3.5` is a MEASURED CANDIDATE, never a reservation.** The PR body
   names it as explicitly provisional. **The orchestrator re-measures at every
   merge-from-main and reports the result to the lane.**
3. **The LANE claims the number** on openxFactory issue #630 row 4 **at the LAST
   merge-from-main before the merge — at cut time and not before** (task 5.1;
   ratification record lines 109–111; the policy forbids reserving a minor
   before merge order is known).
4. **Landing is a MERGE COMMIT.** There is no linear-history rule on this
   repository, and a merge commit keeps the reviewed candidate reachable.
5. **The merge commit IS "a different commit"** under
   `docs/contract-versioning-policy.md` § *Bundle Realization Order* step 4, so
   the LANE performs the final merge-from-main inside its Rule 6 window,
   **RE-RUNS every gate against that merge commit**, and only then merges.
6. **If `main` advanced under `contracts/` between integration and merge, the
   lane REPEATS the integration.** A bundle measured against a tree that has
   since moved is not a measurement.
7. **The annotated tag (§ 5.6, Brett's act) targets the LANDED MERGE COMMIT.**
8. **§ 5.5 is the lane's tick**, in a follow-up bookkeeping commit while the
   packet is still live. This feature leaves it NOT-OWED-HERE with a dated line.

## Implementation sequence (dependency order)

| Phase | Content | Gate before moving on |
| --- | --- | --- |
| **A** | Speckit tree: research, plan, tasks, checklists | analyze clean |
| **B** | § 2 schema growth | schema self-validates; `git diff` shows zero lines inside `custody`; digest KNOWINGLY stale |
| **C** | § 3 validator legs, WITHHELD outcome, extended walk | validator runs clean over the un-grown corpus |
| **D** | § 4 fixtures — positives, negatives, the withheld bucket, `self_test`'s third bucket | `validate-consent-instruments.py --strict` 0/0 with three bucket counts |
| **E** | `tests/consent_instruments/` | `pytest tests/consent_instruments -q` green |
| **F** | § 4.9 + A1 corpus counts (README, manifest comment, `contracts/README.md`) | counts re-measured, never incremented |
| **G** | Q8's three README amendments | **BLOCKED on the lane's substrate note for the two sibling-row sentences** |
| **H** | § 5.2–5.4 THE CUT: re-measure the number, then manifest + CHANGELOG + built inventory in ONE commit | all five gates green against that exact unchanged candidate |
| **I** | Bookkeeping: 46 notes, evidence in both trees, A2's dated note | note classes sum to 46; every tick has evidence in its own commit |

Phases B–F are strictly ordered. **G may be taken any time after the lane's
note arrives and MUST NOT block H.** **H is LAST**, so the candidate stands on
the final tree.

## Risks, and how each is refused rather than accepted

| Risk | Refusal |
| --- | --- |
| A sibling lane takes `contract-v3.5` | The number is a measurement re-taken at every merge-from-main and CLAIMED by the lane at the last one. Nothing on this branch reserves it. |
| The digest inventory drifts from the tree | It is BUILT by `validate-contract-release.py build`, never hand-edited, and `verify-commit` re-derives it against the exact candidate. |
| The stale manifest digest between § 2 and § 5.2 is read as a defect | § 2's commit message states the staleness and names the commit that closes it. CI runs at the PR head, where it is closed. |
| The withheld fixture reddens a caller | Measured: no caller reads this exit code. The packaged fixture is exempt in any case. |
| The exit-code number is wrong | It is a single named constant, and Q2 records that the number is Brett's ruling. |
| A tick claims an act nobody performed | Every tick's note cites a commit, a record or a transcript, and rides the same commit as its evidence. |
| A README amendment lands without its substrate claim | Phase G is BLOCKED until the lane posts the note. |
| Landing arms a cross-repo refusal nobody scheduled | A2 is recorded as a dated note in two places and built nowhere. |
