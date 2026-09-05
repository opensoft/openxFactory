---
code_surface: openxFactory — TWO SITES, and only two. (1) `tests/review_lane_pin/test_floor_snapshot.py`'s LQ-A7 coverage assertion `test_every_tracked_openspec_spec_path_is_on_the_floor` and the two negative controls that guard the same surface and fail with it by construction (`test_the_unmutated_surface_is_a_positive_first`, `test_a_fabricated_off_floor_spec_path_is_refused`), inside the REQUIRED `pytest-suite`; plus a new replay of the pinned core's exported completeness vectors, and the `EXPECT_SKIPPED` / watched-testcase bookkeeping in `.github/workflows/pytest-suite.yml` that a second skipping test moves. (2) `.github/workflows/merge-master-approval.yml` step 8's completeness computation and its rendered verdict, plus that workflow's base checkout depth. NOT THIS CHANGE'S SURFACE, each for a stated reason: the codexFactory core, its floor document, its generator and its vectors are AUTHORED THERE and read here (this packet edits no codexFactory file and claims no authority over one); `contracts/review-lane-pin.yaml` and the four other pin sites move in the REALIZATION's own first commit as the prerequisite named in requirement 6, not in this proposal; and no floor regeneration is performed by this packet at all.
target_release: a code surface, so per `release-realization` it archives only on merged + green realization evidence. The evidence is: the five pin sites advanced in lockstep to a codexFactory commit carrying the grace; the required assertion and its two negative controls moved onto the mirrored rule with the vector replay green; `merge-master-approval.yml` step 8 reporting `pending_floor_extension` distinct from `floor_incomplete` with its base checkout carrying history; ONE floor regeneration performed after the grace is in force at a LANDED openxFactory commit; and the `pending_floor_extension` outcome observed once on a real run and quoted in the archive record. No contract bundle is involved — this packet adds no registered contract row, moves no digest set, spends no `contract_bundle_version` and owes no release tag.
sequenced_after: [codexFactory:add-floor-addition-grace]
---

# Proposal: mirror-floor-addition-grace

Status: draft
Proposed: 2026-09-05
Origin: codexFactory issue #203, ruled option (c) by Brett Heap 2026-09-05,
verbatim *"rule c, this lane authors it"*; the codexFactory packet
`add-floor-addition-grace` ratified 2026-09-05 (*"ratify 205, B1 stands"*) and
REALIZED by codexFactory PR #206, merge commit `712fc8ca`. That packet's
requirement 6 names this repository's half as the COMPANION CHANGE
`openxFactory: mirror-floor-addition-grace` and deliberately does not author it
(its tasks 4.1–4.3). Governing issue: openxFactory #675.

Authored: 2026-09-05, lane `openXfactory-2` (formerly `openxfactory-1d`), on
Brett Heap's word of the same day, verbatim **"companion"**. **THAT WORD
AUTHORIZED THE AUTHORING, NOT THE CONTENT. RATIFICATION IS OWED AND IS BRETT
HEAP'S ACT**; nothing below is
ratified by being authored, and no requirement here may be cited as approved
until he rules on this packet itself. Every judgment this authoring session took
is listed under § Authoring decisions rather than presented as settled.

## Why

**The pull request that promotes a capability is refused for creating the path
the floor is supposed to protect — and in this repository the refusal BLOCKS.**

codexFactory's `repository_gate_floor` for `opensoft/openxFactory` is an EXACT
SET. Its machine-generated block names every tracked path under this
repository's `openspec/specs` at a pinned commit — 59 paths today, inside a
67-entry floor that is eight hand-reasoned chokepoints plus that one block. So
**promoting a capability is an addition to the set the floor enumerates**, and
the completeness direction — `surface − entries` — reports the new path as
uncovered in two places at once:

* `tests/review_lane_pin/test_floor_snapshot.py`'s
  `test_every_tracked_openspec_spec_path_is_on_the_floor`, inside `pytest-suite`
  — **REQUIRED** on this repository by organization ruleset `21538893`, so a
  pull request cannot merge while it is red — together with the two negative
  controls that guard the same surface and fail with it by construction; and
