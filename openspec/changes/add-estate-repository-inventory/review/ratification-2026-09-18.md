# Proposal Ratification: add-estate-repository-inventory

Status: ratified
Kind: report
Decision date: 2026-09-18 (§§ 1-3); 2026-09-21 (§ 7)
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-18, approximately 12:55Z by Brett Heap (openxFactory
repository owner), verbatim: *"ratify #1101"* — given in the lane's terminal to
lane `openxfactory-5` (display `openXfactory-5`, session `651195c7`,
workstation Eagle), over `proposal.md` § *The decision, put for a veto*
(`design.md` D2, D3, D4, D5), and recorded in full here. **NO GITHUB COMMENT
CARRIES THIS WORD**: the channel was the terminal, not a review thread, and this
record plus the lane register is how the word survives.
**FOLLOWED BY THREE FURTHER WORDS OF THE SAME DAY**, at approximately 15:40Z,
each a multiple-choice answer over a gap Copilot's review of PR #1101 exposed in
the already-ratified text: *"Bind the carrier identity"*, *"#1101 declares #1108
and folds its text"*, *"MAY becomes MUST"*. **AND BY A FIFTH WORD OF A LATER
DAY**, 2026-09-21 at approximately 20:30Z, over a gap Copilot's review of the
REALIZATION pull request #1119 exposed between this packet's ratified `pin`
kind and `design.md` D0.2 row 3: *"Drop the pin admission on row 3"*. All five
acts are recorded here; §§ 1 and 2 carry the first, § 3 carries the three, § 7
carries the fifth.

## 1. The first word, and what it reaches

**"ratify #1101" IS BARE AND NAMES NO ALTERNATIVE**, so every decision put for a
veto takes its RECOMMENDED option, which is what `proposal.md` § *The decision,
put for a veto* and `tasks.md` § 1.1 both state a bare word does. It was given at
approximately 2026-09-18T12:55Z and is recorded, with that instant, on every
document this ratification touches — `proposal.md`, `design.md`, `tasks.md`,
`.openspec.yaml` (`approved_by`/`approved_on`, ADDED beside the unmoved
`proposed_by`/`proposed_on` pair the `add-drafted-proposal-origin` (issue #318)
shape defined), the README OpenSpec Records entry, and this record.

**THE INSTANT IS RECORDED TO THE PRECISION IT WAS GIVEN AT AND NO FINER.** The
word was taken in session, not read off a timestamped comment, so it is written
"approximately 12:55Z" rather than to a minute nobody confirmed; inventing a
false precision would be inventing evidence. The lane recorded it as a `RULED`
entry against `opensoft/openxFactory#1101` in `opensoft/brett-wip`
`lanes/log/openXfactory-5.md`.

**THE FIRST WORD WAS APPLIED BY LEAVING THE DELTA TEXT ALONE.** At the
ratification commit `git diff --numstat` over
`openspec/changes/add-estate-repository-inventory/specs/` was empty: the word
took the option the packet had already encoded, so not one byte of
`specs/release-realization/spec.md` was re-written, restored or deleted by it.
**The three LATER words of § 3 did move that file**, deliberately and on those
words, and § 3 states exactly where.

## 2. The decision, as put and as ruled

| D | `design.md` | Put | Ruled |
| --- | --- | --- | --- |
| **D2** | D2 | Where the inventory lives | **RECOMMENDED — `scripts/estate-repository-inventory.yaml`** beside the code-surface register, `target_release: implemented`; against `contracts/policies/` (a bundle surface owing a manifest entry, a recomputed digest and an additive minor per correction, against a fact that moved nineteen times in seventy-four days) and against no file at all (a required check depending on a network call to a private repository) |
| **D3** | D3 | The delta kind | **RECOMMENDED — one `## MODIFIED` block** over the promoted grammar requirement, restated but for the paragraph whose own stated reason this packet removes; against ADDED-only, which leaves a contradiction standing in canon |
| **D4** | D4 | The authority question #1087 carries | **RECOMMENDED — FIVE closed admission-evidence kinds** (`gitlink`, `pin`, `workflow`, `root`, `change`, `gitlink` reaching ANY governed estate repository's `.gitmodules` with its evidence naming the carrier) and THREE governance classes, the inventory RECORDING an admission and PERFORMING none; against a flat membership list |
| **D5** | D5 | A former address in an active head | **RECOMMENDED — REPORT**, naming the current address; against refuse |

**`tasks.md` § 1.4's TWO REVIEW-FORCED DISCLOSURES WERE TAKEN WITH THE REST** —
the widened `gitlink` kind and the bounded reverse arm — the word having been
given over the packet as it then stood, and neither named separately. They are
not a fifth decision taken by silence; § 1.4 was written to produce exactly that
outcome.

## 3. The three later words, and what each one moved

**ALL THREE WERE GIVEN ON 2026-09-18 AT APPROXIMATELY 15:40Z**, in the lane's
terminal to lane `openxfactory-5`, each as a MULTIPLE-CHOICE answer taking the
recommended option, each recorded as a `RULED` entry in `opensoft/brett-wip`
`lanes/log/openXfactory-5.md`. Each answered a gap Copilot's review of PR #1101
exposed in text that was ALREADY RATIFIED, which is why each is recorded as its
own act rather than folded into § 1: a ratifying word does not reach text it was
not given over.

### 3.1 *"Bind the carrier identity"*

**PUT ON** the scenario *A gitlink row is re-checked only against a supplied
tree*, whose AND clause trusted a supplied working tree without checking WHAT it
was a checkout of.

**RULED, VERBATIM:** *"Bind the carrier identity"* — the supplied tree MUST be
verified as a checkout of the carrier repository the row names (by its origin URL
or by its `contracts/policies/repository-identity.yaml` record) before its
`.gitmodules` evidence is trusted; a supplied tree that fails that verification
leaves the row reported NOT RE-CHECKED — counted, not passed, not failed.

**ENCODED AT** the enumeration requirement's re-check paragraph (a new normative
paragraph naming both identity sources, what a failed verification does, and the
reason: a path is an assertion and not an identity); the AND clause of *A gitlink
row is re-checked only against a supplied tree*, which gains a second AND for the
failed-verification verdict; the membership arm's bound sentence; and the third
bullet of *An inventory row nothing names*. **MIRRORED AT** `design.md` D1.2 and
`tasks.md` §§ 3.2, 3.3, 3.5.

