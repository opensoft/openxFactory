# Design: mirror-floor-addition-grace

Status: draft

The reasoning behind the authoring decisions in `proposal.md`, and the
measurements they rest on. Nothing here is ratified; the proposal's own
`Status:` governs.

## 1. What is actually being mirrored

The codexFactory core exports ONE function and the two lanes are supposed to be
two callers of it:

```python
evaluate_floor_completeness(
    floor,                       # a parsed RepositoryGateFloor
    prefix="openspec/specs",     # a LITERAL; the block declares its prefix in
                                 # prose, and prose is not data
    base_tree_paths=tree,        # `git ls-tree -r --name-only HEAD`
    changed_entries=entries,     # filename, status, previous_filename
    generated_at=header.generated_at,   # report only
    added_since_pin=window,      # `None` = NOT MEASURED = no B1 grace
    tolerance=None,              # None reads the floor's declared field
) -> FloorCompleteness
```

`FloorCompleteness.report()` returns the JSON shape the advisory lane merges
into its verdict, and its keys were chosen to match what step 8 already prints —
`uncovered_paths`, `caused_by_candidate`, `already_unreachable`. Its `refusals()`
order is `floor_drift_caused_by_candidate`, then `floor_partially_unreachable`,
then `floor_incomplete`, with `floor_surface_vacuous` appended LAST so that
`refusals[0]["stage"]` — which step 8 assigns to the run's stage — keeps exactly
the meaning it has today. `stage` is `pending_floor_extension` ONLY when nothing
refuses.

Two facts about the function shape decide most of this packet:

* **It performs no git call.** Every fact arrives as an argument. So each lane
  measures the window with whatever history its own checkout has, and the
  function is hermetically callable from a test.
* **`added_since_pin=None` means NOT MEASURED and grants nothing.** That is the
  ratified fail-safe, and it is the DEFAULT rather than an exception.

## 2. The two lanes are not symmetric, and the asymmetry is the design

| | required lane (`pytest-suite`) | advisory lane (`merge-master-approval`) |
|---|---|---|
| blocks a merge | **yes**, org ruleset `21538893` | no, blocks nobody |
| pinned core present | `continue-on-error: true` — **may be absent** | **fatal** if unreadable (`exit 1`) |
| base history | `fetch-depth: 0` already | **shallow today**, no `fetch-depth` declared |
| candidate's diff | not available — runs on the checked-out tree | available — `pulls/files` with `status` |
| what it reads the floor from | the VENDORED byte snapshot, offline | the pinned core's own document |

Every one of those five rows points the same way: **the required lane must keep
working when the core is unreachable, and the advisory lane has nothing to
protect by pretending it can.** That is the whole of authoring decision A.

### 2.1 Why importing into the required lane spends a property this repository
already paid for

`test_floor_snapshot.py` states the property as load bearing:

> The coverage assertion above keeps holding from the snapshot throughout, so an
> outage never wedges the repository; it only becomes IMPOSSIBLE TO MISS.

An importing assertion cannot hold from the snapshot: on an outage it has no
rule to apply. Skipping makes the blocking assertion stop blocking — the
CSC-F16 silent-false-green species the module was written to guard against, one
level up, inside its own guard. Failing makes a required check red for a cause
no candidate can fix, which `pytest-suite.yml`'s own rule forbids and which
`continue-on-error: true` exists to prevent.

So the mirror is written locally and the FALSIFIER is foreign. The core's
`tests/merge-master/fixtures/floor-addition-grace/` exists for exactly this and
says so:

> Each vector carries `input` and a HAND-WRITTEN `expect`. They are the
> falsifier of the implementation, not a recording of it — regenerating them
> from the code would destroy the only thing they are for.

Measured at `712fc8ca`: **16 accepted vectors and 5 refused ones**, covering
every ratified scenario class — the created-path grace, modification, copy, the
not-yours case, deletion, rename-laundering, mixed addition-and-deletion, the
three B1 cases, both graces in one run, both D-3 cases, the clean case, the
three-way separation case, and the vacuous surface; the five refused vectors are
the prefixes that normalize to nothing.

