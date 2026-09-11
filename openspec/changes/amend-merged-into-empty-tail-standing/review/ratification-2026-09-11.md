# Proposal Ratification: amend-merged-into-empty-tail-standing

Status: ratified
Kind: report
Decision date: 2026-09-11
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-11 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), verbatim: *"Ratify as encoded"*,
given in session as a MULTIPLE-CHOICE ruling over `design.md` **D1** and **D2**
with the recommendation presented first, and recorded on openxFactory PR
[#947](https://github.com/opensoft/openxFactory/pull/947#issuecomment-5632913033)
at **2026-09-11T10:11:53Z** (comment `5632913033`), with the same word
recorded on issue
[#914](https://github.com/opensoft/openxFactory/issues/914#issuecomment-5632913453)
at **2026-09-11T10:11:55Z** (comment `5632913453`). **D1 = the recommended
and encoded sentence, together with the scenario *A merge marker's tail names
no superseded title*, as frozen at `546e2c97`; D2 = one unit retired and
replaced in place, the marker owed.** The alternatives offered and not taken:
*"Veto D1 — prefer a sixth ground at info"*; *"Ratify D1, veto D2 (no
marker)"*. **BOTH DECISIONS ARE RESOLVED AS THE PACKET ALREADY ENCODED, SO THE
DELTA'S WORDING STANDS UNCHANGED AND NOTHING WAS SUBSTITUTED, RESTORED OR
DELETED.**

**THE WORD AND ITS RECORDING ARE THE SAME MINUTE, AND THE DATE IS STATED
RATHER THAN INFERRED.** Brett Heap gave the word in session at
2026-09-11T10:11:50Z (the timestamp the recording comment itself states) and
it was recorded on the pull request three seconds later, at
2026-09-11T10:11:53Z, and mirrored on issue #914 at 10:11:55Z; the recording
comment is the citable artifact and it names the utterance's own timestamp
rather than presenting the recording as the moment of decision. Both instants
fall inside one UTC day, so the `Decision date:`, `approved_on`, this file's
name and its sibling capture's name are all **2026-09-11**, with no boundary
to reconcile.

**THIS RATIFICATION IS SEPARATE FROM, AND LATER THAN, THE RULING THAT
COMMISSIONED THE AUTHORING.** Brett Heap's earlier word of 2026-09-11, given
in session by multiple choice at approximately **01:3xZ** and recorded on
issue #914 at **2026-09-11T02:06:38Z** (comment `5628349929`), verbatim *"Rule
the silence correct in canon"*, chose between #914's two options and settled
`design.md` D1's DIRECTION alone — roughly eight hours before the word this
record cites. That word could not have approved a sentence nobody had written
yet, and it is not read as having done so; it stays recorded as the ORIGIN of
the AUTHORING in `proposal.md`'s `Proposed:` line, in `.openspec.yaml`'s
`proposed_by`, and in `tasks.md` § 1.1.

Ratified baseline: this change as committed on the branch
`change/amend-merged-into-empty-tail-standing` at the frozen head **`546e2c97`**
— `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/doc-health/spec.md` (**ONE `## MODIFIED` requirement**, *Currency of an
active change's MODIFIED requirement blocks*, restated over canon
byte-faithfully with **ONE unit replaced in place** under **ONE
`Removed from canon` marker** and **ONE scenario added** at the end of the
block). THREE merge commits carry current `main` into the branch without
touching that content: `9dfa36f3` (merge of main `1fb6d5cd`, pushed by a
sibling lane pass that froze at this same content and did not survive to post
its own freeze comment), `6d10daed` (merge of main `22efcbe8`, a second lane
pass that likewise froze at this content and did not survive to post its
FREEZE), and this ratification's own merge, `1229006a` (merge of main
`22a2ecbc`, carrying in an unrelated openDox/openXdox pin bump, #957's
bookkeeping tick, and other unrelated corpus movement — none of it under
this packet's own directory or under `openspec/specs/doc-health/spec.md`,
verified below). The delta's normative units are **byte-identical** to the
tree Brett Heap ruled on: `git diff --name-only 546e2c97 -- openspec/changes/amend-merged-into-empty-tail-standing/specs/`
is **EMPTY**, and this ratification adds no line to it (§ 4, and
`review/verification-2026-09-11.md` § 8, which measures it rather than
asserting it).