### 3.2 *"#1101 declares #1108 and folds its text"*

**PUT ON** `proposal.md`'s `sequenced_after: []` root claim, which stopped being
true when `amend-code-surface-grammar-comma-and` (openxFactory #1092, PR #1108)
was ratified on 2026-09-18 and landed to `main` at `60d281a8` carrying a
`## MODIFIED` block over the SAME requirement key.

**RULED, VERBATIM:** *"#1101 declares #1108 and folds its text"* — declare
`sequenced_after: [amend-code-surface-grammar-comma-and]`, and let the
`## MODIFIED` block reproduce the requirement WITH #1108's ratified wording (the
four separators including `, and `, the comma-first behaviour text), taken
byte-for-byte from that packet's delta on `main`, with this packet's own
membership change applied on top. Promotion order is #1108 then #1101; **#1108 is
not touched.**

**ENCODED AT** `proposal.md` front matter (`sequenced_after:`) and § *What
changes* item 1; the delta's preamble; and the MODIFIED block itself, which now
carries #1108's four-separator opening sentence, its `, and `-ahead-of-the-comma
paragraph, its narrowed `, and …` refusal, its `**AMENDED BY**` note and its
added scenario *A declaration spells its list out with an Oxford comma* — taking
the block from ten scenarios to ELEVEN and the packet from 27 to **28**.
#1108's own `Removed from canon` marker is deliberately NOT carried: it declares
three units removed from the canon that PRECEDED it, none of which survives in
the text this block rests on. **MIRRORED AT** `design.md` D6 (which supersedes
its own drafting-time `sequenced_after: []` claim rather than overwriting it) and
D3, and `tasks.md` §§ 1.5, 2.9.

**THIS RULING IS ALSO WHAT MAKES THE SELF-GATE GREEN**, and by a DECLARATION
rather than by an edit to any test:
`tests/doc-health/test_modified_block_currency_self_gate.py::test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree`
failed at `7b2fdf93` with TWO fresh ordering subjects, both blocks reported as an
unstated ordering. The family reads the ordering from the later change's
`proposal.md` by whole-token mention, so the declaration resolves the pair, this
block is measured against #1108's block instead of canon, and the arm reports
nothing — returning `_ORDERING_SUBJECTS` to the empty exact set it already
states. **NOT ONE BYTE OF `tests/` OR `scripts/` IS EDITED BY THIS PACKET.**

### 3.3 *"MAY becomes MUST"*

**PUT ON** the scenario *A repository a ratified change is creating*, whose THEN
read that the inventory MAY carry the provisional row — making the membership
arm's fail-closed verdict depend on an unrecorded choice.

