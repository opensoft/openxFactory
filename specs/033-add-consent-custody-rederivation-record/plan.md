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

Against `.specify/memory/constitution.md` (v1.0.0), principle by principle —
named, not generically asserted.

| Principle | Verdict | How |
| --- | --- | --- |
| **I. Contract-First, Domain-Neutral Core** | PASS | The grown property is domain-neutral; the DOMAIN half — the custody store mapping and the operated re-derivation check — is explicitly the consumer's (§ 6, C-6a/C-7). No domain vocabulary lands here. No consumer file is written. |
| **II. Governed Change Flow** | PASS | The packet is a ratified OpenSpec change with `code_surface: openxFactory` and `target_release:` declared; this Speckit feature owns the implementation tasks and duplicates no governance decision. Under `release-realization` the change archives only on merged, green realization evidence — which is why § 5 is in scope and the archive is not. |
| **III. Document Lifecycle and Status Discipline** | PASS | No `Status:` header is edited by this feature except through the ratified packet's own already-completed transition. The three README amendments carry the `3b530009` form with an `AMENDED <date>` marker — a deliberate, reviewable step, never a silent status edit. Phase F waited on the lane's row-3 substrate note, which is now posted (#630 comment 5603344475, 2026-09-09), and every amendment cites it in its dated clause. |
| **IV. Schema and Artifact Discipline** | PASS | Every new fixture carries `schema_version` and `kind`; the new fixtures are `.example.yaml` / `negative/*.yaml` / `withheld/*.yaml` instantiation stubs, never live configuration; no credential and no host-absolute path is written; the new `examples/consent-instrument/withheld/` bucket is indexed in that directory's README, and `contracts/README.md`'s row is corrected (clarify A1). |
| **V. Validation Gates (NON-NEGOTIABLE)** | PASS, **with no deviation** | T081 runs every affected `scripts/validate-*.py` plus the PINNED `--all --strict`; doc-health is compared as a two-report pair with a pinned `--as-of` (T080); behaviour is proven by fixtures and tests (Phases D and E), never by assertion. **The earlier declared deviation is WITHDRAWN** (panel F2): the `consent-instrument` digest is re-derived in the § 2 commit that moves the schema, so `validate-manifest-digests.py` is green at EVERY commit on this branch, not only at the pushed head. |
| **VI. Versioned, Content-Addressed Releases** | PASS | All five coordinated values move together in ONE candidate commit (T061–T063); the version is allocated at realization and NOT reserved — the PR body names it as provisional and the LANE claims it at the last merge-from-main; the change class is ADDITIVE (minor) with the measurement that justifies it; the tag is left OWED for the operator and targets the LANDED merge commit. |
| **VII. Fail-Closed Authority Boundaries** | PASS | Both new enumerations are CLOSED; an unknown member is a schema refusal. Every refusal leg refuses rather than degrades — WITHHELD is a third outcome precisely so that "cannot admit" is never reported as a pass. Fixtures carry no credential and no tenant data. No authority is claimed that the ratified packet does not carry: the exit-code NUMBER is parked for Brett rather than invented here. |
| **Repository Constraints** | PASS | Work is in an isolated worktree under `../openxFactory-worktrees/`; every commit stages explicit paths and carries `Lane: opsXfactory-1`; no aggregation pin is touched; the validator grown here is a governed reference implementation ratified by this packet. |
| **Development Workflow and Quality Gates** | PASS | specify → clarify → plan → tasks → checklist → analyze, run from the worktree; clarifications recorded in `clarify-questions.md` and encoded into `spec.md`; analyze must reach ZERO before implementation; § 5's release metadata is the shared surface that **serializes at the lane's final integration commit**, which is exactly what the landing contract below prescribes. |

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
tests/intent-compliance/test_release_boundary.py   # cut-coupled (panel F1)
tests/clearing/test_clearing_manifest_rows.py      # cut-coupled IF measured owed
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
2. **WITHHELD gets exit status `3`, "needs a human decision"**, with exit 2
   keeping its ratified wording *"dependency/harness error"* (panel F10) — Brett Heap's
   ruling of 2026-09-09 (Q2), by multiple-choice selection, verbatim *"Exit 3 =
   needs a human decision (Recommended)"*. Behind a single named constant;
   docstring vocabulary extended in this script only; the packaged withheld
   fixture exempt. **It is the repository rule task 3.4b asked for**, and the
   lane records it on #630.
3. **A third fixture directory** `examples/consent-instrument/withheld/` with a
   fail-closed-both-ways `EXPECTED_WITHHELD_OUTCOMES` table (Q3a).
4. **Only `contract_schema_version` moves** (Q4).
5. **The manifest edit SPLITS BY WHAT THE FIELD IS** (Q5 as revised by panel
   F2) — the per-file `sha256` is integrity bookkeeping for the edited file and
   rides § 2's commit; `contract_bundle_version`, the appended
   `consumption_rule` paragraph, the CHANGELOG, the inventory and the
   cut-coupled tests are VERSION IDENTITY and ride the ONE § 5.2 candidate.
   Every intermediate commit is green.
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
15. **The cut-coupled tests are IN SCOPE as declared acts** (panel F1) —
    `tests/intent-compliance/test_release_boundary.py`'s enum member, its TWO
    match arms and its hand-written paragraph, plus whatever
    `tests/clearing/test_clearing_manifest_rows.py` measures as owed.
16. **The question sets are disambiguated** (panel F5): `032-Q<n>` for the
    twin's rulings, bare `Q<n>` for this feature's.

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
   A repeat-integration RETAINS the superseded gate transcripts, struck with a
   dated line naming the head that replaced them; the evidence shows every
   attempt, not only the last.
8. **§ 5.5 is the lane's tick**, in a follow-up bookkeeping commit while the
   packet is still live. This feature leaves it NOT-OWED-HERE with a dated line.

## Implementation sequence (dependency order)

**THE PHASE LETTERS HERE ARE `tasks.md`'s LETTERS, EXACTLY.** An earlier draft
of this table used its own scheme, in which corpus counts were a separate phase
and every letter after it was offset by one — so this table's "Phase G" named
the cut while `tasks.md`'s Phase G named the README amendments, and the risk
row below pointed at the wrong phase. One scheme, and it is the executable
file's.

| Phase | Tasks | Content | Gate before moving on |
| --- | --- | --- | --- |
| **A** | T001–T007 | Speckit tree: spec, clarify answers, plan, research, tasks, checklists | analyze clean |
| **B** | T010–T017 | § 2 schema growth **+ the `consent-instrument` digest re-derivation** (panel F2 — integrity bookkeeping for the edited file, not a release surface) | schema self-validates; `git diff` shows zero lines inside `custody`; **`validate-manifest-digests.py` GREEN at this commit** |
| **C** | T020–T028 | § 3 validator legs, the WITHHELD outcome and exit `3`, the extended walk | validator runs clean over the un-grown corpus |
| **D** | T030–T049 | § 4 fixtures — positives, negatives, the withheld bucket, `self_test`'s third bucket, **and the three corpus-count surfaces (T047–T049)** | `validate-consent-instruments.py --strict` 0/0 with three bucket counts; counts re-measured, never incremented |
| **E** | T050–T054 | `tests/consent_instruments/` | `pytest tests/consent_instruments -q` green, then the full suite |
| **F** | T055–T059 | Q8's three README amendments | **UNBLOCKED 2026-09-09** — the lane's row-3 substrate note is posted at [#630 comment 5603344475](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5603344475), covering both sibling-row sentences, this change's own Records row and `contracts/README.md:102`; every amendment cites it in its dated clause |
| **G** | T060–T066 | § 5.2–5.4 THE CUT: re-measure the number AND the bundle's path list, then `contract_bundle_version` + the appended `consumption_rule` + CHANGELOG + built inventory **+ every CUT-COUPLED TEST (T061a–c, panel F1)** in ONE commit | all five gates green against that exact unchanged candidate, the full suite included |
| **H** | T070–T084 | Bookkeeping: 46 notes, evidence in both trees, A2's dated note, the post-hoc tick/evidence audit | note classes sum to 46; every tick rides its evidence's commit |

**Every phase files a transcript, not only the final ones** (FR-042b): B, C, D
and E each record the run that satisfied their gate, captured raw with its
return code — a phase judged complete on an unrecorded local run is a gate that
was not run.

Phases B–E are strictly ordered. **F and G are INDEPENDENT of each other**
(panel F6): F is takeable — the note arrived on 2026-09-09 — and **G never waits
on F**, in either direction. **G is LAST in the ordering** so the candidate
stands on the final tree, which is a statement about B–E and not about F.

## Risks, and how each is refused rather than accepted

| Risk | Refusal |
| --- | --- |
| A sibling lane takes `contract-v3.5` | The number is a measurement re-taken at every merge-from-main and CLAIMED by the lane at the last one. Nothing on this branch reserves it. |
| The digest inventory drifts from the tree | It is BUILT by `validate-contract-release.py build`, never hand-edited, and `verify-commit` re-derives it against the exact candidate. |
| The stale manifest digest between § 2 and § 5.2 is read as a defect | § 2's commit message states the staleness and names the commit that closes it. CI runs at the PR head, where it is closed. |
| The withheld fixture reddens a caller | Measured: no caller reads this exit code. The packaged fixture is exempt in any case. |
| The exit-code number is wrong | It is not a guess: Brett Heap RULED `3` on 2026-09-09 by explicit selection over two declined alternatives, and the ruling is cited verbatim at the constant, in the design note and in the evidence. It remains a single named constant. |
| A tick claims an act nobody performed | Every tick's note cites a commit, a record or a transcript, and rides the same commit as its evidence. |
| A README amendment lands without its substrate claim | Was the Phase F blocker; **DISCHARGED 2026-09-09** — the note is posted ([#630 comment 5603344475](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5603344475)) and every amendment cites it. |
| The substrate note never arrives *(MOOT — it arrived 2026-09-09; retained as the rule)* | T055 reports the block ONCE, and the orchestrator RE-CHECKS at each merge-from-main (the same cadence the version re-measurement already runs on) rather than polling. If the branch reaches T082 with Phase F still blocked, **T056 is still taken** — this packet's own row rides its standing row-3 claim and needs no note — and **T057/T058 take a dated `REPORTED, NOT PERFORMED` line** naming the block, in the same register as §§ 6–7's NOT-OWED lines. They are not left dangling and they are not silently dropped. |
| A gate reds after the candidate commit is formed | The candidate is **REMADE**, never patched (FR-034a): a fresh single commit, and every gate re-run against it. Amending the reviewed commit's tree while keeping its identity would leave gates certifying a tree that no longer exists. |
| A repeat-integration orphans the evidence already gathered | The superseded transcripts are **RETAINED and STRUCK with a dated line naming the head that replaced them** — never deleted and never silently overwritten. An evidence directory that shows only the last attempt cannot show that the earlier one was superseded rather than skipped. |
| Landing arms a cross-repo refusal nobody scheduled | A2 is recorded as a dated note in two places and built nowhere. |