### 2.2 The replay's skip, and why it is the same shape as the freshness verifier

`TheFreshnessVerifier` is today the ONLY skipping test in
`tests/review_lane_pin/`, and `pytest-suite.yml` watches it two ways:

1. by NAME — `FRESHNESS_CLASSNAME` / `FRESHNESS_TESTNAME` looked up in
   `pytest-report.xml`, verdict required to be `passed`. This is the
   load-bearing signal, and it is the Codex P2 fix from PR #569.
2. by COUNT — `EXPECT_SKIPPED: "21"`, pinned exactly, as the backstop. An
   aggregate cannot distinguish "the verifier vanished" from "the verifier
   vanished AND another conditional skip started running"; the pair cancels.

The vector replay is the second test in that class and takes the same treatment
verbatim: a second watched classname/testname pair, and `EXPECT_SKIPPED` moving
21 → 22 with its reason recorded beside the existing one. This is the discipline
being applied a second time, not loosened.

### 2.3 The rejected sub-option: vendoring the vectors

Vendoring `vectors.json` beside `contracts/review-lane-floor-snapshot.yaml`,
with its own `sha256` in `contracts/review-lane-pin.yaml`, would make the replay
unskippable and remove the `EXPECT_SKIPPED` move entirely. It is rejected on
cost, not on principle:

* it adds a **SIXTH** site to a lockstep whose own obligation field already
  reads *"five sites name this one now, up from three"*;
* the snapshot is vendored because a BLOCKING assertion must read the floor
  offline. The replay is a consistency check BETWEEN LANES — it decides nothing
  about the candidate in front of it — so the reason that forced vendoring for
  the snapshot does not apply to it;
* a vendored fixture drifts silently in exactly the way `floor_snapshot`'s own
  header warns about, and the repair (a sixth digest, a sixth refresh step)
  costs more per pin advance than the skip-and-watch costs per outage.

Put for veto as a sub-decision of A because the cheaper-looking option should
not be mistaken for the unconsidered one.

## 3. How the required assertion gets facts the pulls/files listing gives step 8

Step 8 gets `{filename, status, previous_filename}` from
`repos/:o/:r/pulls/:n/files`, having first PARKED unless the paginated count
equals the authoritative `changed_files` total and the head SHA is unchanged
across the gather. The required suite has no `gh`, by construction —
`tests/hermeticity.py` makes `gh` unreachable — and it runs on the
merged/checked-out tree. So it measures from git:

```
created  = git diff --name-status --diff-filter=A \
             $(git merge-base <base> HEAD)..HEAD -- openspec/specs
window   = git log --diff-filter=A <generated_at>..<base> --name-only \
             -- openspec/specs
```

with `<base>` the base branch ref (`origin/main`, resolved) and `<generated_at>`
read from the vendored snapshot's generated-block header — the same single value
`test_the_generated_block_declares_the_commit_it_was_derived_at` already
asserts is present exactly once and 40-hex.

**Every one of those reads can fail, and every failure is fail-safe.** No
`origin/main` (a developer's bare checkout, a fork), no merge base (unrelated
histories), a `generated_at` that does not resolve (the branch it lived on was
deleted — which is the measured live state of `3afd8a8c`), a `generated_at` that
resolves but is not an ancestor of the base (the range would name the WRONG
window against an unrelated commit, which is worse than naming none): each
yields NO grace from that half, and an off-floor path is reported uncovered
exactly as it is today. This mirrors `paths_added_after_pin`'s own contract,
which returns `None` in the same conditions and for the same stated reason.

### 3.1 A note on which tree the surface is taken over

Step 8 computes the surface over the POST-MERGE tree —
`post_merge_tree_paths(base tree, changed entries)` — so the candidate that adds
the path is the one that sees it. The required assertion runs ON the checked-out
tree, which for a `pull_request` event IS the merge tree. So the two agree
without either of them having to reconstruct anything, and the mirror passes
`base_tree_paths=git ls-files` with an EMPTY `changed_entries` while supplying
the created set separately. That difference in HOW the same set is obtained is
worth stating, because it is the one place the two lanes' inputs are not
literally identical even though their verdict is.

