# Verification record: gate-realization-axis-vocabulary, ratified tree 2026-09-12

Status: record
Kind: report
Date: 2026-09-12
Ratified by: gate-realization-axis-vocabulary — 2026-09-12, Brett Heap, D1 "Keep and gate" / D2 "Sweep in this PR" / D3 "Resolve against the registry that exists" (record `review/ratification-2026-09-12.md`)

**THIS FILE'S SUBJECT IS THE GATE RUN, NOT THE RATIFICATION**, which is why it
keeps `Status: record` while `review/ratification-2026-09-12.md` carries
`Status: ratified`. `document-lifecycle`'s *A review record records a
ratification* governs that file; the sibling scenario *A review record is not
about a ratification* governs this one.

**IT IS A ONE-SHOT CAPTURE.** A dated run report keeps `record`, and a later
re-run writes a different path rather than rewriting this one; bench rounds
after this capture record their own re-runs in `tasks.md` § 3.x, as rounds 7
through 9 already do.

**EVERY FIGURE BELOW WAS TAKEN ON THE RATIFIED TREE — after the merge from
`main`, after the sweep, and after the ratification encode — in the lane's own
fresh clone of the branch.** Nothing is carried forward from the pull request
body's earlier gate tables or from an earlier freeze; where a figure matches
one of those, it matches because it was measured again and came out the same.
`tasks.md` § 4 is the task-list section this file is the evidence for.

The tree: branch `change/gate-realization-axis-vocabulary`, merge of
`origin/main` `1f068646` at `fb55c9e9`, sweep at `3f7236f4`, ratification
encode on top. The control tree, where one is named, is a worktree of
`origin/main` `1f068646` taken in the same shell.

## 1. The packet, through the PATH CLI

`OPENSPEC_TELEMETRY=0 openspec validate gate-realization-axis-vocabulary
--strict` (PATH CLI **1.2.0**) — **exit 0**:

```text
Change 'gate-realization-axis-vocabulary' is valid
```

## 2. The whole corpus, through the PATH CLI, against the control

`OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — **exit 1**:

```text
✗ change/disposition-codexfactory-declared-renames
✗ change/disposition-codexfactory-floor-relocation-retitle
Totals: 101 passed, 2 failed (103 items)
```

The same command in the same shell on the `origin/main` `1f068646` worktree —
**exit 1**, `Totals: 100 passed, 2 failed (102 items)`, the SAME two failures
and no others. **The failure set is IDENTICAL; the item count moves by exactly
one, which is this change; and this change passes.** The two failures are the
known, dispositioned `disposition-codexfactory-*` pair and are not this
packet's.

## 3. The packet and the corpus, through the PINNED CLI, which is the one the gate runs

`python3 scripts/validate-openspec-cli-pin.py --change
gate-realization-axis-vocabulary --no-cache` — **exit 0**:
`@fission-ai/openspec@1.12.0` verified against its content address, its
80-package closure installed with `npm ci --ignore-scripts`,
`Totals: 1 passed, 0 failed (1 items)`, *"every target validated --strict
clean"*.

`python3 scripts/validate-openspec-cli-pin.py --all --no-cache` — **exit 0**,
`Totals: 101 passed, 2 failed (103 items)`, *"every target validated --strict
with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are
ACCEPTED EXCEPTIONS"* — the pre-existing accepted exceptions over
`add-chain-attestation` and `add-composed-view-authoring`, each carrying its
own `accepted by: Brett Heap, 2026-09-05, "take exit 2"`, neither of them this
change.

## 4. THE PACKET'S OWN GATE, BEFORE AND AFTER, ON TWO LIVE TREES

`python3 scripts/validate-target-release.py .`

| tree | exit | active | `implemented` | named release | registered | **refused** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `origin/main` `1f068646` (no gate present there) | **1** | 40 | 10 | 3 | 21 | **6** |
| THIS ratified tree | **0** | 41 | 17 | 3 | 21 | **0** |

BEFORE, in full — the same validator and the same register pointed at the
control worktree:

```text
target_release: 40 active proposals, 40 declaring — 10 `implemented`, 3 a named release, 21 named by the register, 6 outside the vocabulary.
  archive (read, never judged): 163 proposals, 61 of them outside the vocabulary.
target_release validation FAILED:
  - openspec/changes/add-composed-view-authoring/proposal.md: `none` is outside the ratified vocabulary — `implemented` or a release this estate defines
  - openspec/changes/add-cpc-clearing-boundary/proposal.md: `none` is outside the ratified vocabulary — `implemented` or a release this estate defines
  - openspec/changes/add-lens-document-selection/proposal.md: `none` is outside the ratified vocabulary — `implemented` or a release this estate defines
  - openspec/changes/add-substantive-review-lane/proposal.md: `none` is outside the ratified vocabulary — `implemented` or a release this estate defines
  - openspec/changes/amend-kill-switch-to-declared-test-companion/proposal.md: `a` is outside the ratified vocabulary — `implemented` or a release this estate defines
  - openspec/changes/register-gate-rules-council-seats/proposal.md: `none` is outside the ratified vocabulary — `implemented` or a release this estate defines
```

AFTER, in full, on this tree:

```text
target_release: 41 active proposals, 41 declaring — 17 `implemented`, 3 a named release, 21 named by the register, 0 outside the vocabulary.
  archive (read, never judged): 163 proposals, 61 of them outside the vocabulary.