* `.github/workflows/merge-master-approval.yml` step 8, at stage
  `floor_incomplete`, in the advisory lane that blocks nobody.

**The repair has been paid five times in two days, and this repository paid half
of each one.** `contracts/review-lane-pin.yaml`'s own history is the record:
seven regenerations, FOUR of them on 2026-09-04 alone (`79198ac4` at 12:25:19Z,
`bfb8bde3` at 14:05:07Z, `6d35c4fe` at 16:02:21Z, `76fa501c` at 23:47:59Z), each
matched here by an advance moving FIVE SITES IN LOCKSTEP. The floor document's
own comment block concedes the shape: *"TWO ADVANCES IN ONE DAY IS THE FEATURE'S
CADENCE, NOT AN INCIDENT, AND A THIRD IS ALREADY OWED."*

**The ordering that cadence forces has a measured consequence, and it is this
repository's defect rather than codexFactory's.** Because the block must be
regenerated at a tree that ALREADY carries the new path before the pull request
carrying it can merge, codexFactory pins `generated_at` at an openxFactory
PULL-REQUEST HEAD. Re-measured on this branch, 2026-09-05, against
`origin/main`:

| declared `generated_at` | ancestor of openxFactory `main`? |
|---|---|
| `3afd8a8c` — **the live pin** | **NO** |
| `c236c6b1` | **NO** |
| `8d893a0f` | **NO** |
| `0ae74086` | yes |
| `2a3b29c8` | yes |

**Three of the last five are not ancestors of `main`.** They survive only on
undeleted `origin/archive/*` and `origin/change/*` branches. A floor pinned at a
commit a branch deletion makes unresolvable is a floor whose pin-relative
measurement silently disappears — and under the ratified grace, the pin is
exactly what the bystander half is measured FROM.

**codexFactory has already fixed its half. This repository has not.** The core
carries `evaluate_floor_completeness` since `712fc8ca`; its ratified requirement
*"The blocking check and the reporting lane implement one completeness rule"*
names openxFactory's two sites and says, in the fixture README's words, why
prose alone will not hold them together:

> openxFactory's REQUIRED `pytest-suite` assertion (LQ-A7) and its advisory
> `merge-master-approval` step 8 each hand-roll `set(tracked) - set(entries)`,
> and two hand-rolled set differences is exactly how a lane that BLOCKS and a
> lane that REPORTS come to disagree about the same candidate.

Until this change lands, the ratified grace **is inert in the lane that actually
blocks**, and the required check still refuses the promoting pull request. That
is stated here without hedging because the codexFactory packet stated it about
itself in the same terms.

## What Changes

- **One rule, two lanes.** Both openxFactory sites classify an off-floor spec
  path exactly as the pinned core's `evaluate_floor_completeness` does:
  covered-pending when the candidate's own diff creates it (git status `added`),
  or when it was added to `main` after the block's `generated_at`; never for a
  removal, a rename, a copy or a modification; and an empty or degenerate
  surface never passes.
- **How the required assertion learns the candidate's own diff.** It runs on the
  merged/checked-out tree, not against a GitHub `pulls/files` listing, so it
  measures from git: the created set is
  `git diff --name-status --diff-filter=A <merge-base>..HEAD -- openspec/specs`
  against the base branch, and the pin window is
  `git log --diff-filter=A <generated_at>..<base> -- openspec/specs`.
  `pytest-suite.yml` already checks out at `fetch-depth: 0`, so both are
  measurable there today.
- **FAIL-SAFE, and it is the default.** No base, no merge base, an unresolvable
  `generated_at`, or a `generated_at` that is not an ancestor of the base → NO
  grace, path reported uncovered, today's behaviour exactly. *An unresolvable
  pin is a reason to refuse, never a reason to excuse.*
- **The required assertion MIRRORS; the advisory lane IMPORTS.** Authoring
  decision **A**, below, and it is the packet's one real design choice.
- **Reporting.** Step 8 surfaces `pending_floor_extension` distinct from
  `floor_incomplete`, naming and counting the graced paths with a reason per
  path, keeping `refusals[0].stage` semantics; the rendered summary table gains
  a row; the escalation state is shown when the core reports it; and the
  anti-vacuity step gains a positive assertion that the pending computation ran.
