# Proposal Ratification: amend-neutral-product-pin-lockfile-first-line

Status: ratified
Kind: report
Decision date: 2026-09-10
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-10 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), verbatim: *"ratify as encoded"*,
given in session at approximately **19:53Z** and recorded on openxFactory PR
[#923](https://github.com/opensoft/openxFactory/pull/923#issuecomment-5624573662)
at **2026-09-10T19:53:02Z** (comment `5624573662`). **THE WORD IS A
MULTIPLE-CHOICE RULING**, given over a presentation that carried three
decisions with the recommendation stated first and `design.md` **D6** first of
all, because D6 could have ended the packet. **D6 IS RESOLVED AS AMEND, D1 AS
OPTION 1, AND D2 STANDS — EVERY ONE OF THEM THE OPTION THE PACKET ALREADY
ENCODED, SO THE WORDING STANDS UNCHANGED AND NOTHING WAS SUBSTITUTED.**

**THE WORD AND ITS RECORDING FALL IN THE SAME MINUTE, AND BOTH ARE STATED
RATHER THAN COLLAPSED.** Brett Heap gave the word in session at approximately
2026-09-10T19:53Z, four minutes after this lane's freeze comment of
2026-09-10T19:49:21Z put the question in `design.md`'s terms and reported the
bench closed at zero unresolved threads. It was recorded on the pull request at
19:53:02Z. Unlike this lane's previous ratification — PR #887, where the word
and its recording were seven hours apart — there is no gap here to reconcile:
the `Decision date:`, `approved_on`, this file's name and its sibling capture's
name are all **2026-09-10**. The recording comment is the citable artifact; the
session utterance is what it records, and this record says so in as many words
rather than presenting the recording timestamp as the moment of decision.

Ratified baseline: this change as committed on the branch
`change/amend-neutral-product-pin-lockfile-first-line` at the frozen bench head
**`0125741d`** — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/neutral-product-pin/spec.md` (**ONE `## MODIFIED` requirement**, *A
pinned artifact that resolves dependencies at install time carries a vendored
lockfile, and the install runs through it*, restated over canon byte-faithfully
with **ONE sentence replaced in place** under **ONE `Removed from canon`
marker** and **no scenario added or dropped**). The delta's normative units are
**byte-identical** to the tree Brett Heap ruled on: `git diff 0125741d --
openspec/changes/amend-neutral-product-pin-lockfile-first-line/specs/` is
**EMPTY**, and this ratification adds no line to it (§ 3, and
`review/verification-2026-09-10.md` § 10, which measures it rather than
asserting it).

**ONE MERGE FROM `main` SITS BETWEEN THE RULED TREE AND THIS ENCODE, AND IT IS
NAMED.** `origin/main` moved from `05c706d6` to `52e42be9` while the packet
awaited the word, so the branch was merged up at `45b02e31` BEFORE the
ratification commit, as its own commit. `52e42be9` ticks three boxes of another
lane's `relocate-review-authority-floor-mirror` `tasks.md` and touches no file
this packet writes; the merge resolved NO conflict. Every figure in the
verification capture is therefore taken on a tree that already carries current
`main`, and no merge-and-re-measure is owed at landing.

## 1. The two words, and exactly what each decided

### 1.1 The ratifying word — given ~2026-09-10T19:53Z, recorded 19:53:02Z

Brett Heap, 2026-09-10, verbatim:

> ratify as encoded

It is one utterance and it does two things at once. It **ratifies the packet**,
and it **answers the packet's own multiple-choice questions** — the three
choices `design.md` D6, D1 and D2 put and refused to take on his behalf. Both
halves are needed to read the act correctly:

- **The ratification half.** The packet was a DRAFT: `.openspec.yaml` carried
  drafting provenance with no approval pair, every document carried
  `Status: draft`, and `tasks.md` § 1 was entirely open and closed to the
  authoring lane by its own terms. This word is the operator's act that flips
  that, and it is the FIRST word to reach the packet's *content*.
- **The D6/D1/D2 half.** *"As encoded"* names a SIDE of each choice: the
  recommendation, not the alternative. Each of the three decisions was put as a
  ballot with the recommendation first, and the recording comment of 19:53:02Z
  states the resolution of each one by name rather than leaving *"as encoded"*
  to be interpreted later.