## 4. The base checkout depth (decision C)

`merge-master-approval.yml` step 3 is:

```yaml
      - name: Checkout base (this repository)
        uses: actions/checkout@v4
        with:
          persist-credentials: false
```

No `ref:` — deliberately, so it takes the BASE branch tip and never the
candidate head — and no `fetch-depth:`, so it is `actions/checkout`'s default
of 1. One commit cannot resolve a pin seven regenerations old.

Measured on this branch, 2026-09-05: openxFactory `main` is **2,025 commits**;
`git count-objects -vH` reports **29.56 MiB** packed. That is the cost of
`fetch-depth: 0` on a step that currently fetches one commit, once per advisory
run.

The targeted alternative — deepen only to the declared pin — is cheaper and
strictly more fragile: the depth required is a function of how stale the pin is,
so a value sufficient today fails INTO THE FAIL-SAFE later, and the lane would
then report `uncovered` for a bystander's path with no visible cause. The
requirement therefore constrains the PROPERTY (the window must be measurable, or
the fail-safe applies and is visible) and leaves the mechanism to a declared
choice.

## 5. Sequencing, and the five sites

The pin advance moves, in ONE act:

1. `contracts/review-lane-pin.yaml` → `core_commit`
2. `.github/workflows/merge-master-approval.yml` → `PINNED_CORE_COMMIT`
3. `.github/workflows/merge-master-approval.yml` → the core checkout's `ref:`
4. `.github/workflows/pytest-suite.yml` → the core checkout's `ref:`
5. `contracts/review-lane-floor-snapshot.yaml` → re-copied bytes, plus
   `floor_snapshot.sha256` and `floor_snapshot.entry_count` in the pin

The existing tests already refuse any disagreement among them, so the lockstep
is machine-held rather than merely documented. Requirement 6 adds only the
ORDER: within one pull request the advance is the earlier commit, so no commit
in the history carries a mirror of a rule its own pin does not yet have.

**The pin's target is a codexFactory commit that CARRIES the grace.** At
authoring, codexFactory `origin/main` IS `712fc8ca` — measured 2026-09-05 — so
the target is that commit unless codexFactory has advanced by the time the
realization runs, in which case it is whatever `origin/main` then names, with
`712fc8ca` an ancestor. The realization re-measures rather than trusting this
sentence.

### 5.1 The regeneration that follows, and the defect it retires

The FIRST regeneration after the grace is in force is the first one that can be
performed at a LANDED openxFactory commit, because the grace is what stops the
promoting pull request from being refused for its own path. That is the whole
mechanism by which the three-of-five non-ancestor finding stops recurring, and
it is why the codexFactory generator now refuses (`--write`) a `--ref` its
source repository's default branch does not carry.

Re-measured here, on this branch, against `origin/main` at `55c95dc1`:
`3afd8a8c`, `c236c6b1` and `8d893a0f` are NOT ancestors; `0ae74086` and
`2a3b29c8` are. The live pin is the worst case in the set. Recorded rather than
tidied away.

## 6. What this design deliberately leaves alone

* **The deletion direction.** `candidate_floor_drift`, the removal requirement,
  LS-A2's DE-FLOOR-BEFORE-YOU-REMOVE ordering: untouched. The grace has no
  removal branch.
* **CSC-C7 and floor authorship.** The generator remains the block's only
  sanctioned writer and codexFactory remains the document's sole author. Option
  (a) from codexFactory issue #203 — letting the archiving pull request extend
  the floor itself — is not what this is, and the distinction is why (c) was
  ruled.
* **The D-3 tolerance number.** Declared in codexFactory's own
  CODEOWNERS-routed document, read here through the core. An absent declaration
  reads as ZERO and restores the pre-grace behaviour exactly, which is the
  fail-closed direction on purpose.
* **Whether the advisory lane becomes required.** LA-C1's ordering condition and
  `add-substantive-review-lane` task 5.1's ruleset half are untouched.