- **The advisory lane's base checkout carries history.** It is shallow today —
  step 3, `Checkout base (this repository)`, declares no `fetch-depth` — so the
  pin window is unmeasurable there and B1 would be permanently fail-safed off in
  the reporting lane while it worked in the blocking one. That is precisely the
  disagreement requirement 6 of the core packet forbids.
- **Sequencing, explicit.** The pin advances first, past `712fc8ca`, five sites
  in lockstep; the mirror cannot land before it; and the first regeneration
  after the grace is in force is performed at a LANDED openxFactory commit,
  which retires the live pin `3afd8a8c`'s non-ancestor defect.
- **What does not change**: the vendored snapshot stays a byte witness; the
  enumeration stays exact; CSC-C7 stands and codexFactory remains the floor's
  sole author; a fabricated off-floor path that no diff creates stays refused.

## Capabilities

### New Capabilities

- `review-lane-floor-mirror` — SEVEN requirements and 28 scenarios (measured
  by grep against the delta at this commit: `grep -c '^### Requirement:'` → 7,
  `grep -c '^#### Scenario:'` → 28), `## ADDED Requirements` ONLY, with no
  `## MODIFIED` and no `## REMOVED` block anywhere in the delta. See authoring
  decision **B** for why a new capability rather than an existing one.

### Modified Capabilities

None. No promoted openxFactory capability today says anything about the review
lane pin, the floor snapshot or LQ-A7 —
`grep -rl "review-lane-pin\|LQ-A7\|floor_snapshot" openspec/specs` returns
NOTHING at this commit, across all 59 promoted capabilities — so there is no
requirement text to modify and no sibling-delta hazard to walk into.

## What this deliberately does not do

- **It authors no codexFactory file** and claims no authority over one. The
  rule's one home is `evaluate_floor_completeness`; the floor document, its
  generator, its vectors and its runbook are codexFactory's.
- **It does not perform the pin advance or the regeneration.** Both are
  REALIZATION acts, named in tasks and in requirement 6, and both are separately
  claimed.
- **It does not touch the deletion direction.** `candidate_floor_drift`, the
  removal requirement and the DE-FLOOR-BEFORE-YOU-REMOVE ordering stand exactly
  as they are; the grace has no removal branch to weaken.
- **It does not set, propose or endorse the D-3 tolerance value.** codexFactory
  shipped `floor.pending_floor_extension_tolerance: 3` in its own
  CODEOWNERS-routed document, put for veto there. This repository READS the
  field through the core and neither declares nor overrides it.
- **It does not make the advisory lane required.** LA-C1's ordering condition
  and `add-substantive-review-lane` task 5.1's ruleset half are untouched, and
  nothing here may be cited as advancing either.
- **It does not fold in option (b)** from codexFactory issue #203 — a scheduled
  regeneration workflow opening the re-pin pull request automatically. That
  option is NOT RULED; nothing here designs it, schedules it or assumes it.

## Authoring decisions — put for veto, not presented as settled

Brett Heap's word authorized the authoring. It settled none of these. Each is
stated with the alternative it beat, so a veto has something to veto.

### A — the required assertion RE-IMPLEMENTS the rule and replays the core's vectors; the advisory lane IMPORTS the core. **Recommended.**

The alternative is the one that makes *"one rule"* literal: have
`test_floor_snapshot.py` import `evaluate_floor_completeness` from the pinned
core, which `pytest-suite.yml` already checks out beside the tree and which
`locate_pinned_core()` already finds. It is rejected on a measurement, not a
preference.

**The pinned core checkout in `pytest-suite.yml` carries `continue-on-error:
true`, and that is deliberate and already reasoned.** The module's own assertion
says why: *"the core checkout must NOT be able to fail this required job
directly: a required check that fails for reasons the candidate cannot fix
blocks everything."* So on any run where the cross-repository fetch fails — a
revoked App grant, a codexFactory outage, a rewritten history — an IMPORTING
assertion has exactly two available behaviours, and this repository has already
refused both by name:

1. **skip** — the BLOCKING assertion silently stops blocking on an outage. That
   is the CSC-F16 silent-false-green species, inside the guard against CSC-F16;
   or