target_release validation passed (every active declaration is admitted).
```

**BOTH ROWS ARE THE SAME VALIDATOR POINTED AT TWO TREES, SO THE ONLY DIFFERENCE
BETWEEN THEM IS THE TREE.** The `+1` active is this packet's own `proposal.md`
(`target_release: implemented`, judged by its own gate like every other active
change); the `+7` `implemented` is that `+1` plus the `+6` from the sweep (D2,
D2a), which `origin/main` has not received and will not until this packet
lands. The archive is read and counted on both sides and judged on neither.

## 5. The packet's own tests

`python3 -m pytest tests/target_release -q` — **exit 0**, **74 passed** (70 at
the last freeze; the four added for the class the merge exposed, `tasks.md`
§ 3.18). `grep -c '^def test_' tests/target_release/test_target_release_gate.py`
= **74**, so the figure is the file's and not a memory of it. A LATER BENCH
ROUND ON THIS SAME PULL REQUEST ADDS FIVE MORE (`design.md` D8j, `tasks.md`
§ 3.19, **79**); that round records its own re-run where this file's preamble
says it will, and does not rewrite this capture.

## 6. The substrate validators

- `python3 scripts/proposal-support.py . verify gate-realization-axis-vocabulary`
  — **exit 0**, *"proposal support verification ok"*.
- `python3 scripts/validate-sequenced-after.py .` — **exit 0**, *"41 active
  changes, 11 declaring the field"*, both archive-date arms passing.
- `python3 scripts/validate-sequenced-after.py . --ledger-diff` — **exit 0**,
  *"per-change sweep ledger consistent with the corpus (204 rows)"*.
- `python3 scripts/validate-scope-globs.py .` — **exit 0**, *"scope_globs
  validation passed (all active changes conform)"*.
- `python3 scripts/doc-health.py --single-repo .` — **exit 0**. Its findings on
  this tree are `info` only and none names this packet.

## 7. The wider suite, and an honest statement of what this clone cannot prove

`python3 -m pytest tests/doc-health tests/sequenced_after tests/scope_globs
tests/proposal-support tests/target_release -q` — **7 failed, 2294 passed, 1
skipped, 68 subtests passed**, exit 1.

**THE SEVEN FAILURES ARE NOT THIS PACKET'S AND THE CONTROL PROVES IT.** The
same `pytest tests/doc-health -q` run on this tree and on the `origin/main`
`1f068646` worktree returns the IDENTICAL failure set and the identical counts
— **7 failed, 1717 passed, 1 skipped** on each side:

```text
tests/doc-health/test_ideation_readiness.py::test_validate_index_finds_pinned_validator_and_checks_bootstrap
tests/doc-health/test_ideation_readiness.py::test_validate_index_rejects_a_broken_index
tests/doc-health/test_ideation_readiness.py::test_pipeline_proof_scores_real_clusters_and_validates_clean
tests/doc-health/test_readiness_dispatch.py::test_merge_wires_the_real_validator_for_a_genuinely_scored_index
tests/doc-health/test_sentinel_vocabulary.py::test_the_declared_emitters_are_measured_rather_than_believed
tests/doc-health/test_sentinel_vocabulary.py::test_unknown_is_not_folded_into_the_unreadable_repository_condition
tests/doc-health/test_status_reader_real_lines.py::test_the_reader_finds_what_the_writer_just_wrote_through_an_exotic_header
```

They are a property of this local environment, not of the branch: every one of
them is present on an unmodified `main`, and this packet touches none of those
modules. **THE AUTHORITATIVE FULL-SUITE FIGURE IS THIS PULL REQUEST'S OWN
REQUIRED `pytest-suite` RUN**, which is where `tasks.md` § 4.10 is settled and
which this record does not pre-empt or predict. Stating a local full-suite pass
here would be claiming something this clone did not show.

## 8. The delta was not rewritten by the ratification

`git diff --name-only fb55c9e9..HEAD --
openspec/changes/gate-realization-axis-vocabulary/specs/` returns **0 files**:
no byte of the `## ADDED Requirements` block was rewritten, restored or deleted
by the ratification or by the sweep. All three ruled options were the ones the
packet had already encoded, so there was nothing for the ratification to move.

## 9. The approval pair is an ADDITION beside an unmoved origin block

`git diff --numstat -- openspec/changes/gate-realization-axis-vocabulary/.openspec.yaml`
reads **`46 0`** — forty-six insertions, zero deletions. The pre-existing
`origin:` lines are byte-identical: lines 1–94, which are every line of the file
up to and including `proposed_on:`, hash to sha256
`70da6366fa4e9134f797310d052413f42a41d2d743260692e08c84ee77282193` BEFORE the
edit and to the same value AFTER it. `kind` and `id` never move. That is the
shape `add-drafted-proposal-origin` (issue #318) defined for this transition,
and it is why the `reason:` block keeps its drafting tense: it describes the
unapproved state the packet was authored in, and the approval sits beside it
rather than over it.

## 10. What this record does not cover

**A SECOND MERGE FROM `main` LANDED AFTER THIS CAPTURE** — `origin/main`
`5972c8f3`, pull request #1004 — and this file is not rewritten for it, because
a dated capture is of the tree it names. Its re-run lives where this file's
preamble says: `tasks.md` § 3.20, with § 4.1, § 4.3, § 4.4, § 4.6 and § 4.9
re-recorded there (42 active / 18 `implemented` / 0 outside here against the new
control's 41 / 11 / 6; `--all --strict` 101/3/104 against 100/3/103, the third
failure arriving with that merge and failing on BOTH trees; 205 ledger rows).

The required checks on the pull request head — `pytest-suite` above all — are
GitHub's runs and are read from the pull request, not from this clone. The
freeze comment posted after this capture carries that rollup. Nothing under
`openspec/specs/` is touched by this pull request, so there is no promotion to
verify; the archive's realization evidence is a later act's subject
(`tasks.md` § 5.1).
