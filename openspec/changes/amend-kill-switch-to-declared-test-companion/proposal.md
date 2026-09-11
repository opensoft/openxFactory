---
code_surface: openxFactory's half of this packet carries NO CODE — its rules land as text (a `## MODIFIED` requirement delta, a design record and a task list), and no byte under `.github/`, `scripts/` or `contracts/` moves in this repository by this pull request. No test implementation or runtime code moves either: the only file under `tests/` this pull request touches is the machine-derived per-change sweep ledger `tests/sequenced_after/corpus-ledger.yaml`, whose two rows this filing moves by construction (its own row, and the parent's `sole` → `co-modifier` flip), seeded by `scripts/validate-sequenced-after.py --seed-ledger --moved-by '#959'`. THE REALIZATION IS A codexFactory COMPANION CHANGE, authored THERE by that repository's own lane after ratification, and it is TWO surfaces and not more: (1) `.github/merge-approval-envelope.yml`'s BANNER/COMMENT BLOCK beside EACH ENROLLED CANDIDATE CLASS — today TWO, `codexfactory-routine-code` and `openxfactory-floor-regeneration`, because the requirement binds every enrolment and nothing is grandfathered — where the false "takes one edit" sentence is corrected and each candidate's DECLARED TEST COMPANION is named as `# companion:` / `# companion-artefact:` comment lines beside it, which is a comment-only edit and therefore NO SCHEMA CHANGE; (2) ONE conformance test in codexFactory running, PER ENROLLED CLASS, the FIVE-STEP PROCEDURE `tasks.md` § 3.2 fixes in order — capture the declarations from the pre-withdrawal envelope, commit the withdrawal of that class alone as the baseline, measure the assertions over the WHOLE pinning suite with the conformance module excluded by its own path, regenerate EVERY allowlisted artefact and diff against the baseline, record — and asserting TWO EQUALITIES — that the declared companion ASSERTIONS equal the set that actually pin that enrolment, and that the declared companion ARTEFACTS equal the set of paths reported changed by regenerating EVERY ARTEFACT IN THE ALLOWLIST TABLE — the whole table, not only the entries the declaration names — through ITS OWN `regenerate:` IDENTIFIER — an ALLOWLISTED TOKEN resolved to a fixed argv only in the trusted, code-owner-reviewed test module and never a command carried in the pull-request-editable declaration — with both equalities taken against a COMMITTED POST-WITHDRAWAL BASELINE and the measured assertion set required to be NON-EMPTY, no more and no less; so artefact movement is MEASURED rather than inferred from the failing node ids or from an existence check, and the declaration cannot go stale silently nor pass vacuously on an enrolment that nothing pins. NOT THIS PACKET'S SURFACE, each for a stated reason: the envelope's `openxfactory-floor-regeneration` CANDIDATE MAPPING itself is untouched — this packet amends the ACCOUNT of the switch, never throws it, and the entry is INTACT on codexFactory `main` (blob `fa8773628ef69dceab3a912740850c0432ffbce3`, 356 lines); NO RULESET IS EDITED BY ANY AGENT and NO BYPASS ACTOR IS PROPOSED IN ANY FORM; no schema member is added and `active:` is refused again exactly as N-4 refused it; no repository variable is introduced, for N-4's own reason (invisible in the diff); `scripts/` and `contracts/` do not move in either repository; and THIS LANE AUTHORS NO codexFactory BYTE — the split is the same one `extend-merge-master-envelope-to-floor-bot-lanes` made.
target_release: a code surface (in codexFactory), so per `release-realization` this packet archives ONLY on merged + green realization evidence, and the evidence is the codexFactory companion landed with that repository's required `validate` check green — `tests/merge-master/` included — plus the new conformance test passing against the declared companion. No contract bundle is cut, nothing under `contracts/` moves, no `contract_bundle_version` is spent, no openxFactory CONTRACT digest set moves and NO RELEASE TAG IS OWED (the codexFactory BEHAVIOUR-SNAPSHOT digest is a different artefact entirely: it is a DECLARED COMPANION ARTEFACT and it DOES move, in THAT repository, at the throw and again at the restore, by the companion realization — that movement is the point of design.md D-3, not an exception to this sentence). The parent's box 3.6 OBSERVATION is a further and separate thing this packet does not claim as its own archive evidence: it needs a real bot cycle, which does not exist today (hourly floor-regeneration has reported "nothing owed" since 2026-09-10T17:22Z) and which no agent may manufacture (the class pins `expected_author: openxfactory[bot]`).
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

**Two things in that set are not ordinary code**, and this is why the answer is a
DECLARATION rather than a loosening:

1. the **golden behaviour digest** — every movement of it is individually
   reasoned in `test_behaviour_snapshot.py`, where this enrolment is recorded as
   "the SIXTH movement"; and
2. `test_S_the_kill_switch_is_not_held_outside_the_diff`, in
   `test_floor_regeneration_enrolment.py` — the **scenario test for this very
   requirement**, asserting that the switch IS the reviewed declaration. It
   fails on the throw only because it looks the entry up by id. A scenario
   test that reds when its own scenario is exercised is the sharpest possible
   statement of the gap.

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
- a **SHALL** that the conformance test asserts BOTH equalities, each taken
  against the **declaration captured before the withdrawal** in a **committed
  post-withdrawal baseline** — the captured assertions against the set that
  actually pin the enrolment, measured by running THE COMPLETE PINNING SUITE
  WITH THE CONFORMANCE MODULE EXCLUDED BY ITS OWN PATH, and the captured
  artefacts against the paths that regenerating EVERY ALLOWLISTED ARTEFACT
  rewrites — **NEITHER MEASURED SET DRAWN FROM THE DECLARATION IT IS COMPARED
  AGAINST**, so that what a declaration OMITS is still run, still measured and
  still caught — with a
  **SHALL NOT** on inferring an artefact's movement from the failing assertions
  or from an existence check, and a **SHALL NOT** on narrowing that diff to the
  declared paths, so a regenerated path no declaration names is still caught;
