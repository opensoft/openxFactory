# Proposal Ratification: refresh-install-repository-enumerations

Status: record
Kind: report
Decision date: 2026-09-09
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-09 by Brett Heap (openxFactory operator authority) —
in-session, lane `openxfactory-3`, verbatim: *"ratify
refresh-install-repository-enumerations"*, recorded on openxFactory issue
[#591](https://github.com/opensoft/openxFactory/issues/591) as comment
**5593837071** at 2026-09-09T00:24:24Z. The word names this packet and nothing
else. It was given over a text carrying **all three** of the packet's veto
points — `design.md` **D1** (WIDEN the enumerations and state the index rule,
against replacing the hand lists with a list derived from the aggregation's
`installs/` mount list), **D3** (the SIX-`## MODIFIED` scope, of which exactly
TWO widened units are absent from issue #796's own list) and **D5** (the one
deliberately OPEN-ENDED widening, *"Submodule sequencing"*) — each carried
verbatim in `tasks.md` § 1.2, in openxFactory PR
[#818](https://github.com/opensoft/openxFactory/pull/818)'s body under the
heading *"Veto points, put verbatim"*, and in the README records row.
**NONE OF THE THREE WAS VETOED.**
Ratified baseline: this change as it stood at openxFactory PR **#818**'s merge
— squash **`6da94302`** (2026-09-09T00:20:31Z), which landed `proposal.md`,
`design.md`, `tasks.md`, `.openspec.yaml`, the three delta files under `specs/`
(**6 `## MODIFIED` requirements and 1 `## ADDED`**), one README *"OpenSpec
Records"* row and one `tests/sequenced_after/corpus-ledger.yaml` row, and
touched nothing else — plus the records-only edits of the ratification commit
carrying this record, which flip the three `Status:` headers, add the ONE
citation line to each document, ADD the approval pair to `.openspec.yaml`
beside the drafting provenance, write this record, and move the README row's
status wording. **NO DELTA IS PROMOTED BY EITHER COMMIT** and
`openspec/specs/` is untouched by both.

**THIS RECORD IS CAPTURED AT MERGE, NOT AT FIRST PUSH.**
`record-immutability` forbids editing a `Status: record` document AFTER
capture, and capture is the merge of the pull request that establishes it. A
commit cannot write its own hash into its own tree, so the ratification commit
is named by its subject and its position on the branch rather than by a hash.

## 1. What was ratified

**A REFRESH OF FOUR HAND-WRITTEN INSTALL-REPOSITORY ENUMERATIONS, PLUS THE
INDEX RULE THAT SAYS WHAT THEY ARE.** `opensoft/OmniWorker-Install` was created
2026-09-05T16:15:48Z, admitted to the top-level xFactory aggregation at
`installs/omniworker-install` by opensoft/xFactory#274 → `648c8bd3`, and given
a promoted boundary requirement by openxFactory#803 → `d7fbe933` — a fifth
install repository that exists, is mounted and is governed, while four hand
lists across three capabilities still described an estate of two or four.

- **6 `## MODIFIED` requirements**, each restating the promoted text word for
  word and each carrying a `Removed from canon by
  refresh-install-repository-enumerations (2026-09-08):` marker naming ONLY the
  unit its block genuinely replaces:
  `repo-boundary-governance` — *Install repository scope*, *Canonical workflow
  authority*, *Copy-first migration*; `shared-contract-ownership` — *Contract
  version pinning*, *Submodule sequencing*; `canonical-contract-migration` —
  *Contract provenance and compatibility*.
- **1 `## ADDED` requirement** — *Install-repository enumerations are an index
  with a named authority*: the enumerations are an INDEX and not the authority
  for which repositories exist; authority for ADMISSION AND MOUNTING is the
  aggregation's `installs/` mount list, while authority for a repository's
  EXISTENCE and scope is the reviewed act that created it plus its own boundary
  requirement; a mechanical derivation must declare its filter and is refused
  where its SELECTED SET EXCEEDS ITS DECLARED SCOPE; and a change admitting a
  further install repository must refresh every enumeration or NAME the
  successor that will.
- **No generator, checker, script, workflow or test** — deliberately, as D1's
  refusal of the derived option and D4's reasoning state.

## 2. The three decisions ratified knowingly

### D1 — WIDEN NOW and state the index rule, against DERIVE from `installs/`

Ratified as designed. The derived option — issue #796's own second option — is
recorded **NOT TAKEN rather than foreclosed**, refused on a measurement: the
aggregation mounts **NINE** paths under `installs/` against an indexed set of
**FIVE**, so a derivation would enrol `AgentTower` and
`xFactory-MedxRootTruth-Install` into a requirement no reviewed act placed them
under, overlap `CloudPC-Install` (governed by `workstation-intake`), and
duplicate `xFactory-Installer` (governed by its own *"Neutral installer
repository integration"*). What the derived option gets right is kept as a
REQUIREMENT instead of a script, and the ADDED requirement's third scenario
says what a future derivation would owe.

### D3 — the SIX-`## MODIFIED` scope, two units wider than issue #796's list

Ratified as designed. **Exactly TWO** widened units are absent from #796's
list, both `WHEN` bullets in `repo-boundary-governance` — *Canonical workflow
authority* and *Copy-first migration*. Refusing D3 would have meant deleting
exactly those two blocks; the `canonical-contract-migration` delta was NOT part
of that refusal, because that widening is #796's own item 2 under the corrected
reading (that capability names `Hermes-Install` nowhere, so its in-scope unit is
the runtime-adapter trigger rather than a repository pair). The reason for
going wider was put with the decision: a packet whose stated purpose is *"the
enumerations are stale"* that widens one bullet and leaves the bullet two
requirements below it reproduces, inside its own diff, the failure the issue's
addendum names.

### D5 — the one OPEN-ENDED widening, *"Submodule sequencing"*

Ratified as designed. That scenario governs the admission of a repository which
by definition is not yet indexed, so it carries the five names **`or a later
install repository`** while every other widened unit is a closed five-name list
in canon's own grammar, serial comma included.

## 3. What this word does NOT reach

1. **THE ARCHIVE IS A SEPARATE ACT ON A SEPARATE WORD.** `code_surface: none`,
   so under `release-realization` this packet archives ON LANDING rather than on
   merged-plus-green realization evidence — but landing is not this pull
   request's to take for it. **This word ratifies; it does not archive**, and
   the archive is what PROMOTES the six MODIFIED blocks and the one ADDED
   requirement into canon. Until then no promoted specification byte has moved.
2. **THE `## Purpose` WIDENING STAYS OWED** (`tasks.md` § 4.1, UNTICKED).
   `repo-boundary-governance`'s `## Purpose` has not moved since `9ebceeff`
   (2026-06-26) and is three repositories behind. A `## Purpose` in a spec delta
   is read ONLY at capability creation and ignored on any later archive, so the
   edit cannot travel in this packet's deltas; it is booked for the archive
   commit, in a hunk SEPARATE from the promotion, on the
   `publish-openspec-cli-pin-as-contract-member` § 5.8 precedent (`d712ce29`),
   with the proposed sentence quoted verbatim in the task and its edit stated
   character by character — three names appended AND the conjunction `and `
   moving to the last item of the serial list, every other character
   byte-identical.
3. **openxFactory#796 STAYS OPEN** (`tasks.md` § 4.2, UNTICKED). It closes when
   the enumerations MOVE, which is the archive, not when they are ratified —
   which is why this pull request says `Refs` and never a closing keyword.
4. **§ 3's SIX STATEMENT BOXES STAY UNTICKED BY DESIGN.** They state what the
   packet does NOT do — no promoted spec edited, no generator written, no
   contract cut, no repository touched, the two candidate sites left alone,
   *Install repo scope links* not widened — and the archive act disposes them.
5. **THE LEDGER ROW DOES NOT MOVE ON A RATIFICATION.** `state` is still
   `active`, and `class`, `declares`, `depth` and `prose` are unchanged, so the
   ratifying commit re-seeds nothing; § 4.3 re-seeds `active` → `archived` at
   the archive.
6. **The two unclaimed candidate sites are not filed and not edited**:
   `contracts/README.md` line 18 (an editorial release-inventory member whose
   edit would put a `release-inventory-drift` finding on `main` until the next
   cut) and `docs/repo-boundary-pilot-plan.md` line 100 (a dated historical
   record).

## 4. The record of the two words, kept apart

**TWO WORDS EXIST AND ONLY THE SECOND RATIFIES.** *"do 794, 795 and 796"*
(Brett Heap, 2026-09-08 ~14:3xZ, same issue) ADMITTED the work: it selected
three filed issues to be worked and said nothing about which of #796's two
options is right, what any requirement should say, or whether the widening
should happen at all. The packet said so in its own words — *"THAT WORD ADMITS
THE WORK; IT RATIFIES NO TEXT"* — and was authored `Status: draft` with drafting
provenance only, which is the lawful unapproved shape
`add-drafted-proposal-origin` defined. *"ratify
refresh-install-repository-enumerations"* (2026-09-09 ~00:24Z) is the word that
reaches the text.

**THE DRAFT-STATE SENTENCES ARE QUOTED IN PLACE, NOT DELETED.** FOUR sentences
are superseded by this act — three in `proposal.md` (the `Status: draft` /
no-citation claim, *"Every box in `tasks.md` is unticked"*, and the sentence
opening its § Ratification) and one in `tasks.md` (*"EVERY BOX BELOW IS
UNTICKED"*) — and each is carried verbatim under a dated file-forward note or
disposition, because ratified bytes do not move to tidy a tense and because
those sentences are the record of the state the packet was reviewed in.

**THE RECORDING SURFACE IS DISCLOSED.** `tasks.md` § 1.1 names two surfaces
for the ratifying word — the pull request, or openxFactory#796 — and the word
arrived on **neither**: it was given in session and recorded on
**openxFactory#591**, the surface that same box already cites for Brett Heap's
word of 2026-09-08 on this packet. The obligation the box carries is that the
word be DURABLY RECORDED and citable rather than asserted from a session, and
it is: issue, comment id and timestamp are all named above. **The precedent is
in this packet's own family** — the archived
`implement-omniworker-install-repo` took Brett Heap's *"Accept Omni001-XEAON"*
ruling and the approval of its four dated amendments on openxFactory#591 and
archived on them. The enumeration is under-inclusive rather than the record
being absent, and it is disclosed here rather than edited, because ratified box
text does not move to fit the act that satisfied it. Raised by
`chatgpt-codex-connector` as a **P2** and taken as this disclosure.

**APPROVAL IS AN ADDITION.** `.openspec.yaml` gains `approved_by` and
`approved_on` BESIDE the drafting provenance it was authored with; `kind`, `id`
and `reason` never move. That is `add-drafted-proposal-origin`'s own rule for
this transition, and the shape the archive gate's origin-retention arm reads.

## 5. The bench that stood behind the ratified text

The ratified baseline is the FOLDED text of openxFactory PR **#818**, not its
first draft: **six review rounds, fourteen findings, ALL TAKEN, NONE
DECLINED** (Copilot rounds 1, 2, 4 and 6; Codex rounds 1, 3 and 5), of which
three were correctness defects in the proposed canon — the
existence-versus-admission conflation in the ADDED requirement, its
unconditional derivation veto, and three widenings that changed canon's GRAMMAR
where a pure list extension was available — four were internal inconsistencies,
three were punctuation or rendering defects each falsifying a *"word for word"*
claim by one character, and two were unsupported claims. **Four of the corrected
items were introduced by the lane's own fix rounds**, and each commit message
says which. Copilot's sixth round, at `28641bf0`, returned 🟢 *"Approval
recommended — the changes are governance/docs-only and internally
consistent"*. Sourcery's comments were the private-repository upsell stub, not
a review.

## 5a. The review of THIS recording pull request

**Round 1 — Copilot (1 finding) and Codex (1 P2). BOTH TAKEN; nothing
declined.**

| Finding | Verdict |
|---|---|
| Copilot: this record's § 6 named the lane registry by a **home-directory path** — a workstation-specific location, against the constitution § IV rule that committed files carry no host-absolute paths | **TAKEN.** § 6 now names the lane registry as `LANES.md` at the aggregation workspace root and cites the rule. **THE OFFENDING FORM IS DESCRIBED HERE AND NOT REPRODUCED**, on this lane's own #818 lesson that a sentence quoting the defect verbatim reintroduces it. Disclosed with it: **three archived ratification records in this corpus carry the same form** — a pre-existing class this record does not widen and does not edit, because `record-immutability` forbids editing a captured record |
| Codex **P2**: § 1.1 names the pull request or openxFactory#796 as the ratifying word's surface, while the evidence cites openxFactory#591 — so ticking it records a ratification whose own location condition is unmet | **TAKEN AS A DISCLOSURE, and the tick STANDS.** § 4 above and § 1.1's evidence now state the surface question in terms: the word is durably recorded (issue, comment id, timestamp), #591 is the surface § 1.1's own third sentence already cites for Brett Heap's word on this packet, and `implement-omniworker-install-repo` archived on two rulings taken there. The enumeration is under-inclusive; the record is not absent |

**One correction was self-found rather than raised, and is disclosed rather
than smoothed over.** The README row carried the clause *"all boxes in
`tasks.md` are unticked"*, which this pull request's own § 1/§ 2 ticks falsify.
It now reads that § 1 and § 2 are ticked while § 3 and § 4 stay unticked. That
is one clause of the same row whose status wording this act moves, and no other
byte of README moves with it.

**Sourcery:** the private-repository upsell stub, not a review.

## 6. The landing obligation

**Rule 6 applies.** This pull request touches `openspec/changes/` and carries a
README *"OpenSpec Records"* edit, so lane `openxfactory-3` posts
`LANDING — lane openxfactory-3, session <id>, <UTC>, PR #<n> into openxFactory
main` on the pull request and in the lane registry `LANES.md` at the xFactory
aggregation workspace root — named repo-relatively rather than by a
workstation path, on the constitution's § IV rule that committed files carry no
host-absolute paths — before the merge, and `LANDED — lane openxfactory-3,
<UTC>, PR #<n> → <merge sha>` after it. **The landing is the coordinator's
act, not this author's**, and this author neither merges nor archives.
