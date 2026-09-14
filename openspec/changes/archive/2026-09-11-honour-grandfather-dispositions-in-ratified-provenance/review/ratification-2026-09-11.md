# Proposal Ratification: honour-grandfather-dispositions-in-ratified-provenance

Status: ratified
Kind: report
Decision date: 2026-09-11
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-11 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), a MULTIPLE-CHOICE ruling over
`design.md`'s two declared veto points with the recommendation presented first
in each: **D1 verbatim *"info row carrying the citation"*** and **D2 verbatim
*"Archived-only boundary"***, given in session at **2026-09-11T10:11:50Z** and
recorded on openxFactory PR
[#945](https://github.com/opensoft/openxFactory/pull/945#issuecomment-5632913794)
at **2026-09-11T10:11:56Z** (comment `5632913794`). **BOTH ARE THE OPTIONS THIS
PACKET HAD ALREADY ENCODED, SO THE WORDING STANDS UNCHANGED AND NOTHING WAS
SUBSTITUTED, RESTORED OR DELETED.**

**THE WORD AND ITS RECORDING ARE THE SAME MINUTE, AND THE DATE IS STATED RATHER
THAN INFERRED.** The utterance is timestamped 10:11:50Z inside the recording
comment and the comment itself was created at 10:11:56Z — six seconds apart,
one UTC minute, one UTC day. So `Decision date:`, `approved_on`, this file's
name and its sibling capture's name are all **2026-09-11**, with no boundary to
reconcile. Every timestamp in this packet is UTC, as `proposed_on`, `created`
and the origin word of ~01:3xZ are.

## 1. The three words, and exactly what each decided

**THE COMMISSIONING WORD IS NOT AN APPROVAL AND IS NOT READ AS ONE.** Brett
Heap's word of 2026-09-11 at approximately 01:3xZ, verbatim *"Commission the
packet"*, was itself a multiple-choice ruling and it commissioned the
AUTHORING. It named no wording, resolved neither veto point and admitted no
text to canon. `.openspec.yaml`'s `origin:` block was authored under it in the
lawful unapproved shape `add-drafted-proposal-origin` (issue #318) defined —
`proposed_by` + `proposed_on`, no approval pair — and **that block is kept
byte-unmoved by this ratification**, its drafting tense included. The approval
pair is an ADDITION beside it, measured in `review/verification-2026-09-11.md`
§ 9 as `42 0` on `git diff --numstat`.

**THE RATIFYING WORD IS THE SECOND ONE**, quoted in full because it is short
and because its own text says what it settles:

> **WORD 2026-09-11T10:11:50Z — Brett Heap (openxFactory operator authority),
> multiple choice over design.md D1 and D2, each with the recommendation first:
> D1 "info row carrying the citation" (not suppression); D2 "Archived-only
> boundary" (not active paths).** Both encoded options → the wording stands
> unchanged: ratify as encoded. Encode follows the verify-and-freeze pass now
> in flight, as a separate commit; landing on the standing 'land each when
> green'; archive on realization evidence (this PR's green suite at canon's
> grain); #939 closes at the archive.

It is Brett Heap's act and not the authoring lane's. What it moves is recorded
in § 3.

**THE THIRD WORD IS ABOUT WHAT COMES AFTER THIS PULL REQUEST, AND IT IS
RECORDED HERE SO THE OWED LIST IN § 6 IS CURRENT.** At **2026-09-11T12:08:24Z**,
recorded on this pull request at 12:08:31Z
([comment `5634204587`](https://github.com/opensoft/openxFactory/pull/945#issuecomment-5634204587)),
Brett Heap said verbatim *"land each when green, archive both when landed,
claim 955 and 956"*. For this packet that reaffirms the standing LANDING word
and gives the ARCHIVE word IN ADVANCE. **IT CHANGES NOTHING THIS RECORD
RATIFIES AND IT PERFORMS NEITHER ACT**: the archive is still a separate pull
request, it still waits on this packet's own realization evidence at canon's
grain, and openxFactory #939 still closes THERE.

## 2. What the ruling was given over

**THE WORD WAS GIVEN OVER THE PACKET AS IT STOOD AT `468df2ef`**, the head the
verify-and-freeze pass had just pushed, and the ruling's own text says the
encode follows that pass "as a separate commit". Between that head and this
ratification the packet moved five times and **NOT ONE OF THOSE COMMITS TOUCHES
THE DELTA**:

| commit | what it is |
| --- | --- |
| `468df2ef` | merge of `origin/main` `1fb6d5cd` |
| `a343f017` | merge of `origin/main` `22efcbe8` |
| `cd27180c` | the THIRD bench round, taken (§ 5.11) |
| `f281c1fa` | merge of `origin/main` `78d2c6f5` |
| `5a8bba3e` | the FOURTH bench round, taken (§ 5.12) |
| `ad6d542c` | merge of `origin/main` `38c076d1` |

`git diff --name-only 468df2ef..HEAD -- openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/specs/`
returns **0 files**, which is the mechanical form of *the wording stands
unchanged*. The two bench rounds after the word are repairs to the REALIZATION
and to the packet's own accounting; neither reaches the `## MODIFIED` block,
and both are dispositioned in § 4 below.

## 3. D1, D2 and the carried decisions — and why the wording stands

**D1 — THE BAND — IS RULED *"info row carrying the citation"***, the
RECOMMENDED option, against the alternative *"Suppress, matching the four
siblings"*.

A grandfathered finding is reported at **`info`**, keeping its family, repo,
path and resolution class, with the recorded citation quoted behind
`GRANDFATHERED by a recorded disposition — `. The declined alternative was the
PRECEDENT and that is why it was a veto point: all four sibling *A finding is
dispositioned* scenarios (promotion fidelity, duplicate packet, modified-block
currency, the sibling-addition pairing class) SUPPRESS. The cost of the veto
was written out at design time and is retained in `design.md` D1 as the record
of what was put and declined, not as work owed: suppression would have been a
smaller diff and would have matched four promoted requirements exactly, at the
price of the eighteen records' visibility, an uncountable grandfathered
population, and a stale entry become invisible rather than inexplicable.
**BECAUSE THE RULED OPTION IS THE ENCODED ONE, THE RULING IS APPLIED BY LEAVING
THE TEXT ALONE** — one `THEN` bullet of the delta and one branch of
`_honour_grandfather_dispositions` stand exactly as the bench reviewed them.

**D2 — THE BOUNDARY — IS RULED *"Archived-only boundary"***, the RECOMMENDED
option, against *"Admit active paths too"*.

A disposition downgrades ONLY where the finding's path is under
`openspec/changes/archive/`. A finding against an ACTIVE packet's record stays
`critical` however the file names it.
`finding.path.startswith("openspec/changes/archive/")` is the whole test, the
`and` that admitting active paths would have cost was not added, and the
scenario's ACTIVE-packet bullet was not removed. The declined alternative would
have cost the distinction between a ruling on something nobody may repair and a
deferral of something somebody could fix this afternoon — the failure mode
`uncited-resolution` exists to prevent elsewhere. D1 and D2 rest on no shared
predicate; either would have stood whichever way the other went.

**D0 AND D3 THROUGH D6 WERE CARRIED BESIDE THEM AND NONE WAS VETOED.**

- **D0 — the measurement taken before the design.** An aggregation assembled
  from `opensoft/xFactory` @ `bc84d325` with `openxFactory` @ `96b4835b` and
  `codexFactory` @ `a67fb0ae`: the real `health/dispositions.yaml` carried 40
  entries across 8 families, **18** of them `family: ratified-provenance` — 15
  `openxFactory`, 3 `codexFactory` — every one dated, cited and naming a path
  under `openspec/changes/archive/`; the family reported **41 rows, all
  `critical`**, and under the pass **41 rows, 23 `critical` + 18 `info`**, the
  moved set equal to the disposition key set and the remaining twenty-three
  byte-identical. **THAT MEASUREMENT IS DATED AND PINNED AND IT STANDS AS
  TAKEN.** It was re-taken on the ratified tree against TODAY's aggregation and
  the re-take is in `review/verification-2026-09-11.md` § 10, including the one
  figure that has moved since and why.
- **D3** — `health/dispositions.yaml`, not a new file and not a new key; the
  admission rule DELEGATED to `promotion_fidelity.load_dispositions`, the
  estate's one reader; the bounded, one-line cite excerpt.
- **D4** — `doc-health` is amended and `document-lifecycle` is NOT.
- **D5** — the sibling search, pasted rather than summarized.
- **D6** — what is deliberately not taken, including the `--single-repo` route
  to an aggregation dispositions file.

## 4. The bench, round by round, and what each round settled

**THE BENCH WAS CLOSED WHEN THIS RECORD WAS WRITTEN: five Copilot rounds,
FIVE THREADS, ALL FIVE TAKEN, ZERO UNRESOLVED.** Two rounds arrived AFTER the
ratifying word; both are repairs to the realization and to this packet's own
accounting, neither reaches the delta, and both are recorded here rather than
folded into the earlier rounds.

| # | round | raiser | subject | disposition |
| --- | --- | --- | --- | --- |
| T1 | 1, 2026-09-11T02:44:30Z | Copilot | the citation lookup keyed `(repo, path)` alone, so a neighbouring family's entry at the same path could supply the text, and it honoured an UNDATED entry | **TAKEN** in `2dc6c303` — both predicates applied in the pass, each a narrowing; `design.md` D3's delegation untouched |
| T2 | 1, 2026-09-11T02:44:31Z | Copilot | the pass-through-BY-IDENTITY invariant was documented but uncovered — the test compared findings from two separate runs, which can only compare VALUES | **TAKEN** in `2dc6c303` — the arms run once and the pass is called on their own list, with `is` on every untouched row; measured both ways against a probe build |
| T3 | 3, 2026-09-11T10:18:18Z | Copilot | a same-family entry with a list- or dict-valued `repo`/`path` made the lookup key UNHASHABLE and `key in admitted` raised `TypeError` out of the family and the whole run | **TAKEN** in `cd27180c` — the shared reader's own `isinstance` test applied BEFORE the key is built; reproduced first at `families.py:451` on the frozen head, pinned by a test asserted both ways |
| T4 | 4, 2026-09-11T11:01:02Z | Copilot | a dispositions FILE whose top-level value is a SCALAR reaches `load_dispositions`' `for entry in entries` and raises `TypeError`, and this family did not read that file before this change | **TAKEN** in `5a8bba3e`, and taken WIDER than asked — see below |
| T5 | 4, 2026-09-11T11:01:03Z | Copilot | the verification counts were inconsistent across the packet and the pull request body | **TAKEN** in `5a8bba3e` — one measurement everywhere, re-taken on the final tree |

**T4 IS THE ROUND WORTH READING TWICE, BECAUSE THE NARROW FIX WOULD HAVE BEEN
COSMETIC.** Measured end to end before anything was changed: over an
aggregation carrying a `42`-rooted dispositions file,
`doc-health.py --repo-root <aggregation>` exits **1** on `origin/main` at
`scripts/doc_health/runner.py:758` — the runner's own unconditional read of the
same file, which fires on every aggregation run with or without this packet —
and exited 1 one frame earlier on this branch. **SO THE GUARD IS IN BOTH
READERS OR IT BUYS NOTHING**: repairing only the shared reader would have moved
the abort back to the runner's line rather than removed it. Both now refuse a
non-list root, which is the refusal each loop already applies to an ENTRY that
is not a mapping, taken one level up. **IT NARROWS NOTHING**: every non-list
root the guard refuses already yielded an empty set by iteration — a mapping
root iterates keys, a string root characters, neither being a mapping — so the
honoured set is identical and only the exception is gone, asserted shape by
shape rather than argued. `tasks.md` § 3.9 carries the measurement and
`review/verification-2026-09-11.md` § 11 re-takes it on the ratified tree.

**TWO ITEMS WERE REFUSED IN ROUND 3, WITH THE REASON RECORDED RATHER THAN THE
COMMENT DROPPED**, and both refusals stand at this head. They are written out
in `tasks.md` § 5.11 and summarized here: **(a)** that the added scenario
contradicts *A proposal carries an uncited ratified header* and that the older
bullet should be amended — REFUSED on custody first (that bullet is PROMOTED
CANON carried here byte-faithfully as the `## MODIFIED` block's pre-text,
`sha256 d32aaa43…` on both sides, so amending it would edit promoted text and
break the carriage proof) and on the merits second (the older bullet asserts
scan-set/governed-corpus PARITY, which this scope-blind pass preserves
exactly); **(b)** that the downgraded row should carry `CONTESTED` rather than
the family's `auto-fixable` class — REFUSED as a re-decision rather than a fix,
with § 2.6's measurement of the consequence and a named successor question.

**THE SUPPRESSED COMMENTS ARE ACCOUNTED FOR, NOT IGNORED.** Copilot's round 2
(2026-09-11T03:27:52Z, five suppressed) and round 5 (2026-09-11T11:44:11Z, two
suppressed, zero new threads) opened no thread. Round 5's two are ONE finding
in two places — the same count inconsistency T5 names — and they are settled by
`5a8bba3e` and by the pull request body rebuilt beside this record.

**SOURCERY POSTED A REVIEWER'S GUIDE AND NO FINDING** (2026-09-11T02:40:09Z): a
summary and two diagrams, the upsell stub this estate records as such.

**SONARCLOUD'S QUALITY GATE PASSED** on this pull request — 0 accepted issues,
0 security hotspots, 3 new issues raised and none blocking the gate
(2026-09-11T11:41:31Z).

**CODEX NEVER REVIEWED THIS PULL REQUEST AT ANY HEAD.** The one review request
this lane is permitted to make was made at 2026-09-11T12:34:54Z on head
`ad6d542c`, and the connector answered at **2026-09-11T12:35:03Z**: *"You have
reached your Codex usage limits for code reviews."* **THAT IS AN ABSENCE AND IT
IS RECORDED AS ONE, NEVER AS APPROVAL.** The exchange is quoted in full in
`review/verification-2026-09-11.md` § 12.

## 5. THE RATIFIED SURFACE — what this word admits, and what it does not

**ADMITTED.** The `## MODIFIED Requirements` block for *Governed corpus
membership and the lifecycle scan set* exactly as encoded: the requirement
sliced byte-faithfully from `openspec/specs/doc-health/spec.md` (the pre-text
hashing to `sha256 d32aaa43dc6ad118af3a57d58a2a3ffcb80c66ae128ca36b2921224a30bfdbe3`
on both sides) plus ONE added `#### Scenario: A finding is grandfathered by a
recorded disposition`, whose four arms are the ones D1 and D2 rule on: a dated,
cited entry keyed `(family, repo, path)`; an archived path reported at `info`
with the citation quoted; an ACTIVE packet's path left `critical`; an undated
or uncited entry not honoured.

**NOT ADMITTED, AND NOT BY THIS WORD.**

- **Nothing reaches `openspec/specs/`.** This ratification edits no promoted
  file. The block is still a delta and promotion is the ARCHIVE's act.
- **No other family, arm, scope, threshold, resolution class, report field,
  workflow, contract member, schema or path moves.** The one edit outside
  `families.py` is the pair of non-list-root guards, which change what no run
  REPORTS and only whether a malformed FILE aborts it.
- **The `CONTESTED` class question and a stale-disposition check are NOT
  decided** — `tasks.md` § 7.1 and § 5.11(b), each a successor's act on its own
  word.
- **No `--single-repo` route to an aggregation dispositions file** (`design.md`
  D6): a `--single-repo` run has `agg_root is None` and this arm does nothing
  in that scope, which `review/verification-2026-09-11.md` § 6 measures.

## 6. What is owed AFTER this word

- **THE LANDING.** Brett Heap's standing word *"land each when green"*,
  reaffirmed at 2026-09-11T12:08:24Z, pre-gives it for a ratified head that is
  green. The landing is the orchestrator's act under the lane-collision
  protocol's Rule 6 window, not this record's and not this lane author's. **No
  landing has been performed as of this file.**
- **THE ARCHIVE, WHICH IS A SEPARATE ACT ON ITS OWN PULL REQUEST.** The WORD
  for it is now given in advance (*"archive both when landed"*,
  2026-09-11T12:08:24Z), but the EVIDENCE is not yet in existence.
  `code_surface` is NON-EMPTY, so under `release-realization` this packet
  archives on **MERGED-PLUS-GREEN REALIZATION EVIDENCE AT CANON'S GRAIN** —
  this pull request merged into `main` and a green `pytest-suite` run at the
  tree that merge carries — rather than on landing. `tasks.md` § 6 stays
  ENTIRELY OPEN, and the sanctioned archive path refuses an open box, so every
  box in it must be ticked in the commit BEFORE the move.
- **openxFactory issue #939 CLOSES AT THE ARCHIVE AND NOWHERE ELSE.** This pull
  request carries `refs #939` and no closing keyword, in its body and in every
  commit message on this branch, so `closingIssuesReferences` is `[]`.
- **THE RESIDUE NAMED AND NOT TAKEN**: `tasks.md` § 7.1 (a stale-disposition
  check — and see `review/verification-2026-09-11.md` § 10, where that
  successor's population is no longer zero), § 7.2 (the other seven families'
  entries), § 7.3 (`docs/doc-health.md`'s family table row 3) and § 7.4 (a
  `--single-repo` route), plus the two round-3 refusals recorded in § 4.

## 7. Provenance of this record

Written in the ratification commit itself, in a fresh clone, by lane
`openxfactory-1`. It carries `Status: ratified` because `document-lifecycle`'s
*A review record records a ratification* governs a `review/ratification-*`
file, and `ratified-provenance` reads such a record's SUBJECT whatever status
it carries. Its sibling `review/verification-2026-09-11.md` keeps
`Status: record`: that file's subject is the GATE RUN, so the scenario *A
review record is not about a ratification* governs it instead. Every path in
this file is repo-relative.
