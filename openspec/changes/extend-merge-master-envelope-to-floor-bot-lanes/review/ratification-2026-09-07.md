# Proposal Ratification: extend-merge-master-envelope-to-floor-bot-lanes

Status: record

Decision date: 2026-09-07

Ratifier: Brett Heap (openxFactory repository owner) — in session, lane
`openXfactory-2`, session `de9d8fd4`, recorded on openxFactory issue
[#745](https://github.com/opensoft/openxFactory/issues/745) at
**2026-09-07T12:32:44Z**, the comment beginning "RULING — RATIFIED AS
RECOMMENDED" and stating its own ruling time as 2026-09-07T12:32Z. The same
ruling is posted on PR #746, on codexFactory #272 and on codexFactory #232.

Ratified verbatim: **"ratify 746 and 272 as recommended when green, then land
them"** — Brett Heap, 2026-09-07T12:32Z, in session. **It is a PAIR WORD**: it
ratifies this packet and its codexFactory companion
`extend-merge-master-envelope-to-floor-bot-lanes` (codexFactory PR #272, head
`8f601982`, record
`openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/review/ratification-2026-09-07.md`
in that repository) in one act, and each repository records it separately in its
own review directory.

**THE WORD WAS CONDITIONAL AND THE CONDITION WAS MET, WHICH IS RECORDED RATHER
THAN ASSUMED.** "When green" was satisfied before the word was given: the ruling
comment applies it at head `6ebd7b24` with **all nine checks green** —
`pytest-suite`, `merge-master-approval`, `lane-line`, `openspec-cli-pin`,
`openreposhape-pin`, `wallet-validation`, `signed-execution-chain-gate`,
`clearing-dispatch-gate`, `release-tag-gate` — and **zero open review threads**
(four Copilot rounds across the pair, every thread replied and resolved).

## What is ratified

The proposal as written at `6ebd7b24`, and **decisions N-1 through N-5 STAND AS
RECOMMENDED** with no veto exercised:

- **N-1 — SCOPE: the codexFactory REGENERATION lane only.** The openxFactory
  re-pin lane is NOT admitted.
- **N-2** — admission conditions are the envelope members the schema and pinned
  core already carry, measured off observed bot pull requests; no diff-shape
  condition is declared, because the envelope has none.
- **N-3** — the default-branch-head ordering property is recorded as a
  requirement and NO new mechanism is added.
- **N-4** — the existing sticky comment is extended; the candidate entry itself
  is the one-edit kill switch.
- **N-5** — the codexFactory companion carries the code surface; this half
  carries the rules and no code.
- **OQ-2 / OQ-C1** — the admitting act is **recommended as a Gate-Rules Council
  record** rather than an operator word.

Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`tests/sequenced_after/corpus-ledger.yaml`'s row, this record, and the two spec
deltas: `specs/roles-authority-model/spec.md` carrying **5** `### Requirement:`
and **10** `#### Scenario:`, and `specs/review-lane-floor-mirror/spec.md`
carrying **3** and **7** (measured by `grep -c` against the deltas at this
commit), each with exactly ONE `## ADDED Requirements` heading and **no**
`## MODIFIED Requirements` or `## REMOVED Requirements` block anywhere.

**NOTHING IN THE SPEC DELTAS, THE DESIGN OR THE TASKS CHANGES BETWEEN THE HEAD
THE RULING WAS GIVEN OVER (`6ebd7b24`) AND THIS COMMIT**, stated first rather
than left to a diff, and verified mechanically rather than asserted:
`git diff 6ebd7b24 -- openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/specs/
openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/design.md
openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/tasks.md` is
EMPTY at this commit. No requirement, no scenario, no design line and no task
line moves in the ratifying commit.

What DOES change here is `proposal.md` (the `Status:` / `Ratified:` headers and
the dated note), `README.md` (the OpenSpec Records entry's standing),
`.openspec.yaml` (the kept-and-answered `approved_by` statement), and this new
record. **This differs by ONE FILE from the archived `mirror-floor-addition-grace`
precedent, which took its `.openspec.yaml` statement in a separate later commit;
this commit takes it here, exactly as `mirror-floor-regeneration-automation` did
on 2026-09-06. The difference is named rather than papered over with a sentence
that would not be true of this commit.**

## What is NOT ratified, and what this performs

- **NO REALIZATION.** No candidate class is enrolled, no
  `.github/merge-approval-envelope.yml` is edited in either repository, no floor
  path moves, no ruleset changes, no auto-merge is armed, and **every box in
  `tasks.md` remains unticked.** Realization is a separate later word.
- **The alternatives N-1 (d) and N-1 (e) are NOT taken**, and neither is
  foreclosed. (d) status quo and (e) — satisfy `Bounded autonomous surface` as
  written by moving the machine-generated block off the code-owner-gated surface
  — remain on the record; (e) is the successor to file if the narrowing is later
  refused.
- **The openxFactory re-pin lane stays under a HUMAN MERGE WORD.** It is refused
  by `.github/workflows/merge-master-approval.yml`'s floor composition before any
  envelope decides, and nothing here changes that.
- **The admitting act is NOT performed.** OQ-2 / OQ-C1 recommend a Gate-Rules
  Council record for it; no council has convened and no envelope has been
  widened.
- **The § 5.3 enabling act is NOT performed.** `Require Code Owner Review` is
  still ACTIVE in both repositories with no bypass actor added.

## The catch-up merge

The catch-up merge of `origin/main` (`d5a549e4`) is carried in the same act. It
brought **no conflict** and no README OpenSpec Records collision: main's single
commit was PR #747, a `review-lane-repin-bot` advance of the pinned decision core
to codexFactory `aced582b`, touching only
`.github/workflows/merge-master-approval.yml`,
`.github/workflows/pytest-suite.yml`, `contracts/review-lane-floor-snapshot.yaml`
and `contracts/review-lane-pin.yaml`. It added no change directory, so **the
per-change sweep ledger needed no re-seeding**:
`python3 scripts/validate-sequenced-after.py --ledger-diff` reports "per-change
sweep ledger consistent with the corpus (179 rows)" after the merge, with this
change's row intact at `moved_by: "#745"`, `moved_on: "2026-09-07"`, `depth: 2`.
`python3 -m pytest tests/sequenced_after -q` reports **163 passed** after the
merge.

It is worth recording what that merge is: **the bot lane this packet proposes to
enrol landed a pull request on `main` during the ratification of the packet about
it, and a human clicked merge to do so.** That is the cost N-1 measures,
observed once more on the day the word was given.

## Landing order

This packet declares `sequenced_after: [mirror-floor-regeneration-automation,
codexFactory:add-floor-regeneration-automation, add-substantive-review-lane]`;
the codexFactory companion declares `sequenced_after:
[add-regular-pr-council-clearance, add-floor-regeneration-automation]`. **NEITHER
NAMES THE OTHER**, and nothing in either half depends on the other having landed:
this half changes only `openspec/specs/` deltas and repository bookkeeping, and
the companion's `## MODIFIED` block is measured against codexFactory canon and
reads nothing from this repository. The two may land in either order.

## Records

- Governing issue: openxFactory
  [#745](https://github.com/opensoft/openxFactory/issues/745) — the § 6.3
  proposal claim, and the ruling comment.
- Origin record: codexFactory
  [#232](https://github.com/opensoft/codexFactory/issues/232) — the option-(b)
  governing issue and the first-cycle record.
- The deferred boxes this packet answers:
  `openspec/changes/mirror-floor-regeneration-automation/tasks.md` § 6.3 and
  codexFactory `openspec/changes/add-floor-regeneration-automation/tasks.md`
  § 6.3.
- Companion: codexFactory
  [#272](https://github.com/opensoft/codexFactory/pull/272), head `8f601982`.
- This packet's pull request: openxFactory
  [#746](https://github.com/opensoft/openxFactory/pull/746).