2. **fail** — a required check red for a reason no candidate can fix, which
   `pytest-suite.yml`'s own rule forbids.

Today the coverage assertion survives an outage because it reads only the
vendored snapshot and `git ls-files`; the module states that property as load
bearing — *"the coverage assertion above keeps holding from the snapshot
throughout, so an outage never wedges the repository."* Importing would spend
it.

**So the mirror is local, and the FALSIFIER is foreign.** The core exports its
rule as replayable vectors for exactly this purpose, and its README expects this
change to use them: *"The openxFactory companion `mirror-floor-addition-grace`
is expected to replay the same file, read from the pinned core checkout, so a
divergence between the two lanes shows up as a failing vector rather than as a
contradictory verdict on somebody's pull request."* The replay is then the part
that may skip, and its skip is watched BY NAME in the JUnit report exactly as
`test_the_snapshot_is_byte_identical_to_the_pinned_core`'s already is — the
Codex P2 fix from PR #569, reused rather than reinvented — with `EXPECT_SKIPPED`
moving 21 → 22 in the same act.

**The advisory lane is the opposite case and takes the opposite answer.** Step 8
already treats an unreadable core as FATAL (*"Decision core unreadable"*, `exit
1`), because evaluating the floor is the whole of what it does. It has nothing
to lose by importing and everything to lose by keeping a second copy of the
classification — so it imports `evaluate_floor_completeness` and deletes its
hand-rolled `sorted(set(tracked) - set(floor.never_clearable_paths))`.

**The sub-decision inside A, also put for veto: the vectors are READ FROM THE
PINNED CORE CHECKOUT, not vendored.** Vendoring them as a second byte witness
beside `contracts/review-lane-floor-snapshot.yaml`, with its own `sha256` in the
pin, would make the replay unskippable — but it adds a SIXTH site to a lockstep
the pin file already describes as *"five sites name this one now, up from
three"*, for a TEST FIXTURE rather than for a governance document. The snapshot
is vendored because a BLOCKING assertion must run offline; the replay is a
consistency check between two lanes and can legitimately skip-and-be-watched.
Recommended: read from the checkout. Named so the cheaper-looking option is not
mistaken for the unconsidered one.

### B — a NEW capability, `review-lane-floor-mirror`, rather than an existing one. **Recommended.**

Two existing capabilities were examined and both were rejected with grounds:

* **`neutral-product-pin`** governs openxFactory's consumption of an external
  neutral PRODUCT, pinned by commit plus per-file digests, in the
  `kind: pinned_contract_manifest` shape. `contracts/review-lane-pin.yaml`
  DELIBERATELY is not that: it declares `kind: pinned_workflow` and states the
  reason on its own face — *"This pins EXECUTABLE GOVERNANCE CODE consumed by a
  workflow — no bundle, no digest set … Reusing `pinned_contract_manifest` would
  have claimed a digest discipline this pin does not have and cannot have."*
  Filing these requirements under that capability would contradict the pin
  file's own reasoning in the capability that governs it.
* **`release-surface-integrity`** governs the declared contract bundle against
  its release digest inventory. Nothing here touches a bundle, an inventory or a
  cut.

The name was chosen over `pinned-decision-core`, `foreign-gate-rule-mirror` and
`gate-floor-mirroring` for findability: `review-lane` is this repository's
established vocabulary for this surface — `contracts/review-lane-pin.yaml`,
`contracts/review-lane-floor-snapshot.yaml`, `tests/review_lane_pin/` — and a
capability nobody can grep for is a capability nobody reads. Alternative names
are a live veto.

### C — the advisory lane's base checkout goes to `fetch-depth: 0`. **Recommended, with the cost stated.**

Measured on this branch, 2026-09-05: openxFactory `main` is **2,025 commits**
and the packed history is **29.6 MiB**. That is what a full-history base
checkout costs the advisory lane per run, against a `checkout` step that today
fetches one commit. It is a real cost and it is small in absolute terms.