- a **SHALL** that each declared artefact is regenerated by an **allowlisted
  recording tool NAMED BY IDENTIFIER** in the declaration and **resolved only in
  reviewed test code**, with a **SHALL NOT** on the declaration carrying a
  command, an argument or any other executed text, and an identifier absent from
  the reviewed table failing the check rather than being executed — so a
  pull-request-editable declaration can never introduce execution into the
  required check;
- a **SHALL NOT** on an enrolment whose withdrawal fails **NO** conformance
  assertion: the measured set for every enrolled class **SHALL be non-empty**,
  and an empty measured set is a failing check, never a vacuous pass on two
  empty sets — the enrolment nobody would notice leaving is refused;
- a **SHALL NOT** on a switch held in a value that does not appear in a
  reviewable diff (unchanged in force from the parent, restated);
- a **SHALL NOT** on an enrolment whose withdrawal, **with the declared
  companion applied and nothing else**, is not landable against the required
  checks — which is the measured defect, stated as a rule;
- the **amended** scenario "Withdrawing an enrolment", written to what is
  observable (no envelope decision, human merge gate, no comment);
- the restated and **BROADENED** scenario "A kill switch outside the diff" —
  the parent's "repository or environment setting" is widened to name
  secrets and any other value that does not appear in a reviewable diff;
- three **new** scenarios: "The companion is declared beside the declaration",
  "An undeclared companion is a finding against the enrolment" and "An enrolment
  nobody would notice leaving is refused".

**The widening, declared explicitly.** The parent refused a switch held in "a
repository or environment setting". This packet's restated scenario refuses a
switch held in "a repository variable, a secret, an environment setting or
any other value that does not appear in a reviewable diff" — SECRETS and a
general reviewable-diff catch-all are newly named, closing two gaps the
parent's enumeration left open. The requirement's own body paragraph already
carried this fuller enumeration (`not a repository or organization variable,
not a secret, not an environment setting, not a platform toggle, and not any
store whose change leaves no reviewable record`); the scenario is restated to
match it rather than left narrower than the requirement it tests.

**The per-change sweep ledger also moves.** This pull request carries two
bookkeeping rows in `tests/sequenced_after/corpus-ledger.yaml` — this
packet's own row, and the parent's `sole` → `co-modifier` flip — seeded by
`scripts/validate-sequenced-after.py --seed-ledger --moved-by '#959'`. They
carry no requirement and no grant.

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
- No contract bundle, no tag, no pin movement, and **no openxFactory contract
  digest set, pin byte or `contract_bundle_version` movement IN THIS FILING**.
  This sentence is about openxFactory's contract digests and about this pull
  request. It is NOT a prohibition on the codexFactory BEHAVIOUR-SNAPSHOT digest
  (`specs/018-per-tree-floor-instance/behaviour-snapshot.json`), which is a
  DECLARED COMPANION ARTEFACT and **does** move — at the throw and again at the
  restore, in that repository, by the companion realization. That movement is
  the POINT of `design.md` D-3 and of § Impact's procedure, not an exception to
  this bullet.
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
3. **the restore** — a FORWARD change by the same procedure as the throw and
   NEVER a revert: the candidate entry and its companion comment lines re-added
   byte-identical, the declared assertions re-targeted back to the enrolled tree
   and the declared artefacts regenerated, so the entry and the companion return
   in one act AND the behaviour digest records the restore as a second movement
   beside the throw's (`design.md` D-3) rather than losing the throw's movement
   to a reverted patch;
4. **the second observation** — autonomous approval resumes on the following
   cycle.

**THE ARCHIVE IS BLOCKED PER ENROLLED CLASS, AND THIS PACKET GRANDFATHERS
NONE.** The amended requirement binds EVERY enrolled candidate class, so the
codexFactory companion declares a companion for every class enrolled in
`.github/merge-approval-envelope.yml` at realization time — today TWO,
`codexfactory-routine-code` and `openxfactory-floor-regeneration` — each
measured by the SAME FIVE-STEP PROCEDURE, in the order `tasks.md` § 3.2 fixes
and this packet states once there (capture the declarations, commit the
withdrawal as the baseline, measure the assertions over the whole pinning suite
with the conformance module excluded by its own path — a measured set that may
not be empty — regenerate every allowlisted artefact and diff against the
baseline, record), and
each with its own passing conformance test over BOTH equalities.
**This packet is NOT ARCHIVABLE while ANY enrolled candidate class lacks a
declared companion and a passing conformance test over both equalities**
(`tasks.md` § 5.1): green evidence for one class does not stand in for
another, and a class enrolled later by another change carries the same block.

**What is still owed and is NOT delivered by this packet:** a real bot cycle to
observe. None exists today, and none can be manufactured by hand. Consequence
(4) of the ruling states this exactly: *"3.6's observation resumes only after
that successor lands and a real bot cycle exists."* This packet removes the
first blocker only.

**On this repository:** no runtime impact whatsoever. openxFactory's half is
text.

**On codexFactory:** two comment-and-test surfaces at realization, named in
`code_surface` above, authored by that repository's lane.
