---
code_surface: openxFactory's half of this packet carries NO CODE — its rules land as text (a `## MODIFIED` requirement delta, a design record and a task list), and no byte under `.github/`, `scripts/` or `contracts/` moves in this repository by this pull request. No test implementation or runtime code moves either: the only file under `tests/` this pull request touches is the machine-derived per-change sweep ledger `tests/sequenced_after/corpus-ledger.yaml`, whose two rows this filing moves by construction (its own row, and the parent's `sole` → `co-modifier` flip), seeded by `scripts/validate-sequenced-after.py --seed-ledger --moved-by '#959'`. THE REALIZATION IS A codexFactory COMPANION CHANGE, authored THERE by that repository's own lane after ratification, and it is TWO surfaces and not more: (1) `.github/merge-approval-envelope.yml`'s BANNER/COMMENT BLOCK beside the `openxfactory-floor-regeneration` candidate — the false "takes one edit" sentence is corrected, and the candidate's DECLARED TEST COMPANION is named there (the exact files and the assertion each carries), which is a comment-only edit and therefore NO SCHEMA CHANGE; (2) ONE conformance test in codexFactory asserting that the declared companion EQUALS the set of assertions that actually pin the enrolment, so the declaration cannot go stale silently. NOT THIS PACKET'S SURFACE, each for a stated reason: the envelope's `openxfactory-floor-regeneration` CANDIDATE MAPPING itself is untouched — this packet amends the ACCOUNT of the switch, never throws it, and the entry is INTACT on codexFactory `main` (blob `fa8773628ef69dceab3a912740850c0432ffbce3`, 356 lines); NO RULESET IS EDITED BY ANY AGENT and NO BYPASS ACTOR IS PROPOSED IN ANY FORM; no schema member is added and `active:` is refused again exactly as N-4 refused it; no repository variable is introduced, for N-4's own reason (invisible in the diff); `scripts/` and `contracts/` do not move in either repository; and THIS LANE AUTHORS NO codexFactory BYTE — the split is the same one `extend-merge-master-envelope-to-floor-bot-lanes` made.
target_release: a code surface (in codexFactory), so per `release-realization` this packet archives ONLY on merged + green realization evidence, and the evidence is the codexFactory companion landed with that repository's required `validate` check green — `tests/merge-master/` included — plus the new conformance test passing against the declared companion. No contract bundle is cut, nothing under `contracts/` moves, no `contract_bundle_version` is spent, no digest set moves and NO RELEASE TAG IS OWED. The parent's box 3.6 OBSERVATION is a further and separate thing this packet does not claim as its own archive evidence: it needs a real bot cycle, which does not exist today (hourly floor-regeneration has reported "nothing owed" since 2026-09-10T17:22Z) and which no agent may manufacture (the class pins `expected_author: openxfactory[bot]`).
sequenced_after: [extend-merge-master-envelope-to-floor-bot-lanes]
---

# Proposal: amend-kill-switch-to-declared-test-companion

