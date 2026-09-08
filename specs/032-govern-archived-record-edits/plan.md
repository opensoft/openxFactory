# Implementation Plan: The promoting repository performs its own acts under the archived-record-edit rule

**Branch**: `032-govern-archived-record-edits` | **Date**: 2026-09-08 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/032-govern-archived-record-edits/spec.md`,
seeded from the ratified OpenSpec change `govern-archived-record-edits`
(openxFactory `main` `3504287a`, PR #788).

## Summary

Three artifacts change and one is created. `docs/document-lifecycle.md` gains one
top-level bullet at the end of § *Status Claim Rules* recording the neutral
bookkeeping-note minimum (task 3.4). The packet's `tasks.md` becomes a truthful
record of the 28 boxes — ticked where the act is done, unticked with a dated
NOT-OWED line where it belongs to another repository, packet or act. The packet
gains `evidence/realization-2026-09-08.md` carrying every § 4 gate result and two
measurements the archive act reads. And `proposal.md` gains one purely additive
dated note so its ratified enumeration of the packet's whole diff stays true.

There is no code. The packet declares `code_surface: none` and builds no checker
by design (design.md D-6), so "implementation" here is governed prose plus
measured gate evidence, and the gates are the test suite.

## Technical Context

**Language/Version**: none — Markdown governance text; Python 3 only as the
runner for the repository's existing validators.

**Primary Dependencies**: the PINNED OpenSpec CLI `@fission-ai/openspec@1.12.0`
at `<scratchpad>/cli-pin-prefix/bin/openspec`, reached ONLY through
`scripts/validate-openspec-cli-pin.py` (PATH's 1.2.0 is never used);
`scripts/validate-sequenced-after.py`, `scripts/validate-scope-globs.py`,
`scripts/validate-manifest-digests.py`, `scripts/doc-health.py`, `pytest`.

**Storage**: N/A.

**Testing**: `pytest tests/sequenced_after tests/proposal-support
tests/scope_globs -q`, plus the validators above; the doc-health finding set is
diffed against `main`.

**Target Platform**: the openxFactory repository, single-repo Speckit shape.

**Project Type**: governance-text realization of a ratified OpenSpec change.

**Performance Goals**: N/A.

**Constraints**: no archived byte edited; `design.md`, `.openspec.yaml` and the
spec delta frozen; no checker written; no pin edited; work only in the dedicated
clone; explicit-path staging; the three trailers on every commit; no PR, no
comment, no merge, no `openspec archive`.

**Scale/Scope**: 1 doc bullet (~12 lines), 28 task boxes annotated, 1 evidence
file, 1 additive proposal note, 1 Speckit feature directory.

## Constitution Check

*GATE: passed before Phase 0; re-checked after Phase 1.*

| Principle | Bearing on this feature | Verdict |
| --- | --- | --- |
| I. Contract-First, Domain-Neutral Core | The rule being realized is estate-neutral and lives in the promoted `document-lifecycle` capability; the domain half is OpsxFactory's and is out of scope. | PASS |
| II. Governed Change Flow | The OpenSpec change exists, is ratified, and this feature realizes it. No new boundary is decided here. | PASS |
| III. Document Lifecycle and Status Discipline | The one edited governance document keeps its `Status: standard` header and gains an inline change citation; the new `evidence/` file is deliberately outside the lifecycle scan set. | PASS |
| IV. Schema and Artifact Discipline | No YAML artifact is authored or changed. | PASS (N/A) |
| V. Validation Gates (NON-NEGOTIABLE) | Every § 4 gate runs at the final head and its output is recorded verbatim; the doc-health finding set is diffed against `main`. | PASS |
| VI. Versioned, Content-Addressed Releases | No contract bundle is cut; `contracts/manifest.yaml` is untouched; measured — no in-repo `sha256` pin names any file this feature edits. | PASS (N/A) |
| VII. Fail-Closed Authority Boundaries | The realization performs no operator act it was not given: the § 1 `[OPERATOR]` boxes are ticked against a resolvable record (review `5141756427`) and never against an invented word. | PASS |

**Complexity**: none to justify. No new project, no new dependency, no new
tooling.

## Project Structure

### Documentation (this feature)

```text
specs/032-govern-archived-record-edits/
├── spec.md                  # written (specify + clarify applied)
├── clarify-questions.md     # written, answered inline
├── plan.md                  # this file
├── research.md              # Phase 0 — the measurements this plan rests on
├── quickstart.md            # Phase 1 — how a later reader re-runs every gate
├── tasks.md                 # Phase 2 (/speckit-tasks)
├── checklists/              # /speckit-checklist, no-arg = maximum coverage
└── evidence/                # captured gate output at the final head
```

### Repository files this feature writes

```text
docs/document-lifecycle.md                                   # + one top-level bullet in § Status Claim Rules
openspec/changes/govern-archived-record-edits/
├── proposal.md                                              # + one additive dated realization note
├── tasks.md                                                 # 28 boxes annotated; ticks where the act is done
└── evidence/realization-2026-09-08.md                        # NEW — gate output + two measurements
```

**Frozen, and named so the freeze is checkable**:
`openspec/changes/govern-archived-record-edits/design.md`, `.openspec.yaml`,
`specs/document-lifecycle/spec.md`, every path under
`openspec/changes/archive/`, `tests/sequenced_after/corpus-ledger.yaml`,
`README.md`, `contracts/**`.

**Structure Decision**: single repository, Speckit feature directory at
`specs/032-govern-archived-record-edits/`, worked on the feature branch inside a
dedicated clone rather than in a linked worktree — the clone is exclusive to this
realization, so the rule the worktree convention protects (never work the base
branch of a shared checkout) is satisfied without a second tree.

## Phase 0 — Research (measurements, not options)

Recorded in [research.md](./research.md). Five measurements the plan rests on:

1. The packet has not moved since ratification, and neither has promoted canon
   or the § 3.4 target (`git log 3504287a..68712924` over those three paths is
   empty).
2. No in-repo `sha256` pin names `docs/document-lifecycle.md`.
3. doc-health's `GOVERNED_ROOTS` excludes the Speckit tree and includes `docs/`.
4. `EVIDENCE_PARTS` excludes `evidence/` from the lifecycle scan set.
5. The corpus ticks `[OPERATOR]` boxes when the act is done, and marks a
   not-owed box with a dated line rather than a tick.

## Phase 1 — Design decisions taken from the architect's answers

- **The bullet's shape** (Q2a/Q2b/Q3): one top-level bullet at the end of
  § *Status Claim Rules*, sub-bullets beneath it, the note form quoted
  byte-exact, two explanatory sentences, the inline citation "Ratified by
  `govern-archived-record-edits` (2026-09-08)" with the archive-act phrase in a
  FOLLOWING sentence.
- **The tick policy** (Q1/Q5/Q6/Q7): act-done, not actor-class; per-box dated
  notes; one NOT-OWED line per unticked box; 3.1 and 4.2 deliberately unticked;
  no invented quotation anywhere.
- **The amendments** (FR-017): the three ratified "stays unticked" sentences are
  amended in the same commit that ticks, each naming the superseded sentence and
  the reason.
- **The evidence home** (Q4/Q8): the packet's `evidence/` file plus this feature
  directory; the pinned-target measurement is also a dated note in `tasks.md`.
- **The `proposal.md` note's anchor** (FR-010a): immediately after the `Lane:`
  line, never inside the YAML and never above `Status:` — measured, because
  `Status: ratified` sits at real-line index 8 of a 15-line header window and the
  folded `code_surface` scalar counts as one real line.
- **The enumeration note** (Q10): one additive dated note in `proposal.md`.

No data model and no contracts directory: this feature creates no entity and no
interface. `quickstart.md` stands in for both, as the re-run recipe.

## Implementation sequence (dependency order)

1. **S1 — the doc bullet.** `docs/document-lifecycle.md`. Independent of
   everything else; it is the only act that can move gate 4.4.
2. **S2 — the evidence file skeleton + the two measurements.** The pinned-target
   measurement and the MODIFIED-block currency measurement, both re-taken at the
   branch head rather than copied from this plan.
3. **S3 — the gate run.** Every § 4 gate at the head that carries S1 and S2, with
   output captured to files (rc plus the summary line, never a bare tail).
4. **S4 — `tasks.md`.** Ticks, per-box notes, NOT-OWED lines, the § 4 pinned-target
   note, and the three sentence amendments — one commit, evidence already
   recorded (FR-018).
5. **S5 — the `proposal.md` enumeration note.**
6. **S6 — the final gate re-run** at the head that carries S4 and S5, since those
   commits touch `openspec/changes/**` and are inside the pinned CLI's scan.
7. **S7 — the Speckit tree.** Commit `checklists/` and `analysis.md`; verify
   FR-016 (nothing under `scripts/`, `.github/`, `contracts/`, `tests/`),
   FR-019 and SC-006's 28-box count.
8. **STOP (B) → architect report.** Then the analyze loop's fixes, then the gate
   report; the lane claims, opens the PR, lands and archives.

**Sequence → task mapping**: S1 = T005–T010; S2 = T011–T013; S3 = T014–T018;
S4 = T019–T027; S5 = T028; S6 = T029–T031; S7 = T032–T033; STOP (B) = T034.

## Risks and how each is refused rather than accepted

| Risk | Refusal |
| --- | --- |
| The doc bullet moves doc-health's finding set. | Gate 4.4 diffs the finding set against `main`; a non-empty diff is a blocker, not a note. |
| A tick lands ahead of its evidence. | FR-018: same commit or neither. |
| A note invents a ratification quote. | The record says the approval body is EMPTY; notes cite review id + timestamp + record path only. |
| The doc restates the requirement in different words. | The note form is quoted byte-exact; the two extra sentences are explanation, and the passage carries its change citation. |
| Ratified prose drifts. | `design.md`, `.openspec.yaml` and the delta are frozen; `proposal.md` takes ONE additive dated note; SC-007 checks the diff's path set. |
| Canon moves under the MODIFIED block mid-flight. | S6 re-runs the currency measurement at the final head. |
| The twin's state is misreported. | Notes cite PR #279 as the landing vehicle and no merge sha, because none exists. |
| A gate fails mid-sequence. | FR-020: blocker — the dependent task stops, no box is ticked against it, the output is recorded as produced and reported at STOP (B). |
| A defect is found after a commit. | FR-021: forward-only repair, a new commit naming what it supersedes; no force-push, no deleted evidence. |
| Brett Heap exercises one of the three flagged vetoes after the branch is built. | Each is reversible by one named act (revert the proposal note; untick and restore the three sentences; delete the two explanatory sentences), recorded as a forward-only correction. |
| The doc-health baseline is taken from a differently-named checkout. | `--previous-report` REFUSES on repo-identity mismatch by design; the plan uses two independent `--report-out` runs and a normalized diff instead. |
| A gate is green here and red in CI. | FR-023: these results are LOCAL evidence at a named head; CI on the lane's PR is a separate confirmation this feature does not claim. |
