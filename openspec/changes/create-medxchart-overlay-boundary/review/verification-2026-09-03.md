# Verification record: create-medxchart-overlay-boundary, 2026-09-03

Status: record
Kind: report
Captured: 2026-09-03, in the ratification lane `openxfactory-max001`
(session `5e783e4d`), on branch `change/ratify-create-medxchart-overlay-boundary`
(openxFactory PR #608). Every number below was RE-DERIVED TWICE, BOTH TIMES
PRE-CAPTURE: first ON THE REBASED TREE at
`c39d29bc7b8e1b5309efb577facd396a76361df8`, in the second commit on this branch,
subject "Ratification of create-medxchart-overlay-boundary: the records
re-derived pre-capture (86/86) …"; and again ON THE MERGED TREE, after `main`
moved to `6da1e1f5` (#606, #593, #589) and this branch took the catch-up merge,
in the commit that carries this line — subject "Ratification of
create-medxchart-overlay-boundary: records re-derived a second time pre-capture
after main moved (#606, #593, #589)". A commit cannot write its own hash into
its own tree, so each is named by its subject and its position on the branch
rather than by a hash; § 9 lists what each corrected and why.

**Why this file exists.** `tasks.md` 4.3 says "Run targeted YAML/Markdown/Git
consistency checks and report any pre-existing dirty work left untouched" and is
ticked, but **no such report was ever written**. The checkbox is NOT unticked —
the checks were run in session on 2026-08-23 and unticking would assert they
were not. What is done instead is this: everything reproducible has been RE-RUN
now, with its command and its output, so the reader gets a report rather than a
claim; and the one half that cannot be reproduced is named as unreproducible
rather than described from memory.

**This record is CAPTURED AT MERGE, not at first push.** It was RE-DERIVED ON
THE REBASED TREE before capture, and § 9 lists what changed and why. After the
merge that captures it, it is written once and never edited.

---

## 1. `openspec validate create-medxchart-overlay-boundary --strict`

```console
$ OPENSPEC_TELEMETRY=0 openspec validate create-medxchart-overlay-boundary --strict
Change 'create-medxchart-overlay-boundary' is valid
```

Run against the ratified content — the two spec deltas
(`specs/medxchart-overlay-boundary/spec.md`, THREE ADDED requirements;
`specs/domain-descendant-boundary/spec.md`, ONE MODIFIED requirement),
`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`. `openspec` 1.2.0.

## 2. `openspec validate --all --strict`

```console
$ OPENSPEC_TELEMETRY=0 openspec validate --all --strict
…
✓ spec/workstation-intake
✓ spec/xfactory-semantic-kernel
Totals: 86 passed, 0 failed (86 items)
```

Eighty-six items, zero failures — every active change and every promoted
specification in the repository, this change included. **The total moved THREE
TIMES while this branch was open and NONE OF THE MOVES IS THIS PACKET'S**: it
read 85 as first written; 86 once `add-project-repo-schema` (PR #605) landed on
`main` at `642ac147` and this branch was rebased onto it; 87 once
`update-standards-body-current-publications` was adopted as an ACTIVE change
(PR #593) and this branch took the catch-up merge of `main` at `6da1e1f5`; and
back to 86 once `declare-spent-bundle-state` was ARCHIVED (#611) and this
branch took the second catch-up merge of `main` at `2b0615da` — an archive
retires an active change id without adding a replacement, which is the
opposite direction from the two authoring moves before it. This packet adds no
change id of its own — it ratifies one that was already active and already
counted — so it moves this total not at all. The total was re-derived on each
tree and corrected before capture (§ 9).

## 3. The pin agreement, read from an INDEPENDENT clone

Read from a fresh shallow clone of `opensoft/MedxChart` rather than from any
working tree, so the result does not depend on the state of a shared checkout:

```console
$ git clone -q --depth 1 https://github.com/opensoft/MedxChart.git mcverify
$ git -C mcverify rev-parse HEAD
68d2f1f5db932cb5099ceac75dab66316ef22579
$ git -C mcverify ls-tree HEAD openChart
160000 commit d2376a31dbafa413d8e5ba032f4a2620a75d578e	openChart
$ grep -n revision mcverify/contracts/openchart-pin.yaml
7:  revision: d2376a31dbafa413d8e5ba032f4a2620a75d578e
```

**The two pins agree.** The nested `openChart` gitlink and
`contracts/openchart-pin.yaml`'s `pin.revision` both name
`d2376a31dbafa413d8e5ba032f4a2620a75d578e`. The manifest also carries
`schema_version: 1`, `kind: medxchart_openchart_pin`,
`repository: opensoft/openChart`, `remote: git@github.com:opensoft/openChart.git`,
`submodule_path: openChart`, `source_path: .`,
`relationship: pinned_upstream_composition` — the shape
`domain-descendant-boundary`'s pin rule names, and one of the two live examples
that rule was written from.

**What this verification does NOT establish, and the reason § 5 of `tasks.md`
exists:** that the agreement is ENFORCED. It is a human reading of two files.
`opensoft/MedxChart` carries no `tests/validate_pin.py`, no `pin-validation`
workflow, and no required check — its entire tracked tree is listed at § 5
below. The ratified rule's own scenario ("the descendant's own validator REFUSES
the tree rather than preferring either") has no implementation here yet.

## 4. The aggregation entry and gitlink, read from GitHub `main`

Read through the API rather than from the local superproject checkout. The
first command is GREPPED to the two Medx entries and says so in the command
itself: the aggregation carries thirteen submodules, and a block showing two
under a command that prints thirteen would be an elision the reader could not
see.

```console
$ gh api repos/opensoft/xFactory/contents/.gitmodules --jq .content | base64 -d | grep -A2 'submodule "xFactories/Medx\(Chart\|Practice\)"'
[submodule "xFactories/MedxChart"]
	path = xFactories/MedxChart
	url = git@github.com:opensoft/MedxChart.git
[submodule "xFactories/MedxPractice"]
	path = xFactories/MedxPractice
	url = git@github.com:opensoft/MedxPractice.git

$ gh api repos/opensoft/xFactory/contents/xFactories --jq '.[] | select(.name=="MedxChart" or .name=="MedxPractice") | "\(.name) \(.type) \(.sha)"'
MedxChart file 68d2f1f5db932cb5099ceac75dab66316ef22579
MedxPractice file d8d73195609df3b567643a7bf1252eac352d9996
```

The aggregation's gitlink `68d2f1f5db932cb5099ceac75dab66316ef22579` is EQUAL to
`opensoft/MedxChart`'s own `main` (§ 3). The URL is the ABSOLUTE
`git@github.com:opensoft/MedxChart.git` form, **not** the relative
`../MedxChart` this proposal originally decided on:

```console
$ gh api repos/opensoft/xFactory/commits/386e7ee2 --jq '.sha, .commit.message, .commit.author.date'
386e7ee29fffab36197fbe12fe0139706a715f90
A relative submodule URL resolves to whatever cloned the superproject

MedxChart and MedxPractice entered .gitmodules as ../Medx* — on the
nightly runner the superproject is HTTPS, so they resolved to plain
https:// URLs the workflow's git@-only token rewrite never touches, and
every nightly since 2026-08-24 died at their clone. Normalize both to the
git@github.com: form their eighteen siblings use; the openxfactory App
now carries both repos, so the rewritten token'd clone succeeds.

2026-08-25T19:13:51Z
```

The boundary itself landed at `bed2a69` ("Replace openChart aggregate with
MedxChart", 2026-08-23T20:14:55Z). `0c6ea39` (2026-08-26) moved
`opensoft/MedxFactory` and `opensoft/MedxEHR` to the `MedxSoft` organization and
**did not touch either Medx descendant** — MedxChart's `opensoft/` home stands.

## 5. Host-absolute paths, and the descendant's whole tracked tree

```console
$ git grep -n '/home/' -- openspec/changes/create-medxchart-overlay-boundary ':!*/review/*'
$ echo $?
1
$ git -C mcverify grep -n '/home/'
$ echo $?
1
$ git -C mcverify ls-files
.gitmodules
AGENTS.md
README.md
contracts/openchart-pin.yaml
openChart
openspec/changes/archive/.gitkeep
openspec/specs/.gitkeep
```

**`review/` IS EXCLUDED FROM THE FIRST SWEEP, and the exclusion is the finding
rather than a convenience.** Without it the sweep matches THIS RECORD'S OWN
quoted command lines — the pattern `/home/` is printed in the commands above —
so once this record exists the unexcluded form can never return nothing, and the
`(no matches)` this section printed as first written was falsified by the very
file it was written into. Copilot's round-1 review named exactly that, and it is
taken. `git grep` prints nothing and exits `1` where there is no match, so the
exit status is shown rather than a prose rendering: on a page, "no output" and
"never run" look alike.

No host-absolute path in the GOVERNED artifacts — `proposal.md`, `design.md`,
`tasks.md`, `.openspec.yaml` and the two spec deltas — and none in the
descendant. And the file list is the evidence for `tasks.md` 6.1: **seven tracked entries, all
composition metadata, ZERO openChart profile artifacts.** `opensoft/MedxPractice`
at `d8d73195` reads the same way — `.gitmodules`, `AGENTS.md`, `README.md`,
`contracts/openpractice-pin.yaml` (`kind: medxpractice_openpractice_pin`,
revision `9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`), and the `openPractice`
gitlink.

## 6. The remote

```console
$ gh repo view opensoft/MedxChart --json visibility,pushedAt,url
{"pushedAt":"2026-08-23T20:23:45Z","url":"https://github.com/opensoft/MedxChart","visibility":"PRIVATE"}
```

The remote `design.md`'s Open Question said "does not currently exist" has
existed since 2026-08-23T20:23:45Z — hours after the question was written.

## 7. The MedxFactory documentation edit, measured

```console
$ git show --stat 933c5025
commit 933c502511e2f9fb714a72cbcde8b9d6362d1b34
    Point intake plan at MedxChart composition
 ...-patient-intake-vertical-slice-delivery-plan-and-acceptance-gates.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

`tasks.md` 3.3's "affected MedxFactory documentation links" is **one line in one
brainstorm file**: row P4 of the delivery-plan table, repointed from `openChart`
/ `../../../openChart/openspec/…` to `MedxChart` /
`../../../MedxChart/openChart/openspec/…`. The plural overstates the act.

## 8. What could NOT be reproduced

`tasks.md` 1.1's second half ("the unrelated dirty/staged state of the shared
xFactory and MedxFactory checkouts") and 4.3's "report any pre-existing dirty
work left untouched" describe a point-in-time observation of shared working
trees on 2026-08-23. **That state is gone and is not reconstructable**, ten days
and many sessions later. It is reported as unreproducible rather than restated
from memory.

What CAN be checked about it is the file list of each landing commit, and it is
reported here as measured rather than as clean:

Both commits belong to OTHER repositories — `opensoft/xFactory` and
`opensoft/MedxChart` — so neither is reachable from this checkout by a bare
`git show`. They are read through the GitHub API instead, as §§ 3 and 4 are, and
the output is pasted one file to a line exactly as the command emits it:

```console
$ gh api repos/opensoft/xFactory/commits/bed2a69 --jq '"\(.sha[0:7]) \(.commit.message | split("\n")[0])"'
bed2a69 Replace openChart aggregate with MedxChart
$ gh api repos/opensoft/xFactory/commits/bed2a69 --jq '.files[] | "\(.status)\t\(.filename)\t+\(.additions) -\(.deletions)"'
modified	.gitmodules	+3 -3
modified	CLAUDE.md	+2 -1
modified	README.md	+7 -1
modified	openxFactory	+1 -1
modified	project-register.yaml	+3 -1
added	xFactories/MedxChart	+1 -0
modified	xFactories/MedxFactory	+1 -1
removed	xFactories/openChart	+0 -1
$ gh api repos/opensoft/xFactory/commits/bed2a69 --jq '"\(.files|length) files changed, \(.stats.additions) insertions(+), \(.stats.deletions) deletions(-)"'
8 files changed, 18 insertions(+), 9 deletions(-)

$ gh api repos/opensoft/MedxChart/commits --jq '.[] | "\(.sha[0:7]) \(.commit.message | split("\n")[0])"'
68d2f1f Keep MedxChart bootstrap paths portable
4b0b6da Create MedxChart pinned openChart composition
$ gh api repos/opensoft/MedxChart/commits/68d2f1f5db932cb5099ceac75dab66316ef22579 --jq '.files[] | "\(.status)\t\(.filename)\t+\(.additions) -\(.deletions)"'
modified	AGENTS.md	+3 -3
added	openspec/changes/archive/.gitkeep	+0 -0
$ gh api repos/opensoft/MedxChart/commits/4b0b6da97642625c77e8cb0003ecf706b7dddfd2 --jq '.files[] | "\(.status)\t\(.filename)\t+\(.additions) -\(.deletions)"'
added	.gitmodules	+3 -0
added	AGENTS.md	+30 -0
added	README.md	+37 -0
added	contracts/openchart-pin.yaml	+10 -0
added	openChart	+1 -0
added	openspec/specs/.gitkeep	+0 -0
```

Six of `bed2a69`'s eight paths are this packet's own — the `.gitmodules` swap,
the two gitlinks it trades, and the three documents `tasks.md` 3.2 names.
**TWO ARE NOT, and are disclosed rather than glossed:** the `openxFactory` and
`xFactories/MedxFactory` gitlinks moved in the same commit. Those are ordinary
submodule pin-syncs and neither is unrelated user work, but they are outside the
paths `tasks.md` 3.1–3.2 describe, so a reader comparing the task text to the
commit will find two entries the text does not account for. That is what the
commit contains.

Worth recording separately, because the ratified pin rule turns on it:
MedxChart's initial commit `4b0b6da` carries `contracts/openchart-pin.yaml` AND
the nested `openChart` gitlink **in the same commit**, which is exactly the
"BOTH SHALL be changed in the SAME commit" discipline
`domain-descendant-boundary` states. The boundary was built to the rule before
the rule was written (2026-08-23 against a 2026-08-28 ratification); § 5's
follow-on is what will keep it there without a human re-reading two files.

## 9. This record's own capture, and what was corrected before it

**CAPTURE IS MERGE.** `record-immutability` forbids editing a `Status: record`
document after capture, and capture is the merge of the pull request that
establishes it. **Nothing is merged yet**, so editing these two records on the
branch is lawful — and saying plainly what was edited, and why, is the price of
doing it.

**The rebase reset record-immutability's baseline.** The first push was branch
`ratify/create-medxchart-overlay-boundary` (PR #607, head `edae4c66`).
`add-project-repo-schema` (PR #605) landed on `main` at `642ac147` minutes later
and moved the SAME live corpus pin, so #607 went conflicting; the repository
forbids force-pushing, so the work was rebased onto `642ac147` and re-pushed as
`change/ratify-create-medxchart-overlay-boundary` (PR #608, head `c39d29bc`).
Because the record had never been merged, it had never been captured, and the
rebase gave it a fresh baseline. The honest statement is therefore **not** that
the record was captured exactly once with the numbers it was measured at — it is
that **the record was RE-DERIVED PRE-CAPTURE.** What the rebase moved:

```console
$ git diff edae4c66 c39d29bc --numstat -- openspec/changes/create-medxchart-overlay-boundary/review/
15	7	openspec/changes/create-medxchart-overlay-boundary/review/ratification-2026-09-03.md
```

Twenty-two changed lines, all in `ratification-2026-09-03.md` § 6 and all of them
the corpus-pin readings following the rebase: `co_modified` 107 → 108 became
108 → 109, `active_co_modified` 20 → 21 became 21 → 22, the measured-by-exclusion
baseline 156 / 107 / 49 / 20 / 12 became 157 / 108 / 49 / 21 / 12, and a paragraph
was added saying the readings are stated against `main` at `642ac147`.
**`verification-2026-09-03.md` did not move in that commit, and that is the
defect this section records** — its `--all --strict` total SHOULD have moved with
the rebase and did not.

**Corrected in the fix commit that carries this section, before capture:**

1. **§ 2's total, `85 passed / 85 items` → `86 passed / 86 items`**, and the same
   figure in `ratification-2026-09-03.md`'s "Ratified baseline" line
   (`85/85` → `86/86`). `add-project-repo-schema` promoted one more item into the
   count while this branch was open.
2. **The `Captured:` header**, which still named the pre-rebase branch.
3. **§ 5's host-absolute-path sweep**, which printed `(no matches)` for a command
   this very file falsifies — re-run with `review/` excluded, and the exclusion
   explained rather than hidden.
4. **§ 8's two console blocks**, which were reformatted several files to a line
   and run without naming the repository they belong to (`git show --stat
   bed2a69` and `git -C xFactories/MedxChart log` both address the AGGREGATION,
   not this checkout) — re-read through the GitHub API, verbatim and runnable
   from any checkout, and every command in this record was executed from the
   page and its output compared before capture. **§ 4's `.gitmodules` read** was
   corrected in the same pass for the same reason: it printed two submodule
   entries under a command that returns thirteen, so the command now carries the
   `grep` that makes the two the whole of its output.
5. **Outside this file**, at their own sites: `tasks.md` 1.1's note, which
   contradicted § 8 above (Copilot round 1, finding 2 — taken); the
   sibling-citation tense in FOUR places, moved from the present indicative to
   the future obligation because at this head no sibling pull request has merged
   and that packet carries no reference to this delta; the `STANDING` clause and
   the archive→ratification trigger in the `domain-descendant-boundary` delta;
   the self-referential "the draft establishing act archives" scenario, reworded
   to a live obligation that names `tasks.md` § 5's evidence; `tasks.md` § 6.1,
   a NEW checkbox authored already ticked and now a plain report carrying no box;
   and the subject/body break in `design.md`'s quote of `386e7ee2`, marked as
   `[subject] / [body]` rather than left reading as one sentence. Line-number
   pointers inside `ratification-2026-09-03.md` were re-derived to match.

**THE COMMIT MESSAGE OF `c39d29bc` IS SUPERSEDED BY THE MESSAGE OF THE FIX
COMMIT.** It carries the pre-rebase validation block — `--all --strict 85/85`
and doc-health `6 critical, 5 error, 29 warning, 13 info` — and both are stale.
It cannot be amended: force-pushing is forbidden here, so the earlier message
stands in history unedited, and the measured figures are stated in the fix
commit's own message and in the pull request body instead of by rewriting it.
The measured figures at the fix commit are `--all --strict 86/86` and doc-health
`6 critical, 6 error, 29 warning, 14 info`, 0 new regressions, with zero findings
naming this change.

**AND THE FIX COMMIT'S OWN MESSAGE CARRIES ONE WRONG STATEMENT, CORRECTED HERE
BY THE SAME MECHANISM.** `998a31b8`'s closing "STANDING RACE" paragraph names
openxFactory **#599** as a pull request carrying a `## MODIFIED Requirements`
block that would move the live corpus pin ahead of this branch. **That is
false, and it was written without being measured.** #599 changes exactly one
file:

```console
$ gh api repos/opensoft/openxFactory/pulls/599/files --jq '.[] | "\(.status) \(.filename) +\(.additions) -\(.deletions)"'
modified openspec/changes/add-credential-escrow-checkout/tasks.md +25 -2
```

A `tasks.md` edit moves no reading of the sweep. **The race is real but it is
not #599's**, and it is wider than one pull request: any open change that ADDS a
packet or a spec delta moves `change_ids` / `active`, and any that adds or drops
a `## MODIFIED Requirements` block moves the co-modified and sole sets. Measured
against the open queue on 2026-09-03, seven pull requests touch a
`proposal.md` or a `specs/**/spec.md` under `openspec/changes/` — **#609** (this
change's own MedxPractice sibling), #595, #594, #593, #548, #491 and #447 — and
whichever of them lands first re-breaks this branch's pin. Nothing is done about
that here; the merge order is the convener's, and the remedy is the same rebase
this branch has already taken once.

**RE-DERIVED A SECOND TIME, 2026-09-03, AFTER MERGING `main` AT `6da1e1f5`
(#606, #593 AND #589 LANDED).** The race the paragraph directly above measures
ran while this pull request sat: `update-standards-body-current-publications`
(#593) merged and moved the same live corpus pin,
`add-project-repo-schema`'s ratification (#606) and the SPENT-state containment
hardening (#589) merged beside it, and this branch took the CATCH-UP MERGE of
`main` rather than a second rebase — the repository forbids force-pushing here.
Counts moved, and only counts:

- `openspec validate --all --strict` **86/86 → 87/87** (#593 added one ACTIVE
  change; this packet adds none).
- The live sweep ON THIS BRANCH'S OWN TREE, `157 / 109 / 48 / 22 / 11` →
  **`158 / 109 / 49 / 22 / 12`** (change ids / co-modified / sole modifiers /
  active co-modified / active sole), so the four-pin move this packet
  contributes now reads `co_modified` 108 → 109, `active_co_modified` 21 → 22,
  `sole_modifiers` 50 → 49 and `active_sole` 13 → 12 — the same +1 / +1 / -1 /
  -1 shape it always had, restated from main's new baseline, with `change_ids`
  and `active` still moving not at all.
- The MEASURED-BY-EXCLUSION baseline, which is `main`'s own reading,
  `157 / 108 / 49 / 21 / 12` → **`158 / 108 / 50 / 21 / 13`** — proved by moving
  `openspec/changes/create-medxchart-overlay-boundary/specs/domain-descendant-boundary/`
  aside on the merged tree and re-running the sweep, and independently confirmed
  by running the same sweep on `origin/main` at `6da1e1f5` itself, which prints
  the same three-and-two numbers.

Doc-health on the merged tree reads `6 critical, 6 error, 29 warning, 14 info`,
0 new regressions, with zero findings naming this change — and the report is
BYTE-IDENTICAL to the same run on `origin/main` at `6da1e1f5` once the checkout
directory name is normalised, so this branch introduces no finding at all.
`openspec validate create-medxchart-overlay-boundary --strict` is valid and
`python3 -m pytest tests/sequenced_after -q` is 118 passed against the re-derived
pin. **NOTHING ELSE IN EITHER RECORD CHANGED** — beyond those counts and the
`Captured:` header's naming of the second tree, no governance statement, no
evidence block, no console output, no finding and no citation moved.

**AND NO CAPTURE HAPPENED BEFORE THE MERGE.** Capture is the merge of PR #608
and PR #608 has not merged; the record is still uncaptured, which is the whole
reason this correction is lawful. The re-derivation is a SECOND pre-capture
correction, not an edit to a captured record.

**RE-DERIVED A THIRD TIME, 2026-09-03, AFTER MERGING `main` AT `2b0615da`
(#611, #614, #602 AND #604 LANDED).** The race the two paragraphs above
measure ran a third time while this pull request still sat: `main` moved
seven commits past `6da1e1f5`, of which #611 ARCHIVED
`declare-spent-bundle-state` — the very change whose AUTHORING the second
re-derivation measured — and #614, #602 and #604 landed beside it touching
neither the corpus pin nor this record. This branch took a SECOND CATCH-UP
MERGE of `main` rather than a third rebase — the repository forbids
force-pushing here. Counts moved, and only counts:

- `openspec validate --all --strict` **87/87 → 86/86** (#611 ARCHIVED one
  ACTIVE change without adding a replacement; this packet adds none and
  moves this total not at all).
- The live sweep, ON THIS BRANCH'S OWN TREE before this merge,
  `158 / 109 / 49 / 22 / 12` → **`158 / 109 / 49 / 21 / 12`** (change ids /
  co-modified / sole modifiers / active co-modified / active sole) — of the
  five readings, ONLY `active_co_modified` moves, by exactly one, because
  `declare-spent-bundle-state` was itself a co-modified ACTIVE change and its
  archive is the only event in the window that touches this sweep at all.
  This packet's own four-pin contribution is UNCHANGED IN SHAPE a third
  time: +1 `co_modified`, +1 `active_co_modified`, -1 `sole_modifiers`, -1
  `active_sole`, relative to whatever baseline `main` presents.
- The MEASURED-BY-EXCLUSION baseline, which is `main`'s own reading,
  `158 / 108 / 50 / 21 / 13` → **`158 / 108 / 50 / 20 / 13`** — proved by
  moving
  `openspec/changes/create-medxchart-overlay-boundary/specs/domain-descendant-boundary/`
  aside on the merged tree and re-running the sweep, and independently
  confirmed by running the same sweep on `origin/main` at `2b0615da` itself,
  which prints the same five numbers.

Doc-health on the merged tree reads `6 critical, 6 error, 29 warning, 14
info`, 0 new regressions, with zero findings naming this change — matching
the same run on `origin/main` at `2b0615da` in every finding and count, the
two differing only in one `staged-candidate-aging` trend line's day count (a
clock artifact of wall time between the two runs, not a corpus difference).
`openspec validate create-medxchart-overlay-boundary --strict` is valid and
`python3 -m pytest tests/sequenced_after -q` is 118 passed against the
re-derived pin. **NOTHING ELSE IN EITHER RECORD CHANGED** — beyond those
counts and the `Captured:` header's naming of the third tree, no governance
statement, no evidence block, no console output, no finding and no citation
moved.

**NO CAPTURE HAPPENED BEFORE THE MERGE — #611 (and the three after it) won
the race this time.** Capture is the merge of PR #608 and PR #608 has not
merged; the record is still uncaptured, which is the whole reason this
correction is lawful. The re-derivation is a THIRD pre-capture correction,
not an edit to a captured record.