**RULED, VERBATIM:** *"MAY becomes MUST"* — the inventory MUST carry the
provisional row (admitted by `change`) for a repository a ratified active change
declares it is creating; the membership arm stays unconditional and fails closed.

**ENCODED AT** the `change` bullet of the enumeration requirement (the inventory
SHALL carry that row and SHALL NOT omit it at an author's discretion); the THEN
of *A repository a ratified change is creating* (MAY -> MUST) plus a new AND
stating that the membership arm is unconditional and still fails closed; and the
membership requirement's opening paragraph, which now states that the arm takes
no exception for the forward-looking window. **MIRRORED AT** `design.md` D1.1 and
`tasks.md` §§ 3.1, 3.4, 3.5.

## 4. What these words admit, and what they do not

**ADMITTED.** The packet as it now stands: one `## MODIFIED` block over
*Code-surface declaration grammar is gated* written over
`amend-code-surface-grammar-comma-and`'s outcome (eleven scenarios), and two
`## ADDED` requirements — *The estate's repositories are enumerated in a governed
inventory* (eight scenarios) and *A declared repository is judged for membership
against the estate inventory* (nine scenarios). **TWENTY-EIGHT scenarios**,
counted from the delta file.

**NOT ADMITTED, AND NOT BY ANY OF THESE WORDS.**

- **Nothing reaches `openspec/specs/`.** These acts edit no promoted file.
  Promotion happens at archive, which `tasks.md` § 5 holds behind
  merged-plus-green realization evidence and a separate word.
- **The REALIZATION (`tasks.md` § 3) is not performed here.** The first word
  authorizes it to be AUTHORED, as a later pull request in this repository.
- **No script, no test, no workflow and no contract member moves.** The
  self-gate is made green by the ordering DECLARATION, never by an edit to
  `tests/doc-health/`.
- **`amend-code-surface-grammar-comma-and` is not edited.** Its files, its
  ratification record and its ledger row are untouched; the fold is performed
  entirely inside this packet's delta.
- **openxFactory #1087 stays OPEN.** `code_surface` is non-empty, so the archive
  is a separate act on merged-plus-green realization evidence and a separate
  word, and the issue closes THERE, never at this landing.
- **No merge word is quoted anywhere in this packet.** The verbatim first word is
  "ratify #1101" and nothing further; the merge is a separate act performed by
  whoever holds it, never by this lane alone.

## 5. What is owed after these words

- **§ 3 (realize) may now be authored**, as a LATER pull request under this lane,
  carrying the two obligations §§ 3.1 and 3.2 above created: the carrier-identity
  verification in the `--estate-tree` mode, and the owed `change`-admitted row.
- **§ 4 (verification) is taken at the realization head**, not here; § 4.3
  re-measures the 33 rows by the five D0.1 commands.
- **§ 5 (archive) stays entirely open**, held behind merged-plus-green
  realization evidence and a separate word; openxFactory #1087 closes only there,
  and the promotion order is #1108 then #1101.

## 6. Provenance of this record

Written in the ruling-encoding commit `089b02e0`, by lane `openxfactory-5`
(display `openXfactory-5`, session `651195c7`); **EXTENDED 2026-09-21 BY A
SECOND, SEPARATE COMMIT — § 7 below, the same lane three days later.** It
carries `Status: ratified` because `document-lifecycle`'s *A review record
records a ratification* governs a `review/ratification-*` file. Every path in
this file is repo-relative. The lane register `opensoft/brett-wip`
`lanes/log/openXfactory-5.md` is a SEPARATE repository and is the channel of
record for all FIVE words.

## 7. The fifth word, a later day, and what it resolved

**GIVEN 2026-09-21, APPROXIMATELY 20:30Z**, in the lane's terminal to lane
`openxfactory-5`, as a MULTIPLE-CHOICE answer taking the RECOMMENDED option,
recorded as a `RULED` entry in `opensoft/brett-wip`
`lanes/log/openXfactory-5.md`. Unlike the three words of § 3, the gap this
word answers was named by Copilot's review of a DIFFERENT and LATER pull
request — **#1119**, the realization (`tasks.md` § 3) — and not #1101, merged
three days earlier; #1101's own Copilot round is § 3's alone.

**PUT ON** `design.md` D0.2 row 3, which admitted `codeXfactory/codexFactory`
(governance `governed`) by THREE kinds, one of them `pin
(`review-lane-pin.yaml`)`. The delta's `pin` kind reads: "an openxFactory file
under `contracts/` names the repository as the source of a commit-and-digest
pin. This is openxFactory's act, for a product PINNED rather than governed."
`contracts/review-lane-pin.yaml` is `kind: pinned_workflow`; its own header
states it pins "EXECUTABLE GOVERNANCE CODE consumed by a workflow — no bundle,
no digest set", and it records `core_commit`, never a digest. Row 3 fails BOTH
clauses of the kind's own definition: the pin carries no digest set, and
`codeXfactory/codexFactory` is `governance: governed`, not `pinned`. Copilot
named exactly this (PR #1119, `estate-repository-inventory.yaml:153`, thread
`PRRT_kwDOTAvnrs6j3KY4`, 2026-09-18T19:05:23Z): *"This admission does not
satisfy the inventory's closed `pin` kind: `contracts/review-lane-pin.yaml` is
`kind: pinned_workflow` and explicitly says it has no digest set; it records
`core_commit` for executable governance code instead. Because the row already
has the aggregation gitlink and workflow evidence, remove this `pin` entry (or
change the schema/validator to define a separate pin kind) rather than
recording evidence that the `pin` contract does not permit."* Brett Heap's own
reply on that thread the same day (2026-09-18T20:19:43Z) found the claim TRUE
on the ratified text and left it **RULING NEEDED**, because every remedy
available to a realization seat edits RATIFIED text — dropping the admission
edits `design.md` D0.2 row 3, re-classing it as `workflow` is refused by the
loader's own ratified directory bound (row 3's real workflow evidence is
already named), and widening the kind's wording edits the delta's requirement
text — and under the estate's post-word rule a realization seat may fold a
non-normative fix but must send a requirement-or-record change to Brett Heap
as RULING NEEDED.

