# Proposal Ratification: create-medxpractice-overlay-boundary

Status: record
Kind: report
Decision date: 2026-09-03
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-03 by Brett Heap (openxFactory operator authority) —
in-session, verbatim: *"ratify both, 1 and 1"*.
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/medxpractice-overlay-boundary/spec.md` (THREE ADDED requirements,
NARROWED at this ratification, and NO `## MODIFIED Requirements` block) — with
`openspec validate --strict` and `--all --strict` green and the verification run
captured beside this file at `verification-2026-09-03.md`.

This is a CAPTURED record. **Capture is the MERGE of the pull request that
establishes it, not the first push**, and nothing is merged yet — so the
paragraph below is a correction made BEFORE capture, not an edit of a captured
record. After merge this record is written once and never edited.

**Corrected pre-capture, 2026-09-03, on the adversarial review of openxFactory
pull request #609.** The review found the packet sound and well-evidenced and
raised one P1 and several P2/P3 defects. They are fixed on this branch, before
capture, and they are listed here by the review's own numbering so that a later
reader can see WHAT changed between first push (`df8bd27a`) and the head this
record is captured at, rather than having to diff for it:

- **P1-1** — `specs/medxpractice-overlay-boundary/spec.md` Requirement 3
  restated, in its BODY, the placement path, the absolute remote and the gitlink
  that the sibling's MODIFIED delta already states normatively, while its own
  third scenario swore that "this change states no second version of that rule".
  The body now obliges only "the placement the cited delta ratifies, at the
  gitlink and remote form that delta records"; the three concrete values live in
  that requirement's scenarios as EVIDENCE. The scenario is now true.
- **P2-2** — the same file's Requirement 2 obliged where a developer's
  standalone `openPractice` checkout sits on a LOCAL FILESYSTEM, which no remote
  and no CI can settle and which this packet's own verification record § 9 says
  is not reproducible. It now obliges only the checkable half — the aggregation
  reaches `openPractice` ONLY through `MedxPractice`'s nested gitlink and no
  direct `xFactories/openPractice` entry exists — and its title, "The
  aggregation reaches openPractice only through MedxPractice", says so. The
  workspace-root sentence moved to `design.md` Decision 4 as a recorded LOCAL
  CONVENTION, and both scenarios were rewritten to the checkable form.
- **P2-3** — Requirement 1 listed the pin manifest's eight fields as though all
  were top-level. The live `contracts/openpractice-pin.yaml` in
  `opensoft/MedxPractice` at `d8d73195` NESTS six of them under `pin:`, which is
  why the scenario beneath already read `pin.revision`. The requirement now
  states the nested shape, and `tasks.md` 5.1's validator wording was corrected
  to match — a validator written to the flat shape would pass a file that does
  not exist.
- **P2-4** — § 3, P1-2 said "four" promoted requirements were relied on. It is
  FIVE, as the spec delta's head, `proposal.md` and § 4 of this record all say.
- **P2-5** — the answer this packet records to the sibling's open `tasks.md` 5.5
  did not say what it could not do. Both here and at `tasks.md` § 5 it now adds:
  this paragraph is the answer; the sibling's 5.5 checkbox cannot be ticked from
  this pull request and is left for the sibling's own pass to tick with a
  pointer here.
- **P2-6** — `tasks.md` 6.2 called an out-of-order merge "a broken reference,
  not a wrong rule". That understated it, and the note is corrected: merging
  this packet before the sibling would leave promoted
  `domain-descendant-boundary:80-85` still reading "still `Status: draft`" while
  this packet's ratified spec asserts the placement ratified — a ratified change
  CONTRADICTING promoted canon, which is the Explicit delta rule's own defect,
  repaired only by merging the sibling. The corrected note also states plainly
  that **nothing in the repository gates the order** — no `sequenced_after:` is
  owed, because the two packets co-modify nothing — so the order is protected by
  this prose, the pull request body and the coordinator, and by nothing else.