## 1. The two words, and exactly what each decided

### 1.1 The origin word — given ~2026-09-11T01:3xZ, recorded 02:06:38Z

Brett Heap, 2026-09-11, verbatim:

> Rule the silence correct in canon

A multiple-choice ruling over openxFactory issue #914's own two options —
*"Rule the silence correct"* and *"Report it as a sixth ground"* — filed
UNCLAIMED by this lane at the archive of `amend-marker-declaring-nothing` (PR
#926 → `114d6e3d`), which owed this residue at its own `tasks.md` § 7.1 and
`design.md` D6. **THIS WORD COMMISSIONED THE AUTHORING AND SETTLED `design.md`
D1's DIRECTION — WHETHER THE SILENCE IS CORRECT — AND NOTHING ELSE.** It was
given before a sentence existed, so it could not have approved one: no
wording, no scenario and no marker were decided by it. The packet was
therefore authored as a `Status: draft` proposal with no approval pair, the
lawful unapproved shape `add-drafted-proposal-origin` (issue #318) defined,
and `design.md` recorded D1 as STILL a veto point (the WORDING) and D2 as a
second one (the MARKER, decided by measurement).

### 1.2 The ratifying word — given ~2026-09-11T10:11Z, recorded 10:11:53Z

Brett Heap, 2026-09-11, verbatim:

> Ratify as encoded

A multiple-choice ruling over this packet's own `design.md`, put with the
recommendation presented first: **"Ratify as encoded"** (recommended and
taken); **"Veto D1 — prefer a sixth ground at info"** (declined); **"Ratify
D1, veto D2 (no marker)"** (declined). **THIS IS THE FIRST WORD TO REACH THE
PACKET'S CONTENT.** It ratifies the packet — `.openspec.yaml` gains the
approval pair, and `proposal.md`, `design.md` and `tasks.md` — the three
documents this packet authored as `Status: draft` — flip to `Status:
ratified`, joined by the new `review/ratification-2026-09-11.md` (this file)
at that same status. `review/verification-2026-09-11.md` keeps `Status:
record`, its subject being the gate run and not the ratification, per
`document-lifecycle`'s *A review record is not about a ratification*. It
answers both questions `design.md` reserved for the owner: D1's
sentence (confirm, as written) and D2's marker (confirm, as written). Neither
alternative was taken, so **THE RULING IS APPLIED BY LEAVING THE TEXT ALONE**,
verified by diff rather than asserted (§ 4).

## 2. D1 as it was put, and D1 as it is resolved

### What was on the table

`design.md` D1 — **THE VETO POINT: the sentence, and the sixth ground it is
not**:

- **OPTION A (RECOMMENDED, and what the delta encodes).** One sentence added
  to the grounds paragraph, immediately after the fifth ground's scoping
  sentence:

  > AND A `Merged into` MARKER WHOSE TAIL NAMES NO SUPERSEDED TITLE IS SILENT
  > BY RULE RATHER THAN BY OMISSION: that form declares its DESTINATION IN ITS
  > PREFIX, complete before the closing colon and where this form's
  > declaration has always been read, so the tail names what the destination
  > ABSORBED and a marker whose tail names nothing has still declared
  > everything the form obliges it to declare; it SHALL NOT be reported on the
  > fifth ground, which is read on the `Removed from canon` form alone, and
  > where its tail carries NO CODE SPAN AT ALL it reaches none of the other
  > four either, each of those being read through a name or a quoted span such
  > a tail does not carry — so NO ground fires on it and NO ground is added
  > here; a code span its reason DOES quote remains subject to the second
  > ground exactly as in every other marker.

  Written so it cannot be read as a sixth ground (a PROHIBITION in a paragraph
  of obligations; the count stays FIVE in the sentence directly above it,
  unedited; the added scenario's `THEN` bullet says MUST NOT report), and
  scoped at the SHAPE rather than the FORM (a code span the reason DOES quote
  stays subject to the second ground).
- **OPTION B — report it as a SIXTH GROUND at `info`** on the `Merged into`
  form alone: one predicate, one `_WHY_*` template clause, a flipped test, and
  `code_surface: openxFactory` rather than `none` — which would have reported
  a marker that declared everything its form requires, and would have changed
  this packet's archive rule under `release-realization`. #914's own second
  option, not a straw one.

### The resolution

**OPTION A.** The scope Brett Heap named is the recommended and
already-encoded option, so the ruling is applied **by leaving the text
alone**. A veto to option B would have cost the added sentence, the added
scenario and the marker's one name, and would have restored the retired
clause verbatim; none of that was performed. The one retired unit, the
one-name marker and the one added scenario are ratified **exactly as the
bench reviewed them**, verified by diff rather than asserted:
`git diff --name-only 546e2c97 -- .../specs/doc-health/spec.md` is **EMPTY**.

## 3. D2 as it was put, and D2 as it is resolved

### What was on the table

`design.md` D2 — **the marker: owed, and decided by measurement rather than
by preference**:

- **A pure ADDITION**, owing no `Removed from canon` marker — the cheaper
  shape, and the first one tried. Refused mechanically: `derive_units` reads
  the whole fifth-ground sentence as ONE body unit of 478 characters, and this
  corpus has no instrument for retiring a CLAUSE. Leaving the sentence
  standing and adding a second one beside it would have made canon say the
  requirement does not decide the question and then decide it, two sentences
  apart — the identical fault the packet exists to correct.
- **RETIRE AND REPLACE IN PLACE (encoded)** — one unit retired, one marker
  owed, naming the one retired unit with no code span in its reason.

### The resolution

**THE MARKER STANDS AS WRITTEN.** Brett Heap's word did not re-derive the
counts; it ratified them as measured at authoring: **165 canon units, 1
uncarried (the retired fifth-ground sentence), that one named by the marker
and suppressed, 0 marker defects, 21 of 21 promoted scenario titles carried,
0 missing** (`tasks.md` § 3.1, re-derived independently at § 3.9 through the
family's own `carried()` and `suppression()` callables). The marker is
assembled from `derive_units`' own output rather than retyped, is fenced with
a longer backtick run because its name contains backticks, and is re-parsed by
`parse_marker` to yield exactly one name, an empty `quoted`, and a reason with
no code span — surviving all five grounds.

## 4. THE RATIFIED SURFACE — verified by diff, not by assertion

Diffed against `546e2c97`, the frozen content the word was given on (three
merge commits sit between that head and this ratification, carrying in
unrelated corpus movement from `main` — none of it touching this packet's own
directory, and the two specific surfaces this packet's design and residue
name are re-checked by NAME rather than by directory-wide EMPTY claim, below):

| surface | command | result |
| --- | --- | --- |
| the ratified delta | `git diff --name-only 546e2c97 -- openspec/changes/amend-merged-into-empty-tail-standing/specs/` | **EMPTY** |
| the promoted requirement this block writes over | `git diff --stat 546e2c97 -- openspec/specs/doc-health/spec.md` | **EMPTY** |
| the predicate this delta cites (`design.md` D0/D3) | `git diff --stat 546e2c97 -- scripts/doc_health/modified_block_currency.py tests/doc-health/test_modified_block_currency.py` | **EMPTY** |
| `openspec/specs/` at large | `git diff --stat 546e2c97 -- openspec/specs/` | **NOT empty** — one unrelated file, `lifecycle-notebook-projection/spec.md` (1 insertion/1 deletion), landed by an already-ratified packet's own promotion via the intervening `main` merges; not this packet's requirement and not touched by it |
| `scripts/` and `tests/` at large | `git diff --stat 546e2c97 -- scripts/ tests/` | **NOT empty** — fifteen files, all unrelated corpus movement (openDox/openXdox pin verifiers, the corpus adapter, the sweep ledger's own row additions, and one doc-health SELF-GATE test file's redaction-tracking comment) carried in by the three merges from `main`; none of it is `scripts/doc_health/modified_block_currency.py` or `tests/doc-health/test_modified_block_currency.py` |
| `.openspec.yaml` | `git diff --numstat -- .../.openspec.yaml` (this commit) | **`41  0`** — forty-one lines ADDED, zero removed |

**ONE `## MODIFIED` REQUIREMENT, ONE UNIT REPLACED IN PLACE, ONE SCENARIO
ADDED, ONE MARKER.** The requirement is *Currency of an active change's
MODIFIED requirement blocks* of `doc-health`; the retired fifth-ground
sentence is replaced by a sentence carrying its removal-form scoping and its
entire pairing-form exclusion word for word, dropping only the clause that
called the merge form's empty tail undecided; the added sentence is a
PROHIBITION, not a sixth ground; the added scenario, *A merge marker's tail
names no superseded title*, states the WHEN/THEN/AND exactly as design.md D1
quotes it; and the marker —

> **Removed from canon by amend-merged-into-empty-tail-standing (2026-09-11):**
> the retired fifth-ground sentence, quoted in full in the block itself

— names the one retired unit, carries no code span in its reason, and is
measured at 0 marker defects. No promoted scenario moves, is retitled or
loses a bullet; no ground is added or withdrawn; no severity, threshold, arm,
parse or marker grammar moves; no code moves.

## 5. The bench, and what it settled before the word arrived

### 5.1 The rounds

| bench | commit | verdict |
| --- | --- | --- |
| Sourcery | `82cd3d64` (2026-09-11T02:41:54Z) | a Reviewer's Guide summary, not a finding set |
| Copilot round 1 | `82cd3d64` (2026-09-11T02:47:04Z) | 🟡 Changes recommended — the missing per-change ledger row (**T1**) |
| Codex, one request | `779752ed` (requested 2026-09-11T03:24:38Z) | **ABSENCE** — a usage-limit notice at 03:24:48Z (§ 5.3) |
| Copilot round 2 | `b639cf1d` (2026-09-11T03:22:28Z) | 🟡 Changes recommended — the stale verification snapshot (**T2**) |
| Copilot round 3 | `779752ed` (2026-09-11T03:31:11Z) | 🟡 Changes recommended — the sentence-order reading (**T3**) and the residue-accounting gap (**T4**), plus 5 SUPPRESSED wording nits, all taken at this same commit |
| Copilot round 4 | `e5acb0ba` (2026-09-11T03:45:48Z) | 🔵 Needs a closer look — 2 SUPPRESSED nits, 0 new comments, one of which becomes **T5** at the next round |
| Copilot round 5 | `c144eb7c` (2026-09-11T03:51:49Z) | 🔵 Needs a closer look — **T5** raised as a thread (the `.openspec.yaml` present-tense claim) |
| Copilot round 6 | `546e2c97` (2026-09-11T09:51:30Z) | 🔵 Needs a closer look — 7 SUPPRESSED comments, 0 new; standing verdict at the freeze (quoted § 5.4) |
| Copilot round 7 | `9dfa36f3` (2026-09-11T10:28:54Z) | 🔵 Needs a closer look — 6 SUPPRESSED comments, 0 new, naming that the recorded ratification had not yet been encoded (§ 5.5) |
| (merge, no review) | `6d10daed` (2026-09-11T06:37:46-04:00) | second lane pass's merge of main `22efcbe8`; died before its own FREEZE |
| Copilot round 8 | `6d10daed` (2026-09-11T10:51:52Z) | 🔵 Needs a closer look — 5 SUPPRESSED comments, 0 new, the same "still draft" theme, now doubly repeated and doubly resolved by this encode (§ 5.5) |
| (merge, no review) | `1229006a` (this ratification's own merge of main `22a2ecbc`) | third merge from `main`; no review posted before the ratification commit |

### 5.2 The five threads on the pull request, and their disposition

**FIVE THREADS, ALL FIVE TAKEN OR REFUSED WITH REASON, ZERO UNRESOLVED** at
the freeze of 2026-09-11T09:55:42Z and zero unresolved at this ratification
(confirmed again via `reviewThreads` GraphQL on 2026-09-11: `isResolved: true`
on all five).

| # | site | finding | disposition |
| --- | --- | --- | --- |
| T1 | `tasks.md` (per-change ledger) | the sanctioned ledger row was never seeded, so `--ledger-diff` was stale by one row and seven derived totals | **TAKEN** at `6806b714` — seeded with `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#947'`; `--ledger-diff` exit 0, 198 rows. `tasks.md` §§ 4.1–4.9 also brought current at `b639cf1d`, and the five wording findings folded into the same round (below) at `779752ed` |
| T2 | `tasks.md` § 4.2 | the PR body's verification snapshot (`main @ 96b4835b`, unpinned 1.2.0) disagreed with `tasks.md`'s pinned-CLI re-measurement (`origin/main @ f0eea7ed`) | **TAKEN** — already reconciled by the time of reply (2026-09-11T03:35:03Z): the PR body was edited at 03:24:01Z to the same pinned-CLI figures `tasks.md` § 4.2 carries; the two agree |
| T3 | `specs/doc-health/spec.md:186` | the added sentence's OPENING clause, read alone, is broader than the no-code-span guard that follows it two clauses later | **REFUSED** — the exact wording is `design.md` D1, the one decision this packet reserved for Brett Heap's word rather than a bench-finisher's; the guard the finding asked for already exists (the closing clause, and the scenario's first `WHEN`), traced against `_reason_boundary`/`parse_marker`/`suppression` rather than argued from prose |
| T4 | `tasks.md` § 6.1 | the residue list named two stale-prose sites (module docstring, predicate comment) and missed a third (the test's own docstring) | **TAKEN** at `e5acb0ba` — `tasks.md` § 6.1 and `design.md` D6 now name all THREE sites |
| T5 | `.openspec.yaml` `origin.reason` | present-tense claim *"canon says so in one sentence"*, when README and `proposal.md` both record that promoted canon still carries the undecided clause | **TAKEN** at `546e2c97` — the sole holdout of a tense correction `779752ed` had already made everywhere else in the packet; now reads *"canon is to say so ... canon does not say it yet ... that step is the ARCHIVE act's alone"* |

### 5.3 Codex — ABSENCE, recorded verbatim

**ONE review request stands on this pull request, and no other was made.**
Requested at 2026-09-11T03:24:38Z (head `779752ed`, comment `5628978280`).
Codex's connector reply, 2026-09-11T03:24:48Z, quoted exactly:

> You have reached your Codex usage limits for code reviews. You can see your
> limits in the Codex usage dashboard.
> To continue using code reviews, you can upgrade your account or add credits
> to your account and enable them for code reviews in your settings.

**NO CODEX PASS STANDS ON THIS PULL REQUEST AT ANY HEAD.** This is recorded
as an ABSENCE rather than as approval, and per the RELAUNCH instruction this
lane did not request a second round: one stands, and it drew a usage-limit
refusal.

### 5.4 Copilot's standing verdict at the freeze, quoted verbatim

Copilot's review at `546e2c97` (2026-09-11T09:51:30Z, 7/7 files, **0 new
comments**, Lite effort), verdict line:

> ### 🔵 Needs a closer look
>
> The specification has unresolved moderate consistency and regression-coverage
> comments, along with documentation corrections.

All 7 accompanying comments are marked SUPPRESSED (Copilot's own count: 0
new) — restatements or minor variants of threads already TAKEN or REFUSED
above, none opened as a new thread. This lane's own freeze comment
(2026-09-11T09:55:42Z, `issuecomment-5632737451`) recorded the check rollup at
this head as `SUCCESS` (SonarCloud pass, `merge-master-approval` pass,
Copilot review completed), all local gates exit 0, `closingIssuesReferences`
empty, and no closing keyword in any of the branch's 8 commit messages —
i.e., a packet mechanically clean and awaiting the ratification word.

### 5.5 The merge-from-main lane's round, and what this ratification does with it

A further Copilot round landed on `9dfa36f3` (2026-09-11T10:28:54Z, 6
SUPPRESSED comments, 0 new), after the ratifying word had already been
recorded (10:11:53Z) but before this encode: five of its six comments repeat
the pre-existing "every document carries `Status: draft`" over-generalization
(the packet's `specs/doc-health/spec.md` delta carries no `Status:` header at
all, so the precise claim names `proposal.md`, `design.md` and `tasks.md`
rather than "every document" — the phrasing this record and the edited
prose now use throughout); the sixth names the ratification directly:

> Issue #914 now records Brett Heap's 2026-09-11T10:11:50Z word, "Ratify as
> encoded," explicitly ratifying PR #947's D1/D2 encoding. This packet still
> says ratification has not been given ... encode the ratification (and
> re-run the affected gates) before treating this as a draft packet.

**THIS COMMIT IS THAT ENCODE.** No new thread was opened by this round (all
six SUPPRESSED, 0 new), so nothing here required a reply-and-resolve; it is
recorded rather than silently superseded.

A second lane pass then merged main again (`6d10daed`, merge of main
`22efcbe8`) and died before posting its own FREEZE. A further Copilot round
landed on THAT head (2026-09-11T10:51:52Z, id `5177848411`, 5 SUPPRESSED
comments, 0 new) — the identical theme a third time, all five comments
pointing at README.md:538, `.openspec.yaml:84`, `design.md:31`,
`proposal.md:172` and `tasks.md:17`, each saying the site still reads
`Status: draft` / carries no approval pair against the 10:11:50Z ratifying
word. **THIS COMMIT IS ALSO THAT ENCODE.** No new thread was opened (all five
SUPPRESSED, 0 new), so nothing here required a reply-and-resolve either; it is
recorded rather than silently superseded, alongside round 7's disposition
above. A dedicated search of every PR and issue comment on this pull request
for the phrasing "FR-018", "regression test" and "already states FIVE"
returns NOTHING: no Copilot, Codex or human comment on this thread makes
either of those two claims, at any round from `82cd3d64` through `6d10daed`
(the full API sweep is in `review/verification-2026-09-11.md` § 9). Both
themes some prior guidance for this encode named as expected findings do not
appear on this pull request; the actual eight Copilot rounds (1 through 8,
§ 5.1) are the ones disposed of above and here, and every one of their
comments is either a resolved thread (§ 5.2) or a SUPPRESSED restatement of
the single "still draft" finding, addressed by this ratification itself.

### 5.6 One correction made on independent verification, not on a located comment

Prior guidance for this encode described two further Copilot findings — one
asking whether `openspec/specs/doc-health/spec.md` owed a regression test for
a `Merged into` marker whose reason quotes a code span, one disputing
`tasks.md` § 6.2's premise that FR-018 "already states FIVE grounds." **A
targeted search of every review, issue comment and review-thread comment on
this pull request finds neither claim, at any round from `82cd3d64` through
`6d10daed`** (`gh api .../pulls/947/comments`, `.../pulls/947/reviews`,
`.../issues/947/comments`, and the `reviewThreads` GraphQL query, each
searched for "FR-018", "regression test" and "already states FIVE" — zero
matches). Neither finding is disposed of here as a Copilot disposition, for
want of one to cite.

**THE UNDERLYING FR-018 QUESTION WAS CHECKED ANYWAY, ON ITS OWN MERITS, AND IT
WAS WRONG.** `tasks.md` § 6.2 (as this lane's prior pass over this packet
wrote it) said FR-018 "states the ONE reporting ground a marker had before
`amend-marker-defect-reporting` made it three" and that the restatement was
"owed by openxFactory #915 ... and OPEN." Neither clause is true on this
tree: `specs/019-modified-block-currency-family/spec.md:442` already states
**FIVE** grounds, restated by `8a2ed38c` and `125a7d96` (both `refs #915`,
landed 2026-09-10, before this packet was authored), and **openxFactory #915
is CLOSED** (closed 2026-09-11T01:29:59Z). § 6.2 is corrected in this same
ratification commit to state the tree as it actually stands. This does not
touch this packet's own delta or its `code_surface: none` measurement — FR-018
sits in a Speckit build record outside every family's `GOVERNED_ROOTS`, and
this packet adds no marker-defect ground for it to restate — so the
correction is prose-only, confined to `tasks.md` § 6.2.

## 6. Why the packet exists

**ONE OWED SUCCESSOR, RULED BEFORE IT WAS AUTHORED.** openxFactory issue #914
was filed UNCLAIMED by this lane at the archive of
`amend-marker-declaring-nothing` (PR #926 → `114d6e3d`), which owed it at its
own `tasks.md` § 7.1 and `design.md` D6 rather than deciding it: whether a
`Merged into` marker whose tail names no superseded title declares nothing,
or declares a destination that absorbed nothing named in the tail, was a
question nobody had ruled. The predecessor PINNED the silence with
`test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT` so it would be
*"a decision a later act can overturn rather than a gap it has to
rediscover"*. This packet, and the two words it took to ratify it, is that
later act.

## 7. What is NOT ratified, and the residue this word does not reach

- **NOTHING IS PROMOTED.** This ratification edits no file under
  `openspec/specs/`, no script, no test, no contract, no schema and no
  workflow. The `## MODIFIED` block is a DELTA; canon still carries the stale
  clause until the archive writes the block over it.
- **`tasks.md` § 5 (ARCHIVE) STAYS ENTIRELY OPEN.** `code_surface: none` means
  this packet archives ON LANDING plus its own task list under
  `release-realization`, rather than on merged-plus-green realization
  evidence — but that archive is a SEPARATE act on a SEPARATE word, not
  performed or authorized here. openxFactory #914 closes THERE, and this pull
  request's body carries `refs #914` and no closing keyword.
- **§ 6.1 — THREE PIECES OF STALE PROSE ARE OWED AT THE ARCHIVE, NOT HERE.**
  `scripts/doc_health/modified_block_currency.py`'s `suppression` docstring
  (`:1432`) and the comment beside the fifth-ground predicate (`:1535`), and
  `tests/doc-health/test_modified_block_currency.py`'s
  `test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT` docstring
  (`:2698-2710`), all still say the merge form's empty tail is *"a question
  nobody has ruled."* No behaviour moves and no test assertion changes;
  taking it here would give this packet a code surface and change its archive
  rule. A successor is to be NAMED at the archive act.
- **§ 6.2 — `specs/019-modified-block-currency-family/` IS NOT EDITED, AND ITS
  FR-018 ALREADY MATCHES CANON.** FR-018 (`:442`) states FIVE grounds today
  (`8a2ed38c`/`125a7d96`, `refs #915`, landed 2026-09-10, before this
  packet's own authoring); openxFactory **#915 is CLOSED**
  (2026-09-11T01:29:59Z), not open — corrected in this ratification (§ 5.6,
  above) rather than left standing. This packet adds no ground, so it
  neither widens nor reopens #915's now-closed scope.
- **§ 6.3 AND § 6.4 — NO ESTATE-WIDE RUN AND NO WIDENING OF THE
  UNCITED-RESOLUTION RULE.** Both directions of this amendment are silence,
  so no governed repository can gain or lose a row; the per-class grain of
  `report.uncited_resolutions` is openxFactory #893's work, filed by
  `amend-modified-block-currency-standing` at its own archive.
- **NO PROMOTED MARKER AND NO ARCHIVED DELTA IS EDITED.** They are records of
  ratified removals, and every one of them is correct under the amended
  sentence once it is promoted.

## 8. Sequencing, and the landing obligation this word does NOT carry

**`sequenced_after: []` IS A POSITIVE ROOT CLAIM**, measured rather than
assumed (`design.md` D5): no other active change carries a `## MODIFIED` block
over *Currency of an active change's MODIFIED requirement blocks*, so the
two-writers ordering that very requirement states is not in play.

**THE ARCHIVE IS A SEPARATE ACT ON A SEPARATE WORD, AND #914 CLOSES THERE.**
`code_surface: none` archives on landing plus its own task list rather than
on merged-plus-green realization evidence, but neither landing nor archive is
performed or authorized by this commit.

**THIS LANE ENCODES AND FREEZES; IT DOES NOT MERGE OR LAND.** The recording
comment of 2026-09-11T10:11:53Z names the landing as riding Brett Heap's
standing word *"land each when green"*, and the merge-from-main this commit's
own head carries as its own separate act; the Rule 6 LANDING/LANDED post
belongs to the landing lane, on that standing word, and is not requested or
assumed here.
