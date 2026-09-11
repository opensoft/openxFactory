# Proposal Ratification: amend-repo-boundary-governance-scope-first-line

Status: ratified
Kind: report
Decision date: 2026-09-11
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-11 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), verbatim: *"ratify as encoded"*,
given in session as a MULTIPLE-CHOICE ruling and recorded on openxFactory PR
[#937](https://github.com/opensoft/openxFactory/pull/937#issuecomment-5628461153)
at **2026-09-11T02:18:13Z** (comment `5628461153`). **THE WORD IS A
MULTIPLE-CHOICE RULING** over the three decisions `design.md` put for the
owner — **D6**, **D1** and **D2**, presented with the recommendation first and
D6 first of all — and it takes the recommendation on each: **D6 = A (AMEND)**,
**D1 = option 1**, **D2 as written in both halves**. **EVERY ONE OF THOSE IS
THE OPTION THE PACKET ALREADY ENCODED, SO THE DELTA'S WORDING STANDS UNCHANGED
AND NOTHING WAS SUBSTITUTED, RESTORED OR DELETED.**

**THE WORD AND ITS RECORDING ARE THE SAME MINUTE, AND THE DATE IS STATED RATHER
THAN INFERRED.** Brett Heap gave the word in session at 2026-09-11T02:18Z and it
was recorded on the pull request at 2026-09-11T02:18:13Z; the recording comment
is the citable artifact and it names the same instant as the utterance. Both
fall inside one UTC day, so the `Decision date:`, `approved_on`, this file's
name and its sibling capture's name are all **2026-09-11**, with no boundary to
reconcile. In the lane's local zone that instant reads 2026-09-10 22:18, which
is why some in-session shorthand of the day calls it "the word of 2026-09-10";
**the record uses UTC throughout, as the packet does** — `proposed_on`,
`created`, `design.md`'s `Date:` and the origin word of 2026-09-11T00:42Z are
all UTC, and mixing zones inside one packet is exactly the reconciliation
problem this paragraph exists to foreclose.

## 1. The two words, and exactly what each decided

**THE ORIGIN WORD IS NOT AN APPROVAL AND IS NOT READ AS ONE.** Brett Heap's word
of **2026-09-11T00:42Z**, verbatim *"do 915 and 931, land each when green"*,
recorded in this lane's CLAIMED comment on openxFactory issue #931, commissioned
this AUTHORING and pre-gave the LANDING word for whatever head is ratified and
green. It named no wording, resolved none of the three decisions and admitted no
text to canon. `.openspec.yaml`'s `origin:` block was authored under it in the
lawful unapproved shape `add-drafted-proposal-origin` (issue #318) defined —
`proposed_by` + `proposed_on`, no approval pair — and **that block is kept
byte-unmoved by this ratification**, its drafting tense included.

**THE RATIFYING WORD IS THE SECOND ONE.** *"ratify as encoded"*, 2026-09-11,
given over this packet's own `design.md`. It is Brett Heap's act and not the
authoring lane's. What it moves is recorded in § 3.

**THE PRECEDENT IS A THIRD THING AND IT DECIDED NOTHING HERE.** The identical
phrase *"ratify as encoded"* was given on 2026-09-10 over
`amend-neutral-product-pin-lockfile-first-line` (PR #923, recorded
2026-09-10T19:53:02Z) for ONE requirement of `neutral-product-pin`. `design.md`
D6 quotes it as PRECEDENT ONLY and says why it is not entailment: of its three
grounds, two read differently here — the convention inside the file is ten to
one rather than seventeen to one, and the cost is four words ADDED to ratified
canon rather than two case flips and a comma. The question was therefore asked
FRESH for this requirement, and was answered by its own word.

## 2. D6 as it was put, and D6 as it is resolved

**D6 WAS PUT FIRST BECAUSE IT COULD END THE PACKET**, and the asymmetry it turns
on is stated here rather than softened: the defect this packet answers is REAL
on the OpenSpec CLI at **1.2.0** and is reported by **no required check**.

| binary | on `spec/repo-boundary-governance` | exit |
| --- | --- | --- |
| 1.2.0 on `PATH` | `✗ [ERROR] requirements.1.text: Requirement must contain SHALL or MUST keyword` | 1 |
| 1.12.0, pinned and content-verified | `Specification 'repo-boundary-governance' is valid`, six INFO notes | 0 |

openxFactory validates through the pinned entrypoint, as `neutral-product-pin`'s
own promoted requirement obliges, so the failing reading is the one no gate
performs. **THE TWO OPTIONS WERE AMEND ANYWAY, OR CLOSE #931 ON THE
MEASUREMENT**, and option 2 was written out with its case made at its strongest
— the remedy costs four added words rather than none, and the 1.12 migration
will retire the reading that makes the failure visible at all, so the question
expires on its own.

**RESOLVED: OPTION A — AMEND.** The packet is not withdrawn, D1 and D2 are
reached rather than falling with it, and the three grounds `design.md` records
are what the ruling was given on: **(a)** ten to one inside this one file, with
all ten compliant first lines at 79 characters or fewer; **(b)** an unfinished
1.12 migration in which every engineer and agent who types the command this
repository's own notes prescribe meets a red specification and must be told it
is not theirs; **(c)** this is the corpus's LAST instance, so taking it empties
the class rather than leaving one standing exception.

**WHAT D6 DOES NOT DECIDE.** It rules this requirement, not a standing rule. A
later first-line question is asked fresh again, and the ruling of 2026-09-11 is
available to it as precedent on the same terms this packet used its own
predecessor's.

## 3. D1, D2 and the carried decisions — and why the wording stands

**D1 — THE VETO POINT — IS RESOLVED AS OPTION 1**, the recommended and ENCODED
wording:

> The following install repositories SHALL be scoped to subsystem install,
> operations, backup, restore, upgrade, verification, and disaster recovery:
> `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`,
> and `OmniWorker-Install`.

First body line **72 characters**, `SHALL` at word five. **Four words added, none
removed**; the five names keep canon's order, spelling and serial comma.

**BECAUSE OPTION 1 IS WHAT THE PACKET ENCODED, THE RULING IS APPLIED BY LEAVING
THE TEXT ALONE, AND THAT IS VERIFIED BY DIFF RATHER THAN ASSERTED.** The
ratification commit touches no file under
`openspec/changes/amend-repo-boundary-governance-scope-first-line/specs/`; the
verification capture beside this record states the diff. The two declined
options are retained in `design.md` D1 as the record of what was put and
declined, not as work owed: option 2 (re-flow only, 0 uncarried / 0 added, no
marker, a 108-character first line) was NOT substituted, and option 3 (the
counted subject issue #931 itself floats) was REFUSED at design time and stays
refused.

**D2 — BOTH MARKER DECISIONS — STANDS AS WRITTEN.** **D2a**: ONE
`Removed from canon` marker for the replaced sentence, ONE name, no code span in
its reason, at the END of the block — written, and kept. **D2b**: the marker
this requirement INHERITS from `refresh-install-repository-enumerations` is NOT
carried forward, on canon's own *"A marker is NOT a carriage unit, in either
direction"* and on a four-times-repeated precedent. Neither half was vetoed, and
this ratification re-derives neither count: the `derive_units` figures in
`tasks.md` § 3.3 are the authoring measurement and the ruling left the block
alone.

**D0, D3, D4, D5 AND D7 WERE CARRIED BESIDE THEM AND NONE WAS VETOED.**

- **D0 — the measurement taken before the design**, on the clone of `main`
  `114d6e3d` this packet was authored against: **62** promoted spec files,
  **641** `### Requirement:` headings across them, and **exactly ONE** whose
  first body line carries neither `SHALL` nor `MUST` — `repo-boundary-governance`
  index **1**, heading `:34`, body `:35`. That measurement is what makes ground
  (c) a fact rather than a hope, and it stands as taken.
- **D3** — why an OpenSpec change and not a patch to promoted text.
- **D4** — `code_surface: none`, `target_release: implemented`. The
  `target_release` value was corrected from `none` to canon's own vocabulary at
  the bench, on a Copilot finding, and the corpus-wide divergence it exposed is
  named as residue in `tasks.md` § 6.8 rather than swept.
- **D5** — `sequenced_after: []`, the positive root claim, with the sibling
  search pasted rather than summarized.
- **D7** — what is deliberately NOT taken: the requirement's heading, the
  sibling index requirement's count of five, the marker-carriage question as a
  general `doc-health` rule, the two dispositioned findings the pinned run
  names, `prepare-openspec-1-12-readiness`, and the other three enumerations
  `refresh-install-repository-enumerations` touched.

## 4. The bench, and what it settled before the word arrived

**THE BENCH WAS CLOSED WHEN THE WORD ARRIVED.** Five review threads across four
rounds, **ALL FIVE TAKEN, ZERO UNRESOLVED**, frozen at `d50a1251` — the head the
word was given over. The freeze comment for that head is PR #937's
`issuecomment-5628708162`; it supersedes the earlier freeze of 01:57:37Z, which
was posted at `9898889e` and outrun by two fix commits.

| # | raiser | subject | disposition |
| --- | --- | --- | --- |
| T1 | Copilot | the per-change sweep ledger row was not seeded when the box was ticked | **TAKEN** — seeded by the sanctioned tool in `a99f1703`; `--ledger-diff` measured red (exit 1, one missing row and seven derived-total mismatches) then green (exit 0, 198 rows) |
| T2 | Copilot | `target_release: none` is outside `release-realization`'s vocabulary | **TAKEN** — `implemented` declared in `9898889e` across front matter, `tasks.md` and `design.md` D4; the 33-of-180 corpus divergence named as residue |
| T3 | Copilot | the README active row claimed no test is touched | **TAKEN** — `9898889e`; the ledger named as a GENERATED REGISTRY in all three places the claim appears |
| T4 | Copilot | the same inventory claim in `tasks.md` § 3.8 | **TAKEN** — `9898889e` |
| T5 | Copilot | *"no consumer's conformance outcome changes"* is too broad beside D6 | **TAKEN** — `e9a4986b`; split into repository conformance (unmoved in either direction) and the PARSER'S VERDICT (which moves, at the archive, on purpose) |

**COPILOT'S LAST VERDICT ON `d50a1251` IS "Needs a closer look" WITH ZERO NEW
COMMENTS**, submitted 2026-09-11T02:32:11Z, on the ground that *"The draft has
coordinated governance and lifecycle decisions, with terminology nits still
unresolved."* **THAT IS THE STANDING OF A PACKET AWAITING A RATIFICATION WORD,
AND IT IS WHAT THIS WORD SUPPLIES** — the verdict names no defect in the delta
and opened no thread.

**ONE THING IS REFUSED AND RECORDED RATHER THAN DROPPED.** Three SUPPRESSED
comments accompany that verdict and they are ONE nit in three places:
`README.md`, `.openspec.yaml` and `tasks.md` describe the pinned 1.12.0 run as
coming from *"the required gate"*, while `.github/workflows/openspec-cli-pin-gate.yml`
says in its own header *"NOT A REQUIRED CHECK, and saying so is part of the
change rather than an omission from it."* **COPILOT IS RIGHT ON THE FACT.** It is
refused at this head on custody grounds, all three stated: (1) the instance in
`.openspec.yaml` is a line of the `origin:` block, which
`add-drafted-proposal-origin` fixes at authoring and which this ratification
keeps byte-unmoved — and Copilot's own ask is CONSISTENCY across the sites, which
a partial fix would defeat; (2) the instance in `design.md` is inside a verbatim
QUOTATION of the archived predecessor's own record, which may not be edited to
suit this packet; (3) the word landed on `d50a1251`, and rewording packet prose
after the word would ratify something other than what was read. **IT IS RESIDUE,
NOT AGREEMENT**: nothing behavioural rides on the phrase, and correcting it is
available to a later act where the origin block is no longer the constraint.

**CODEX NEVER REVIEWED THIS PULL REQUEST AT ANY HEAD.** One review request was
made (01:17:42Z) and the connector answered at **2026-09-11T01:17:49Z**:
*"You have reached your Codex usage limits for code reviews."* **THAT IS AN
ABSENCE AND IT IS RECORDED AS ONE, NEVER AS APPROVAL.**

**SonarCloud's quality gate PASSED** on this head with 0 new issues.

## 5. THE RATIFIED SURFACE — what this word admits, and what it does not

**ADMITTED.** The `## MODIFIED Requirements` block for *Install repository
scope* exactly as encoded at `d50a1251`: the re-ordered first sentence, the
carried tail (canon `:38`–`:64`, byte-identical), the three scenarios unchanged
in count, order and title, and the one `Removed from canon` marker naming the
replaced sentence. The block is byte-faithful BY CONSTRUCTION — a slice of
`openspec/specs/repo-boundary-governance/spec.md:34-66` with one
single-occurrence substitution and one paragraph re-wrapped at 79 — and the
digests that prove it are in `tasks.md` § 4.9.

**NOT ADMITTED, AND NOT BY THIS WORD.**

- **Nothing reaches `openspec/specs/`.** This ratification edits no promoted
  file. The block is still a delta.
- **The `spec/repo-boundary-governance` failure on the 1.2.0 binary is NOT
  cleared here.** A delta does not edit the promoted specification, so the
  strict run on `PATH` still reports it at the ratified head — measured, not
  assumed, in `review/verification-2026-09-11.md`. **THE ARCHIVE IS WHAT CLEARS
  IT.**
- **The requirement's heading, the sibling index requirement's count, and the
  three other enumerations** are untouched (D7).
- **No `doc-health` rule is proposed or amended.** The marker-carriage question
  as a GENERAL rule stays residue (`tasks.md` § 6.1).
- **The corpus-wide `target_release` divergence is not swept** (`tasks.md`
  § 6.8).

## 6. What is owed AFTER this word

- **The LANDING.** Brett Heap's word of 2026-09-11T00:42Z pre-gives it for a
  ratified head that is green — *"land each when green"* — and the landing is
  the orchestrator's act under the lane-collision protocol's Rule 6 window, not
  this record's. **No landing word specific to this head is recorded as of this
  file.**
- **The ARCHIVE, which is a SEPARATE ACT ON A SEPARATE WORD.**
  `code_surface: none` with `target_release: implemented` means this packet
  archives ON LANDING plus its own task list under `release-realization` rather
  than on merged-plus-green realization evidence — but the word has not been
  given. `tasks.md` § 5 stays ENTIRELY OPEN, and the sanctioned archive path
  refuses an open box, so every box must be ticked in the commit BEFORE the
  move.
- **openxFactory issue #931 CLOSES AT THE ARCHIVE AND NOWHERE ELSE.** This pull
  request carries `refs #931` and no closing keyword, in its body and in every
  commit message on this branch, so `closingIssuesReferences` is `[]`.
- **The archive pull request owes two statements in its body**: that the
  promoted block is BYTE-IDENTICAL to the delta, measured rather than asserted;
  and that the archive REMOVES the inherited marker from the promoted file
  (`design.md` D2b), stated rather than left for a reader to find in the diff.
- **The residues named and not taken**: `tasks.md` § 6.1 (marker carriage as a
  `doc-health` rule) and § 6.8 (the corpus-wide `target_release` divergence),
  plus the *"required gate"* phrasing refused in § 4 above.

## 7. Provenance of this record

Written in the ratification commit itself, in a fresh clone, by lane
`openxfactory-1`. It carries `Status: ratified` because
`document-lifecycle`'s *A review record records a ratification* governs a
`review/ratification-*` file, and `ratified-provenance` reads such a record's
SUBJECT whatever status it carries. Its sibling
`review/verification-2026-09-11.md` keeps `Status: record`: that file's subject
is the GATE RUN, so the scenario *A review record is not about a ratification*
governs it instead. Every path in this file is repo-relative.