Status: draft
Proposed: 2026-09-11, in lane `openxfactory-2` (display `openXfactory-2`), on
Brett Heap's SELECTION **"Accept the finding; file a successor"**
(2026-09-11 ~03:40Z, in session, multi-choice; recorded on openxFactory #745
comment 5632569506
(https://github.com/opensoft/openxFactory/issues/745#issuecomment-5632569506,
2026-09-11T09:42:11Z) and codexFactory #232, 2026-09-11T09:42:12Z) —
**FILING ≠ RATIFYING.** This document is a PROPOSAL. It admits no text to
canon, ratifies no design decision, moves no byte in either repository, and
ticks no box anywhere. Ratification, realization and archive are three
further and separate acts on Brett Heap's word; none has been given.

## THIS FILING AMENDS A RATIFIED DECISION (N-4) BY SUPERSESSION, AND SAYS SO HERE

Decision **N-4** of `extend-merge-master-envelope-to-floor-bot-lanes`
(ratified 2026-09-07, PR #746; **not yet archived**) is amended here by
supersession, together with the requirement that decision carries,
**"An enrolled autonomous lane carries a one-edit kill switch"**.

N-4 reads, verbatim and as ratified:

> **The kill switch is the candidate entry.** Deleting it from
> `.github/merge-approval-envelope.yml` returns the lane to human merges,
> takes one edit, is a code-owner-reviewed act by construction, is read from
> the base branch so it takes effect on the next run, and is visible in the
> diff forever.

The clause **"takes one edit"** is measured false (§ Why). Everything else
N-4 decided stands and is re-affirmed by this packet: the switch IS the
candidate entry; a boolean `active:` member is still refused (it is a schema
change, and a disabled entry reads as enrolled); a repository variable is
still refused (invisible in the diff); the act is still code-owner-reviewed
by construction; it still takes effect on the next evaluation because the
envelope is read from the base branch; and it is still visible in the diff
forever.

**The amendment is therefore narrow and additive in substance:** the switch is
**one reviewed edit PLUS ITS DECLARED TEST COMPANION**. It is written as a
`## MODIFIED` and not as a `REMOVED` + `ADDED` pair, and the requirement
header is **unchanged**, because the requirement's subject, scope and
authority are unchanged — only its account of the act's shape is corrected.

Because the parent is ratified but **unarchived**, the requirement this packet
modifies is not yet in the promoted `openspec/specs/roles-authority-model/spec.md`:
it lives in the parent's own delta at
`openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/specs/roles-authority-model/spec.md`
lines 53–65. The `## MODIFIED` therefore targets a SIBLING'S ADDITION, which is
declared in the delta per `govern-sibling-added-modified-deltas` and recorded
in the front matter as `sequenced_after: [extend-merge-master-envelope-to-floor-bot-lanes]`.
This packet SHALL NOT archive before the parent promotes.

## Why

**The finding, measured 2026-09-11 and posted as the RESULT on openxFactory #745
at 03:08Z**
(https://github.com/opensoft/openxFactory/issues/745#issuecomment-5628853801),
with the ruling that accepts it recorded on #745 comment 5632569506 and
codexFactory #232. The figures below are quoted from that measurement and are
not re-derived here.

Measured in a throwaway clone at codexFactory `main` = `0ad92bd5`, with
`PYTHONPATH=scripts python3 -m pytest tests/merge-master/ -q`:

| tree | result |
| --- | --- |
| clean | **3993 passed, 28 skipped** |
| the one edit — delete envelope lines 173–356, the `openxfactory-floor-regeneration` mapping and nothing else (356 → 172 lines; the YAML still parses) | **29 failed, 3964 passed, 28 skipped** |

The 29 failures fall across **five test files**, plus a sixth file that must
move with them:

| file | failures |
| --- | --- |
| `tests/merge-master/test_floor_regeneration_enrolment.py` | 17 |
| `tests/merge-master/test_enrolled_surface_config.py` | 7 |
| `tests/merge-master/test_behaviour_snapshot.py` | 3 |
| `tests/merge-master/test_caller_workflows.py` | 1 |
| `tests/merge-master/test_class_floor_differential.py` | 1 |
| `specs/018-per-tree-floor-instance/behaviour-snapshot.json` (the golden digest) | — the sixth file, which must move for the three snapshot failures |

**Those tests are inside a REQUIRED check.** codexFactory's
`.github/workflows/validate.yml` runs `bash scripts/validate-docs.sh`, whose
line 217 lists `tests/merge-master/`. So the one edit does not merely fail a
local run: **the withdrawing pull request cannot land** on the repository's own
required checks. A kill switch that cannot be thrown is not a switch.

**The pinning is not the defect, and this packet says so plainly.**
`test_the_envelope_enrols_exactly_two_candidate_classes` asserts
`ids == ["codexfactory-routine-code", "openxfactory-floor-regeneration"]`. A
suite that did NOT notice the enrolment leaving would be strictly worse: the
notice-it-leaving property is the thing worth keeping. The defect is the **gap
between the suite and N-4's ratified account** — N-4 says "takes one edit", and
the act measurably takes one edit plus twenty-nine failing assertions across
five test files, plus a sixth file — the golden digest — that moves with
them, none of it declared.

**Two of the six files are not ordinary code**, and this is why the answer is a
DECLARATION rather than a loosening:

1. the **golden behaviour digest** — every movement of it is individually
   reasoned in `test_behaviour_snapshot.py`, where this enrolment is recorded as
   "the SIXTH movement"; and
2. `test_S_the_kill_switch_is_not_held_outside_the_diff` — the **scenario test
   for this very requirement**, asserting that the switch IS the reviewed
   declaration. It fails on the throw only because it looks the entry up by id.
   A scenario test that reds when its own scenario is exercised is the sharpest
   possible statement of the gap.

**What the measurement settles about the parent scenario's wording.**
`_find_surface` matches on repository AND head ref only — **never on author** —
so with the entry removed, ANY `floor/bot-regeneration` pull request returns
`is_candidate: false`, exit **11** (`_EXIT_NOT_CANDIDATE`), `decision=skip`, and
**no sticky comment** (the "Explain park or block" step is gated on
`decision == 'park'`). The parent scenario's "parks for a human" is therefore
NOT what is observable. What is observable is: **the pull request reaches no
envelope decision at all and stays at the human merge gate, with no comment.**
The amended scenario is written to what is observable.

**Context, not part of the finding.** No bot cycle exists to observe today —
hourly floor-regeneration has reported "nothing owed" since 2026-09-10T17:22Z —
and an APPROVE cannot be constructed by hand, because the class pins
`expected_author: openxfactory[bot]`. The candidate entry is **INTACT** on
codexFactory `main` (blob `fa8773628ef69dceab3a912740850c0432ffbce3`, 356 lines):
nothing has been thrown, and this packet throws nothing.

## What changes

**One requirement, by supersession, with its header unchanged:**
`### Requirement: An enrolled autonomous lane carries a one-edit kill switch`.

N-4's amended statement, in substance:

> **The kill switch is the candidate entry TOGETHER WITH ITS DECLARED TEST
> COMPANION.** Returning an enrolled lane to human merges is ONE REVIEWED EDIT
> to the enrolment declaration PLUS the companion set of conformance assertions
> that pin that enrolment — a set DECLARED beside the enrolment, in the reviewed
> declaration itself, so that the withdrawing pull request is landable against
> the repository's required checks and the companion is itself diff-visible and
> reviewed. It remains a code-owner-reviewed act by construction, remains read
> from the base branch so it takes effect on the next evaluation, and remains
> visible in the diff forever.

The requirement gains, in the delta:

- a **SHALL** that a withdrawal is the declaration edit together with its
  declared companion, taking effect on the next evaluation with no redeploy and
  no lane reconfiguration;
- a **SHALL NOT** on a switch held in a value that does not appear in a
  reviewable diff (unchanged in force from the parent, restated);
- a **SHALL NOT** on an enrolment whose withdrawal, **with the declared
  companion applied and nothing else**, is not landable against the required
  checks — which is the measured defect, stated as a rule;
- the **amended** scenario "Withdrawing an enrolment", written to what is
  observable (no envelope decision, human merge gate, no comment);
- the **unchanged** scenario "A kill switch outside the diff";
- two **new** scenarios: "The companion is declared beside the declaration" and
  "An undeclared companion is a finding against the enrolment".

Every parent scenario's intent is kept. Nothing is silently dropped.

## What does NOT change

- **The switch is still the candidate entry.** The declaration site does not
  move, and no indirection is introduced.
- **No schema change.** The companion is declared in the envelope's own
  banner/comment block beside the candidate. `active:` stays refused for N-4's
  own reason — it is a schema change, and a disabled entry reads as enrolled.
- **No repository variable**, for N-4's own reason: invisible in the diff.
- **The enrolment itself is untouched.** `openxfactory-floor-regeneration` stays
  enrolled; `codexfactory-routine-code` stays enrolled; the entry is not thrown,
  narrowed, widened or moved by this packet.
- **The pinning suite keeps the notice-it-leaving property.** No assertion is
  relaxed and no test is taught to read the enrolment out of the envelope.
- **The requirement header is unchanged**, and so is the capability it lives in
  (`roles-authority-model`).
- **The parent's other decisions (N-1, N-2, N-3, …) are untouched**, as are its
  other requirements.
- **The parent's box 3.6 stays OPEN.** It is an OBSERVATION box, not an
  owed-successor box: it does **not** tick on this packet being named, and this
  pull request ticks no box anywhere.

## What is NOT proposed

- No throw of the kill switch, in either repository, by anyone, now.
- No edit to `.github/merge-approval-envelope.yml`'s candidate MAPPING.
- No schema member, no `active:` boolean, no repository variable, no
  environment-held value.
- No ruleset edit and no bypass actor in any form.
- No codexFactory byte authored by this lane — the realization is for that
  repository's lane to author, after ratification.
- No relaxation of any conformance assertion, and no rewrite of the pinning
  suite to read the enrolment from the envelope (alternative (B); rejected in
  `design.md` D-1, because a suite that adapts to the entry leaving no longer
  notices it leaving).
- No contract bundle, no tag, no pin movement, no digest movement.
- No tick of the parent's box 3.6, here or anywhere, by this pull request.

## Impact

**On the parent's box 3.6**, which is the reason this packet exists: with the
amendment ratified and the codexFactory companion realized, the observation
becomes performable, because the throw becomes **landable**. The procedure
becomes:

1. **the throw** — ONE codexFactory pull request carrying the candidate entry's
   removal **together with exactly the declared companion**, which passes that
   repository's required checks and therefore lands;
2. **the observation** — the next real bot pull request of that class reaches no
   envelope decision (exit 11, `decision=skip`, no sticky comment) and stays at
   the human merge gate;
3. **the restore** — a revert of that same pull request, which restores the entry
   and the companion assertions in one act;
4. **the second observation** — autonomous approval resumes on the following
   cycle.

**What is still owed and is NOT delivered by this packet:** a real bot cycle to
observe. None exists today, and none can be manufactured by hand. Consequence
(4) of the ruling states this exactly: *"3.6's observation resumes only after
that successor lands and a real bot cycle exists."* This packet removes the
first blocker only.

**On this repository:** no runtime impact whatsoever. openxFactory's half is
text.

**On codexFactory:** two comment-and-test surfaces at realization, named in
`code_surface` above, authored by that repository's lane.