- **P3-7** — § 3, P1-2 cited `proposal.md:30-32` for a comment that exists only
  in the file AS AUTHORED. The comment is now quoted and the head line range for
  the correction is given instead.
- **P3-8** — three console blocks in `verification-2026-09-03.md` (§ 4's compare
  reading, § 5's `.gitmodules` reading, § 6's sweep) printed filtered or
  composite output as though it were raw. They now show the filter actually run
  or carry an excerpt marker, matching § 2's `…` convention.
- **P3-9** — the pull request body reported "13 info" from
  `scripts/doc-health.py`. The measured figure is **14**, on this tree and on the
  base branch alike. The body is corrected.
- **P3-10** — § 2's `ideation/staging/INDEX.md` quote range was `:2400-2405`; the
  quoted sentence spans `:2399-2403`.
- **P3-11** — Requirement 3's title named only the aggregation half of what its
  body obliges. It now reads "MedxPractice is aggregated at the cited placement
  and named by MedxFactory".

**Two consequences of the base branch moving, recorded rather than glossed.**
The sibling's own fix round landed while this one was in flight, so
`origin/change/ratify-create-medxchart-overlay-boundary` advanced from
`c39d29bc` to `4cb31b17` and was MERGED into this branch (no conflict) before
these fixes were written, so that the citations here are read against the
sibling's current delta. First: the sibling's ratification record now states
`86/86` where it once stated 85, which makes this packet's
`verification-2026-09-03.md` § 2 parenthetical about that number stale — it is
corrected there. Second: that delta's own head says the citation from this
packet "does not yet exist … that packet carries zero references to this file",
a sentence written against the SIBLING's head and true there. It is not edited
from here, because the sibling's delta has one writer and this is not it; it is
named so a reader who meets both files on `main` after both merge knows the
sentence is dated to its own branch rather than wrong about this one.

