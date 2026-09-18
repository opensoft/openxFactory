# Proposal Ratification: add-estate-repository-inventory

Status: ratified
Kind: report
Decision date: 2026-09-18
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
and folds its text"*, *"MAY becomes MUST"*. All four acts are recorded here; §§ 1
and 2 carry the first, § 3 carries the three.

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

Written in the ruling-encoding commit, by lane `openxfactory-5` (display
`openXfactory-5`, session `651195c7`). It carries `Status: ratified` because
`document-lifecycle`'s *A review record records a ratification* governs a
`review/ratification-*` file. Every path in this file is repo-relative. The
lane register `opensoft/brett-wip` `lanes/log/openXfactory-5.md` is a SEPARATE
repository and is the channel of record for all four words.
