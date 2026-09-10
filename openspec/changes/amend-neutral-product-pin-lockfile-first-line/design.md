# Design: amend-neutral-product-pin-lockfile-first-line

Status: draft
Date: 2026-09-10
Kind: design

## 0. The brief

openxFactory issue [#882](https://github.com/opensoft/openxFactory/issues/882),
filed 2026-09-10 by this lane at the archive of
`amend-neutral-product-pin-interim-copy-vocabulary` as the named successor of
that packet's `tasks.md` 5.2 and `design.md` D6:

> `openspec/specs/neutral-product-pin/spec.md` fails `--strict` on `main` … It
> is one requirement, one sentence … Requirement index 16 … its **first body
> line** … is: *"Where a pinned external neutral product is distributed as a
> published artifact"*. No `SHALL`, no `MUST`. … **the OpenSpec parser reads
> only the FIRST LINE of a requirement's body** when it checks for the keyword,
> so a `SHALL` on line two is invisible to it.

The issue names one remedy and one example wording. This document takes the
remedy, writes THREE candidate wordings out with their costs, and records one
measurement the issue did not have — which is why **D6 is put first**.

## D0 — the measurement, taken before the design

On the clone of `main` `ea34f22a` this packet was authored against, 2026-09-10.
Re-measured unchanged after the branch was merged up to `origin/main`
`05c706d6`: `git diff` over `openspec/specs/neutral-product-pin/spec.md`
between the two commits is empty, so every line number below is the current
one.

| measure | value |
| --- | --- |
| promoted spec files in the corpus | **62** |
| `### Requirement:` headings across them | **641** |
| …whose FIRST BODY LINE carries neither `SHALL` nor `MUST` | **2** |
| …in `neutral-product-pin` | **1** — index 16, heading `:668`, body `:669` |
| …in any other capability | **1** — `repo-boundary-governance` index 1, `:34-35` (D5, not taken) |
| requirements in `neutral-product-pin` | **18** |
| …whose first body line carries the keyword | **17** |
| `derive_units` units in the promoted requirement | **25** — 9 body, 4 scenario titles, 12 scenario bullets |
| scenarios in the requirement | **4** |
| `SHALL` occurrences in the block below `:669` | **8** |
| active changes carrying a `neutral-product-pin` delta | **1** (`split-opendox-two-layer-product`) |
| …of them writing THIS requirement's key | **0** |
| scripts/tests/workflows/contracts quoting any part of the sentence | **0** |

**THE FILE'S OWN CONVENTION IS THE ARGUMENT, AND IT IS SEVENTEEN TO ONE.** Every
other requirement in this specification opens its body with the obligation's
SUBJECT and reaches its modal on the first line — *"A consumption pin SHALL be a
PUBLISHED contract member…"*, *"A resolver SHALL prefer the pin recorded in the
CONSUMING repository…"*, *"A change that moves a pinned tool's version SHALL be
HUMAN-ONLY…"*. TEN do it inside 80 characters; SEVEN do it on a line of
80 characters or more (80, 156, 183, 201, 221, 284 and 397 characters), so a
long first line is ALSO house style here and is not a style objection to
option 2.
Index 16 is the only one that opens with a condition.

### D0a — the issue's own scenario count is corrected, on the measurement

Issue #882 says *"all nine scenarios and both trailing body paragraphs
unchanged"*. The requirement carries **FOUR** scenarios, not nine — *A pinned
artifact declares dependency ranges*, *The committed resolution and the pin
disagree*, *The install re-resolves a range*, *A reuse cache serves a tree it
was not built for* — and two trailing body paragraphs, which is right. The
correction is recorded here rather than by editing the issue's prose, and it
changes nothing about the remedy: all four are carried, byte for byte.

## D6 — PUT FIRST, BECAUSE IT CAN END THE PACKET: the pinned CLI does not report this failure

**RECOMMENDATION: AMEND ANYWAY. THE DECISION IS THE OWNER'S AND IT IS PUT
BEFORE THE WORDING.**

`neutral-product-pin`'s own promoted requirement *A consuming repository runs
OpenSpec validation only through the pinned entrypoint, so a PATH binary cannot
affect the gate* (`:479-509`) holds that a repository *"SHALL invoke strict
validation ONLY through the entrypoint the pin names"* and that *"A repository
that calls a bare `openspec` binary is NOT running the pinned tool whatever
version answers"*. openxFactory obeys it:
`.github/workflows/openspec-cli-pin-gate.yml:101` runs
`python3 scripts/validate-openspec-cli-pin.py --all --no-cache`, and
`contracts/openspec-cli-pin.yaml:255` pins `version: "1.12.0"`.

**ON THAT BINARY THIS SPECIFICATION PASSES.** Four runs — two binaries over two
trees, each tree named rather than left to be inferred — 2026-09-10. The
CONTROL tree is `origin/main` `05c706d6` — the base this branch is merged up to
— in its own worktree; the PACKET tree is this change's branch, which differs
from the control by this packet's directory, its README row and its two ledger
rows and nothing else. The promoted sentence is BYTE-IDENTICAL at the authoring
basis `ea34f22a` and at `05c706d6`:

| tree | binary | totals | exit | `spec/neutral-product-pin` |
| --- | --- | --- | --- | --- |
| control `05c706d6` | 1.2.0 on `PATH` | `97 passed, 4 failed (101 items)` | 1 | **✗** |
| this branch | 1.2.0 on `PATH` | `98 passed, 4 failed (102 items)` | 1 | **✗** |
| control `05c706d6` | 1.12.0, pinned, content-verified | `99 passed, 2 failed (101 items)` | 0 | **✓** |
| this branch | 1.12.0, pinned, content-verified | `100 passed, 2 failed (102 items)` | 0 | **✓** |

The failure SET is byte-identical across the two 1.2.0 runs — `diff` over the
sorted `✗` lines is empty — and the one extra passing item on the branch is
this packet's own change. On the pinned binary the two failures are the two
DISPOSITIONED scenario-omission findings, accepted on Brett Heap's word of
2026-09-05 *"take exit 2"*, and `spec/neutral-product-pin` carries INFO notes
only.

**THE MECHANISM, MEASURED ON A CONTROLLED FIXTURE RATHER THAN INFERRED.** A
three-requirement probe spec was written — one with the keyword on line one, one
with it on line two only, one with no keyword anywhere — and both binaries were
run over it:

| probe requirement | 1.2.0 | 1.12.0 |
| --- | --- | --- |
| keyword on line one | pass | pass |
| keyword on line TWO only | `✗ [ERROR] requirements.1.text: Requirement must contain SHALL or MUST keyword` | pass, silent |
| no keyword anywhere | `✗ [ERROR] requirements.2.text: Requirement must contain SHALL or MUST keyword` | `⚠ [WARNING] requirements[2]: Requirement "No keyword anywhere" should contain SHALL or MUST (RFC 2119 best practice for English specs)` |

**AND ONE THING THE TABLE WOULD HIDE IS STATED.** On 1.12.0 the probe SPEC is
still reported invalid — `✗ [ERROR] probe: the report marks this item INVALID
and names no ERROR-level issue for it`, the pinned entrypoint's own reading of a
report that carries the WARNING and no error — so 1.12.0 is not indifferent to a
requirement with NO keyword anywhere. What it is silent about is the case this
packet is about: a keyword on line TWO draws NOTHING on 1.12.0, no error and no
warning, which is why the real corpus run counts `spec/neutral-product-pin`
among its passes.

So 1.2.0 reads ONE LINE and errors; 1.12.0 reads the WHOLE BODY and, when the
keyword is missing altogether, warns. **The first-line rule this corpus has
written down for a year is a fact about 1.2.0 and about no other binary the
estate runs.** (`prepare-openspec-1-12-readiness` is the active change carrying
the migration; it does not record this behaviour change, and this measurement is
offered to it rather than claimed by this packet.)

**THE TWO OPTIONS, AND WHY AMENDING IS STILL RECOMMENDED.**

1. **AMEND (recommended, and encoded).** Three reasons, none of them the red
   gate. (a) **Seventeen to one**: the sentence is the only one of eighteen in
   its own file that defers its subject, and a requirement's obligation should be
   legible in its first line to a human skimming eighteen headings as much as to
   a parser. (b) **The estate has not finished migrating.** 1.2.0 is what is on
   PATH on this machine today, `prepare-openspec-1-12-readiness` is still an
   ACTIVE change, and every engineer and agent who types `openspec validate
   --all --strict` — which is what this repository's own `CLAUDE.md` and its
   OpenSpec authoring notes tell them to type — sees a red specification and has
   to be told it is not theirs. That cost has already been paid twice, in
   #868's packet and in this one. (c) **It costs almost nothing**: two case
   flips and one comma, no word added, no word removed, no obligation moved.
2. **CLOSE #882 ON THE MEASUREMENT.** Legitimate, and cheaper: publish the two
   runs, record that the pinned gate is green, and leave ratified text alone —
   the estate's default posture toward promoted canon. Its cost is that the
   only requirement in the file that hides its obligation on line two stays
   that way, and the next reader who runs the on-PATH binary re-opens the
   question from scratch.

**WHAT A VETO HERE COSTS: the whole packet.** If D6 resolves to option 2, no
delta is written, no marker is owed, this packet is withdrawn rather than
re-wired, and #882 closes with the measurement as its answer. That is why it is
asked before the wording.

## D1 — THE VETO POINT: the wording of the first sentence

**Recommended: OPTION 1. Written that way.** All three options put the subject
and the modal on line one; they differ in what they cost.

### Option 1 — RECOMMENDED AND ENCODED: re-order canon's own words

Exact bytes, as the delta carries them:

> The pin SHALL carry a VENDORED RESOLUTION where a pinned external neutral
> product is distributed as a published artifact whose installation RESOLVES
> dependency ranges — a lockfile in the format that product's own package
> manager consumes, committed beside the pin, addressed by a digest over its
> exact bytes recorded in the pin, together with the size of the tree it locks.

First body line, 73 characters: `The pin SHALL carry a VENDORED RESOLUTION where a pinned external neutral`.

**Accounting, measured, whitespace-split and CASE-SENSITIVE:** the retired
sentence's tokens minus this one's are `Where`, `ranges,` and `the`; this one's
minus the retired one's are `The`, `where` and `ranges`. Two case flips and one
comma. 374 characters become 373. **No word is added and no word is removed.**

**Why it is recommended.**

1. **It matches the seventeen siblings exactly** — subject, modal, obligation,
   then the condition. It is not a new sentence shape for this file; it is the
   file's only shape, applied to the one requirement that lacks it.
2. **Compliance becomes a property of the SENTENCE rather than of its line
   breaks.** Once the subject and the modal are the first six words, ANY sane
   wrapping puts them on line one, so a later author who re-flows the paragraph
   cannot silently reintroduce the defect. That is exactly what option 2 cannot
   promise (below).
3. **The bearer does not move.** `The pin SHALL carry` is canon's own clause,
   lifted whole.
4. **It is the smallest edit that achieves 2 and 3 together.**

**Its cost, stated:** `The pin` opens the sentence before the clause that
defines which pin, so the definite article looks forward by one clause. The
file's siblings do the same thing (*"A resolver SHALL prefer the pin recorded in
the CONSUMING repository wherever more than one checkout…"*), and the
requirement's heading has already named the subject one line above.

### Option 2 — ALTERNATIVE: change not one word; move only the line breaks

Leave canon's sentence exactly as ratified and re-flow the paragraph so the
whole first sentence sits on one 374-character line, with the rest wrapped at
79. `SHALL` then stands on line one at column 135.

**It is genuinely the smaller act, and it owes NO MARKER AT ALL.** Canon says so
itself: *"Normalization collapses runs of whitespace to a single space and
strips leading and trailing whitespace, so a re-wrapped paragraph compares equal
to the same paragraph wrapped differently; no normalization beyond it applies"*
(`openspec/specs/doc-health/spec.md:1668-1672`). **Measured, not argued:** a
second block was generated on this same tree with only the line breaks moved,
and `derive_units` returns **25 units, 0 uncarried, 0 added** — the family sees
no change, so no `Removed from canon` marker is owed and none would be written.
Five of the file's eighteen first body lines are already 156 to 397 characters,
so the long line is not a style break either.

**Its cost, and it is the reason option 1 is recommended.** The requirement's
compliance with the first-line rule would rest entirely on a LINE BREAK, and
`doc-health`'s currency family is blind to line breaks BY DESIGN and by ratified
rule. So the next author who re-wraps that paragraph — a perfectly ordinary,
declaration-free act under the family — silently restores the defect, and
nothing in the corpus reports it. A rule enforced only by whitespace, in a
corpus whose one checker is contractually indifferent to whitespace, is not
enforced. **Second cost:** an amendment of ratified canon whose entire content is
a line break is hard to read as an amendment at all, and it would set the
precedent that promoted text may be re-flowed under a change id — which is
either trivial or a large new permission, and this packet does not want to
decide which.

### Option 3 — REFUSED: the wording issue #882 itself floats

> A pinned external neutral product distributed as a published artifact whose
> installation RESOLVES dependency ranges SHALL carry a VENDORED RESOLUTION — …

**It moves the obligation's BEARER from the pin to the product**, and the
requirement contradicts that in four places this packet does not touch: *"a
digest over its exact bytes **recorded in the pin**"* (same sentence), *"**A
pin** that declares NO vendored resolution for such a product SHALL be
refused"* (`:680-681`), the first scenario's `THEN` *"**the pin** carries a
vendored resolution beside it"* (`:705`), and the realized fields
`lockfile:`/`lockfile_integrity:`/`lockfile_packages:` which live in
`contracts/openspec-cli-pin.yaml` — the pin file — and not in the product. A
product is published by someone else; it cannot be obliged by this corpus to
carry anything. **That is a change of substance, in a packet whose whole
argument is that it moves no rule**, so it is written out here and refused
rather than encoded. It is recorded, not dismissed: the requirement's own
HEADING says *"A pinned artifact … carries a vendored lockfile"*, so the issue's
wording is a reasonable reading of the heading — and the heading is a title,
while the body is the normative sentence. **Nothing about the heading is edited
by this packet**, and if the owner prefers option 3 the honest form of it would
also re-word the heading and the four sites above, which is a larger amendment
than this word commissions.

## D2 — the marker: ONE is owed, ONE is written, and BOTH branches are proven

**Recommended and written: one `Removed from canon` marker, one name, no code
span in its reason, placed at the END of the block.**

The grammar decides it, and the grammar is `document-lifecycle`'s (*"A
deliberate deletion is legitimate, and it SHALL be declared by form rather than
by prose … naming each deleted unit as a CommonMark code span"*) as realized by
`doc-health`'s `modified-block-currency` (`openspec/specs/doc-health/spec.md:1686-1786`).
Applied to this delta:

- **Under option 2 (re-flow only) no marker is owed**, because no unit changes.
  Canon's normalization rule says a re-wrapped paragraph compares equal, and the
  generated option-2 block measures **0 uncarried, 0 added**.
- **Under option 1 the sentence's WORD ORDER changes, so the sentence is a
  REPLACED unit** — `normalize` collapses whitespace and does NOTHING else (it
  deliberately does not casefold, *"because promotion writes the block's BYTES
  into canon, so a case change is a text change"*). The generated option-1 block
  measures **1 uncarried, 1 added**. One canon unit is absent from the block, so
  one marker is owed, and it names exactly that one unit.

**IT IS ASSEMBLED FROM `derive_units`' OWN OUTPUT RATHER THAN RETYPED**, the
method PR #908's packet used, so it cannot name a fragment or a unit as its
author remembers it. The retired sentence contains no backtick, so a single-
backtick span fences it correctly; the ` — ` inside the sentence falls INSIDE
that span and is therefore not the reason boundary, which canon requires be *"THE
FIRST ` — ` SEPARATOR STANDING OUTSIDE EVERY CODE SPAN"*. The assembled paragraph
is then re-parsed by `parse_marker` and asserted to yield form `removed`, change
id `amend-neutral-product-pin-lockfile-first-line`, date `2026-09-10`, exactly
one name equal to the derived unit, and an EMPTY `quoted` list.

**THE REASON CARRIES NO CODE SPAN AT ALL, DELIBERATELY.** That is what makes the
marker unreportable under every ground the corpus has or is about to have: the
existing second ground fires on a code span inside a reason that matches a unit
the block does not carry, and a reason written entirely in prose cannot trip it;
the two grounds the ACTIVE draft `amend-marker-declaring-nothing` (PR #908) adds
fire on a marker naming a unit the BLOCK itself adds and on a `Removed from
canon` marker carrying neither a name nor a quoted span, and this marker names a
CANON unit and carries one name. **Checked against the draft rather than only
against promoted canon**, because that packet may land first.

**Rejected: an `AMENDED BY` dated bold note beside the marker.** The method
packet used one and it is precedented, but a dated bold note is ONE UNDIVIDED
UNIT under this same family (`is_dated_bold_note`), so it would promote into
canon and every later block modifying this requirement would have to restate it
forever. This packet's whole claim is that it adds nothing to the requirement.
The accounting therefore lives in the delta file's HEADER PROSE — outside the
`## MODIFIED Requirements` block, where the family reads no units — and in the
marker's own reason, which is the shape
`amend-neutral-product-pin-interim-copy-vocabulary` used.

## D3 — why an OpenSpec change and not a patch

**Because the sentence is PROMOTED, RATIFIED CANON, and this estate has a
standing refusal on exactly this point, five days old.**

Working rule 3 routes contract, boundary and policy changes through OpenSpec.
`document-lifecycle` makes the MODIFIED block the instrument. And the precedent
is not abstract: Codex raised a vocabulary defect in THIS SAME specification as
a P2 on PR [#780](https://github.com/opensoft/openxFactory/pull/780), and lane
`openxfactory-1` refused to fix it there —

> Rewording the requirement here would (1) edit ratified text with no word
> behind it and (2) destroy the very byte-identity that makes this archive
> auditable. **Amending promoted canon is an amendment packet's act, on its own
> ratification** — the estate has a shape for exactly this (`amend-*` changes
> with a `## MODIFIED` block), and it is not something an archive may do in
> passing.

— and the successor became `amend-neutral-product-pin-interim-copy-vocabulary`,
ratified 2026-09-09 and archived 2026-09-10. **A packet that quietly `sed`-ed
one line of `openspec/specs/` would be the act that refusal refused**, and it
would do it to a sentence whose promotion is auditable: the archived delta of
`pin-openspec-cli-dependency-closure` carries the same bytes, so anyone can
check that what was ratified is what was written.

## D4 — `code_surface: none`, and what that decides

Measured in `proposal.md`'s front matter: `grep` over `scripts/`, `tests/`,
`.github/` and `contracts/` for any part of the sentence returns NOTHING, and
the obligations the sentence states are realized by
`scripts/validate-openspec-cli-pin.py` and by
`contracts/openspec-cli-pin.yaml`'s three lockfile fields — none of which this
block changes. No test pins the requirement's scenario count or titles, and the
block adds no scenario and drops none.

Under `release-realization` an empty code surface **archives ON LANDING plus its
own task list** rather than on merged-plus-green realization evidence. That is
why `tasks.md` § 5 is one archive act rather than a realization group, and why
**the "realization" of a wording amendment IS its promotion at archive** — a
separate act on a separate word, at which openxFactory #882 closes.

## D5 — sequencing, and the sibling search pasted rather than summarized

`sequenced_after: []`, the positive root claim.

- **The file's LAST WRITER is the archived
  `amend-neutral-product-pin-interim-copy-vocabulary`** (commit `88cc12b5`,
  2026-09-10), and before it `pin-openspec-cli-dependency-closure`
  (`fa58a1a3`). Both are ARCHIVED, so neither is an active co-writer.
- **Active deltas over this capability:**
  `ls -d openspec/changes/*/specs/neutral-product-pin` returns exactly one line,
  `openspec/changes/split-opendox-two-layer-product/specs/neutral-product-pin`.
  Its `## MODIFIED Requirements` section carries two headings — *An external
  neutral product is pinned by commit and digest, never by tag* (`:86`) and *The
  consuming repository's pin is authoritative among reachable checkouts*
  (`:186`) — **neither of them this requirement**.
- **The requirement key across every active delta:**
  `grep -rln "A pinned artifact that resolves dependencies at install time"
  openspec/changes/ --include=spec.md | grep -v archive` returns **nothing**.
- **Open pull requests:** the NINE open when this packet's branch was cut —
  #917, #916, #913, #912, #910, #908, #888, #594, #518 — were each read with
  `gh pr view <n> --json files` and **not one touches any `neutral-product-pin`
  path** (nine zeroes, printed one per line). #908 is the nearest neighbour and
  it is a `doc-health` delta, `Status: draft`, open and unmerged at this
  commit.

So this change is the **SOLE ACTIVE MODIFIER** of the requirement key, no
ordering declaration is owed in either direction, and the ledger's
`class: co-modifier` is the whole-corpus grading `proposal.md` § Sequencing
explains rather than a contradiction of it.

## D7 — what is NOT taken here

- **`repo-boundary-governance` index 1** (*Install repository scope*,
  `openspec/specs/repo-boundary-governance/spec.md:34`), whose first body line
  is a list of repository names in code spans and which fails 1.2.0's check on
  the identical ground (`requirements.1.text`). It is the corpus's ONLY other
  instance — measured across 62 files and 641 requirements — and it is a
  different capability, a different requirement and a different sentence. Taking
  it here would be a second amendment of ratified canon with no word behind it,
  which is precisely the act D3's precedent refuses. `tasks.md` § 6 names it as
  residue; it needs its own issue and its own word.
- **The requirement's HEADING.** *"A pinned artifact … carries a vendored
  lockfile"* attributes the carrying to the artifact where the body attributes
  it to the pin. That is a real looseness and it is NOT fixed here: editing a
  ratified heading changes the requirement KEY every consumer, marker and
  currency check matches on, which is a much larger act than this word
  commissions. It is recorded so a later reader does not mistake the silence for
  an oversight.
- **The two DISPOSITIONED findings** the pinned run names
  (`add-chain-attestation` / `signed-execution-chain`, `add-composed-view-authoring`
  / `ideation-dashboard`). Accepted exceptions on Brett Heap's word of
  2026-09-05 *"take exit 2"*, unrelated to this requirement, and untouched.
- **`prepare-openspec-1-12-readiness`.** D6's fixture measurement is directly
  relevant to that change's subject and is offered to it rather than folded into
  this packet: this packet writes no readiness evidence and claims no part of
  that migration.
