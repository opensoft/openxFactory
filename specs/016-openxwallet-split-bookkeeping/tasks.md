# Tasks: split-openxwallet-repo §1 bookkeeping

**Input**: Design documents from `/specs/016-openxwallet-split-bookkeeping/`
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [quickstart.md](./quickstart.md)

**Tests**: No test tasks. This feature has no code surface (plan.md § Technical
Context); the constitution's Principle V evidence requirement is met by
byte-diffs against ratified text plus two validator gates, which appear as
explicit verification tasks rather than as a test suite.

**Organization**: Phases 3–5 map one-to-one onto the spec's three user stories.
US1 (naming record) and US2 (working rule) are both P1 and fully independent of
each other — different repositories, different pull requests. US3 (the ledger) is
P2 and strictly last, because it records the other two.

## Path conventions

Two repositories, two worktrees. All paths below are relative to one of:

- `OX` = `/home/brett/projects/xFactory/openxFactory-worktrees/016-openxwallet-split-bookkeeping`
  (openxFactory, branch `016-openxwallet-split-bookkeeping`; created at `origin/main` = `5ef6d8d2`, fast-forwarded to `1dd822ea` before any edit when origin/main advanced by two unrelated commits — baselines were re-captured on the new base)
- `AGG` = `/home/brett/projects/xFactory-worktrees/openxwallet-working-rule`
  (`opensoft/xFactory` aggregation, branch `change/openxwallet-working-rule`, base `origin/main`)

Neither shared checkout (`/home/brett/projects/xFactory/openxFactory`,
`/home/brett/projects/xFactory`) is edited.

---

## Phase 1: Setup

**Purpose**: Both worktrees exist on the right base, and the Speckit artifacts
are in place. Already discharged during specify/plan; listed so the record is
complete.

- [X] T001 Confirm `OX` worktree is on branch `016-openxwallet-split-bookkeeping` on the current `origin/main` via `git -C $OX status -sb` and `git -C $OX rev-parse origin/main`, fast-forwarding if behind and re-capturing baselines on the resulting base
- [X] T002 [P] Confirm `AGG` worktree is on branch `change/openxwallet-working-rule` with base `origin/main` via `git -C $AGG status -sb`
- [X] T003 [P] Confirm the feature artifacts exist under `OX/specs/016-openxwallet-split-bookkeeping/`: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `checklists/requirements.md`

**Checkpoint**: both worktrees isolated from the shared checkouts; artifacts present.

---

## Phase 2: Foundational (blocking prerequisites)

**Purpose**: Pin the ratified source texts and the measurement baselines *before*
any file is edited. Every later task is a comparison against something captured
here, so an unmeasured baseline makes the evidence unverifiable after the fact.

**⚠️ CRITICAL**: T005 and T006 must be captured before Phase 3 edits the tree.

- [X] T004 Extract the three ratified source blocks from `OX/openspec/changes/split-openxwallet-repo/proposal.md` and hold them for verbatim transcription: Amendment 2's body (`:236-258`), the inline pointer's "after" text (`:264-265`), and the working-rule replacement (`:276-279`)
- [X] T005 Capture the pre-edit doc-health baseline on the branch base by running `python3 scripts/doc-health.py --single-repo .` in `OX` and recording the `Findings:` line (expected `5 critical, 7 error, 41 warning, 4 info`)
- [X] T006 [P] Capture the pre-edit OpenSpec baseline by running `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` in `OX` and recording the totals line (expected `77 passed, 0 failed`)
- [X] T007 [P] Record the task-1.10 differential already measured in research.md § R5 — pre-packet `5ef6d8d2^1` = `64486a51` at `5/6/41/4` versus post-packet `5ef6d8d2` at `5/7/41/4`, and the single `location-conformance` / `contested` finding on `ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md` — as the text T018 will cite
- [X] T008 [P] Confirm the edit sites are where research.md says: `grep -c 'openxWallet' OX/docs/openxdox-naming.md` = 1 (line 24), `wc -l OX/docs/openxdox-naming.md` = 109, `## Amendment 1` at line 84, and `AGG/CLAUDE.md` rule 1 at lines 61-62

**Checkpoint**: source texts pinned, baselines recorded. User stories may now proceed.

---

## Phase 3: User Story 1 — The naming record stops contradicting the ratified ruling (Priority: P1) 🎯 MVP

**Goal**: `docs/openxdox-naming.md` records that `openXwallet` is on the house
`openX<type>` form, that the wire label stays lowercase, and that
`openXwallet-Install` is a registered name with no repository — and its § Decision
pointer stays grammatical with one exception named.

**Independent test**: read the record end to end. Amendment 2 exists, is dated
2026-08-26, sits last, matches Amendment 1's shape; the inline pointer reads as
grammatical English naming one exception; doc-health adds no finding against the
file. Realizes tasks.md §1 task 1.11(a) and 1.11(b).

