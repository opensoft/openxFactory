# Proposal Ratification: amend-neutral-product-pin-interim-copy-vocabulary

Status: record
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
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/neutral-product-pin/spec.md` (**ONE `## MODIFIED` requirement**, *"A
consumption pin that another repository reads is a PUBLISHED contract member,
adopted by pin-sync"*, restated over canon byte-faithfully with **TWO scenario
bullets replaced in place, one word each**, **ONE body paragraph added** stating
the reservation in one place, and **ONE scenario added** at the end of the block
asserting the record obligation).

## 1. The word, and exactly what it decided

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
added scenario) are ratified **exactly as written**.

**The two sentences the packet encodes, and which this ruling ratifies**, are
the fallback scenario's replaced bullets:

> **THEN** the copy is TOLERATED ONLY as a declared interim naming the
> `openxFactory` commit it was taken from, the digest of what it copied, and the
> divergence it accepts, and is never LAWFUL, which this requirement spends on a
> stack-pinned read alone

> **AND** it is retired when that repository adopts a stack pin, an undeclared
> duplicate never becoming tolerated by being useful

So `lawful` is now spent on a stack-pinned consumption and on nothing else, the
declared interim copy is TOLERATED on the **same four terms** it was always
admitted on, and **an undeclared duplicate never becomes tolerated by being
useful** — the admission attaches to the DECLARATION, not to the copy's
usefulness. The added body paragraph states the same reservation in one place and
adds the record obligation: *"a gate record SHALL NOT describe a tolerated
interim as lawful or as compliant, and SHALL say TOLERATED where it means
admitted-as-an-interim"*.

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

## 3. Why the packet exists: a refused finding, not a fix

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
closes at the archive (§ 6).

## 4. The bench

Four bench passes stand on this pull request. **Two rounds of Copilot, both
"Approval recommended"; one Codex round, whose two findings were TAKEN.**

| bench | commit | verdict |
| --- | --- | --- |
| Copilot round 1 | `9c26a97c` (2026-09-09T21:55:37Z) | 🟢 **Approval recommended** — *"limited to documentation/spec artifacts and ledger bookkeeping, with only minor Markdown inline-code formatting issues noted in README.md"* |
| Codex round | `9c26a97c` (2026-09-09T21:59:45Z) | one **P2**; taken (below) |
| Copilot round 2 | `d42dbf6b` (2026-09-09T22:12:59Z) | 🟢 **Approval recommended** — 7/7 files reviewed, **0 new comments**, *"no functional code changes and no review-blocking issues found"* |
| Sourcery | `947eec04` | ABSENT — upsell stub (*"Your private repo does not have access to Sourcery"*), not a review |

**TWO FINDINGS WERE TAKEN, AND BOTH ARE FIXED AT `d42dbf6b`** — the frozen head
this ratification is encoded on:

1. **Codex P2 on `design.md`: "Count every replacement required by the veto."**
   Codex measured that the normative block carries **SEVEN**
   `TOLERATED`/`tolerated` occurrences, not the four the packet had claimed a
   veto would cost, and named the consequence that makes it a defect rather than
   an arithmetic slip: *"Replacing only one word in each named unit leaves both
   status terms active, while replacing all occurrences changes more text than
   the stated ratification surface."* **TAKEN.** D1 now ENUMERATES the
   replacement set line by line rather than counting it, and records what each of
   the seven does — so the set is deliberately NOT reduced, because a scenario
   whose whole subject is the word cannot assert it without naming it, and
   shrinking a hypothetical veto's diff would weaken the requirement. This
   finding is the reason a PERMITTED ruling would have been applicable
   faithfully, and it is directly upstream of § 2's confidence that TOLERATED
   changes nothing.
2. **Copilot on `README.md`: two broken inline code spans.** The `grep`
   measurement and a `class:`/`co-modifier` span were split across a line break.
   **TAKEN as an edit, with the stated defect corrected on the record**: the
   rendering claim as given is not right — CommonMark converts a line ending
   inside a code span to a space, so both spans render and copy whole — but the
   edit is worth making for a different reason, namely that a command a reader is
   invited to re-run (this one is the `code_surface: none` measurement's own
   evidence) should be copyable without depending on that conversion.

**CODEX HAS NOT REVIEWED `d42dbf6b`. As of this record, the only Codex pass on
this pull request is the round on `9c26a97c`, and the fixes for its P2 have not
been re-reviewed by it.** A fresh `@codex review` is requested on the
ratification-encoded head in the same comment that announces this record, and
its outcome is a freeze obligation on the landing lane rather than a claim this
record makes. Copilot round 2 DID read the fixed tree and returned zero comments
over all seven files.

## 5. What is NOT ratified, and the residue this word does not reach

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
  touches it. This packet's own delta validates clean (`verification-2026-09-09.md`
  § 1), and the repository-wide failure SET is byte-identical to `origin/main`'s
  (§ 2 there) — this change adds nothing to it and removes nothing from it.
  `tasks.md` § 5.2 records the strict failure as an OWED SUCCESSOR and not as
  this packet's work; fixing a promoted requirement's first line is itself an
  amendment of ratified canon and needs its own word.
- **Issue #775 is a different defect on the same requirement** and is untouched
  (`tasks.md` § 5.3).
- **The estate's one live declared copy is unaffected in both directions**
  (`tasks.md` § 5.4): no consumer's conformance outcome moves, which is exactly
  what the refusal on #780 promised of this remedy.
- **`tasks.md` § 4 (archive) STAYS OPEN**, and § 5.2–§ 5.4 stay open as measured
  residue rather than work performed.

## 6. Ordering against the sibling delta, and the landing obligation

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
(`verification-2026-09-09.md` § 5).

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
and the required checks are green on the ratification-encoded head.
