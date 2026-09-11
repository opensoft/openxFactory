# Design: amend-repo-boundary-governance-scope-first-line

Status: draft
Date: 2026-09-11
Kind: design

## 0. The brief

openxFactory issue [#931](https://github.com/opensoft/openxFactory/issues/931),
filed 2026-09-10 UNCLAIMED by this lane at the archive of
`amend-neutral-product-pin-lockfile-first-line` as the named successor of that
packet's `tasks.md` § 6.1, `design.md` D7 and its delta header:

> `openspec/specs/repo-boundary-governance/spec.md` fails `--strict` on `main`
> on the OpenSpec CLI at **1.2.0**, and it is the corpus's **only remaining**
> requirement with this shape once `neutral-product-pin`'s index 16 is
> amended. … A list of repository names in code spans. No `SHALL`, no `MUST`.
> … **the OpenSpec parser at 1.2.0 reads only the FIRST LINE of a
> requirement's body** when it checks for the keyword, so a `SHALL` on line
> two is invisible to it.

The issue names one remedy and floats two example shapes. This document takes
the remedy, writes THREE candidate wordings out with their costs, and records
the measurements the issue did not have — which is why **D6 is put first** and
why **D2 carries two marker decisions instead of one**.

**THREE DECISIONS ARE FOR THE OWNER: D6, D1 AND D2.** They are presented with
the recommendation first and D6 first of all. Nothing below is ratified; this
packet carries no approval pair.

## D0 — the measurement, taken before the design

On the clone of `main` `114d6e3d` this packet was authored against, 2026-09-11.

| measure | value |
| --- | --- |
| promoted spec files in the corpus | **62** |
| `### Requirement:` headings across them | **641** |
| …whose FIRST BODY LINE carries neither `SHALL` nor `MUST` | **1** |
| …and it is | `repo-boundary-governance` index **1**, heading `:34`, body `:35` |
| requirements in `repo-boundary-governance` | **11** |
| …whose first body line carries the keyword | **10** |
| …of those ten, first body lines of 80 characters or more | **0** (63, 67, 70, 71, 73, 74, 75, 75, 76, 79) |
| `derive_units` units in the promoted requirement | **13** — 4 body, 3 scenario titles, 6 scenario bullets |
| scenarios in the requirement | **3** |
| `SHALL` occurrences in the promoted block | **2** (one body, one inside the inherited marker) |
| `MUST` occurrences in the promoted block | **3** — one per scenario |
| active changes carrying a `repo-boundary-governance` delta | **5** |
| …of them writing THIS requirement's key | **0** |
| scripts/tests/workflows/contracts quoting any part of the sentence | **0** |
| markers already standing INSIDE the promoted block | **1** (`refresh-install-repository-enumerations`, 2026-09-08, at `:66`) |

**THE FILE'S OWN CONVENTION IS THE ARGUMENT, AND IT IS TEN TO ONE.** Every
other requirement in this specification opens its body with the obligation's
SUBJECT and reaches `SHALL` on the first line — *"`openxFactory` SHALL be the
canonical repository for domain-neutral factory…"*, *"An install-repository
enumeration SHALL be read as an INDEX…"*, *"Install repositories SHALL explicitly
link back to `openxFactory` for canonical…"*. Index 1 is the only one that opens with an
enumeration.

**AND THE SECOND HALF OF THAT MEASUREMENT MATTERS FOR D1, SO IT IS TAKEN HERE
RATHER THAN ASSERTED THERE: ALL TEN DO IT INSIDE 80 CHARACTERS.** The longest
first body line in this file is **79**. That is the reverse of what the
predecessor packet found in `neutral-product-pin`, where seven of seventeen
first lines ran from 80 to 397 characters and a long first line was therefore
house style. **In THIS file it is not**, which is a real cost against D1's
option 2 and is recorded as such rather than borrowed from the sibling packet.

### D0a — this is now the corpus's LAST instance, and the predecessor's count is carried forward correctly

`amend-neutral-product-pin-lockfile-first-line`'s `tasks.md` § 2.1 measured
**two** such requirements across 62 files and 641 headings. Its archive
promoted the amendment of one of them. Re-measured here on the same corpus and
the same predicate, the count is **one**, and it is this requirement. The two
measurements agree; the corpus moved between them.

## D6 — PUT FIRST, BECAUSE IT CAN END THE PACKET: should promoted canon be amended for a binary no required check runs?

**THIS IS A QUESTION FOR BRETT HEAP AND IT IS ASKED FRESH FOR THIS
REQUIREMENT.** A ruling exists on the same question for a DIFFERENT
requirement of a DIFFERENT capability, it is quoted below as precedent, and it
is deliberately NOT read as a standing rule.

`repo-boundary-governance` is validated in CI through the PINNED CLI, never
through a `PATH` binary. `neutral-product-pin`'s own promoted requirement *A
consuming repository runs OpenSpec validation only through the pinned
entrypoint, so a PATH binary cannot affect the gate* holds that a repository
*"SHALL invoke strict validation ONLY through the entrypoint the pin names"*.
openxFactory obeys it: `.github/workflows/openspec-cli-pin-gate.yml` runs
`python3 scripts/validate-openspec-cli-pin.py --all --no-cache`, and
`contracts/openspec-cli-pin.yaml:255` pins `version: "1.12.0"`.

**ON THAT BINARY THIS SPECIFICATION PASSES.** Measured on `main` `114d6e3d`,
2026-09-11, both binaries over the same tree:

| binary | named spec | whole corpus | exit |
| --- | --- | --- | --- |
| 1.2.0 on `PATH` | `Specification 'repo-boundary-governance' has issues` / `✗ [ERROR] requirements.1.text: Requirement must contain SHALL or MUST keyword` | `Totals: 97 passed, 3 failed (100 items)`, `spec/repo-boundary-governance` among the three | **1** |
| 1.12.0, pinned, content-verified | `Specification 'repo-boundary-governance' is valid`, six INFO notes | `Totals: 98 passed, 2 failed (100 items)`, `spec/repo-boundary-governance` among the PASSES | **0** |

The two failures the pinned run names are the two DISPOSITIONED
scenario-omission findings accepted on Brett Heap's word of 2026-09-05 *"take
exit 2"* (`add-chain-attestation` / `signed-execution-chain`,
`add-composed-view-authoring` / `ideation-dashboard`); neither is related to
this requirement. The pinned run reports
`@fission-ai/openspec@1.12.0 verified against its content address` and the
80-package dependency closure installed with `npm ci --ignore-scripts`.