- [X] T009 [US1] Append the new final section `## Amendment 2 — openXwallet leaves the exception list (2026-08-26)` to `OX/docs/openxdox-naming.md` after Amendment 1, transcribing the proposal's three paragraphs verbatim as body prose (not a blockquote), wrapped to the file's ~79-column width — data-model.md § E1
- [X] T010 [US1] Replace the § Decision parenthetical in `OX/docs/openxdox-naming.md` (the `- **Capability name:**` bullet, lines 23-25) with the proposal's verbatim "after" sentence, rewriting for singular agreement rather than deleting the token — data-model.md § E2, research.md § R3
- [X] T011 [US1] Verify the record's lifecycle header in `OX/docs/openxdox-naming.md` is byte-identical and still carries exactly ONE ratification citation line: `grep -cE '^(Ratified by:|Ratified:|Amended:)'` = 1, and no `Status`/`Ratified`/`Kind`/`Purpose` line appears in `git -C $OX diff origin/main -- docs/openxdox-naming.md`
- [X] T012 [US1] Verify amend-never-rewrite and the trap checks on `OX/docs/openxdox-naming.md`: the diff shows only an end-of-file append plus the one replaced bullet; the record body ABOVE Amendment 2 carries zero `openxWallet` occurrences (`sed -n '1,109p' | grep -c` = 0) while Amendment 2 itself keeps the two the ratified text names as history; `grep -c 'spellings are the family'` = 0; capability ids, the `xfactory_wallet_*` prefix and finding codes are untouched
- [X] T013 [US1] Diff the written Amendment 2 body and the replaced pointer against the ratified blocks captured in T004 and confirm word-for-word equality modulo line wrapping — quickstart.md § 1

**Checkpoint**: US1 complete and independently valuable — the ratified-record contradiction is resolved even if nothing else lands.

---

## Phase 4: User Story 2 — The aggregation working rule stops being false as written (Priority: P1)

**Goal**: xFactory `CLAUDE.md` working rule #1 permits the neutral `open*` product
repository openxFactory pins, still forbids domain repos from authoring neutral
contracts, and still requires every consumer to pin — delivered as an open PR.

**Independent test**: on `change/openxwallet-working-rule`, rule 1 matches the
proposal's replacement verbatim and `git diff --stat` shows `CLAUDE.md` alone.
Fully independent of US1: different repository, different PR. Realizes tasks.md
§1 task 1.12.

