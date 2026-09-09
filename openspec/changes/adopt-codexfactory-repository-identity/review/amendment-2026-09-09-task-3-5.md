# Task Amendment: adopt-codexfactory-repository-identity task 3.5

Status: record

Decision date: 2026-09-09

Amender: Brett Heap (convener) — in session, interactive walkthrough, lane
`provenance-autonomous-merge`, session `f1356e27-665d-4119-b47e-a5e66efdce00`
/ window `codeXfactory-3` on Eagle.

Verbatim ruling:

> **Respell to github:codeXfactory.**

Given in answer to the two readings recorded in
`review/addendum-2026-09-08-token-namespace.md` (Reading A — the namespace
names the CONSUMER's issuing directory and does not move; Reading B — the
namespace is read as the estate the binding operates across, and becomes
misleading once it sits above two respelled members). The convener chose the
source-repository reading.

Realized by: pull request [#801](https://github.com/opensoft/openxFactory/pull/801),
branch `realize/codexfactory-identity-b1`, slice **B1** of
`adopt-codexfactory-repository-identity`'s realization.

Ratified head this amends: `5bfdcf3c06478167bd7509f1576db3528ce4ede1`
(ratification 2026-09-07, record `review/ratification-2026-09-07.md`). Merged
as PR **#763**, `eb30db7a`.

---

## 1. What was blocked

Task 3.5 as ratified 2026-09-07 enumerates the review-lane decision-core pin
and everything that asserts it, line by line, for
`contracts/review-lane-repin-binding.template.yaml` naming only **lines 46 and
110**. Line **103** (`consumer.identity_namespace`) is a third occurrence of
the `opensoft` owner segment in the same file, in a different governed member,
that task 3.5's list does not cover and no other task names either. The
adversarial review of PR #801 raised it as **B-1 recommendation 3** and it was
recorded, not silently applied, as
`openspec/changes/adopt-codexfactory-repository-identity/review/addendum-2026-09-08-token-namespace.md`
— **NEEDS BRETT'S WORD**, because either reading is a claim about what is
true rather than a spelling.

## 2. The original wording, quoted

From `tasks.md` § 3, as ratified 2026-09-07:

> - [ ] 3.5 **ONE COMMIT.** The review-lane decision-core pin and everything
>       that asserts it: `contracts/review-lane-pin.yaml:47` (`repository:`)
>       and its header line 8; `contracts/review-lane-repin-binding.template.yaml`
>       (lines 46, 110); `.github/workflows/review-lane-repin.yml`
>       (`SOURCE_REPOSITORY` at 137, the checkout at 385);
>       `scripts/review_lane_repin.py:62` (`SOURCE_REPOSITORY`);
>       `scripts/doc_health/pin_class.py:793` (the note text); and the three
>       pin tests `tests/review_lane_pin/test_floor_snapshot.py:74`,
>       `tests/review_lane_pin/test_review_lane_caller.py:135` (both
>       `PINNED_REPOSITORY`) and `tests/review_lane_pin/test_repin_lane.py`
>       (lines 851, 1165).

## 3. The amended wording

Task 3.5's original file list and commit grouping are **unchanged**. What is
added is a third occurrence in the same already-in-scope file:

> - [ ] 3.5 **ONE COMMIT.** The review-lane decision-core pin and everything
>       that asserts it: `contracts/review-lane-pin.yaml:47` (`repository:`)
>       and its header line 8; `contracts/review-lane-repin-binding.template.yaml`
>       (lines 46, 110). **AMENDED 2026-09-09: task 3.5 now also covers line
>       103 (`consumer.identity_namespace`) of the same file, respelled to
>       `github:codeXfactory` by convener ruling — see
>       `review/addendum-2026-09-08-token-namespace.md` and this record.**
>       `.github/workflows/review-lane-repin.yml` (`SOURCE_REPOSITORY` at 137,
>       the checkout at 385); `scripts/review_lane_repin.py:62`
>       (`SOURCE_REPOSITORY`); `scripts/doc_health/pin_class.py:793` (the note
>       text); and the three pin tests
>       `tests/review_lane_pin/test_floor_snapshot.py:74`,
>       `tests/review_lane_pin/test_review_lane_caller.py:135` (both
>       `PINNED_REPOSITORY`) and `tests/review_lane_pin/test_repin_lane.py`
>       (lines 851, 1165).

The task's own checkbox is **not** ticked by this record — task 3.5 ticks on
its pull request's merge, which is Brett's act at the transfer window, per the
packet's existing "Ticks" convention (see PR #801 § Ticks).

## 4. What the amendment does NOT change

- **No requirement moves.** This is an amendment to an implementation task,
  not to a ratified spec delta, so no re-ratification is owed. The four ADDED
  requirements on `repository-identity` are untouched, and
  `credential-contracts`'s requirements (the shared-authority-identity pair
  comparison) are untouched — the amendment respells a value inside an already
  optional, grammar-checked member; it does not change what any requirement
  demands.
- **The other file members task 3.5 names are unaffected.** Lines 46 and 110
  were already respelled to `codeXfactory/codexFactory` at this branch's head
  before this amendment; this record adds only line 103.
- **No `sequenced_after` consequence.** Unlike the task 1.1 amendment
  (`amendment-2026-09-08-task-1-1.md` § 5), this amendment touches no
  declared change dependency.
- **The evidence file's arithmetic is updated, not reopened.** See
  `evidence/codexfactory-identity-sweep-2026-09-08.md` § 17.

## 5. Why this is a task amendment and not a silent edit

The addendum (`addendum-2026-09-08-token-namespace.md` § 3) is explicit that
line 103 is a governed contract member the ratified packet does not name, and
that "either answer is a claim about what is true rather than a spelling."
Widening task 3.5's own file-list wording to say so, in the same manner as the
2026-09-08 task 1.1 amendment records an authorship-clause change, keeps the
packet's task list an accurate record of what a merge of PR #801 actually
does.
