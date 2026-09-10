# Proposal Ratification: amend-neutral-product-pin-interim-copy-vocabulary

Status: ratified
Kind: report
Decision date: 2026-09-09
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-09 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), verbatim: *"Ratify with
TOLERATED"*, recorded on openxFactory PR
[#870](https://github.com/opensoft/openxFactory/pull/870) at
2026-09-09T23:31:12Z. **THE WORD IS A MULTIPLE-CHOICE RULING**, given over a
presentation that carried `design.md` **D1** as the packet's declared veto point
— **TOLERATED** (recommended and encoded) against **PERMITTED** (the word the
refusal on PR #780 itself floated) — with the alternative written out beside the
recommendation and the full cost of taking it ENUMERATED line by line. **D1 IS
RESOLVED AS TOLERATED, WHICH IS THE OPTION THE PACKET ALREADY ENCODED, SO THE
DELTA'S WORDING STANDS UNCHANGED AND NO SUBSTITUTION WAS PERFORMED.**

**THIS RECORD IS RE-DERIVED AND IT SUPERSEDES THE ONE WRITTEN AT `d0ddb126`.**
Two things about the earlier writing were wrong and Brett Heap ruled on both at
**2026-09-10T00:20Z** (§ 1.2): it carried `Status: record` where
`document-lifecycle` requires `Status: ratified` of a review record whose
subject IS the ratification, and it repeated the packet's *"one word each"*
accounting of the two replaced bullets, which is false of the `THEN` bullet.
Neither correction moves a normative unit of the delta, and the ratified word
itself is untouched: `Decision date:` stays **2026-09-09**, this file keeps its
2026-09-09 name, and the citation above is the one the ruling of 2026-09-09
produced. What is re-derived is the RECORD, on the corrected tree, on
2026-09-10. The gate run beside it is a SECOND RUN and therefore writes a
SECOND PATH — `review/verification-2026-09-10.md` — with the 2026-09-09 capture
preserved unedited (§ 4.5, T7).

Ratified baseline: this change as committed on the branch
`change/amend-neutral-product-pin-interim-copy-vocabulary` — `proposal.md`,
`design.md`, `tasks.md`, `.openspec.yaml` and `specs/neutral-product-pin/spec.md`
(**ONE `## MODIFIED` requirement**, *"A consumption pin that another repository
reads is a PUBLISHED contract member, adopted by pin-sync"*, restated over canon
byte-faithfully with **TWO scenario bullets replaced in place**, **ONE body
paragraph added** stating the reservation in one place, and **ONE scenario
added** at the end of the block asserting the record obligation). The delta's
normative units are byte-identical to the tree Brett Heap ruled on at
`d0ddb126`; the ONLY edit inside `specs/` since that commit is the `Removed from
canon` marker's REASON text, which is a declaration about the edit and not one
of the units it declares (§ 3).

## 1. The words, and exactly what each decided

### 1.1 The ratifying word — 2026-09-09T23:31:12Z

Brett Heap, 2026-09-09, verbatim:

> Ratify with TOLERATED

It is one utterance and it does two things at once. It **ratifies the packet**,
and it **answers the packet's own multiple-choice question** — the choice
`design.md` D1 put and refused to take on his behalf. Both halves are needed to
read the act correctly:

- **The ratification half.** The packet was a DRAFT: `.openspec.yaml` carried
  drafting provenance with no approval pair, every document carried
  `Status: draft`, and `tasks.md` § 1 was entirely open and closed to the
  authoring lane by its own terms. This word is the operator's act that flips
  that, and it is the FIRST word to reach the packet's *content*.
- **The D1 half.** The word names a WORD — `TOLERATED` — and that word is one of
  exactly two options D1 put. It is therefore a ruling on D1 and not merely an
  approval that happens to mention the packet's subject.

**The earlier word is the ORIGIN of the authoring and is NOT read as an
approval.** Brett Heap's *"R1 'lawful' amendment packet"*, also of 2026-09-09,
given in session as one option of several put to him, commissioned a lane to
WRITE this remedy. It ratified no wording and took no design decision, which is
why the packet was authored as a draft with no approval pair. That word stays
recorded as the origin in `proposal.md`'s `Proposed:` line, in `.openspec.yaml`'s
`proposed_by`, and in `tasks.md` § 1.1.

### 1.2 The two corrective rulings — 2026-09-10T00:20:16Z

Both were given as multiple choice over the bench standing on the ratified head
`d0ddb126`, and both are recorded verbatim on PR #870 at **2026-09-10T00:20:16Z**
(comment `5610667992`). **NEITHER RE-OPENS D1 AND NEITHER TOUCHES THE RATIFIED
WORDING.**

**Ruling (1), verbatim:**

> Keep the clause, fix the accounting

**What it decided.** Codex's P2 on `specs/neutral-product-pin/spec.md:188`
measured that the replaced `THEN` bullet does more than substitute a word: it
also APPENDS *"and is never LAWFUL, which this requirement spends on a
stack-pinned read alone"*. Codex offered two remedies — remove the added
normative clause, or record it explicitly as part of the ratified change surface.
**THE CLAUSE STAYS.** It is ratified text, it is the reason the reservation is
stated where the fallback is ADMITTED rather than only in the body paragraph
below, and removing it would be a wording change with no word behind it. What
was wrong was the ACCOUNTING — *"one word each"* — which described the `AND`
bullet's edit and applied it silently to the `THEN` bullet's. Corrected in every
place it appeared: the marker's reason text, `proposal.md`, `tasks.md` § 2.2, the
README row, and § 3 of this record. `.openspec.yaml` is FROZEN by the origin
shape and keeps its drafting-time count; **this record supersedes that count**
and § 3 states the correct one.

**Ruling (2), verbatim:**

> Follow canon: Status: ratified

**What it decided.** Codex's P1 on this file's line 3 read
`openspec/specs/document-lifecycle/spec.md`, scenario *A review record records a
ratification*: a `review/` document whose subject IS the change's ratification
**MUST carry `Status: ratified` and one ratification citation in a sanctioned
spelling**, and a `Ratifier:` or `Decision date:` header **MAY accompany the
citation but MUST NOT stand in place of it**. This file carried `Status: record`.
The ruling is to follow canon rather than the local precedent: the header above
is now `Status: ratified` with **exactly one** citation line — the `Ratified:`
line the earlier writing already carried, unchanged in substance — accompanied by
`Ratifier:` and `Decision date:`, which the scenario expressly permits. The
sibling `review/verification-2026-09-09.md` keeps `Status: record`, correctly: its
subject is the GATE RUN, not the ratification, and the scenario *A review record
is not about a ratification* is the one that governs it. The ruling also records
that the two archived precedents carrying `Status: record` over a ratification
subject, and the doc-health family gap that let this pass, are filed as UNCLAIMED
issues rather than fixed by this lane.

## 2. D1 as it was put, and D1 as it is resolved

### What was on the table

`design.md` D1 — **THE VETO POINT: TOLERATED against PERMITTED**:

- **TOLERATED** — recommended, and written into the delta. Three recorded
  grounds: (1) PERMITTED is a near-synonym of LAWFUL and *the defect is that two
  statuses shared one word*, so PERMITTED asks a reader to hold a distinction
  the two words do not themselves carry, while TOLERATED says admitted AND
  deprecated in one word; (2) the requirement already puts the copy on a clock
  (*"Such a copy SHALL be retired when that repository adopts a stack pin"*), and
  TOLERATED is the word for a conditional, terminal admission where PERMITTED
  reads as durable; (3) PERMITTED is already spent one capability over —
  `domain-descendant-boundary:113`, *"the placement is permitted"*, for a
  genuinely admitted, non-deprecated state — so re-spending it here would create
  the cross-requirement ambiguity this packet exists to end.
- **PERMITTED** — the alternative, and **not a straw option**: it is the word the
  refusal on PR #780 itself floated, in as many words — *"say `PERMITTED as a
  declared interim` in the scenario, reserving `lawful`/`compliant` for the
  required-check claim"*. That is why the decision was put for veto rather than
  simply taken.

### The resolution

**TOLERATED.** The word Brett Heap named is the recommended and already-encoded
option, so the ruling is applied **by leaving the text alone**. The
case-preserving substitution D1 described — an upper-case occurrence to
`PERMITTED`, a lower-case one to `permitted` — was **NOT** performed. The seven
occurrences D1 enumerated inside the `## MODIFIED Requirements` block
(`specs/neutral-product-pin/spec.md` lines 121, 133, 134 in the added body
paragraph; 170 and 171 in the two replaced canon bullets; 185 and 186 in the
added scenario) are ratified **exactly as written**, and they are still at those
lines: the corrective commit changed one line of that file, line 188, and it is
the marker.

**Why the enumeration mattered even though nothing moved.** D1's list of seven
was not decoration: it is what made the choice mechanical rather than a judgment
call, and it is the reason a PERMITTED ruling could have been applied
faithfully. Replacing only SOME of the seven would have left both status words
live inside one requirement — the exact defect this packet closes — so a veto
applied to a wrong count would have re-created the contradiction. The
enumeration was added in response to a review finding (§ 4).

### What D1 did NOT decide

D2 (state the reservation in the requirement BODY rather than leaving the two
bullets to carry it alone) and D4 (add a scenario rather than rely on the body
alone), together with D3, D5 and D6, were carried beside D1 in the pull request
body, in `tasks.md` § 1.2–1.3 and in the README row. **None was vetoed**, and
each stands as designed. `tasks.md` § 1.3 records that.

## 3. THE RATIFIED SURFACE, ACCOUNTED FOR CORRECTLY

**THE TWO REPLACED BULLETS ARE NOT THE SAME SIZE, AND THE PACKET USED TO SAY
THEY WERE.** This section replaces the *"two scenario bullets replaced in place,
one word each"* claim the record written at `d0ddb126` carried, and it is the
accounting ruling (1) required. The two bullets sit under the scenario *A
repository with no stack pin adopts the gate anyway*, both are declared by ONE
`Removed from canon` marker, and neither is dropped:

| bullet | canon (removed) | ratified (replaced in place) | the edit |
| --- | --- | --- | --- |
| `THEN` | *"the copy is **lawful** ONLY as a declared interim naming the `openxFactory` commit it was taken from, the digest of what it copied, and the divergence it accepts"* | *"the copy is **TOLERATED** ONLY as a declared interim naming … the divergence it accepts, **and is never LAWFUL, which this requirement spends on a stack-pinned read alone**"* | **ONE WORD REPLACED *AND* A RESERVATION CLAUSE APPENDED** |
| `AND` | *"it is retired when that repository adopts a stack pin, an undeclared duplicate never becoming **lawful** by being useful"* | *"…an undeclared duplicate never becoming **tolerated** by being useful"* | one word replaced, and nothing else |

**THE APPENDED CLAUSE IS RATIFIED SURFACE AND IT STAYS** (ruling 1). It is not
an oversight and it is not a second rule: it states, inside the bullet that
ADMITS the fallback, the same reservation the added body paragraph states in one
place — so a reader who meets the scenario before the body still learns that
LAWFUL is spent on a stack-pinned read alone. **NOTHING THE REQUIREMENT ADMITS OR
REFUSES MOVES BECAUSE OF IT**: the same copies are admitted on the same four
terms, and the required-check claim stays unmet for exactly as long as it did
before, which is what the refusal on #780 predicted of this remedy.

**WHERE THE CORRECTION LANDED.** `specs/neutral-product-pin/spec.md` (the
marker's REASON text only — no unit the marker names, no scenario title, no
`WHEN`/`THEN`/`AND` bullet and no body paragraph moves), `proposal.md`,
`tasks.md` § 2.2, the README row, and this record. **`.openspec.yaml` IS NOT
CORRECTED AND MUST NOT BE**: its `reason` and `proposed_by` are the packet's
frozen DRAFTING-TIME provenance, held byte-stable by the
`add-drafted-proposal-origin` shape and read by the archive gate's
origin-retention arm. Its *"one word each"* is what the authoring lane believed
on 2026-09-09; **this record is where that count is superseded**, and a reader
who meets the origin block reads it as drafting-time provenance rather than as a
current claim.

## 4. The bench

### 4.1 The rounds

| bench | commit | verdict |
| --- | --- | --- |
| Copilot round 1 | `9c26a97c` (2026-09-09T21:55:37Z) | 🟢 **Approval recommended** — *"limited to documentation/spec artifacts and ledger bookkeeping, with only minor Markdown inline-code formatting issues noted in README.md"* |
| Codex round 1 | `9c26a97c` (2026-09-09T21:59:45Z) | one **P2** on `design.md`; TAKEN |
| Copilot round 2 | `d42dbf6b` (2026-09-09T22:12:59Z) | 🟢 **Approval recommended** — 7/7 files reviewed, **0 new comments**, *"no functional code changes and no review-blocking issues found"* |
| Copilot round 3 | `d0ddb126` (the ratification encode) | **three findings** — T1, T2, T3 below |
| Codex round 2 | `d0ddb126` | **one P1, two P2** — T4, T5, T6 below |
| Sourcery | `947eec04` | ABSENT — upsell stub (*"Your private repo does not have access to Sourcery"*), not a review |

### 4.2 The two findings taken before the ratification encode

1. **Codex P2 on `design.md`: "Count every replacement required by the veto."**
   Codex measured that the normative block carries **SEVEN**
   `TOLERATED`/`tolerated` occurrences, not the four the packet had claimed a
   veto would cost, and named the consequence that makes it a defect rather than
   an arithmetic slip: *"Replacing only one word in each named unit leaves both
   status terms active, while replacing all occurrences changes more text than
   the stated ratification surface."* **TAKEN at `d42dbf6b`.** D1 now ENUMERATES
   the replacement set line by line rather than counting it.
2. **Copilot on `README.md`: two broken inline code spans.** **TAKEN as an edit
   at `d42dbf6b`, with the stated defect corrected on the record**: CommonMark
   converts a line ending inside a code span to a space, so both spans render and
   copy whole — but a command a reader is invited to re-run should be copyable
   without depending on that conversion.

### 4.3 The six findings on the ratified head `d0ddb126`, and their disposition

Five TAKEN, one REFUSED with the reason recorded. All six are dispositioned on
the re-derived head.

| # | bench | site | finding | disposition |
| --- | --- | --- | --- | --- |
| T1 | Copilot | `README.md:533` | the verification record is cited as a bare `verification-2026-09-09.md` beside a full-path citation of the ratification record | **TAKEN** — both records now cited at full path |
| T2 | Copilot | `.openspec.yaml:36`, `:55` | `origin.reason` says the packet *"is a DRAFT and carries no approval pair"* while the same file now carries `approved_by`/`approved_on` | **REFUSED** — § 4.4 |
| T3 | Copilot | `proposal.md:238` | the closing bullet still read *"It ratifies nothing. `Status: draft`"* under a `Status: ratified` header | **TAKEN** — reworded to the point it was making |
| T4 | Codex **P1** | `review/ratification-2026-09-09.md:3` | `Status: record` where `document-lifecycle` requires `Status: ratified` plus one citation of a review record whose subject is the ratification | **TAKEN** on Brett Heap's ruling (2) — this file's header |
| T5 | Codex P2 | `proposal.md:238` | same site as T3, same defect, stated as a contradiction with the authoritative lifecycle header | **TAKEN** with T3 |
| T6 | Codex P2 | `specs/neutral-product-pin/spec.md:188` | the marker says the bullets' only edit is the vocabulary replacement, but the `THEN` bullet also appends the reservation clause, so the repeated *"one word each"* accounting is false | **TAKEN** on Brett Heap's ruling (1) — the clause STAYS, the accounting is corrected (§ 3) |
| T7 | Codex **P1** (on `27b31718`) | `review/verification-2026-09-09.md:11` | a dated run report is a one-shot `record`; a SECOND run must write a different path rather than rewrite the first capture | **TAKEN** — § 4.5 |
| T8 | Codex **P1** (on `27b31718`) | `specs/neutral-product-pin/spec.md:129` | reserving LAWFUL to the entrypoint-invoking read is said to make the sanctioned resolver-backed ARCHIVE path unlawful, so the amendment would change behaviour | **REFUSED** — § 4.5 |

### 4.4 T2 REFUSED, and why the origin prose stays in the present tense

Copilot asks that `origin.reason`'s *"this packet is a DRAFT and carries no
approval pair"* be switched to the past tense now that `approved_by` and
`approved_on` exist. **REFUSED, and the refusal is the shape of the origin block
rather than a preference about tense.**

- **The origin block is DRAFTING-TIME PROVENANCE and it is frozen.**
  `add-drafted-proposal-origin` (issue #318) defined exactly this transition:
  the lawful unapproved shape is drafting provenance with no `approved_by` and no
  `approved_on`, and approval, when it comes, is a **pure ADDITION beside a fixed
  `kind` and `id`** — never a rewrite of what the drafting lane declared. Editing
  `reason` or `proposed_by` to read as though the packet had always been approved
  would destroy the record of what was true when the packet was proposed, which
  is the one thing the block exists to preserve.
- **The archive gates hold it byte-stable.** `scripts/proposal-support.py`'s
  origin-retention arm (`--archive-gate … --ratified-ref`) reads the declaration
  this branch establishes and compares it across the ratification; a tense edit
  is a byte change to a field the gate is written to find unchanged.
- **The precedent is this lane's own, one packet back.** `#850` —
  `openspec/changes/archive/2026-09-09-amend-marker-defect-reporting/.openspec.yaml`
  — carries the same drafting-time tense in `proposed_by` through ratification
  AND through archive, unedited. A reader who meets either block reads it the
  same way in both.
- **There is no contradiction to remove.** The two halves of the file are dated
  by their own keys: `proposed_on: 2026-09-09` governs the origin prose,
  `approved_on` governs the approval prose, and the approval prose says in as
  many words that it **IS ADDED, NOT SUBSTITUTED**. Nothing on the page claims the
  packet is a draft TODAY.

The one thing the origin block does carry that is now known to be wrong is its
*"one word each"* count, and **that is superseded by § 3 of this record rather
than by an edit to the frozen field** — for the same reason.

### 4.5 T7 TAKEN and T8 REFUSED — the two P1s on the re-derived head

**T7 — "Write the rerun to a new verification record". TAKEN, and Codex is right
on the contract.** `openspec/specs/document-lifecycle/spec.md`, under *Controlled
document status taxonomy*: a one-shot capture — *"a simulation report, an audit
output, **a dated run report**, a byte-exact evidence snapshot"* — is NOT a
projection, keeps `record`, and **"a second run of such a generator writes a
different path rather than rewriting the same one"**. The 2026-09-10 gate run is
a SECOND run of the same report, and the first draft of it rewrote
`review/verification-2026-09-09.md` in place. Codex also named the right reason
the rewrite looked clean: `record-immutability` does not scan `review/` — its
family iterates the GOVERNED corpus while a `review/` record lives in the
LIFECYCLE scan set — and **a checker-coverage gap is not a licence**. Fixed:
`review/verification-2026-09-09.md` is RESTORED byte-for-byte to its `d0ddb126`
bytes (`git diff d0ddb126 -- …/review/verification-2026-09-09.md` is EMPTY), and
the re-run is written at `review/verification-2026-09-10.md`, which names what it
supersedes in its own header. The family gap is filed rather than relied on.

**T8 — "Keep the sanctioned archive path lawful". REFUSED, on the merits AND on
authority, in that order.**

Codex reads the added paragraph's *"LAWFUL names … the read a repository carrying
an `xfactory:` stack pin performs by checking `openxFactory` out at its own
`stack.yaml` `xfactory.contract_ref` and invoking the entrypoint the registered
pin names FROM THAT CHECKOUT"* as excluding `scripts/proposal-support.py`'s
archive path, which resolves the pin and invokes the resolved binary directly
because the entrypoint rejects the `archive` verb — and concludes the amendment
changes behaviour.

1. **THE SENTENCE IS CANON'S OWN, WORD FOR WORD, AND THIS PACKET DID NOT NARROW
   ANYTHING.** `openspec/specs/neutral-product-pin/spec.md:294-297` already
   states, as promoted canon: *"A repository that carries an `xfactory:` stack pin
   SHALL, where it gates on the pinned product, check `openxFactory` out at its
   own `stack.yaml` `xfactory.contract_ref` and invoke the entrypoint the
   registered pin names FROM THAT CHECKOUT."* The added paragraph names the
   lawful consumption by QUOTING that sentence. If the phrase excluded the
   resolver-backed archive, it excluded it before this packet was written, and
   the defect would be canon's rather than the amendment's.
2. **THE SAME REQUIREMENT ALREADY RECONCILES IT, FOUR PARAGRAPHS UP, AND THE
   BLOCK CARRIES THAT TEXT UNCHANGED.** *"WHERE THE TWO GOVERNED ACTS ARE REACHED
   BY TWO DIFFERENT COMMANDS, THE REGISTER SHALL NAME BOTH … Where an act is
   reached through a second tool that resolves the pin rather than through the
   entrypoint itself, that tool SHALL be named, with the fact that it verifies
   the content address before invoking the resolved binary"*, asserted by the
   carried scenario *The published instructions name a verb the entrypoint
   rejects*. **"The entrypoint the registered pin names" is read against the
   REGISTER**, and `contracts/manifest.yaml`'s own `consumption_rule` for this pin
   names BOTH commands in as many words — the validating entrypoint, and
   *"the ARCHIVE act runs through `scripts/proposal-support.py <root> archive
   <change-id>` in the SAME pinned checkout"*. The sanctioned archive is a
   registered command performed from the repository's own stack-pinned checkout;
   it is on the LAWFUL side of this reservation, not outside it.
3. **THE RESERVATION'S SUBJECT IS COPY-VERSUS-PINNED-READ, NOT
   ENTRYPOINT-VERSUS-RESOLVER.** It is scoped *"WHERE THIS REQUIREMENT SPEAKS OF
   A CONSUMPTION'S STATUS"*, and the two statuses it separates are a DECLARED
   CONSUMPTION COPY in a repository with no stack pin (TOLERATED) and the read a
   stack-pinned repository performs from its own checkout (LAWFUL).
   `proposal-support.py` is not a declared consumption copy under any reading.
4. **AND THE TEXT IS RATIFIED.** Brett Heap ruled D1 over exactly this wording at
   2026-09-09T23:31:12Z. Working rule 3 — a ratified requirement changes only by
   a ratified change — is the limit the refusal on PR #780 respected, and it is
   the reason this packet exists at all. Editing the added paragraph now, on a
   review finding and with no word, would repeat the error #780 declined to make.

**IF THE READING IS STILL THOUGHT TOO NARROW, THE REMEDY IS A SUCCESSOR WITH ITS
OWN WORD**, not an edit here — and it would be an amendment about the
ENTRYPOINT/RESOLVER pair, which is a different subject from this packet's
vocabulary reconciliation. It is named here as an available successor rather
than taken.

## 5. Why the packet exists: a refused finding, not a fix

**The origin is a review finding on a DIFFERENT act.** Codex raised it as a
**P2 on PR [#780](https://github.com/opensoft/openxFactory/pull/780)** — the
ARCHIVE of `publish-openspec-cli-pin-as-contract-member`, the act that promoted
that packet's delta into `openspec/specs/neutral-product-pin/spec.md` — against
the promoted requirement *A consumption pin that another repository reads is a
PUBLISHED contract member, adopted by pin-sync*:

> For a repository without an `xfactory:` stack pin, this scenario declares a
> properly documented copy "lawful," while [the same requirement] explicitly
> state[s] that declaring the copy does not make it lawful and leaves the
> required-check claim unmet. … distinguish "permitted as an interim" from
> "compliant with the required-check requirement", or use one consistent status.

**THE FINDING WAS REFUSED IN THAT PULL REQUEST — ON THE PULL REQUEST'S LIMIT AND
NOT ON THE READING.** The text is promoted, ratified canon: ratified by Brett
Heap on 2026-09-07 as part of `publish-openspec-cli-pin-as-contract-member`
(PR #757 → `a5940811`, ratifying commit `05a9db8b`) and written into the
specification byte-for-byte by the archive act, whose own evidence is that the
promoted block is byte-identical to the ratified delta (sha256
`8d31ffee932339919461da8d69ec4287ad15d14f39f9e64df7c2b13f82bbd902`, 9,462 bytes,
on both sides). Rewording it in that pull request would have edited ratified text
with no word behind it and destroyed the byte-identity that makes the archive
auditable. The refusal recorded the remedy instead — *"the fix is a vocabulary
change … and NOT a change to which behaviours are admitted — no consumer's
conformance outcome moves either way"* — and left the successor to the owner's
word, which working rule 3 requires in general: **a ratified requirement changes
only by a ratified change.**

The successor was filed by this lane as openxFactory issue
[#868](https://github.com/opensoft/openxFactory/issues/868) and authored on
Brett Heap's *"R1 'lawful' amendment packet"*. **This record is the word that
closes that loop at the RATIFICATION step; it does not close #868**, which
closes at the archive (§ 7).

## 6. What is NOT ratified, and the residue this word does not reach

- **NOTHING IS PROMOTED.** This ratification edits no file under
  `openspec/specs/`, no script, no test, no contract, no schema and no workflow.
  The `## MODIFIED` block is a DELTA; canon still carries the defect until the
  archive writes the block over it.
- **`spec/neutral-product-pin` FAILS `--strict` ON `main` TODAY, AND THIS PACKET
  NEITHER INHERITS NOR FIXES IT.** The failure is
  `✗ [ERROR] requirements.16.text: Requirement must contain SHALL or MUST
  keyword` — a promoted requirement whose body's FIRST LINE carries neither
  keyword, which is the parser's documented limit. It is **unrelated to this
  packet's subject**: requirement 16 is not the requirement this block modifies,
  the defect is structural rather than vocabulary, and no edit in this packet
  touches it. This packet's own delta validates clean
  (`verification-2026-09-10.md` § 1, the re-run capture), and the repository-wide
  failure SET is byte-identical to `origin/main`'s (§ 2 there). `tasks.md` § 5.2 records the
  strict failure as an OWED SUCCESSOR and not as this packet's work.
- **Issue #775 is a different defect on the same requirement** and is untouched
  (`tasks.md` § 5.3).
- **The estate's one live declared copy is unaffected in both directions**
  (`tasks.md` § 5.4): no consumer's conformance outcome moves, which is exactly
  what the refusal on #780 promised of this remedy.
- **`tasks.md` § 4 (archive) STAYS OPEN**, and § 5.2–§ 5.4 stay open as measured
  residue rather than work performed.
- **THE TWO ARCHIVED `Status: record` PRECEDENTS AND THE DOC-HEALTH FAMILY GAP
  ARE NOT FIXED HERE.** Ruling (2) files them as unclaimed issues: `Status:
  ratified` on this record follows canon, and correcting archived records or
  widening `ratified-provenance` to catch a review record whose SUBJECT is a
  ratification are separate acts on separate words.

## 7. Ordering against the sibling delta, and the landing obligation

**There is exactly one other active `neutral-product-pin` delta, it is another
lane's, and NO ORDERING DECLARATION IS OWED IN EITHER DIRECTION.** The pull
request body states the measurement rather than the assumption, and it is quoted
here verbatim as the claim this ratification rests on:

> **NO ORDERING DECLARATION IS OWED, in either direction, and it is measured
> rather than assumed.** `ls openspec/changes/*/specs/neutral-product-pin/`
> returns exactly ONE other active delta — `split-opendox-two-layer-product`
> (ratified 2026-09-05, another lane's) — which modifies *An external neutral
> product is pinned by commit and digest, never by tag* and *The consuming
> repository's pin is authoritative among reachable checkouts*. **Neither is the
> requirement this packet modifies**, and no active change writes this
> requirement's key. `modified-block-currency`'s two-writers rule is scoped to
> two ACTIVE writers and does not reach the pair; the two blocks share a spec
> FILE and no requirement key, which is not a collision. `sequenced_after: []`
> is the positive root claim.

`sequenced_after: []` is therefore a POSITIVE root claim and not an omission, and
`scripts/validate-sequenced-after.py` passes on it
(`verification-2026-09-10.md` § 4).

**THE ARCHIVE IS A SEPARATE ACT ON A SEPARATE WORD, AND #868 CLOSES THERE.**
Under `release-realization` an empty `code_surface` archives ON LANDING plus its
own task list rather than on merged-plus-green realization evidence — but that
archive is not performed by this commit and is not authorized by this word. The
pull request body carries **`refs #868`** and **no closing keyword anywhere**,
which is what keeps the origin issue open through this landing.

**This lane encodes and freezes; it does not merge.** Brett Heap's separate word
of 2026-09-09, recorded on PR #870 at 2026-09-09T23:33:18Z — *"land 870 when
green"* — is the landing authority, and it is conditioned on green: the Rule 6
LANDING/LANDED post belongs to the landing lane once the bench is dispositioned
and the required checks are green on the re-derived head.
