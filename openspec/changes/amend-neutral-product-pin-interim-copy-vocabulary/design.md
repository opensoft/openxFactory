# Design: amend-neutral-product-pin-interim-copy-vocabulary

Status: draft
Date: 2026-09-09
Kind: design

## 0. The brief

openxFactory issue [#868](https://github.com/opensoft/openxFactory/issues/868),
filed 2026-09-09 out of Codex's refused P2 on PR
[#780](https://github.com/opensoft/openxFactory/pull/780):

> For a repository without an `xfactory:` stack pin, this scenario declares a
> properly documented copy "lawful," while [the same requirement] explicitly
> state[s] that declaring the copy does not make it lawful and leaves the
> required-check claim unmet. … distinguish "permitted as an interim" from
> "compliant with the required-check requirement", or use one consistent status.

Codex offers TWO remedies. This document takes the FIRST — two statuses, two
words — and writes the second out beside it with its cost (D3). The word the
first remedy gets is the packet's veto point (D1).

## D0 — the measurement, taken before the design

Read on the clone of `main` this packet was authored against, 2026-09-09.

| measure | value |
| --- | --- |
| occurrences of `lawful` in `openspec/specs/neutral-product-pin/spec.md` | **5** |
| …inside the requirement this packet amends | **4** — `:299`, `:345`, `:373`, `:374` |
| …used there for the REQUIRED-CHECK claim (body) | 2 — `:299-300`, `:344-345` |
| …used there for THIS requirement's own admission (scenario) | 2 — `:373`, `:374` |
| …in a DIFFERENT requirement, on a different subject | **1** — `:555`, and it is NOT touched (D0a) |
| requirements in the specification | 18 |
| active changes carrying a `neutral-product-pin` delta | 1 (`split-opendox-two-layer-product`) |
| …of them writing THIS requirement's key | **0** |
| scripts/tests asserting the word from this specification | **0** (see `proposal.md` front matter) |

**Inside the requirement the word is used four times, for two statuses, two
apiece. That symmetry is the design**: neither use is a stray, so a fix that
changes one occurrence would leave the requirement inconsistent with itself in
the other direction. All four are read together, two are reserved and two are
replaced.

### D0a — the fifth occurrence, and why the reservation is SCOPED rather than capability-wide

`:555` is a fifth use, and it belongs to a different requirement — *A
dispositioned finding is cited, upgrade-coupled, and refused when stale* — where
it reads *"a non-empty CITATION to the canon that makes the acceptance lawful"*.
That is neither of this requirement's two statuses: its subject is a
DISPOSITION's acceptance, not a consumption's standing, and no reader can
confuse the two.

**This is why the reservation is written as *"WHERE THIS REQUIREMENT SPEAKS OF A
CONSUMPTION'S STATUS, LAWFUL names exactly ONE consumption"* and not as a
capability-wide reservation of the word.** A capability-wide claim would put a
ratified sentence in another requirement in violation on the day this packet
promoted, which is a rule change and a scope widening in one — and it would be
made by a packet whose whole argument is that it moves no rule. The narrower
form does the work the defect needs (the two statuses inside this requirement
get two words) and reaches nothing else.

## D1 — THE VETO POINT: TOLERATED against PERMITTED

**Recommended: TOLERATED. Written that way. One veto changes four words and
nothing else.**

The refusal on #780 itself floated the alternative in as many words — *"say
`PERMITTED as a declared interim` in the scenario, reserving `lawful`/`compliant`
for the required-check claim"* — so PERMITTED is not a straw option; it is the
word the lane that refused the finding had in mind, and it is the reason this
decision is put for veto rather than simply taken.

**Why TOLERATED is recommended.**

1. **PERMITTED is a near-synonym of LAWFUL and the defect is that two statuses
   shared one word.** "Permitted" and "lawful" are the same register — both say
   *allowed by the rule* — so a reader who has just been told the copy is
   PERMITTED but not LAWFUL is being asked to hold a distinction the two words
   do not themselves carry. TOLERATED carries it: a thing tolerated is admitted
   AND deprecated in one word, which is exactly the fallback's standing.
2. **The requirement already says the copy is on a clock.** *"Such a copy SHALL
   be retired when that repository adopts a stack pin"* — the admission is
   conditional and terminal, and TOLERATED is the word for a conditional,
   terminal admission. PERMITTED reads as a standing permission a reader could
   take as durable.
3. **TOLERATED is not spent elsewhere in the corpus in a conflicting sense.**
   `PERMITTED` is: `domain-descendant-boundary`'s promoted scenario uses *"the
   placement is permitted"* for a genuinely admitted, non-deprecated state, and
   re-spending the word here would create the very cross-requirement ambiguity
   this packet exists to end, one capability over.

**What a veto costs.** Four words: two in the scenario bullets, one in the added
body paragraph, one in the added scenario, plus the marker's reason sentence.
Nothing else in the packet moves — not the reservation, not the added
paragraph's structure, not the scenario, not the tasks, not the sequencing. The
veto is one `sed` and a re-run of the gates.

**Rejected: leaving the scenario's word alone and changing the BODY's instead**
(make the body say "not compliant with the required-check requirement" and let
`lawful` mean this requirement's admission). It is the smaller diff — one
sentence — but it points the wrong way: `lawful` would then name the WEAKER
status, and the requirement's other body use at `:299-300` (*"a copy is not made
lawful by being current on the day it is taken"*) would flip meaning without
being edited, which is the failure mode of changing a shared word in one place.

## D2 — the reservation goes in the BODY, not only in the scenario

**Recommended and written.**

Codex's finding is satisfiable by editing two bullets alone. That would remove
the contradiction and leave the READER doing the work the text failed to do:
deriving the two scopes from two paragraphs eighty lines apart. The refusal on
#780 named exactly that gap — *"what it does not do is say that in one place
with one pair of words"* — so a fix that reconciles the words without stating
the reservation fixes the symptom.

One body paragraph is therefore added, after *"THE ONE ADMITTED FALLBACK, AND
ITS PRICE"* and before the enforcement paragraph, so the word is defined before
the paragraph that spends it. It does three things and no more: it names the
copy's status (TOLERATED, on the four terms), it reserves LAWFUL to the
stack-pinned read, and it forbids the substitution in records.

**Rejected: a new requirement carrying the vocabulary.** A definition split from
the requirement that uses it is a second place to keep current, and this
capability's own history — a fallback admitted in one paragraph and priced in
the next — is the argument against spreading one rule over two requirements.

## D3 — Codex's SECOND remedy, "use one consistent status", is refused

The finding offers it as an alternative: make the fallback and the required-check
claim the SAME status. Two readings, both refused.

- **Both LAWFUL** — the declared interim satisfies the required-check
  requirement. That is a rule change, it certifies an interim copied gate as
  compliant, and it contradicts a ratified sentence this packet has no word to
  touch: *"A packet admitting the fallback SHALL NOT describe the interim as
  satisfying the required-check requirement."*
- **Both UNLAWFUL** — the fallback is withdrawn. That is also a rule change, in
  the other direction, and it strands the estate's one live declared copy
  (`xFactory-Hermes-Install` #72 → `06c9083d`) with no admitted state at all.

**Both change which behaviours are admitted, which the refusal on #780 said this
successor must not do.** The two-word remedy is the only one available to a
wording amendment, and that is why it is the one taken.

## D4 — one ADDED scenario, at the end of the block

**Recommended and written.**

The reservation is an obligation on records (*"SHALL NOT describe a tolerated
interim as lawful or as compliant"*), and an obligation with no scenario is one
a reviewer cannot point at. One scenario is added — *A record describes a
declared interim copy as lawful* — at the END of the block, so no promoted
scenario moves, is retitled, or loses a bullet.

**It is deliberately about RECORDS and not about gates.** A scenario about a
gate would be a claim about machinery this packet does not build and that
`code_surface: none` says does not exist.

## D5 — the marker, and why the reason carries no code span

The two replaced bullets are declared by ONE `Removed from canon` marker,
placed after the scenarios it names — the placement
`refresh-install-repository-enumerations` used for the same edit shape
(2026-09-09, archived).

The first bullet contains a backtick (`` `openxFactory` ``) and is therefore
fenced with a doubled run, as `doc-health`'s marker grammar requires; the second
contains none and takes a single span. **The reason carries NO code span at
all**, deliberately: `amend-marker-defect-reporting` (archived 2026-09-09) added
a reporting ground for a marker whose reason quotes a span matching EXACTLY a
unit the block does not carry, and a reason written entirely in prose cannot
trip it. The reason is also the record of WHY the two bullets moved, which is
what makes the marker falsifiable rather than decorative.

## D6 — the strict failure this specification already carries is NOT fixed here

`openspec validate neutral-product-pin --strict --type spec` fails on `main`,
and has for as long as this packet's authors have measured it:

> ✗ [ERROR] requirements.16.text: Requirement must contain SHALL or MUST keyword

Requirement index 16 is *A pinned artifact that resolves dependencies at install
time carries a vendored lockfile, and the install runs through it*
(`openspec/specs/neutral-product-pin/spec.md:645`), whose first body line reads
*"Where a pinned external neutral product is distributed as a published
artifact"* — no SHALL, no MUST, and the parser reads only the first line.

**This block does not inherit it.** The requirement this packet modifies is
index 9, and its first body line is *"A consumption pin SHALL be a PUBLISHED
contract member wherever any repository other than `openxFactory` is expected to
read it"*. The change validates `--strict` clean on its own.

**And it is not fixed in passing.** It is a DIFFERENT requirement and a
DIFFERENT sentence — not the sentence this packet reconciles — so fixing it here
would be a second amendment of ratified canon with no word behind it, which is
precisely the act the refusal on #780 refused. It is named as an available
successor: one sentence, moving `SHALL` onto the first line of that
requirement's body, on its own issue and its own word.

## D7 — what is NOT taken here

- **The `:299-300` and `:344-345` sentences.** Both use `lawful` the reserved
  way and are correct as written. Editing them would be churn and would break
  the byte-faithfulness the rest of the block keeps.
- **Issue #775** — the two sibling consumption pins (`contracts/openxwallet-pin.yaml`,
  `contracts/openreposhape-pin.yaml`) that carry no `contracts/manifest.yaml`
  row. A live conformance defect against the SAME requirement, and a different
  one: it is about the register, not the vocabulary, and it is fixed by
  registering rows rather than by amending text.
- **`xFactory-Hermes-Install` #72 → `06c9083d`**, the estate's one live declared
  copy, still owing this requirement's third field. Unaffected in both
  directions; the owed digest stays owed and is not re-characterized here.
- **Any change to `scripts/validate-pin-registrations.py`.** Its docstring quotes
  the requirement's REGISTRATION sentences, which this packet does not touch, so
  its quotation stays accurate.