**RULED, VERBATIM:** *"Drop the pin admission on row 3"* — row 3 loses the
`pin` admission and keeps `gitlink (`opensoft/xFactory`)` and `workflow`; the
`pin` kind's definition in the delta is UNCHANGED.

**ENCODED AT** `design.md` D0.2 row 3 (the `pin` item dropped) and a new note
at D0.1's pin-declaration measurement naming `review-lane-pin.yaml`'s hit as
excluded; `.openspec.yaml` `approved_by` (this ruling appended, `approved_on`
unmoved); `tasks.md` § 1.5, new bullet (d). Written in a SEPARATE, LATER pull
request than §§ 1-5 above, landing directly on `main`, touching only this
packet's directory.

**TWO REMEDIES WERE PUT BESIDE THE RECOMMENDED ONE, AND BOTH WERE DECLINED.**

- *Widen the `pin` kind's definition* to admit a commit-only pin of a GOVERNED
  repository's governance code. *Cost:* it would blur the one distinction D4
  calls "not decoration" — `pin` evidences the `pinned` governance class
  (openxFactory consumes a repository's CONTENT at a commit and digest and
  authors none of it), and row 3's governance class is `governed`:
  codexFactory's content is authored inside that repository's own estate, not
  consumed by openxFactory at a pin. Widening the kind to cover this case
  would let a `governed` row carry `pinned`-class evidence, the collapse D4
  already refused. Declined.
- *Add a sixth admission kind* for a commit-only pin of governance code —
  Copilot's own alternative ("change the schema/validator to define a
  separate pin kind"). *Cost:* row 3 is ALREADY admitted without it, by
  `gitlink` and `workflow`, neither disturbed by this ruling, so a sixth kind
  would admit nothing the inventory does not already carry — it would exist to
  answer a membership question row 3 never posed. Declined.

**WHAT THIS DOES NOT REACH.** The `pin` kind's own definition (the delta's
enumeration requirement) is untouched: every row it still admits (12-16, 26)
IS a real commit-and-digest pin of a `pinned`-class product, and the defect
ruled on was never the definition, only row 3's mistaken claim to it.
`contracts/review-lane-pin.yaml` itself is not edited by this ruling; it
continues to govern `.github/workflows/merge-master-approval.yml` exactly as
before, and which commit of codexFactory's governance code that workflow
trusts does not move. Nothing under `openspec/specs/` moves, no script and no
test moves, and openxFactory #1087 stays OPEN and closes at the archive.
**THE RECLASSIFICATION OF THE INVENTORY ROW ITSELF, AND THE RESOLUTION OF THE
#1119 THREAD IT LEFT OPEN, ARE NOT DONE HERE**: the ruling's own words send
them THEN — after this amendment lands on `main` — to PR #1119, a separate act
in a separate pull request.