**RE-DERIVED AFTER MERGING `main` AT `0f1edc0e` (the sibling #608 landed at
15:11:52Z, after #611/#614/#602/#604): strict total 86/86 → 86/86; sweep
`157 / 109 / 48 / 22 / 11` → `158 / 109 / 49 / 21 / 12`, identical to `main`'s
own pin because this packet carries no `## MODIFIED Requirements` block;
nothing else in either record changed; no capture happened before the merge —
capture is the merge of #609.** This branch was retargeted from the sibling's
branch to `main` and `git merge origin/main` was taken directly (merge commit
`de975f81`) rather than a further catch-up merge of the sibling; the full
re-derivation, including the `README.md` resolution proof, is
`verification-2026-09-03.md` § 10.

---

## 1. The ruling, and what "1 and 1" meant

**"ratify both, 1 and 1."**

Three acts in six words, taken in session on 2026-09-03 over the two Medx
overlay-boundary packets after their review fixes were reported:

- **"ratify both"** — `create-medxchart-overlay-boundary` AND
  `create-medxpractice-overlay-boundary` (this packet) are ratified. Two
  packets, one word, two separate ratification acts recorded in two separate
  pull requests.
- **The first "1" — decision 1, option 1.** The question put was how to treat
  two descendant repositories that exist, are pinned, are aggregated, and carry
  no profile artifact of the product they pin. Option 1 was taken: **record both
  as REPORTED EMPTY BOUNDARIES**, explicitly NOT citable as precedent for
  creating more (§ 4 below), **and commission each descendant's pin validator
  plus required check as a BOUND FOLLOW-ON that gates ARCHIVE, not
  ratification** (§ 5 below).
- **The second "1" — decision 2, option 1**, and THIS is the packet that
  performs it. The question was whether this change's spec delta should stand as
  authored or be narrowed. Option 1: **narrow it to what is genuinely
  MedxPractice-specific and CITE the placement delta the MedxChart ratification
  carries**, so that one requirement has one writer. § 3, P1-2 below is the
  execution.

**What the ruling did not do.** It did not merge this pull request, it did not
archive the change, it did not build the validator § 5 commissions, and it did
not move a contract byte — `contracts/` is untouched by the ratified diff, no
bundle is cut, and no release tag is owed. Ratification authorizes; it does not
perform.

## 2. The standing this packet had before today, and why it needed fixing

**Admission is not ratification.** On 2026-08-25, openxFactory **PR #345** —
"Admit the two medx boundary packets: origin metadata only, not a ratification"
— merged at **`f90f3a0872e7b310ed63abb9d1dbb92ac7638635`**
(2026-08-25T14:04:20Z), writing this packet's `.openspec.yaml` origin block on
Brett's word *"admit the two medx boundary packets"*. That block says so in its
own text: "THIS IS AN ADMISSION INTO THE PROPOSAL QUEUE, NOT A RATIFICATION OF
CONTENT … the packet remains `Status: draft`, it carries no ratification
citation, and none is owed … Whether this change's content is ratified is a
separate act that has not happened."

Today is that separate act. **`.openspec.yaml` IS NOT TOUCHED BY IT.** It
records the 2026-08-25 admission, `release-realization`'s origin-retention rule
requires the archive gate to find that declaration unchanged, and mutating it
after ratification is a refusal at the gate. The origin stands as written —
including its "NO STAGING ORIGIN IS CLAIMED: none exists", which remains true.

**openxFactory issue #318** — "A drafted-but-unapproved change packet has no
lawful origin shape — every draft is a proposal-origin error until it is
approved" — is the general question this packet's history raised, alongside its
sibling's. It remains **OPEN and unclaimed** (no assignee, no label) as of this
ratification. This record does not close it, does not answer it, and does not
treat two packets' ratification as its resolution: #318 is about every draft in
the corpus, and two packets leaving the draft state settles nothing for the
rest.

**And one recorded conflict IS discharged by this act, in full.**
`split-openxwallet-repo`'s staged record carries, under "Conflicts recorded, not
resolved", this line at `ideation/staging/INDEX.md:2399-2403`: *"TWO of the
three descendant precedents are NOT ratified in this repo — checked 2026-08-26,
`create-medxchart-overlay-boundary` and `create-medxpractice-overlay-boundary`
both stand `Status: draft`, leaving DTN-022's openAvatar ruling as the single
ratified member of the precedent table."* The sibling's ratification discharged
HALF of that conflict; **this one discharges the rest.** As of today the
precedent table has three ratified members rather than one. The INDEX line is
NOT edited by this change — it is a dated observation of 2026-08-26 and was true
when written; a captured conflict is discharged by the act that answers it and
by a record naming the discharge, not by rewriting the observation.

## 3. The review's findings and how each was disposed

Every finding was **re-verified live by this lane before it was written down** —
the re-verification is `verification-2026-09-03.md`, and where re-verification
changed the finding's shape the record says so. Disposition, one line each, with
the file and line where the fix landed.

### P1 — blocking

- **P1-1, no realization front-matter.** `proposal.md:1` was a bare
  `Status: draft` with no `---` block at all, so NEITHER declaration
  `release-realization` requires existed — this is not a wrong value being
  corrected, it is two missing declarations being made.
  **FIXED**: `proposal.md:1-7` now carries a front-matter block.
  `code_surface` (`:2`) names the real THREE-repository surface with its actual
  paths and commits — `opensoft/MedxPractice` created at `d8d73195`;
  `opensoft/xFactory`'s `.gitmodules`, gitlink, `README.md`, `CLAUDE.md` and
  `project-register.yaml` at `3a365206`; MedxFactory `README.md` at `ccd40789`
  — and states plainly that the descendant pin validator and its required check
  DO NOT YET EXIST, with the API readings that establish it.
  `target_release: implemented` (`:3`) is true and evidenced: MedxPractice's
  `main` IS the aggregation's gitlink. The `Status:` (`:4`) reads `ratified` and
  the citation line (`:6`) is the record-citing spelling.
- **P1-2, the spec delta restated promoted policy — NARROWED under decision 2
  option 1.** The three ADDED requirements as authored restated
  `domain-descendant-boundary` in differing words: "MedxPractice owns the
  branded practice-operations boundary" restated **A domain consumes a neutral
  product through a descendant repository**
  (`openspec/specs/domain-descendant-boundary/spec.md:6-16`) and **A descendant
  carries profile, never fork** (`:55-62`); "The upstream revision is immutable
  and reviewable" restated **A descendant pins the product by commit, twice**
  (`:30-41`) near-verbatim; "Aggregate and domain references use MedxPractice"
  restated **A descendant is placed at a ratified placement** (`:76-85`).
  Accidental restatement of promoted policy in differing words is a DEFECT under
  `document-lifecycle`'s **Explicit delta rule**
  (`openspec/specs/document-lifecycle/spec.md:149-161`), not a strengthening of
  it. **FIXED — the delta is narrowed, not deleted.** Three requirements
  survive, each keeping what only this packet can say:
  **MedxPractice pins openPractice at one named revision**
  (`specs/medxpractice-overlay-boundary/spec.md:52`) — the IDENTITY of the pin
  (`opensoft/openPractice` at `9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`,
  `contracts/openpractice-pin.yaml`, `kind: medxpractice_openpractice_pin`,
  `relationship: pinned_upstream_composition`) plus the PRIVATE-over-PUBLIC
  visibility asymmetry that is the boundary's reason for existing;
  **The aggregation reaches openPractice only through MedxPractice** (`:99`) —
  the single route the relocation left behind, which NO promoted requirement
  covers; and **MedxPractice is aggregated at the cited placement and named by
  MedxFactory** (`:134`) — the aggregation's carrying of this descendant and
  MedxFactory's naming of it, with the placement RULE cited rather than
  restated and the concrete values held in the scenarios as evidence. (Those
  last two titles and bodies were narrowed FURTHER in the pre-capture fix round
  — see the "Corrected pre-capture" paragraph at the head of this record.) The
  file's head (`:1-48`) records the narrowing, maps each retired requirement to
  the promoted one it restated, and names ALL FIVE promoted requirements this
  change RELIES ON WITHOUT MODIFYING; `proposal.md:64-79` says the same in the packet's own
  Capabilities section, which is where the Explicit delta rule's reader will
  look.
  **The Modified Capabilities section AS AUTHORED — a bare
  `<!-- No existing openxFactory capability requirements change. -->` — is
  CORRECTED rather than deleted** (the correction is `proposal.md:48-63` at this
  head; the comment it replaced survives only in the pre-ratification file, so it
  is quoted here rather than cited by a line range that no longer holds it): the
  placement requirement DOES change, that modification is carried by
  `create-medxchart-overlay-boundary` at
  `openspec/changes/create-medxchart-overlay-boundary/specs/domain-descendant-boundary/spec.md`,
  and **this change cites it and carries no `## MODIFIED Requirements` block of
  its own**. ONE REQUIREMENT, ONE WRITER.
- **P1-3, no validator, no workflow, no required check — decision 1 option 1.**
  Re-verified today rather than assumed:
  `gh api repos/opensoft/MedxPractice/actions/workflows` returns
  `{"total_count":0,"workflows":[]}`, and `gh api repos/opensoft/MedxPractice/rulesets`
  returns exactly two, BOTH `"source_type":"Organization"` — "Copilot
  Auto-Review All PRs" (`8981805`) and "Require Code Owner Review"
  (`18834180`) — neither of which requires a status check. **FIXED as an
  UNCHECKED BOUND FOLLOW-ON**: `tasks.md` § 5 (`:73`), five items on the sibling's
  shape and on LedgerxWallet's live pattern — the fail-closed
  `tests/validate_pin.py` (5.1), the `pin-validation` workflow (5.2), the
  `[OPERATOR]` ruleset that makes the check REQUIRED (5.3), the realization
  evidence that opens the archive gate (5.4), and the SSH-URL limitation to
  close while that tree is open (5.5, which gates nothing). **ARCHIVE WAITS ON
  IT; RATIFICATION DOES NOT.**
  **AND IT ANSWERS THE SIBLING'S OPEN 5.5** (`tasks.md:92`): MedxChart's
  `tasks.md` 5.5 asks whether MedxPractice takes the same validator, and the
  answer recorded here is YES — the two descendants carry the identical two-pin
  shape and differ only in the product name and the four literal values that
  follow from it, so one validator shape covers one pin shape. The question is
  answered in the packet that owns the repository it is about. **This paragraph
  is the answer; the sibling's 5.5 checkbox cannot be ticked from this pull
  request and is left for the sibling's own pass to tick with a pointer here.**

### P2 — substantive

- **P2-4, placement sequencing.** **RECORDED** at § 7 below and at
  `tasks.md` 6.2 (`:155`): this change ratifies SECOND, after
  `create-medxchart-overlay-boundary`; the placement delta lives THERE; and the
  archive order is MedxChart first. The reason is ownership rather than
  courtesy — the amendment must be on the base branch before the packet citing
  it can be read against it.
- **P2-5, the empty boundary.** **RECORDED** at § 4 below and at `tasks.md` 6.1
  (`:138`), with the five-entry file list that makes the report checkable rather
  than assertive.
- **P2-6, the pin is two commits behind upstream.** Re-verified:
  `opensoft/openPractice`'s `main` is
  `0ec9fca72ecf493e2520e676387f0c3f327cc6e6`, the pin is
  `9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`, and the compare API reports the
  pin two commits behind (`0205901b` "Document reimbursement retention
  control", then the `#1` merge). **DISPOSED AS A NOTE, NOT A TASK**, at
  `design.md:37-49`: the distance is what an immutable pin IS, an upstream
  commit reaches this composition only when a change moves the gitlink and the
  manifest together under the cited same-commit rule, and **no re-pin runbook
  exists in this repository today** — which is stated so a later reader neither
  reads the distance as neglect nor invents a procedure for closing it. The
  sibling recorded no re-pin task either, so the two packets stay consistent.

### P3 — evidence precision

- **P3-7, the SSH URL for a public upstream.** MedxPractice's own `.gitmodules`
  reads `url = git@github.com:opensoft/openPractice.git` for an upstream that is
  PUBLIC, so an anonymous recursive clone cannot initialize the nested checkout.
  **RECORDED as a known limitation** at `design.md:88-101`, with its cost named
  (small — MedxPractice is itself private, so every clone of it is already
  authenticated) and NOT changed from here: the fix is a commit in
  `opensoft/MedxPractice`, and it is carried to `tasks.md` 5.5 so the next act
  on that tree does not rediscover it.
- **P3-8, `3a365206` bundled a gitlink no task accounts for.** The aggregation's
  landing commit carries seven paths; `xFactories/MedxFactory` is task 3.2's own
  pin-sync, but **`openxFactory` moved `f879070f` → `a3248684` in the same
  commit and no task in this list explains it**. **DISCLOSED by an append-only
  note** at `tasks.md` 2.3 — the checkbox is not unticked and the task text is
  not edited. The note also states that the "remove any direct public
  openPractice aggregate entry" half was a NO-OP by construction: the
  aggregation never carried such an entry, so the commit adds one and removes
  none.
- **P3-9, the README row.** **REWRITTEN** to RATIFIED 2026-09-03 with the ruling
  quoted, the narrowing and the citation named, the sequencing after MedxChart
  stated, the empty-boundary standing reported, and the archive gate named.
- **P3-10, the `.gitkeep` asymmetry** (MedxChart carries two `openspec/`
  placeholders, MedxPractice none). **NOT ACTED ON, deliberately.** It changes
  nothing either boundary asserts, and adding placeholders to make two empty
  trees look alike would be cosmetic work on a repository this packet does not
  otherwise edit. It is named here so its absence from the fix list is a
  decision on the record rather than an oversight.

### One thing the review did not raise, fixed because the ratified text made it a contradiction

`design.md`'s third risk read *"Relative aggregate submodule URLs can resolve
differently in local configuration → sync local submodule configuration and
verify the published remote URLs"* — and **that risk materialized**. The entry
landed at `3a365206` as `url = ../MedxPractice`; a relative URL resolves against
whatever cloned the SUPERPROJECT, so on the HTTPS-cloned nightly runner it
became a plain `https://` URL the `git@`-only token rewrite never touches, and
every nightly from 2026-08-24 died at the clone until `opensoft/xFactory`
`386e7ee2` (2026-08-25T19:13:51Z) normalized BOTH Medx entries. Leaving the risk
open while `specs/medxpractice-overlay-boundary/spec.md` now OBLIGES the
absolute form would have been a contradiction inside one packet, which is the
Explicit delta rule's own concern. Recorded at `design.md:73-86`, citing the
sibling's Decision 2 for the full reversal narrative rather than restating it.

## 4. The empty-boundary position

**MedxPractice is a REPORTED EMPTY BOUNDARY, and this ratification does not make
it a precedent.**

`domain-descendant-boundary`'s fifth requirement
(`openspec/specs/domain-descendant-boundary/spec.md:103-120`) says a descendant
"SHALL NOT be created before the domain tree carries at least one artifact of
the product's profile kind … so that an empty boundary is never stood up as
precedent", and its last scenario says that where one exists anyway, "it is an
empty boundary, and it is reported rather than cited as precedent for creating
more."

MedxPractice's entire tracked tree at `d8d73195` is FIVE entries — `.gitmodules`,
`AGENTS.md`, `README.md`, `contracts/openpractice-pin.yaml`, and the
`openPractice` gitlink. **Composition metadata only. Zero openPractice profile
artifacts.** It is also a ONE-COMMIT repository: `d8d73195` is its whole history,
and that commit carries the pin manifest AND the nested gitlink together, which
is exactly the same-commit discipline the rule states — built to the rule on
2026-08-23, five days before the rule was ratified.

So the position taken under decision 1 option 1 is:

1. **Both boundaries are REPORTED**, here and at `tasks.md` 6.1, with the file
   list that makes the report checkable rather than assertive.
2. **Neither is citable as precedent for creating another descendant.** Anyone
   proposing a new `<Domainx><Product>` repository meets the lazy-creation rule
   on its own terms and gets no help from these two.
3. **The PLACEMENT is what is ratified, and it is a different requirement.**
   Requirement 4 (where a descendant is aggregated) and requirement 5 (when a
   descendant may be created) are separate obligations; ratifying the first
   grants nothing under the second — and this packet does not even ratify the
   first, it cites the sibling that does.
4. **Neither boundary is refused, and the reason is chronology, not
   indulgence.** Both were created on 2026-08-23; the rule that would have gated
   them was ratified with `split-openxwallet-repo` on 2026-08-28. Reporting is
   what the rule itself prescribes for the state it finds.

## 5. The bound follow-on, which gates ARCHIVE

**Commissioned by this ruling; ratification does not wait on it, ARCHIVE does.**
`tasks.md` § 5, five items, four of them unchecked and gating.

The reason is that the pin agreement this packet rests on is verified **by a
human reading two files**, and nothing re-reads them.
`domain-descendant-boundary`'s pin rule requires that when a descendant's
gitlink and pin manifest disagree, "the descendant's own validator REFUSES the
tree rather than preferring either, because an unanswerable question is never an
implicit pass." **`opensoft/MedxPractice` has no such validator** — no
workflows at all, and two organization-sourced rulesets neither of which
requires a status check. Until it does, this boundary is asserted rather than
enforced, and a silent divergence would be found by whoever next happened to
look.

The pattern is LedgerxWallet's, which is live and recorded at
`docs/domain-neutralization-candidate-register.md:812-820`:
`tests/validate_pin.py` with four fail-closed checks, the REQUIRED
`pin-validation` check, ruleset `21701436`. § 5 commissions the same three parts
— the validator (5.1), the workflow (5.2), and the ruleset, marked
**`[OPERATOR]`** (5.3), because creating a branch-protection ruleset is Brett's
console act and an agent-reported "ruleset created" without it is not evidence.
5.4 records the ruleset id and one green required run as realization evidence
and is what opens the archive gate. 5.5 carries the SSH-URL limitation and gates
nothing.

**This change therefore stays ACTIVE after merge**, which is also what
`release-realization` requires of a change with a code surface: it archives only
on merged code plus green realization evidence, never on landing.

## 6. What this pull request changes, and what it does not

**Changes.** `proposal.md` (a front-matter block where there was none, the
citation line, the Capabilities section rewritten so the narrowing and the
citation are stated where a reader looks, the Impact bullets measured);
`design.md` (the re-pin note, the reachability risk discharged, the relative-URL
risk recorded as materialized-and-reversed, a Known limitations section, and —
added in the pre-capture fix round — the workspace-root layout recorded at
Decision 4 as a LOCAL CONVENTION rather than obliged as an uncheckable SHALL);
`specs/medxpractice-overlay-boundary/spec.md` (NARROWED — three requirements
kept, each rewritten to what only this packet can say, with the retired
restatements mapped to the promoted requirements they restated); `tasks.md`
(append-only notes at 2.3, 3.1, 4.1 and 4.2, plus §§ 5 and 6); this record and
`verification-2026-09-03.md`; and the `README.md` "OpenSpec Records" row.

**Does not change.** `.openspec.yaml` — see § 2. **No `## MODIFIED Requirements`
block anywhere in this packet** — the placement amendment is the sibling's, by
design. No existing `tasks.md` checkbox is flipped in either direction; every
task edit is an append. No promoted specification is edited directly. No
contract byte, schema, manifest row, digest, or release tag moves. And
`tests/sequenced_after/test_sweep.py` is **NOT touched**: the corpus pin does not
move for this ratification, because this packet's delta is ADDED-only both
before and after the narrowing and its capability
`medxpractice-overlay-boundary` has exactly one writer — so the change was a
SOLE modifier before today and is a SOLE modifier after, and `co_modified` /
`active_co_modified` / `sole_modifiers` / `active_sole` / `change_ids` all read
what the sibling's ratification left them reading. That is verified rather than
assumed, in `verification-2026-09-03.md` § 6, and it is the CONTRAST with the
sibling worth noticing: adding a MODIFIED block moved four readings there,
narrowing an ADDED-only delta moves none here.

## 7. Sequencing, and the lane

**THIS CHANGE RATIFIES SECOND.** `create-medxchart-overlay-boundary`'s
ratification pull request (openxFactory **#608**) comes first and merges first;
this pull request is STACKED on that branch and retargets to `main` after it
merges. **The placement delta lives THERE, not here**: the sibling's
`specs/domain-descendant-boundary/spec.md` names `xFactories/MedxPractice` at
gitlink `d8d73195609df3b567643a7bf1252eac352d9996` among its realized
placements, and this packet cites it by path. **Archive order follows merge
order: MedxChart archives first**, and each archives only when its own § 5
follow-on produces green realization evidence.

**This is now FACT, not plan: #608 merged 2026-09-03T15:11:52Z, merge commit
`0f1edc0e`, and this pull request was retargeted to `main` and merged with it
after that landing.**

**Lane claim.** This pull request is authored and carried by lane
`openxfactory-max001` (max-001, session `5e783e4d`) **through merge**. The lane
AUTHORS and does NOT MERGE: the merge of this pull request is the convener's own
act, as is the merge of the sibling, and neither is performed by this record.