- [X] T014 [P] [US2] Replace § "Working rules" item 1 in `AGG/CLAUDE.md` (lines 61-62) with the proposal's verbatim four-line replacement text — data-model.md § E3, research.md § R4
- [X] T015 [US2] Verify the aggregation diff is minimal: `git -C $AGG diff origin/main --stat` names `CLAUDE.md` only; the `## Working rules` heading and rules 2 onward are byte-identical; no `.gitmodules`, gitlink or submodule pin is touched
- [X] T016 [US2] Commit in `AGG` with an explicit pathspec (`git -C $AGG commit -m … -- CLAUDE.md`), after checking `git -C $AGG status -sb` for the current branch and `git -C $AGG diff --cached --stat` for foreign entries, then `git -C $AGG push -u origin change/openxwallet-working-rule`
- [X] T017 [US2] Open the pull request with `gh pr create -R opensoft/xFactory --base main`, body citing §1 of the ratified openxFactory `split-openxwallet-repo` (PR #391) with the Claude Code footer, and leave it **unmerged**; record the URL

**Checkpoint**: US2 complete and independently valuable — the aggregation rule is corrected and under review.

---

## Phase 5: User Story 3 — §1's ledger tells the truth about itself (Priority: P2)

**Goal**: `openspec/changes/split-openxwallet-repo/tasks.md` §1 has every box
ticked, each new tick carries resolvable evidence, and task 1.1 no longer claims a
status the ratification falsified.

**Independent test**: read §1. Zero unticked boxes; each newly ticked box names a
file and a commit or PR; 1.1's trailing clause describes the ratified state; §2–§12
untouched. Depends on US1 and US2 only because it cites their outcomes. Realizes
tasks.md §1 tasks 1.1 and 1.10 and the ticks for 1.11 and 1.12.

- [X] T018 [US3] Tick task 1.10 in `OX/openspec/changes/split-openxwallet-repo/tasks.md` (line 88) with an evidence note carrying the T007 measurement — both commits, both finding counts, and the one differential finding named by family, path and class, with the statement that it lies outside 1.10's stated scope and outside §1's authority to remedy — data-model.md § E4b
- [X] T019 [US3] Replace task 1.1's stale trailing `` `Status: draft`. `` in `OX/openspec/changes/split-openxwallet-repo/tasks.md` (line 37) with a clause naming the header's actual ratified state, without renumbering R1–R8 and without touching the LOCKED block — data-model.md § E4a
- [X] T020 [US3] Tick tasks 1.11 (line 91) and 1.12 (line 103) in `OX/openspec/changes/split-openxwallet-repo/tasks.md`, each with a trailing evidence note naming the changed file and the carrying commit or PR, in the shape §1's existing ticked entries use
- [X] T021 [US3] Verify §1 has zero unticked boxes and that the `- [x]` count in §2–§12 is identical between `origin/main` and `HEAD` — quickstart.md § 3
- [X] T022 [US3] Confirm `OX/README.md` § "OpenSpec Records" needs no edit: task 1.9 already listed the change and no §1 task requires a README change (FR-014); leave the file untouched

**Checkpoint**: all three user stories complete; §1's open tasks are discharged and recorded.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: run the gates, land the openxFactory commit, open its PR, and leave
both PRs for the human merge gate.

- [X] T023 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` in `OX` and confirm `77 passed, 0 failed` — unchanged from the T006 baseline (FR-015)
- [X] T024 Run `python3 scripts/doc-health.py --single-repo .` in `OX` and confirm the `Findings:` line equals the T005 baseline exactly; an error count of 8 means the naming-record edit introduced a finding and must be fixed before commit (FR-016)
- [X] T025 Commit in `OX` with explicit pathspecs naming `docs/openxdox-naming.md`, `openspec/changes/split-openxwallet-repo/tasks.md`, `specs/016-openxwallet-split-bookkeeping/` and `.specify/feature.json`, after checking `git -C $OX status -sb` and `git -C $OX diff --cached --stat` for foreign entries; subject ≤72 chars in house style, body citing §1, PR #391 and `5ef6d8d2`
- [X] T026 Push with `git -C $OX push -u origin 016-openxwallet-split-bookkeeping`
- [X] T027 Open the pull request with `gh pr create -R opensoft/openxFactory --base main`, body covering what/why, the Amendment 2 text summary, a link to the xFactory PR from T017, the validation results from T023/T024, and the Claude Code footer; leave it **unmerged**
- [X] T028 [P] Confirm both PRs are `OPEN` and unmerged (`gh pr list` per quickstart.md § 5) and that no box in `tasks.md` §2–§12 was ticked (FR-013, FR-017)

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)**: no dependencies.
- **Foundational (Phase 2)**: needs Phase 1. **Blocks everything** — T005/T006
  baselines must be captured before the tree is edited, or the differential
  evidence cannot be reconstructed.
- **US1 (Phase 3)** and **US2 (Phase 4)**: both need Phase 2, and **neither needs
  the other**. Different repositories, different pull requests.
- **US3 (Phase 5)**: needs US1 and US2 complete, because T020's evidence notes
  cite their commit and PR. T018 and T019 depend only on Phase 2 and could run
  earlier; they are grouped here because they belong to the same file and the same
  ledger story.
- **Polish (Phase 6)**: needs Phases 3 and 5 (the openxFactory edits) complete.
  T017 (the aggregation PR) is in Phase 4 because it is that story's delivery, not
  a polish step.

### Story dependencies

- US1 (P1) — independent. **This is the MVP.**
- US2 (P1) — independent of US1.
- US3 (P2) — records US1 and US2; runs last.

### Parallel opportunities

- Phase 1: T002 and T003 run alongside T001.
- Phase 2: T006, T007 and T008 run alongside T005.
- **Across stories**: T014 (`AGG/CLAUDE.md`) is parallel with all of Phase 3 —
  different repository, no shared file.
- Within Phase 3: T009 and T010 touch the same file and must be sequential;
  T011–T013 are verifications over the finished file.
- Phase 6: T028 is parallel with nothing else outstanding.

```bash
# Example: the two P1 stories in parallel
# Agent A (US1, openxFactory):   T009 → T010 → T011 → T012 → T013
# Agent B (US2, aggregation):    T014 → T015 → T016 → T017
# Then, once both land:          T018 → T019 → T020 → T021 → T022
# Then:                          T023 → T024 → T025 → T026 → T027 → T028
```

---

## Implementation Strategy

### MVP first

**US1 alone is a shippable increment.** It removes a live contradiction inside a
`ratified` record, which is the only §1 item doing so, and it gates nothing else.
If the feature had to stop after Phase 3, the corpus would be strictly better.

### Incremental delivery

1. Phases 1–2 → baselines pinned, nothing edited yet.
2. Phase 3 → naming record correct. **Independently valuable.**
3. Phase 4 → aggregation rule correct and under review. **Independently valuable.**
4. Phase 5 → ledger truthful about all of the above.
5. Phase 6 → gates green, both PRs open for the human merge gate.

### Standing constraints (apply to every task)

- **The ratified text wins.** Improving on the proposal's wording is a defect.
- **Explicit pathspecs on every `git add`/`git commit`** — both checkouts are
  shared; `git add -A` would sweep other sessions' work.
- **Case-sensitive edits only.** `openXwallet` (brand), `openxwallet` (wire
  label) and `openxWallet` (retired) are three distinct strings.
- **Merge nothing.** Both PRs stay open for the human gate.
- **Successors are untouchable.** No box in `tasks.md` §2–§12 is ticked.