**The earlier word is the ORIGIN of the authoring and is NOT read as an
approval.** Brett Heap's *"do 882 packet"*, also of 2026-09-10, recorded in
this lane's CLAIMED comment on openxFactory
[#882](https://github.com/opensoft/openxFactory/issues/882#issuecomment-5623510674)
at 18:29:31Z, commissioned a lane to WRITE the remedy issue #882 proposes. It
ratified no wording and took no design decision, which is why the packet was
authored as a draft with no approval pair. That word stays recorded as the
origin in `proposal.md`'s `Proposed:` line, in `.openspec.yaml`'s
`proposed_by`, and in `tasks.md` § 1.1.

### 1.2 What the recording comment adds, and what it does not

The recording comment of 2026-09-10T19:53:02Z states the resolution of every
decision the packet carried, and it is quoted here because it is the artifact
this record cites:

> **"ratify as encoded"** — D6 resolved as A (AMEND, although the pinned 1.12.0
> binary does not report the first-line failure that PATH 1.2.0 reports); D1
> resolved as option 1 (re-order canon's own words so line one reads `The pin
> SHALL carry a VENDORED RESOLUTION where a pinned external neutral…` — no word
> added or removed); D2 stands (one `Removed from canon` marker, one name, no
> code span in its reason); D0/D3/D4/D5/D7 carried, none vetoed. All are the
> options the packet already encodes, so THE WORDING STANDS UNCHANGED.

**IT ADDS NO NEW RULE AND CHANGES NO WORDING.** Each clause names a decision
the packet had already encoded and put for veto, and records that it stands.
The comment also names the ratification encode as the next act, and the landing
and the archive as separate, later acts on separate, later words — which is why
this record exists and why this lane does not merge.

**ONE LETTERING NOTE, SO THE AUDIT TRAIL RESOLVES.** The ballot put to Brett
Heap lettered D6's two arms **A** (amend) and **B** (close #882 on the
measurement); `design.md` D6 numbers the same two arms **1** and **2**. The
recording says *"D6 resolved as A"*, and **A is D6's option 1 — AMEND**. D1's
options are numbered 1/2/3 in both the ballot and `design.md`, so *"option 1"*
means the same thing on both sides with no mapping needed.

## 2. Decision by decision, as ruled

| decision | what was put | ruled | effect on the packet |
| --- | --- | --- | --- |
| **D6** (put FIRST) | AMEND promoted canon, or CLOSE #882 on the measurement that the pinned CLI does not report the failure | **AMEND** (arm A = option 1) | The packet stands. A veto here would have WITHDRAWN it |
| **D1** (the veto point) | three wordings: (1) re-order canon's own words, (2) move only the line breaks, (3) the wording #882 floats | **OPTION 1** | The encoded sentence stands byte-for-byte; option 2 not substituted, option 3 stays refused |
| **D2** | one `Removed from canon` marker, one name, no code span in its reason — or none at all, under option 2 | **STANDS** | The written marker stands; it is owed BECAUSE option 1 was taken |
| **D0** | the corpus measurement, and the correction of #882's own scenario count | carried, not vetoed | 62 files / 641 requirements / 2 instances / 17-of-18 stand as measured |
| **D3** | why an OpenSpec change and not a `sed` of promoted canon | carried, not vetoed | The packet keeps its shape |
| **D4** | `code_surface: none`, measured not assumed | carried, not vetoed | Archive on landing plus the task list, on a separate word |
| **D5** | `sequenced_after: []`, the positive root claim | carried, not vetoed | No ordering declaration owed in either direction |
| **D7** | what is measured and deliberately NOT taken | carried, not vetoed | `repo-boundary-governance:34` stays residue; the heading is not edited |

### 2.1 D6 — ruled AMEND, and the measurement did not change the answer

This is the decision most worth reading twice, because the packet argued
AGAINST its own convenience to put it. `contracts/openspec-cli-pin.yaml` pins
`@fission-ai/openspec@1.12.0`; `.github/workflows/openspec-cli-pin-gate.yml`
runs `python3 scripts/validate-openspec-cli-pin.py --all --no-cache` through
the content-verified artifact; and **on that binary the specification PASSES**.
The failure issue #882 names is real on the **1.2.0** binary an engineer or an
agent has on `PATH`, and is reported by **no required check**. `design.md` D6
carries the controlled two-binary fixture that measures why: 1.2.0 reads only
the first body line and ERRORS; 1.12.0 reads the whole body and says nothing at
all about a keyword on line two.

So the ruling is *"amend promoted canon for a defect no required check
reports"*, taken deliberately, on three grounds that are not the red gate:
seventeen of the eighteen requirements in this one file already open with the
keyword; the 1.12 migration is unfinished, so the command this repository's own
notes tell an engineer to type still shows a red specification; and the cost is
two case flips and one comma. The alternative — publish the two runs, close
#882 on the measurement, leave ratified text alone — is retained in
`design.md` D6 as the record of what was put and declined.

**AND THE RULING DOES NOT MAKE ANY GATE GREEN AT THIS LANDING.**
`spec/neutral-product-pin` still fails `openspec validate --all --strict` on
the 1.2.0 binary at the ratified head, because a delta does not edit the
promoted specification. **THE ARCHIVE ACT IS WHAT CLEARS IT**, and the archive
is a separate act on a separate word. `review/verification-2026-09-10.md` § 2
measures that failure on the ratified tree rather than predicting it.

### 2.2 D1 — ruled OPTION 1, so nothing was re-written

Option 1 is what the delta already carried:

> The pin SHALL carry a VENDORED RESOLUTION where a pinned external neutral
> product is distributed as a published artifact whose installation RESOLVES
> dependency ranges — a lockfile in the format that product's own package
> manager consumes, committed beside the pin, addressed by a digest over its
> exact bytes recorded in the pin, together with the size of the tree it locks.

**The ruling is applied by leaving the text alone, and that is verified by diff
rather than asserted**: `git diff 0125741d -- openspec/changes/amend-neutral-product-pin-lockfile-first-line/specs/`
is EMPTY. Had option 2 been taken, the block would have been REPLACED with the
re-flow-only block and the marker DELETED; had option 3 been taken, the packet
would have owed a larger amendment reaching the requirement's heading and four
other sites. Neither was performed.

### 2.3 D2 — ruled STANDS, and it follows D1 rather than standing beside it

D2 is not independent of D1 and the packet said so before the ruling: under
option 1 the sentence's word order changes, so the sentence is a REPLACED unit
and exactly one `Removed from canon` marker is owed; under option 2 the family
sees no change at all and **no marker would have been owed**. Both branches were
proven with the family's own `derive_units` (`tasks.md` § 3.3) rather than
argued, so ruling D1 to option 1 decides D2's existence and the word confirms
its shape: one name, no code span in its reason, placed at the end of the block.

**THE MARKER'S SHAPE IS WHAT MAKES IT UNREPORTABLE UNDER EVERY GROUND THE
CORPUS HAS OR IS ABOUT TO HAVE**, which is a claim the bench tested rather than
took on trust. The existing second marker-defect ground fires on a code span
inside a reason that matches a unit the block does not carry, and this reason
carries **zero** code spans in 1,167 characters. The two grounds the ACTIVE
`amend-marker-declaring-nothing` (PR #908) adds fire on a marker naming a unit
the BLOCK itself adds, and on a `Removed from canon` marker carrying neither a
name nor a quoted span; this marker names exactly one CANON unit and carries
one name. Checked against that draft as well as against promoted canon, because
that packet may land first.

## 3. What this ratification moves, and what it does not

**MOVES** — all of it in ONE commit, so the status flip and the approval pair
never disagree:

- `proposal.md`, `design.md` and `tasks.md` go `Status: draft` →
  `Status: ratified`, each with **EXACTLY ONE** citation line (`Ratified:` in
  `proposal.md`, `Ratified by:` in the other two), which is what
  `ratified-provenance` counts.
- `.openspec.yaml` gains `approved_by` + `approved_on` **ADDED BESIDE** the
  drafting provenance, with `kind`, `id`, `reason` and `proposed_by`
  byte-unmoved — the addition-not-rewrite shape `add-drafted-proposal-origin`
  (issue #318) defined, and the shape the archive gate's origin-retention arm
  reads. **THE `origin:` BLOCK'S DRAFTING TENSE IS DELIBERATELY FROZEN**: it
  says the packet is a draft carrying no approval pair because that is what was
  true when it was proposed, and re-tensing it would destroy the very record
  the approval is added beside.
- `tasks.md` § 1 is ticked and names the word that ticked it; a new § 4.10
  names this tree's gate re-run and its capture.
- The README `## OpenSpec Records` row flips to its ratified form.
- These two records are captured beside the packet:
  `review/ratification-2026-09-10.md` (this file), which carries
  `Status: ratified` per `document-lifecycle`'s *A review record records a
  ratification*, and `review/verification-2026-09-10.md`, which keeps
  `Status: record` because its subject is the GATE RUN.

**DOES NOT MOVE** — measured in `review/verification-2026-09-10.md` § 10 by
diff, not asserted here:

- **No promoted canon.** Nothing under `openspec/specs/` is edited.
- **No delta byte.** The packet's own `specs/` directory is untouched.
- **No script, test, contract, schema, workflow or example.**
- **No ledger row**, and no other change's files — active or archived.
- **`tasks.md` § 5 stays OPEN**, and § 6.1 stays open on its own terms (an owed
  successor's box ticks when the successor is NAMED, and naming it means filing
  its issue, which is not this word's act).

## 4. The bench, as it stood when the word arrived

**THE BENCH WAS ALREADY CLOSED.** The lane's freeze comment of
2026-09-10T19:49:21Z recorded head `0125741d`, **three review threads, ZERO
unresolved**, and every check decided green except `pytest-suite`, then pending.
The word came four minutes later.

| thread | reviewer | tree | finding | disposition |
| --- | --- | --- | --- | --- |
| T1 `tasks.md` | Copilot | `0286c76c` | the per-change sweep ledger had no row for this change and `pin-openspec-cli-dependency-closure` was still `class: sole`, so `--ledger-diff` and the sequenced_after tests would report a missing/stale row | **TAKEN** at `44020530` — seeded through `scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#923'`, which wrote `196 rows, 2 moved by #923`. Resolved |
| T2 `.openspec.yaml` | Copilot | `0286c76c` | the recorded ideation-search command used `grep -rli` with an unescaped `\|`, which is a LITERAL in a basic regular expression, so the command did not test the stated alternation | **TAKEN** at `0125741d` — the record now carries `-E`, demonstrated on a three-line fixture where `grep -cE` returns 3 and `grep -c` returns 1. Resolved |
| T3 `README.md` | Copilot | `44020530` | the README row named an `ea34f22a` control where the packet's own documents named `05c706d6`, a reproduction hazard | **TAKEN** at `0125741d` — one control across the packet, with `05c706d6` named as the CONTROL and `ea34f22a` as the AUTHORING BASIS. Resolved |

**COPILOT'S LAST VERDICT ON THE RULED TREE IS AN APPROVAL, AND IT IS QUOTED
RATHER THAN CHARACTERISED.** Round 3, on `0125741d` at 2026-09-10T19:36:54Z:

> 🟢 Approval recommended — The changes are internally consistent, limited to
> adding a draft OpenSpec packet plus its index/ledger entries, and I did not
> find any concrete defects in the modified files.

Files reviewed 7/7, comments generated 0 new, review effort level Lite. **That
is a review of the DRAFT packet and it is not a ratification**: a bot's
approval recommendation says the tree is internally consistent, not that
promoted canon should be amended. The word of 19:53:02Z is what supplies the
second thing.

**CODEX NEVER REVIEWED THIS PACKET, AND THE ABSENCE IS RECORDED AS AN ABSENCE
RATHER THAN AS CLEARANCE.** One review was requested at 2026-09-10T19:27:24Z
and the connector answered ten seconds later, at 19:27:34Z, verbatim:

> You have reached your Codex usage limits for code reviews. You can see your
> limits in the [Codex usage dashboard](https://chatgpt.com/codex/cloud/settings/usage).
> To continue using code reviews, you can upgrade your account or add credits to
> your account and enable them for code reviews in your
> [settings](https://chatgpt.com/codex/cloud/settings/code-review).

No Codex review exists on any tree of this pull request. Sourcery produced a
reviewer's guide only (19:17:24Z) and raised no finding. The SonarCloud quality
gate passed (19:39:12Z).

## 5. What is owed AFTER this ratification, and by whom

**NOTHING IN THIS RECORD AUTHORIZES A MERGE OR AN ARCHIVE.** Two further words
are owed and neither has been given at the time of writing:

1. **THE LANDING WORD.** This lane encodes and freezes; it does not merge. The
   Rule 6 `LANDING`/`LANDED` post belongs to the landing lane on a separate
   landing word, which the recording comment names as a later act in as many
   words.
2. **THE ARCHIVE WORD.** `code_surface: none` and `target_release: none` mean
   this packet archives **ON LANDING plus its own task list** under
   `release-realization` rather than on merged-plus-green realization evidence —
   there is no code surface for evidence to be about. The archive is still a
   SEPARATE ACT on a SEPARATE WORD, performed through `python3
   scripts/proposal-support.py . archive
   amend-neutral-product-pin-lockfile-first-line --date <YYYY-MM-DD> --yes` and
   never a bare `openspec archive`. **AT THAT ACT, AND ONLY THERE:** the block
   is promoted into `openspec/specs/neutral-product-pin/spec.md` byte-identical
   to the delta and measured rather than asserted; `spec/neutral-product-pin`'s
   1.2.0 `--strict` failure clears, which is the ONE gate figure this packet
   changes and it changes it THERE; `tasks.md` § 5 and the still-open § 6.1 are
   ticked in the commit BEFORE the move, because `proposal-support` refuses any
   change whose `tasks.md` still matches `^- \[ \]` and has no bypass flag; and
   **openxFactory #882 closes**, `Closes #882` appearing on the archive pull
   request and on nothing else.

**THIS PULL REQUEST CARRIES NO CLOSING KEYWORD**, and no commit message on this
branch carries one, so `closingIssuesReferences` on PR #923 is `[]` — verified
through GraphQL and recorded in the pull request body. The body says
`refs #882`.
