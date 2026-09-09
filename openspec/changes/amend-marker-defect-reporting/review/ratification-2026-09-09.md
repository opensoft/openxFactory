# Proposal Ratification: amend-marker-defect-reporting

Status: record
Kind: report
Decision date: 2026-09-09
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-09 by Brett Heap (openxFactory operator authority) —
in-session, lane `openxfactory-1`, verbatim: *"merge 842 and 846 when green,
then ratify the 729 packet"* (2026-09-09T13:13:41Z, recorded on openxFactory
issue **#729**). **THE WORD IS ONE UTTERANCE OF THREE CLAUSES IN ORDER, AND THE
ORDER WAS KEPT.** openxFactory PR **#842** merged `4cdadd56` at 16:11:57Z
(closing **#840**) and PR **#846** merged `183d1b43` at 16:12:40Z (closing
**#833**), both green after **#801** cured the codexFactory org-move red; this
act is the third clause. It was given over a presentation that carried
`design.md` **D1** as the packet's veto point — option **A**, a reason-quoted
code span reported only where it matches EXACTLY a unit of the requirement's
basis that the block does not carry and that no marker declares removed, against
option **B**, any code span standing inside a reason (the remedy shape issue
#729's own body proposed) — with both options written out and B's four costs
MEASURED beside A's. **D1 was not vetoed.**
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/doc-health/spec.md` (**ONE MODIFIED requirement**, *"Currency of an active
change's MODIFIED requirement blocks"*, restated in full with every body unit,
all sixteen scenario titles and all their scenario bullets byte-faithful, **ONE
body sentence replaced**, that sentence declared by a reserved
`Removed from canon by` marker, and **TWO scenarios ADDED at the end of the
block**) — together with the CODE this packet's `code_surface` declares
(`scripts/doc_health/modified_block_currency.py`: `Marker.quoted` added,
`suppression` returning `list[_MarkerDefect]` and resolving the two new grounds,
`TEMPLATE_MARKERS` gaining one interpolated `{why}` field) and its tests
(`tests/doc-health/test_modified_block_currency.py` 128 → 139, eleven added, and
THREE existing assertions flipped — two there and
`test_the_inner_backtick_does_not_truncate_the_named_unit` in
`tests/doc-health/test_modified_block_currency_fixtures.py`), plus `README.md`
and this change's row in `tests/sequenced_after/corpus-ledger.yaml`, with
`openspec validate amend-marker-defect-reporting --strict` green and the
verification run captured beside this file at `verification-2026-09-09.md`.

**THE BASELINE IS THE FOLDED TEXT, NOT THE FROZEN TEXT.** The adversarial pass on
the frozen head **`9d4cf85b`** returned **READY TO ENCODE** with ONE
fix-before-encode finding, and that fix rides IMMEDIATELY BEFORE this
ratification rather than after it: commit *"Say exactly what the three grounds
report; record the nameless marker as an unruled fourth case"*. What the word was
given over is the packet's decision — D1 option A, three grounds, the narrow
predicate — and that decision is untouched by the fix, which removed an
over-claim in how the encoded grounds were DESCRIBED. § 5 sets out the finding
and every other disposition.

**This record is CAPTURED AT MERGE, not at first push, and it was RE-DERIVED
PRE-CAPTURE.** `record-immutability` forbids editing a `Status: record` document
AFTER capture; capture is the merge of the pull request that establishes it, and
nothing is merged yet. Every number in `verification-2026-09-09.md` was
re-derived on the tree this record sits in, after the fix commit and after the
ratification was encoded. A commit cannot write its own hash into its own tree,
so the ratification commit is named by its subject and its position on the branch
rather than by a hash.

**THE BRANCH IS BEHIND `main` BY DESIGN AT THIS MOMENT, AND SAYS SO RATHER THAN
MEASURING QUIETLY.** The branch's last merge from `main` took `e86eca35` (#801,
the workflow repoint to `codeXfactory/codexFactory`) at 15:44Z; the two pull
requests the word's first two clauses name landed AFTER that, so `origin/main`
is now `183d1b43` and this branch does not yet carry `4cdadd56` or `183d1b43`.
A merge from `main` and a re-measure are therefore owed AT LANDING, exactly as
the predecessor `amend-marker-reason-boundary` took twice before its own capture,
and `verification-2026-09-09.md` § 9 states which figures move when it is taken.
The ratification act itself reads no `main` sha.

## 1. What was ratified, and what it says

**ONE requirement is MODIFIED and none is added.** `doc-health`'s promoted
*Currency of an active change's MODIFIED requirement blocks* is restated in full
— every body unit, every scenario title and every scenario bullet, INCLUDING the
fenced block that writes the two marker forms out and INCLUDING
`amend-marker-reason-boundary`'s own `AMENDED BY` note and its narrative
paragraph — and exactly one body sentence changes.

**RETIRED:**

> A marker naming a unit the block still carries declares nothing and SHALL
> itself be reported, because a declaration that does not describe the block is
> a declaration no reader can rely on.

**REPLACING IT:**

> A MARKER SHALL ITSELF BE REPORTED ON ANY OF THREE GROUNDS, each of them one
> finding at the `info` band this family's marker-defect class already carries:
> it names a unit the block still carries; or a code span standing INSIDE its
> reason matches EXACTLY a unit of the requirement's basis that the block does
> not carry and that no marker declares removed, the boundary above reading that
> span as prose rather than as a name, so that its author declared nothing about
> a unit they plainly had in mind; or it names something matching no unit of the
> requirement's basis and no unit of the block. Each of the three is a
> declaration that does not describe the block, which is a declaration no reader
> can rely on, and a report on the MARKER is what points an author at the
> paragraph they wrote rather than at the unit it failed to declare. THE SECOND
> GROUND SHALL BE READ NARROWLY, on the exact match and never on the span's
> position alone […] The second ground SHALL NOT withdraw the carriage arms from
> the unit the span would have named […] the report being added BESIDE the
> carriage and never in place of it.

**TWO SCENARIOS ARE ADDED, AT THE END OF THE BLOCK** — *A marker's reason quotes
a unit the block does not carry* and *A marker names something no unit matches* —
so the two new grounds are pinned in CANON and not only in this packet's tests.
No promoted scenario moves, is retitled or loses a bullet.

**THE REPLACED UNIT IS DECLARED.** The block carries
`**Removed from canon by amend-marker-defect-reporting (2026-09-09):**` naming
the retired sentence verbatim as a single-backtick code span — single because the
unit itself contains no backtick — with a reason that carries **no code span
anywhere**, so the marker parses to exactly ONE name and ground two has nothing
to resolve over the packet's own declaration.

**AND THE REPLACING TEXT SAYS WHAT THE THREE GROUNDS REPORT RATHER THAN THE
CONVERSE.** The frozen head's clause opened *"A marker that declares nothing
SHALL itself be reported, on any of THREE grounds"*, and the converse it asserts
is FALSE on this packet's own code: a `Removed from canon` marker whose tail
carries no code span parses to `names = []` and `quoted = []`, so `suppression`'s
per-name loop never runs and the second pass has nothing to resolve — it reaches
NONE of the three grounds and is silent. The clause is reworded to the three
grounds as encoded, and the nameless marker is recorded as an unruled FOURTH
case at `tasks.md` § 5.7. **The ratified sentence is therefore narrower than the
frozen one CLAIMED to be and exactly as wide as the code has always been.**

**No file is added under `openspec/specs/`, so no codexFactory floor advance is
owed.**

## 2. Why the packet exists, in one finding and one measurement

**A marker is a declaration, and two ways of declaring nothing were silent about
the MARKER — so its author was pointed at a unit instead of at their own
paragraph.** openxFactory issue **#729** is the owed successor
`amend-marker-reason-boundary`'s ratified `tasks.md` § 5.1 named and did not
take. The FIRST silence is as old as the family: a name matching no unit of the
requirement suppresses nothing and is reported as nothing, `suppression`'s own
docstring recording that third resolution as *"deliberately NOT a finding … an
obligation this feature has no standing to invent"*. The SECOND is younger than
the reason boundary: #719 correctly stopped reading a code span inside a reason
as a name, and named in the same breath the failure mode that created — an author
separating two NAMES with ` — ` declares only the first, the unit is REPORTED (the
conservative direction), but the MARKER is not, so its author reads an action
string telling them to write a declaration they already wrote. **And the span was
not even kept**: `parse_marker` derived the post-boundary spans and DISCARDED
them, so the second silence was not merely unreported but not mechanically
detectable at all. One field is the enabling half of this packet.

**BOTH NEW GROUNDS HAVE A POPULATION OF ZERO AT LANDING, MEASURED RATHER THAN
ASSUMED.** On `main` @ `6df21737` the corpus carried **16** unit-naming markers;
**8** quote a code span inside their reason, every one of them a PROMOTED
specification's own marker; and **of the 34 spans those eight quote, ZERO is a
derived unit of the document that carries the marker** — they are `WHEN`, `AND`,
`or`, `openspec/specs`, `openxFactory`, `OpenXPKI-Install` and the like, prose a
reason quotes while explaining itself. The SHIPPING PATH is narrower still: the
family reads markers only inside active `## MODIFIED Requirements` blocks, and
exactly **TWO** of those carry a unit-naming marker (`add-chain-attestation`,
`add-composed-view-authoring`, both `Merged into`, one name each matching its
resolved basis, neither quoting a span in a reason). So the amendment is
normative for the NEXT marker written rather than a sweep of the present one.

## 3. The decision ratified knowingly

### D1 — option A (the exact match), against option B (the position)

- **Option A, TAKEN AND RATIFIED.** A code span standing after the reason
  boundary is reported ONLY where it, normalized, matches EXACTLY a unit of the
  requirement's basis that the block does not carry and that no marker in the
  block declares removed. It is SILENT on all eight promoted markers, today and
  on the same shape tomorrow, because none of the spans they quote is a unit at
  all; it fires on exactly the shape #719 created; it costs one field and no
  parse; and its failure direction is silence, never noise — where a span is a
  unit under a different spelling, ground two says nothing and the carriage arm
  still reports the unit.
- **Option B, REJECTED FOR MEASURED COST and written out beside A rather than
  strawed.** Reporting any code span inside a reason would (1) fire on canon's
  own blessed form, which says in as many words that such a span *"is prose the
  reason quotes rather than a unit the marker names"*; (2) make EIGHT of the
  sixteen markers in this corpus reportable, every one of them promoted and
  correct, the moment any MODIFIED block restated one of their requirements — a
  share that grew from 2 of 7 to 8 of 16 in three days; (3) be un-narrowable by
  wording later without a second amendment over the same sentence; and (4) fail
  even to distinguish the defect it aims at, the two-names author and the quoting
  author writing the SAME BYTES in the same positions.

**A VETO OF A WOULD HAVE BEEN A VETO OF GROUND TWO ONLY.** Ground three — a name
matching no unit of the requirement's basis and no unit of the block — rests on
no predicate choice, is the silence `add-modified-block-currency-check` itself
recorded as a plausible later ruling, and stood whichever way D1 went.

**AND ONE NARROWING OF THE RULING'S LITERAL WORDING IS RATIFIED WITH A, HAVING
BEEN DISCLOSED BEFORE THE ACT.** The ruling of 2026-09-09T12:32:46Z described
option A as *"report a marker only where a reason-quoted span exactly matches a
canon unit the block does not carry"*. The ENCODED predicate adds **"and that no
marker declares removed"** (`design.md` D5): a sibling marker that properly
declares the unit gone makes the quotation harmless, and reporting it would send
an author to fix a marker that is already right. The clause is narrower in the
SILENT direction — strictly fewer findings, never more — and it was stated on
issue **#729 at 14:22Z**, after the word was uttered at 13:13:41Z and before the
act that word made conditional on #842 and #846 landing green (16:1xZ), and
before the adversarial pass recorded it as standing as designed.

**Ratified as designed. The reversal was NOT taken.**

## 4. What is NOT ratified, and the residue this word does not reach

1. **`FAMILY_RESOLUTION` HAS CARRIED THIS FAMILY AS `CONTESTED` SINCE #357, SO
   ISSUE #729'S "NOT CONTESTED" PREMISE WAS STALE — AND THE PACKET CLAIMS NO
   EXEMPTION.** `scripts/doc_health/families.py` line 117 reads
   `"modified-block-currency": CONTESTED`, set by the flip of 2026-08-31 (issue
   **#357**), and that table has NO PER-CLASS GRAIN — `runner.main` applies it by
   `Finding.family` alone. So every class this family emits is already
   `contested`, the marker-defect ground that shipped included, and a
   marker-defect finding that stops being reported without a citation already
   owes one under `report.uncited_resolutions`. `design.md` **D7** states the
   inheritance plainly instead of asserting an absence that is no longer true,
   and with a population of zero at landing there is nothing that can vanish
   between two reports. **AND THE MODIFIED BLOCK CARRIES CANON'S NOW-FALSE
   *advisory at launch* PARAGRAPH BYTE-FAITHFULLY BY NECESSITY, NOT BY
   OVERSIGHT** — that paragraph still states `warning` severities and says the
   family *"is deliberately absent from `FAMILY_RESOLUTION`"*, both true at
   launch and neither true since the flip. A `## MODIFIED` block restates canon
   AS CANON STATES IT, this packet replaces exactly ONE sentence, and correcting
   a second is its own amendment with its own ruling. Recorded as residue at
   `tasks.md` **§ 5.3**, disclosed on issue #729 at 14:22Z and at 14:58Z before
   this act, and named here so a later reader does not read a faithful
   restatement as a fresh claim.
2. **#719'S PROMOTED MARKER IS DELIBERATELY NOT RESTATED.**
   `amend-marker-reason-boundary`'s `Removed from canon` marker names, as a code
   span, the sentence THAT change retired — a sentence canon no longer carries —
   so it matches no unit of the requirement or of the block. Restating it in this
   block would make this block report ITSELF under its own new ground three. The
   authority for not restating it is this requirement's own promoted sentence,
   *"A marker is NOT a carriage unit, in either direction … if it were a unit
   every later block would have to restate every marker any predecessor ever
   wrote, forever"*, and the block's `AMENDED BY` note says so in terms. The
   general consequence is disclosed rather than left to be found: after this
   packet, **copying a predecessor's promoted `Removed from canon` marker forward
   into a later MODIFIED block is a reportable defect** (`design.md` D4,
   `proposal.md` § Impact). Measured: no active block does it, so that
   consequence's population is also zero today.
3. **A NAME MATCHING A UNIT THE BLOCK ADDS AND CANON DOES NOT IS STILL SILENT**
   (`tasks.md` § 5.2, UNTICKED; `design.md` D3). Whether a block may declare its
   own additions removed, and against what, is a rule nobody has written, and
   inventing a fourth ground here would repeat on the same afternoon the fault
   this packet corrects. Pinned by a test so the silence is a decision a later
   act can overturn.
4. **A MARKER THAT NAMES NOTHING AT ALL IS STILL SILENT** (`tasks.md` § 5.7,
   UNTICKED). Found by the adversarial pass; it is the FOURTH case of a marker
   declaring nothing about the block, it reaches none of the three grounds, and
   what such a paragraph even is — a marker form carrying no declaration, or
   prose that merely looks like one — is a grammar question this packet does not
   open. No successor is named; the issue is filed at the archive word.
5. **`specs/019-modified-block-currency-family/` STILL STATES THE ONE-GROUND
   RULE AND IS DELIBERATELY NOT EDITED** (§ 5.4, UNTICKED). It is a BUILD RECORD
   of what `add-modified-block-currency-check` specified and was implemented
   against — not promoted canon, pinned by no test and by no gate — and both
   precedents (#688, #719) likewise edited no feature spec when they amended the
   canon those specs describe.
6. **THE ESTATE-WIDE RUN IS OWED AND IS NOT TAKEN HERE** (§ 5.5, UNTICKED).
   `active_blocks()` takes a repository root and the aggregation nightly reads
   every submodule; this lane is confined to its own clone, so the measurement
   here covers openxFactory only. The direction is bounded by construction —
   both grounds REPORT and suppress nothing, so no suppression changes and no
   unit becomes less visible — and both are `info`, so no `--fail-on error` run
   can red on them.
7. **THE PROMOTED MARKERS THIS PACKET COUNTS ARE NOT EDITED**, nor the archived
   deltas that carry them. They are records of ratified removals, and every one
   of them is correct under the narrow ground.
8. **THE ARCHIVE IS A SEPARATE ACT** (§ 5.6, UNTICKED). `code_surface` is
   non-empty, so under `release-realization` this packet archives on
   merged-plus-green realization evidence rather than on landing, and on a
   separate word. **This word ratifies; it does not archive.** openxFactory
   **#729** therefore closes at archive, not at this landing, which is why the
   pull request carries no closing keyword.

## 5. The bench, and the adversarial pass folded into this act

**THE ADVERSARIAL PASS (Opus, read-only, frozen head `9d4cf85b`) RETURNED
READY TO ENCODE**, recorded on the pull request at 2026-09-09T16:44:18Z. Every
gate was green on that head — strict validate for the change and the corpus (the
corpus's three failures byte-identical to `main`'s and none this packet's), the
pinned-CLI validate, `proposal-support verify`, both origin-retention gates,
doc-health inert with the family's findings byte-identical to `main`'s — the
122-carried / 1-retired unit count re-derived through `derive_units`, the census
re-derived on the head, the delta confirmed as exactly one sentence replaced plus
the `AMENDED BY` note, the reserved marker and two appended scenarios, the
implementation matched to the three grounds at every boundary, a mutation probe
against the base tree failing 12 tests (both new scenarios and all three flipped
assertions among them, so they strengthen rather than mask), and 1646 tests
passed.

**ONE FINDING WAS FIX-BEFORE-ENCODE AND IT WAS TAKEN**, in the commit
immediately preceding this ratification:

1. **The headline clause and the pull-request title over-claimed.** The clause
   read *"a marker that declares nothing SHALL itself be reported, on any of
   THREE grounds"*; a marker with ZERO code spans reaches none of them
   (`scripts/doc_health/modified_block_currency.py`, the `for name in
   marker.names` loop). **TAKEN:** the clause now says what the three grounds
   report; `proposal.md` § What Changes is aligned with it; `design.md` D3 gains
   the mechanism; `tasks.md` § 5.7 records the nameless marker as an unruled
   fourth case with an OPEN box; and the pull-request title dropped *", or that
   names nothing"*.

**AND FOUR MORE WERE DISPOSITIONED RATHER THAN TAKEN SILENTLY:**

2. **[RESIDUE — archive-time]** § 5.2, § 5.3, § 5.4, § 5.5 and § 5.6 are open and
   three of them name no successor; `proposal-support` refuses the ARCHIVE act
   until each names a filed issue. That is not a ratification defect — the
   predecessor `amend-marker-reason-boundary` was ratified in exactly this shape
   with § 5.1–§ 5.5 open — and the issues are filed at the archive word. § 5.7,
   added by the fix, is open on the same footing.
3. **[RESIDUE — named in this record]** the byte-faithful carriage of canon's
   now-false *advisory at launch* paragraph: § 4.1 above.
4. **[NIT — TAKEN, no test asserts the words]** the two ADDED scenarios said
   *"the promoted requirement"* where title resolution may substitute a declared
   sibling's outcome as the basis the arms measure against; *"the requirement's
   basis"* is exact, and it is the vocabulary the block already uses. Grepped
   first: no test asserts either scenario title or any of their bullets, and the
   two tests that DO assert this vocabulary assert the CODE's rendered finding
   text, which is not touched.
5. **[NIT — RECORDED, stands as designed]** ground two's encoded predicate adds
   *"and that no marker declares removed"* to the ruling's literal wording: § 3
   above, disclosed on #729 at 14:22Z.

**COPILOT: THREE ROUNDS, BOTH FINDINGS TAKEN.** Round 1 (14:24:51Z) returned
*"Changes recommended"* with two concrete findings — a stale return-type
annotation on `suppression` and a duplicated `basis` comment — and both were
taken in commit **`97a0c5e3`**, *"Take both Copilot findings"*. Round 2
(14:31:56Z) returned **"Approval recommended"** with 0 new comments: *"the
implementation aligns with the stated narrow predicate, keeps existing behavior
stable where promised, and is comprehensively pinned by targeted unit and
corpus-regression tests."* Round 3 (15:47:46Z, after the merge from `main`)
returned *"Needs a closer look"* with 0 new comments, on the ground that the
packet amends promoted normative behaviour and warrants final human review —
which is what this act is. No inline thread stands unresolved.

**CODEX IS ABSENT, AND IT IS RECORDED AS ABSENCE RATHER THAN AS CLEARANCE.**
`@codex review` was requested on this pull request at 14:22:07Z and the connector
answered at 14:22:18Z: *"You have reached your Codex usage limits for code
reviews."* **No Codex round ran on this packet.** **Sourcery** (14:21:43Z) is the
private-repo upsell stub, as on every packet in this arc.

## 6. The landing obligation

**Rule 6 applies.** This pull request adds a README OpenSpec Records entry and
creates a directory under `openspec/changes/`, so lane `openxfactory-1` posts
`LANDING — lane openxfactory-1, session <id>, <UTC>, PR #850 into openxFactory
main` on the pull request and in `~/projects/xFactory/LANES.md` before the merge,
and `LANDED — lane openxfactory-1, <UTC>, PR #850 → <merge sha>` after it. The
landing is the coordinator's act, not this encode's, and **a merge from `main`
and a re-measure are owed before it** (§ the header note above).

**The pull request is self-authored and merges under the B2 provenance pattern**:
`gh` opens pull requests as `brettheap`, so a code-owner ruleset never clears on
Brett Heap's own click; the merge is an admin merge on his recorded word, with
that word — *"merge 842 and 846 when green, then ratify the 729 packet"* —
quoted in the merge provenance. The CI rollup is observed rather than expected,
and the `merge-master-approval` advisory red of the codexFactory org move is
disclosed rather than treated as clearance.