**THE MECHANISM IS THE PREDECESSOR'S, MEASURED THERE ON A CONTROLLED FIXTURE
AND CITED HERE RATHER THAN RE-RUN.**
`amend-neutral-product-pin-lockfile-first-line`'s D6 validated a
three-requirement probe spec — keyword on line one, keyword on line TWO only,
no keyword anywhere — on both binaries: 1.2.0 errors on the second and the
third; 1.12.0 says NOTHING about the second and warns on the third. **A
keyword on line TWO draws nothing at all on 1.12.0**, which is exactly this
requirement's case and is why the corpus run counts it among the passes. That
measurement is archived and this packet does not claim it.

**THE PRECEDENT, QUOTED, AND WHAT IT DOES AND DOES NOT DECIDE.** On 2026-09-10
Brett Heap ruled this same question for `neutral-product-pin`'s index 16,
verbatim **"ratify as encoded"**, recorded on openxFactory PR
[#923](https://github.com/opensoft/openxFactory/pull/923#issuecomment-5624573662)
at 2026-09-10T19:53:02Z. That packet's own record states the grounds: *"the
pinned 1.12.0 binary the required gate runs does NOT report this failure, and
the amendment was ruled anyway, on the seventeen-to-one convention inside the
one file, the unfinished 1.12 migration, and a cost of two case flips and one
comma."* **TWO OF THOSE THREE GROUNDS READ DIFFERENTLY HERE**: the convention
is ten to one rather than seventeen to one, and the cost is four words added
rather than two case flips. The third — the unfinished migration — is
identical. **So the ruling is precedent and not entailment, and the question is
put again.**

**THE TWO OPTIONS.**

1. **AMEND (RECOMMENDED, and encoded).** Three reasons, none of them a red
   gate. (a) **Ten to one, and tighter than the sibling's seventeen to one**:
   every other requirement in this file reaches its modal on line one and all
   ten do it inside 80 characters, so the shape is not merely common here, it
   is uniform. (b) **The estate has not finished migrating.** 1.2.0 is what is
   on PATH on this machine today, `prepare-openspec-1-12-readiness` is still an
   ACTIVE change, and every engineer and agent who types `openspec validate
   --all --strict` — which is what this repository's own `CLAUDE.md` and its
   OpenSpec authoring notes tell them to type — sees a red specification and
   has to be told it is not theirs. That cost has now been paid three times, in
   #868's packet, in #882's and here. (c) **It is the corpus's LAST instance**:
   taking it empties the class, so the rule "a requirement's first body line
   carries its modal" becomes true of the whole corpus rather than true of all
   but one, and the next reader who runs the on-PATH binary meets a clean
   corpus instead of one standing exception they must learn to ignore.
2. **DO NOT AMEND — CLOSE #931 ON THE MEASUREMENT.** Legitimate, and cheaper:
   publish the two runs, record that the pinned gate is green, and leave
   ratified text alone — the estate's default posture toward promoted canon.
   **Its case is stronger here than it was for #882**, and that is said rather
   than hidden: the remedy costs four added words instead of none, and the
   1.12 migration will retire the reading that makes the failure visible at
   all, so the whole question expires on its own. Its cost is that the one
   requirement in the file that hides its verb behind an enumeration stays that
   way until then, and the next reader who runs the on-PATH binary re-opens the
   question from scratch.

**WHAT A VETO HERE COSTS: the whole packet.** If D6 resolves to option 2 no
delta is wanted, D1 and D2 fall with it, this packet is WITHDRAWN rather than
re-wired, and #931 closes with the measurement as its answer. That is why it is
asked before the wording.

## D1 — THE VETO POINT: the wording of the first sentence

**Recommended: OPTION 1. Written that way.** All three options put a subject
and the modal on line one; they differ in what they cost. **NONE OF THEM IS
FREE, AND THAT IS THE MATERIAL DIFFERENCE FROM THE PREDECESSOR PACKET.**

**WHY NO ZERO-WORD RE-ORDER EXISTS, MEASURED RATHER THAN ASSERTED.**
`amend-neutral-product-pin-lockfile-first-line` re-ordered its sentence and
added not one word, because canon had already written the clause *"the pin
SHALL carry a VENDORED RESOLUTION"* and the edit only moved it to the front.
**This sentence contains no such clause: its grammatical subject IS the
five-name list.** Moving `SHALL` ahead of the list therefore requires a
subject noun phrase that canon does not contain, or it requires leaving the
words alone and moving only the line breaks. The whole sentence is **215
characters**, so it cannot be re-wrapped onto one line of 79; a re-wrap that
reaches `SHALL` on line one needs **108 characters**. Those are the only two
families, and both are written out below.

### Option 1 — RECOMMENDED AND ENCODED: re-order, with a closed subject phrase

Exact bytes, as the delta carries them:

> The following install repositories SHALL be scoped to subsystem install,
> operations, backup, restore, upgrade, verification, and disaster recovery:
> `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`,
> and `OmniWorker-Install`.

First body line, **72 characters**: `The following install repositories SHALL be scoped to subsystem install,`,
with `SHALL` at word five.

**Accounting, measured, whitespace-split and CASE-SENSITIVE:** the new
sentence's tokens minus the retired sentence's are `The`, `following`,
`install`, `repositories`, `recovery:` and `` `OmniWorker-Install`. ``; the
retired sentence's minus the new one's are `recovery.` and
`` `OmniWorker-Install` ``. **Four words added, none removed**, plus two
punctuation moves. 215 characters become 251.

**Why it is recommended.**

1. **It matches the ten siblings exactly** — subject, modal, obligation, then
   the enumeration. At 72 characters it also sits inside the file's own
   observed range of 63 to 79, so it is not merely compliant, it is
   indistinguishable in shape from its neighbours.
2. **Compliance becomes a property of the SENTENCE rather than of its line
   breaks.** Once the subject and the modal are the first five words, ANY sane
   wrapping puts them on line one, so a later author who re-flows the paragraph
   cannot silently reintroduce the defect. That is exactly what option 2 cannot
   promise.
3. **"The following" is CLOSED, so the requirement is not widened.** It is
   exhaustively defined by the colon list that follows it and cannot be read as
   a claim about install repositories in general — which matters, because this
   capability's own *Install-repository enumerations are an index with a named
   authority* requirement (`:308`) measures **nine** mounts under `installs/`
   against the **five** this requirement indexes, and forbids reading an
   enumeration as the authority for which repositories exist.
4. **It states no count**, which is why it is preferred over the shape issue
   #931 itself floats. See option 3.
5. **The five names are canon's own bytes**, in canon's order, spelling and
   serial comma, relocated and not rewritten.

**Its cost, stated: it adds four words to ratified canon.** The predecessor
added none. The four are a subject phrase and not an obligation — no new noun
enters the requirement's world, nothing is obliged that was not, and no name,
activity or scenario moves — but it is still more than a permutation, and it is
put for a veto on exactly that ground.

**Second cost, stated:** the enumeration moves from the front of the sentence
to the back. A reader who used to meet the five names first now meets them
after the obligation. The requirement's HEADING already names the subject one
line above, and the sibling index requirement calls this list *"the install
repositories this capability's *Install repository scope* requirement
indexes"*, so the index reading survives the move — but the reading ORDER does
change.

### Option 2 — ALTERNATIVE: change not one word; move only the line breaks

Leave canon's sentence exactly as ratified and re-flow the paragraph so the
whole subject and its modal sit on one line:

> `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, and `OmniWorker-Install` SHALL
> be scoped to subsystem install, operations, backup, restore, upgrade,
> verification, and disaster recovery.

First body line, **108 characters**, `SHALL` at column 103.

**It is genuinely the smaller act, and it owes NO MARKER AT ALL.** Canon says
so itself: *"Normalization collapses runs of whitespace to a single space and
strips leading and trailing whitespace, so a re-wrapped paragraph compares
equal to the same paragraph wrapped differently; no normalization beyond it
applies"* (`openspec/specs/doc-health/spec.md:1668-1672`). **Measured, not
argued:** the block was generated a second way on this same tree with only the
line breaks moved, and `derive_units` returns **13 units, 0 uncarried, 0
added** — the family sees no change, so no `Removed from canon` marker is owed
and none would be written. **Not one word of ratified canon would move.**

**Its costs, and they are the reason option 1 is recommended.**

1. **Compliance would rest entirely on a LINE BREAK, and `doc-health`'s
   currency family is blind to line breaks BY DESIGN and by ratified rule.** So
   the next author who re-wraps that paragraph — a perfectly ordinary,
   declaration-free act under the family — silently restores the defect, and
   nothing in the corpus reports it. A rule enforced only by whitespace, in a
   corpus whose one checker is contractually indifferent to whitespace, is not
   enforced.
2. **A 108-character first line IS a style break in THIS file**, which is the
   opposite of what the predecessor found in its own. All ten compliant first
   body lines here are 79 characters or fewer; this one would be the longest
   line in the requirement by 29 characters and the only line in the file's
   eleven first-body-lines over 80. In `neutral-product-pin` a long first line
   was house style; here it would be a singularity.
3. **An amendment of ratified canon whose entire content is a line break is
   hard to read as an amendment at all**, and it would set the precedent that
   promoted text may be re-flowed under a change id — which is either trivial
   or a large new permission, and this packet does not want to decide which.

**A VETO TO OPTION 2 IS CHEAP TO EXECUTE AND IS COSTED HERE:** the delta's
block is replaced with the re-flow-only block, the `Removed from canon` marker
is DELETED (none is owed), `proposal.md`'s accounting section and this document
are re-written to match, and the gates are re-run. No other packet file moves.

### Option 3 — REFUSED: the counted subject the issue itself floats

> The five install repositories SHALL be scoped to subsystem install, … :
> `Hermes-Install`, …

Issue #931 floats *"opening the body 'The five install repositories SHALL be
scoped to …' and listing the names after the modal"*. It is a reasonable
reading and it is **refused for a measured reason, not a stylistic one**.

**It would copy a COUNT into a second requirement.** This capability's own
promoted requirement *Install-repository enumerations are an index with a named
authority* (`:308`) already states it — *"the install repositories this
capability's *"Install repository scope"* requirement indexes number FIVE"* —
and that requirement exists **precisely because these enumerations drift**: its
own prose records that deferring a refresh without naming where it went *"left
three of these enumerations two repositories behind and one of them four"*, and
it obliges an admitting change to *"either refresh every promoted enumeration
of install repositories or NAME the successor that will"*. **A copy of a
declaration moves separately.** Writing "five" into the scope requirement as
well would create a second place the next admission must find, in the one
capability that has already been burned by exactly that. The list itself must
be refreshed on admission and always has been; a spelled-out count is a second
thing to refresh and buys nothing the list does not already say.

It is recorded, not dismissed: the count is TRUE today, the issue's wording is
grammatical and clear, and nothing about option 1 forecloses it. If the owner
prefers it, the honest form also asks whether the sibling requirement's own
count should then be the single source and this one cite it — which is a larger
amendment than this word commissions.

## D2 — the markers: TWO decisions, both read off a measurement

### D2a — the marker this block OWES: one, and it is written

**Recommended and written: one `Removed from canon` marker, one name, no code
span in its reason, placed at the END of the block.**

The grammar decides it, and the grammar is `document-lifecycle`'s (*"A
deliberate deletion is legitimate, and it SHALL be declared by form rather than
by prose … naming each deleted unit as a CommonMark code span"*) as realized by
`doc-health`'s `modified-block-currency`. Applied to this delta:

- **Under option 2 (re-flow only) no marker is owed**, because no unit changes:
  the generated option-2 block measures **0 uncarried, 0 added**.
- **Under option 1 the sentence is a REPLACED unit** — `normalize` collapses
  whitespace and does nothing else — so the generated option-1 block measures
  **1 uncarried, 1 added**. One canon unit is absent from the block, one marker
  is owed, and it names exactly that one unit.

**IT IS ASSEMBLED FROM `derive_units`' OWN OUTPUT RATHER THAN RETYPED**, the
method PR #908's packet used and the predecessor repeated, so it cannot name a
fragment or a unit as its author remembers it. **The retired sentence CONTAINS
CODE SPANS**, five of them, so a single-backtick fence would not hold it; the
name is fenced with a DOUBLE backtick and one space of padding on each side —
the same fence `refresh-install-repository-enumerations` used in this very file
for the same reason. The ` — ` reason boundary stands outside every code span,
which canon requires. The assembled paragraph is then re-parsed by
`parse_marker` and asserted to yield form `removed`, change id
`amend-repo-boundary-governance-scope-first-line`, date `2026-09-11`, exactly
one name EQUAL to the derived uncarried unit, and an EMPTY `quoted` list.

**THE REASON CARRIES NO CODE SPAN AT ALL, DELIBERATELY.** That is what makes
the marker unreportable under every one of the five grounds the class now
carries: ground one needs a name the block restates, grounds three and four
need a name matching no canon unit, ground two needs a code span in the reason
matching an uncarried promoted unit, and ground five needs a marker naming
nothing. Measured on the committed block: **0 marker defects.**

**Rejected: an `AMENDED BY` dated bold note beside the marker.** A dated bold
note is ONE UNDIVIDED UNIT under this same family, so it would promote into
canon and every later block modifying this requirement would have to restate it
forever. The accounting lives in the delta file's HEADER PROSE — outside the
`## MODIFIED Requirements` block, where the family reads no units — and in the
marker's own reason.

### D2b — the marker this block INHERITS: not carried, on canon's own rule

**THIS IS A DECISION THE PREDECESSOR PACKET NEVER FACED, AND IT IS PUT HERE
RATHER THAN TAKEN QUIETLY.** The promoted requirement ENDS with a marker that
is not this packet's:

> **Removed from canon by refresh-install-repository-enumerations
> (2026-09-08):** `` `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`,
> and `OpenXPKI-Install` SHALL be scoped to … `` — ONE unit, and one only. …

An archive writes a MODIFIED block into the promoted spec **in place of the
whole requirement** — proven on this very file: the promoted block at `:34-66`
is BYTE-IDENTICAL to
`openspec/changes/archive/2026-09-09-refresh-install-repository-enumerations/specs/repo-boundary-governance/spec.md:5-37`
(sha256 `24f6479c…`, 2,885 bytes, both sides). So whether this block carries
that marker decides whether it survives promotion.

**RECOMMENDED AND ENCODED: DO NOT CARRY IT. Canon rules the point in terms.**
`doc-health`'s promoted requirement *Currency of an active change's MODIFIED
requirement* says, at `openspec/specs/doc-health/spec.md:1801-1805`:

> **A marker is NOT a carriage unit, in either direction.** A marker promotes
> into canon with the requirement that carries it, and if it were a unit every
> later block would have to restate every marker any predecessor ever wrote,
> forever. The durable record of a deletion is the archived delta, which is
> where every other archived governance act is read from.

**AND THE PRACTICE MATCHES THE RULE, MEASURED FOUR TIMES OVER IN THE CAPABILITY
THAT OWNS IT.** `doc-health`'s own *Currency of an active change's MODIFIED
requirement* has been amended FOUR times in five days —
`amend-marker-reason-boundary` (2026-09-06), `amend-marker-defect-reporting`
(2026-09-09), `amend-modified-block-currency-standing` (2026-09-10) and
`amend-marker-declaring-nothing` (2026-09-10) — and **each block carried
exactly ONE marker, its own**. Promoted canon today carries the last one and
no other; three predecessors' markers were each dropped by their successor.
Across the whole corpus, 23 promoted requirements have been modified by two or
more archived changes and only ONE accumulates markers from more than one; the
rest carry the most recent writer's or none.

**AND CARRYING IT WOULD BE REPORTED, WHICH IS MEASURED RATHER THAN FEARED.**
The inherited marker names the FOUR-name sentence that left canon on
2026-09-08. That text is no longer a unit of canon and is not a unit of this
block either, which is the marker-defect class's ground THREE — *"naming …,
which matches no unit of the promoted requirement or of the block"*. Generated
both ways on this tree and run through the family's own `suppression()`:

| block | uncarried | added | markers | marker defects |
| --- | --- | --- | --- | --- |
| option 1, inherited marker CARRIED, own marker ALSO written | 1 | 1 | **2** | **1** (ground three) |
| option 2, inherited marker CARRIED | 0 | 0 | 1 | **1** (ground three) |
| option 1, inherited marker DROPPED, own marker written | 1 | 1 | 1 | **0** |
| option 2, inherited marker DROPPED | 0 | 0 | 0 | **0** |

The defect is independent of the wording choice; it is a property of carrying a
predecessor's marker at all. **CORRECTED ON COPILOT'S FINDING, TAKEN: the first
row's marker count is TWO, not one.** Option 1 owes its own marker regardless of
the inherited one's fate — D2a's "one marker is owed" is unconditional on the
sentence being replaced, not conditional on what happens to a different,
inherited marker — so the CARRIED-plus-option-1 row counts both the inherited
marker and this block's own, where the DROPPED-plus-option-1 row (below it)
counts only the one it writes itself. Only the inherited marker is ever the
ground-three defect; the newly-written one is never defective, in any row,
because it always names a unit the block genuinely leaves out.

**THE COST, STATED PLAINLY: the promoted file loses a visible record.** After
the archive, a reader of `openspec/specs/repo-boundary-governance/spec.md` will
no longer see that the enumeration was widened from four names to five on
2026-09-08. Canon's own sentence answers that — *"The durable record of a
deletion is the archived delta"* — and the record is not lost, it is where
canon says to read it:
`openspec/changes/archive/2026-09-09-refresh-install-repository-enumerations/specs/repo-boundary-governance/spec.md:37`.
**The alternative is available and is costed:** carry the marker forward and
accept one `info`-band marker-defect finding on this block for the life of the
packet, disclosed in the pull request body rather than dispositioned.

## D3 — why an OpenSpec change and not a patch

**Because the sentence is PROMOTED, RATIFIED CANON, and this estate has a
standing refusal on exactly this point.**

Working rule 3 routes contract, boundary and policy changes through OpenSpec.
`document-lifecycle` makes the MODIFIED block the instrument. And the precedent
is not abstract: Codex raised a vocabulary defect in a promoted specification
as a P2 on PR [#780](https://github.com/opensoft/openxFactory/pull/780), and
lane `openxfactory-1` refused to fix it there —

> Rewording the requirement here would (1) edit ratified text with no word
> behind it and (2) destroy the very byte-identity that makes this archive
> auditable. **Amending promoted canon is an amendment packet's act, on its own
> ratification** — the estate has a shape for exactly this (`amend-*` changes
> with a `## MODIFIED` block), and it is not something an archive may do in
> passing.

**A packet that quietly `sed`-ed one line of `openspec/specs/` would be the act
that refusal refused**, and it would do it to a sentence whose promotion is
auditable: the archived delta of `refresh-install-repository-enumerations`
carries the same bytes as the promoted block, so anyone can check that what was
ratified is what was written. This packet proves that identity rather than
relying on it — sha256 `24f6479c…` on both sides.

## D4 — `code_surface: none`, `target_release: implemented`, and what that decides

Measured in `proposal.md`'s front matter:
`grep -rn "SHALL be scoped to subsystem install\|subsystem install, operations, backup" scripts/ tests/ .github/ contracts/`
returns NOTHING (exit 1). The five repository names appear elsewhere in the
tree as identifiers of repositories, and this block changes none of them. No
test pins the requirement's scenario count or titles, and the block adds no
scenario and drops none.

**`target_release: implemented` IS CANON'S OWN VOCABULARY AND THE PACKET WAS
CORRECTED TO IT ON A BOT FINDING.** *Realization axis declaration* admits
`implemented` *"or a named release defined in the aggregation repository"* and
names the doc-only default in the same breath — *"A proposal without the
declarations is a doc-only change (`code_surface: none`, `target_release:
implemented`) by default"* (`openspec/specs/release-realization/spec.md:24-30`)
— so `none`, which this packet was authored with by mirroring its ratified
predecessor, is outside the vocabulary. The divergence is CORPUS-WIDE (33 of
180 proposals; 7 against 9 among doc-only changes), no gate reads the value,
and nothing behavioural moves either way because the archive path is decided by
`code_surface`. This packet conforms and does not sweep the rest; `tasks.md`
§ 6.8 names that as residue.

Under `release-realization` an empty code surface **archives ON LANDING plus
its own task list** rather than on merged-plus-green realization evidence. That
is why `tasks.md` § 5 is one archive act rather than a realization group, and
why **the "realization" of a wording amendment IS its promotion at archive** —
a separate act on a separate word, at which openxFactory #931 closes.

## D5 — sequencing, and the sibling search pasted rather than summarized

`sequenced_after: []`, the positive root claim.

- **The requirement's PROMOTER** is `restructure-factory-repo-boundaries`
  (archived 2026-06-26, `7c4dacb9`) and its **LAST WRITER** is
  `refresh-install-repository-enumerations` (archived 2026-09-09, `ca4a1558`,
  PR #825), found with
  `git log -S "Install repository scope" -- openspec/specs/repo-boundary-governance/spec.md`
  and
  `git log -S "SHALL be scoped to subsystem install" -- openspec/specs/repo-boundary-governance/spec.md`.
  Both are ARCHIVED, so neither is an active co-writer.
- **Active deltas over this capability — SIX PATHS ON THIS BRANCH, FIVE
  SIBLINGS ONCE THIS PACKET'S OWN MATCH IS EXCLUDED** — Copilot's finding on
  this pull request, taken: `ls -d
  openspec/changes/*/specs/repo-boundary-governance` matches this packet's own
  directory alongside its siblings, six paths and not five, measured directly
  rather than assumed. Excluding
  `amend-repo-boundary-governance-scope-first-line` from that output leaves
  exactly `add-identity-brokering`, `add-trust-anchor`,
  `implement-keycloak-install-repo`, `implement-openxpki-install-repo` and
  `qualify-avatar-live-voice`. Their `### Requirement:` headings are *Keycloak
  install repository boundary* (ADDED by the first, MODIFIED by the third),
  *OpenXPKI install repository boundary* (ADDED by the second, MODIFIED by the
  fourth) and *Neutral avatar-client repository boundary* (MODIFIED by the
  fifth). **NOT ONE OF THEM IS THIS REQUIREMENT.**
- **The requirement key across every active delta, in a form that
  REPRODUCES** — the archive exclusion is a pipe, not prose:
  `grep -rln "Install repository scope" openspec/changes/ --include=spec.md |
  grep -v '/archive/'` returns **exactly this packet's delta and nothing
  else** on this tree (exit 0, one line). The PRE-ADDITION result is
  re-derivable against the branch point rather than remembered:
  `git grep -l "Install repository scope" 114d6e3d --
  'openspec/changes/*/specs/*/spec.md' | grep -v '/archive/'` returns
  **nothing, exit 1**. Unfiltered, the search also returns three ARCHIVED
  deltas — `2026-06-26-restructure-factory-repo-boundaries`,
  `2026-08-25-admit-install-repos-to-aggregation` and
  `2026-09-09-refresh-install-repository-enumerations` — the first two being
  this requirement's promoter and the aggregation admission it records, the
  third its last writer.
- **Open pull requests:** the SIX open when this packet's branch was cut —
  #934, #932, #921, #888, #594, #518 — were each read with
  `gh pr view <n> --json files` and **not one touches any
  `repo-boundary-governance` path**.

So this change is the **SOLE ACTIVE MODIFIER** of the requirement key, no
ordering declaration is owed in either direction, and the ledger's
`class: co-modifier` is the whole-corpus grading `proposal.md` § Sequencing
explains rather than a contradiction of it.

## D7 — what is NOT taken here

- **The requirement's HEADING.** *"Install repository scope"* is a noun phrase
  and is not edited. Editing a ratified heading changes the requirement KEY
  every consumer, marker and currency check matches on, which is a much larger
  act than this word commissions.
- **The sibling requirement's COUNT.** *Install-repository enumerations are an
  index with a named authority* (`:308`) states *"the install repositories …
  number FIVE"*. That is true today and is not touched. D1 option 3 explains
  why this packet declines to write a SECOND copy of it rather than why it
  would edit the first.
- **THE MARKER-CARRIAGE QUESTION AS A GENERAL RULE.** D2b decides it for THIS
  block on canon's sentence and the corpus's own practice. It does NOT propose
  a rule, amend `doc-health`, or ask for one: a later packet may reasonably
  argue that the currency family should recognise an inherited marker instead
  of reporting it on ground three. **That is named here as residue and is not
  taken** — it is a `doc-health` amendment, a different capability, and it
  needs its own issue and its own word. `tasks.md` § 6 carries it.
- **The two DISPOSITIONED findings** the pinned run names. Accepted exceptions
  on Brett Heap's word of 2026-09-05 *"take exit 2"*, unrelated to this
  requirement, and untouched.
- **`prepare-openspec-1-12-readiness`.** This packet writes no readiness
  evidence and claims no part of that migration; D6 cites the predecessor's
  fixture measurement rather than re-running or re-claiming it.
- **THE OTHER THREE ENUMERATIONS `refresh-install-repository-enumerations`
  TOUCHED.** Its markers also stand in *Canonical workflow authority*,
  *Copy-first migration* and `shared-contract-ownership`'s *Contract version
  pinning*. None of those requirements has a first-line defect, none is edited
  here, and D2b's reasoning is deliberately not applied to them: this packet
  drops one inherited marker because it is amending that one requirement for
  another reason, never as a tidy-up.