The alternative is a TARGETED fetch — deepen the base branch only as far as the
declared `generated_at` — which is cheaper and is strictly more fragile: the
depth needed is a property of how stale the pin is, so a targeted fetch that was
sufficient last week fails silently into the fail-safe this week, and the lane
would then report `uncovered` for a bystander's path with no visible cause. Both
are permitted by requirement 5, which requires only that the depth be a
DECLARED choice carrying its cost. `fetch-depth: 0` is recommended because it
makes the measurement's availability independent of the pin's age; the targeted
fetch is recorded as the option a reviewer may prefer on cost.

### D — `sequenced_after: [codexFactory:add-floor-addition-grace]`, the first CROSS-REPOSITORY declaration in this corpus. **Recommended.**

The house grammar CAN express it. `scripts/sequenced_after.py` accepts
`<repository>:<change-id>`, and a QUALIFIED FOREIGN entry is checked for
well-formedness only — *"the neutral validator cannot read another repository's
corpus and MUST NOT pretend to. Its DISPOSITION is the consumer's, which refuses
it under a named identifier rather than skipping it — skipping would fabricate a
root out of a declaration that says the opposite."* Measured on this branch:
three changes in the corpus declare the field and ALL THREE declare bare local
parents, so this is the corpus's first foreign entry and is flagged as one.

The alternative was to declare nothing and state the dependency in prose plus
`.openspec.yaml` `related:`. Rejected: the dependency is the packet's central
sequencing fact, the grammar exists precisely to make such a fact machine
readable, and the field is FROZEN between ratification and archive — so
declaring it is a commitment rather than decoration. The prose statement is kept
as well, in requirement 6 and in § What Changes, because a foreign entry
resolves for no validator and a reader must be able to see what it means.

### E — the two negative controls MOVE onto the graced expression rather than being deleted or exempted. **Recommended.**

`test_the_unmutated_surface_is_a_positive_first` and
`test_a_fabricated_off_floor_spec_path_is_refused` both call the module's shared
`uncovered()` and both fail by construction whenever the coverage assertion
fails — which is exactly why the 2026-09-04 14:05 pin note records LQ-A7
reddening *"in THREE places"*. Under the grace they must drive the SAME graced
expression the assertion drives, or the controls would falsify a rule that no
longer ships. The fabricated-path control keeps its meaning UNCHANGED and gains
force: its fabricated path is created by no diff and lies in no pin window, so
it stays refused, and that scenario is written into the delta explicitly so the
grace cannot be misread as *"additions are free."* Deleting or exempting either
control was rejected: a control that never runs proves nothing, which is the
module's own stated rule for its first-tier ordering guard.

### F — this packet performs NO regeneration and proposes NO tolerance value. **Recommended.**

Requirement 6 states the landed-pin obligation and tasks name the regeneration,
but the act itself is a later, separately claimed one — and it belongs to
whoever runs codexFactory's generator, which is not this repository. Likewise
the D-3 tolerance: codexFactory ratified the MECHANISM and explicitly left the
NUMBER open, its realization shipped `3` for veto in codexFactory's own
document, and this repository reads the field through the core rather than
declaring one of its own. Proposing a number here would be this repository
legislating in another's CODEOWNERS-routed file.

## Impact

- **Nothing lands green-by-itself.** The mirror is INERT until the pin advances,
  and the pin advance is inert in the required lane until the mirror lands. Both
  are stated without hedging, in the same terms the codexFactory packet used
  about itself.
- **The floor does not move.** No entry is added, removed or reordered; a graced
  path never becomes an entry; `never_clearable_paths`, `matching_paths` and the
  floor's restrictive direction are untouched.
- **The witnesses do not move.** `floor_snapshot.sha256` and
  `floor_snapshot.entry_count` change ONLY as a consequence of the pin advance
  re-copying the document at the new `core_commit`, which is the existing
  refresh procedure and not a new discipline.
- **One required-suite bookkeeping value moves**: `EXPECT_SKIPPED` 21 → 22, with
  the new skip's reason recorded beside it and its testcase watched by name —
  the discipline PR #569 established, applied a second time rather than
  loosened.
- **It discharges nothing else.** CSC-C6's required-check home, LA-C1's ordering
  condition, `add-substantive-review-lane` task 3.2 and task 5.1's ruleset half,
  and the `add-wallet-carried-review-authority` residue are all untouched and
  must not be cited as affected by this change.
