# Proposal Ratification: report-stale-grandfather-dispositions

Status: ratified
Kind: report
Decision date: 2026-09-12
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-12 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), a MULTIPLE-CHOICE ruling over
`design.md` D1 with the recommendation presented first: verbatim **"do all as
recomended"**, given in the lane's window in answer to the orchestrator's list
of open rulings (each put with its recommendation first) and recorded on
openxFactory PR
[#981](https://github.com/opensoft/openxFactory/pull/981#issuecomment-5646922774)
at **2026-09-12T15:45:22Z** (comment `5646922774`; mirrored on openxFactory
issue [#965](https://github.com/opensoft/openxFactory/issues/965#issuecomment-5646922894)
at **2026-09-12T15:45:23Z**, comment `5646922894`). **THIS IS THE OPTION THE
PACKET HAD ALREADY ENCODED, SO THE WORDING STANDS UNCHANGED AND NOTHING WAS
SUBSTITUTED, RESTORED OR DELETED.**

Every timestamp in this file is UTC, as `proposed_on`, `created` and the
commissioning word of ~18:20Z are.

## 1. The two words, and exactly what each decided

**THE COMMISSIONING WORD IS NOT AN APPROVAL AND IS NOT READ AS ONE.** Brett
Heap's word of 2026-09-11 at approximately 18:20Z, verbatim *"usage reset,
resume all. read handoff and resume and fan out wide and do as much as
possible in parallel"*, given to session `c44b04` (team-01f), commissioned the
AUTHORING. It named no wording, resolved none of the packet's nine decisions
and admitted no text to canon. `.openspec.yaml`'s `origin:` block was authored
under it in the lawful unapproved shape `add-drafted-proposal-origin` (issue
#318) defined — `proposed_by` + `proposed_on`, no approval pair — and **that
block is kept byte-unmoved by this ratification**: `git diff --numstat` on
`.openspec.yaml` for this commit reads `43 0`, and lines 1–86 hash to sha256
`82b5b028159508f0c1f7ee9fa3bba417b71aebf4e8006d4e92762ffce7c78326` before and
after.

**THE RATIFYING WORD IS THE SECOND ONE, AND IT IS SHORT**: *"do all as
recomended"*, given at **2026-09-12T15:45:22Z** in answer to the orchestrator's
list of every open ruling across this lane's live packets, each put with its
recommendation first — recorded on this pull request at that same instant
(comment `5646922774`) and mirrored on the origin issue one second later
(comment `5646922894`). Applied to this packet, and quoted from the recording
comment:

> **D1 = option 1** — a STALE grandfather disposition is a PRUNE PROMPT: the
> new finding class (as the frozen packet at `f742c090` names it) at severity
> `warning`, reported against the aggregation's `health/dispositions.yaml` row
> with the entry's target path and cite, action "prune the entry or re-point
> it". Options 2 (info as repair residue) and 3 (error as aggregation defect)
> are NOT taken.
>
> Encode follows: `Status: ratified` + records + approval pair inside
> `origin:`, ready-for-review, bench, FREEZE, land on green; archive ONLY on
> realization evidence at canon's grain (code surface).

It is Brett Heap's act and not the authoring lane's. What it moves is recorded
in § 3.

## 2. What the ruling was given over

**THE WORD WAS GIVEN OVER THE PACKET AS IT STOOD AT `f742c090`**, the FREEZE
head this pull request had carried, untouched, since 2026-09-11 — the FREEZE
comment on this pull request records 0 unresolved review threads, fifteen
Copilot rounds all dispositioned, and one Codex request answered by a
usage-limit absence, at that same head. **BETWEEN THAT HEAD AND THIS
RATIFICATION THE PACKET MOVED ONCE, AND THAT COMMIT DOES NOT TOUCH THE
DELTA**: `d4ccd285`, a merge of `origin/main` `1f068646` (this lane's own act,
performed before the encode, per the brief governing this pass) —
`git diff --name-only f742c090 -- openspec/changes/report-stale-grandfather-dispositions/specs/`
returns **0 files**, which is the mechanical form of *the wording stands
unchanged*.

## 3. D1, and the eight carried decisions

**D1 — THE BAND — IS RULED OPTION 1, "A PRUNE PROMPT"**, the RECOMMENDED
option, against option 2 (the expected residue of a repair, graded `info`, no
action) and option 3 (an aggregation defect, at `error`).

A stale entry is reported at **`warning`**, against the AGGREGATION's own
`health/dispositions.yaml` — the file the entry is a line of — naming the
entry's repository and path and quoting the ruling it records, with the action
*"prune the entry, or re-point it at the record that still carries the
defect"*. **THE RULED OPTION IS THE ONE ALREADY ENCODED, SO THE RULING IS
APPLIED BY LEAVING THE ARM ALONE**: this record re-read
`scripts/doc_health/families.py`'s `_stale_grandfather_dispositions` (and its
four constants, `_AGGREGATION_REPO`, `_DISPOSITIONS_REL`, `_STALE_RULE_PREFIX`,
`_STALE_ACTION`) at this ratification and confirms, byte for byte against
`design.md`'s option 1 text, that severity, subject (`repo="xFactory"`,
`path="health/dispositions.yaml"`), message shape (naming the entry's own
target) and action text all match the ruled option exactly — no fix, no
re-author, no test re-measurement was needed or performed. Options 2 and 3
were put with their own cost in `design.md` and are retained there as the
record of what was declined, not as work owed.

**D0 AND D2, D2a, D2b, D3, D4 AND D5 WERE CARRIED BESIDE D1 AND NONE WAS
VETOED** — SEVEN more, so the packet took nine decisions in all and the ruling
reached exactly one of them (D6 is the sibling search, not itself vetoable):

- **D0 — the measurement taken before the design.** `health/dispositions.yaml`
  at `opensoft/xFactory` `main` `0ecb370e` carries 18 `family:
  ratified-provenance` entries; **15 match a live finding, 3 match nothing** —
  all three from codexFactory, all three stale by REPAIR, zero by a vanished
  path — a split re-measured identically three times across moving pins
  (`b91af6ea`/`2dd4e5a3`; `8015d45f`/`dc67ad82`; `c521504c`/`c3108adc`), the
  aggregation itself byte-unmoved at `0ecb370e` throughout.
- **D2** — the arm is a SECOND AND FINAL grandfather-disposition pass, run
  AFTER the downgrade and appended to its result; it takes the entries
  `_grandfather_cites` honours minus the `(repo, path)` keys the downgrade
  matched; a repository this run did not read is passed over rather than
  called stale on a measurement never taken; a `--single-repo` run (no
  aggregation root) reports nothing of this class; the row lands on the
  dispositions file itself, under repository id `xFactory`; the resolution
  class stays `auto-fixable` (a `contested` row would arm
  `report.uncited_resolutions` and turn the good act of pruning into a manufactured
  error); one row per honoured target, keyed the same way the downgrade's own
  `cites.setdefault` already resolves a duplicate.
- **D2a** — the archived-path boundary belongs to the FINDING the downgrade
  moves, not to the entry this pass reads; an entry over a CLEAN active path
  is reported stale (it reaches nothing and never will), while an entry over
  an active path whose finding still stands is not (raised by Copilot on PR
  #981, taken as a named decision with its own two tests).
- **D2b** — the in-scope set is the repositories that contributed to this
  family's own document scan (the governed corpus UNION the lifecycle scan
  set), not `ctx.repo_paths`: the aggregation's `openxFactory` anchor is
  admitted on `is_dir()` alone, so an unmaterialized pin would otherwise call
  all fifteen openxFactory entries stale on a checkout nobody read — measured
  as fifteen false rows under the wrong reading and zero under this one
  (raised by Copilot on PR #981, taken as a code change, the one item of that
  round that was).
- **D3** — the tests extend the parent's own rig,
  `tests/doc-health/test_grandfather_dispositions.py`, rather than opening a
  second file for one mechanism; 23 → 40 test functions (seventeen net new:
  eighteen added, one renamed).
- **D4** — `code_surface` is non-empty, so the archive waits for
  merged-plus-green realization evidence at canon's grain rather than landing
  with this packet.
- **D5** — this packet rules `ratified-provenance`'s entries alone; the other
  eight families' 31 entries are openxFactory
  [#966](https://github.com/opensoft/openxFactory/issues/966)'s subject, whose
  own packet (PR [#978](https://github.com/opensoft/openxFactory/pull/978),
  DRAFT) writes a disjoint requirement, so `sequenced_after: []` stands.

## 4. The bench, as it stood at the ruling

**AS OF THE HEAD THIS WORD WAS GIVEN OVER (`f742c090`), THE FREEZE COMMENT ON
THIS PULL REQUEST IS THE RECORD**: 0 unresolved review threads (GraphQL
`reviewThreads` `totalCount: 4`, all `isResolved: true`); fifteen Copilot
reviews, opening four threads in total, every one dispositioned (rounds
eleven through fourteen carried findings this pass answered — a possessive
grammar defect in five files, an imprecise `sequenced_after: []` claim, and two
design.md sentences reusing a neighbour's phrase differently — round fifteen,
on that same head, carried nothing); one Codex review request, answered within
seconds by a usage-limit absence (*"You have reached your Codex usage limits
for code reviews…"*) and no second request made or owed; all ten required
checks, including `pytest-suite` (18m28s), reporting `conclusion: success` at
that head. **THIS RECORD DOES NOT RE-OPEN THAT BENCH.** Readying this pull
request for review after this ratification fires a further Copilot pass on the
ratified head; that pass, and its disposition, are recorded on the pull
request itself (a further FREEZE comment), not by editing this file.

**SOURCERY AND SONARCLOUD RAISED NO FINDING AGAINST THE RATIFIED SURFACE**
(Sourcery: a reviewer's guide only; SonarCloud: quality gate passed).

## 5. THE RATIFIED SURFACE — what this word admits, and what it does not

**ADMITTED.** The `## MODIFIED Requirements` block for *Governed corpus
membership and the lifecycle scan set*, exactly as encoded — canon's own bytes
sliced from `openspec/specs/doc-health/spec.md` lines 878–945, unedited, plus
one added `#### Scenario: A recorded disposition matches no finding` — and the
realization it rides: `scripts/doc_health/families.py`'s
`_stale_grandfather_dispositions` (four constants, one function, a two-line
tail on `fam_ratified_provenance`) and the seventeen net new tests in
`tests/doc-health/test_grandfather_dispositions.py`, both confirmed at this
ratification to implement D1 option 1 exactly, with no fix required.

**NOT ADMITTED, AND NOT BY THIS WORD.**

- **Nothing reaches `openspec/specs/`.** This ratification edits no promoted
  file; the block is still a delta and promotion is the ARCHIVE's act.
- **No other family, arm, scope, threshold, resolution class, report field,
  workflow, contract member, schema or path moves.**
- **The other eight families' entries are NOT read for staleness** —
  openxFactory #966's subject, a separate act on its own word (`design.md`
  D5).
- **No `--single-repo` route to an aggregation dispositions file** —
  openxFactory #968's open question (`design.md` D2), left open.

## 6. What is owed AFTER this word

- **THE LANDING.** The lane's standing word, *"land each when green"*, applies
  once this pull request is ready for review, benched and green; the landing
  is the orchestrator's act under the lane-collision protocol's Rule 6 window,
  not this record's and not this lane author's. **No landing has been
  performed as of this file.**
- **THE ARCHIVE, WHICH IS A SEPARATE ACT ON ITS OWN PULL REQUEST.**
  `code_surface` is NON-EMPTY, so under `release-realization` this packet
  archives on **MERGED-PLUS-GREEN REALIZATION EVIDENCE AT CANON'S GRAIN** —
  this pull request merged into `main` and a green `pytest-suite` run at the
  tree that merge carries — rather than on landing. `tasks.md` § 6 stays
  ENTIRELY OPEN, and the sanctioned archive path refuses an open box, so every
  box in it must be ticked in the commit BEFORE the move.
- **openxFactory issue #965 CLOSES AT THE ARCHIVE AND NOWHERE ELSE.** This
  pull request carries `refs #965` (and the sibling refs its body names) and no
  closing keyword, in its body and in every commit message on this branch, so
  `closingIssuesReferences` is `[]`.
- **THE RESIDUE NAMED AND NOT TAKEN**: `tasks.md` § 7 — the other seven
  families' entries beyond this one (§ 7.1, openxFactory #966), the
  duplicate-target-per-line question (§ 7.7), and the other items that section
  names, none of them ruled on by this word.

## 7. Provenance of this record

Written in the ratification commit itself, in the existing clone `pkt-965`, by
lane `openxfactory-1`. It carries `Status: ratified` because
`document-lifecycle`'s *A review record records a ratification* governs a
`review/ratification-*` file, and `ratified-provenance` reads such a record's
SUBJECT whatever status it carries. Its sibling
`review/verification-2026-09-12.md` keeps `Status: record`: that file's
subject is the GATE RUN, so the scenario *A review record is not about a
ratification* governs it instead. Every path in this file is repo-relative.
