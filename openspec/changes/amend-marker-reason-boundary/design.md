# Design: amend-marker-reason-boundary

Status: draft
Date: 2026-09-06
Kind: design

## 0. The brief

openxFactory issue **#692**, filed out of the adversarial review of PR **#685**:

> `parse_marker` … collects every code span in the marker paragraph including
> the reason tail, so the marker promoted by #685 at
> `openspec/specs/doc-health/spec.md:2716` resolves to THREE declared-removed
> names — the intended `WHEN` bullet plus `WHEN` and `AND` quoted in the
> trailing prose. Inert today … Remedy: parse only the code spans before the
> reason, or require the removed units in a fenced list.

The issue offers two remedies. This document takes the first, writes the second
out beside it with its cost, and names the choice as the packet's veto point.

## D0 — the measurement, taken before the design

Every unit-naming marker in `openspec/specs/*/spec.md` and every active
`openspec/changes/*/specs/*/spec.md`, parsed under both rules on 2026-09-06:

| marker | names BEFORE | names AFTER | reason |
|---|---|---|---|
| `govern-sibling-added-modified-deltas` | 2 | 2 | unchanged |
| `amend-published-tip-unreadable-scenario` | **3** | **1** | `None` → the author's |
| `amend-unreadable-read-sibling-scenarios` | **3** | **1** | `None` → the author's |
| `declare-generated-projection-status` | 1 | 1 | unchanged |
| `create-medxchart-overlay-boundary` | 4 | 4 | unchanged |
| `add-chain-attestation` | 1 | 1 | unchanged |
| `add-composed-view-authoring` | 1 | 1 | unchanged |

**SEVEN markers, TWO misread, FIVE unaffected.** Both misreadings are the same
shape and the same two words: an amendment marker whose reason explains that the
retired `WHEN` bullet was replaced *"by the `WHEN` that names both facts and the
`AND` that requires the family to establish which holds"*.

**AND THE SECOND HALF OF THE MEASUREMENT IS WHY IT IS INERT.** Across the same
population, `derive_units` yields **17,566** units and **none** of them is
literally `WHEN` or `AND`. `suppression`'s third resolution — *"the name matches
NO canon unit → nothing suppressed, nothing reported"* — is what has been
absorbing the defect, silently and by luck.

**THE THIRD HALF IS THE ONE THE DESIGN TURNS ON:** no marker in this corpus
separates its NAMES with ` — `. Every one of the seven separates names with
`; ` and uses ` — ` once, to open its reason. That is what makes option A's
failure direction empty on the present corpus rather than merely conservative.

## D1 — THE VETO POINT: option A (the boundary) against option B (a fenced list)

**A — RECOMMENDED, AND WHAT THE DELTA ENCODES.** The names are the code spans
following the colon that CLOSE BEFORE the first ` — ` standing OUTSIDE any code
span; the reason is everything after that separator; a code span inside the
reason is prose the reason quotes and is never a name. A marker with no such
separator names every span and has no reason, which is exactly what canon's own
written-out `Merged into` example is and leaves it unchanged.

- **It rewrites no marker.** All seven parse under it, five to the same answer
  and two to the answer their authors wrote.
- **It rewrites no template.** The two prose templates in `doc-health` and in
  `document-lifecycle` that promote into canon are untouched, and so is the
  fenced example block.
- **Its failure direction is conservative.** If an author ever separated NAMES
  with ` — `, the later spans become reason, suppress nothing, and the units
  that author meant to declare are **REPORTED** rather than silently dropped.
  A carriage check that errs must err toward reporting, and this errs toward
  reporting. **The corpus carries no such marker** (D0), so the cost is
  prospective, and it is written into the shipped code as a comment and into
  the test file as `test_names_separated_by_the_separator_fail_in_the_CONSERVATIVE_direction`.
- **It keeps the promoted claim that survives.** *"Extraction is by code span
  and never by splitting on punctuation"* remains true of UNITS: the boundary
  decides where extraction STOPS, and every unit is still a span.

**B — REJECTED FOR COST, and it is a real alternative rather than a straw one.**
Require the removed units in a fenced list:

```
**Removed from canon by <change-id> (<YYYY-MM-DD>):**
- `first unit`
- ``second unit``
— <reason>
```

It is unambiguous by construction: the reason cannot be confused with a name
because names live in a list and the reason does not. What it costs:

1. **Every existing marker is rewritten** — seven in canon and in active deltas,
   plus every marker inside `openspec/changes/archive/`, which are records of
   ratified acts that must not be edited at all. So B would have to be
   grandfathered, and a grammar with a grandfather clause has two grammars.
2. **The two prose templates are rewritten**, in `doc-health` and in
   `document-lifecycle` — two promoted requirements, two `## MODIFIED` blocks,
   in a packet whose whole subject is one sentence.
3. **A fence inside a MODIFIED block collides with `fenced_regions`**, which
   drops fenced lines before any derivation precisely so that written-out marker
   examples never parse. A marker whose units live in a fence would have to be
   exempted from the rule that protects the requirement defining it.
4. **It does not make the reason unambiguous by itself.** The reason still
   trails the list and still needs a boundary rule — so B is A plus a rewrite of
   the corpus.

**The veto is between A and B, and a veto of A is a veto of the delta.** If B is
ruled, this packet is withdrawn and re-authored; nothing here is salvageable
into it except the measurement.

## D2 — the boundary tests SPAN MEMBERSHIP, never "the last separator"

`_reason_boundary` walks occurrences of ` — ` and returns the first whose three
characters lie in no code span. The alternative readings were considered:

- *"the first ` — ` anywhere"* — WRONG on the corpus. The two misread markers
  each name a unit that CONTAINS ` — ` inside its own bytes (the retired clause
  quotes *"answers nothing — the commonest cause…"*), so a naive first-match
  would cut the marker in half and lose the name entirely. This is the failure
  the promoted rule was avoiding by measuring from behind.
- *"the last ` — ` outside a span"* — WRONG in the other direction: a reason
  containing a second dash would move the boundary rightward and swallow prose
  into the names.

The separator's three characters can never open a code span (neither a space nor
an em dash is a backtick), so every span lies wholly before or wholly after the
boundary and `end <= cut` partitions the spans exactly. That is asserted rather
than assumed in the helper's docstring.

## D3 — the `Merged into` form is amended CONSISTENTLY, not separately

Both unit-naming forms share ONE tail parse. `Merged into`'s destination is
matched inside `_MERGED_PREFIX` and resolved from the PREFIX group; the tail
after the closing colon is then parsed by the same three lines that parse
`Removed from canon`'s. The retired sentence therefore governed both, and the
replacement says so in terms — *"The boundary is read the same way in both
forms"* — rather than leaving a reader to infer it from the parser.

The **third** reserved form (`Modified over`, the pairing form) is untouched.
It names no units and returns before the split, taking its WHOLE tail as its
reason; the branch comment that justified that by contrast with the retired rule
is corrected in the realization, because a comment describing a retired rule is
a comment that will mislead the next reader.

## D4 — THE SELF-REFERENCE HAZARD, and how this packet's own marker survives it

This block's `Removed from canon` marker is read by **two different grammars**:
the RETIRED one, when the doc-health family runs from `main` or from any tree
that does not carry this branch's realization; and the AMENDED one, in this pull
request and after it lands.

They agree only where the reason quotes nothing. So the marker is written with
**no code span anywhere in its reason**:

- under the RETIRED rule, the last code span in the tail is the named unit, and
  the reason is what follows its ` — `;
- under the AMENDED rule, the first outside-span separator is the same one — the
  ` — ` the named unit quotes lies INSIDE its doubled-backtick fence — so the
  names and the reason are identical.

Verified under both parsers in the pull request. **This is a constraint on
amendment markers generally while both grammars are in the estate**, and it is
the reason the packet's own reason clause reads a little stiffly.

## D5 — the named unit is fenced with a doubled backtick run, by canon's own rule

The retired sentence cites ` — ` as a code span, so the unit contains backticks
and *"SHALL be fenced with a longer run of them"*. It is named as
` ``…`` `. A single-backtick fence would end at the unit's first inner backtick
and name a fragment that is not a unit — which is the very defect the paragraph
carrying the retired sentence exists to prevent, and it would have been made
while amending that paragraph.

## D6 — what is NOT taken here

- **The two promoted markers are not edited.** They are the record of ratified
  removals; what is wrong is how they are read.
- **`document-lifecycle` is not amended.** Its marker grammar says only that
  each deleted unit is named as a code span and says nothing about the reason
  boundary, checked on this tree. Amending it would widen the packet for no
  obligation.
- **`suppression`'s third resolution is not touched.** A name matching no canon
  unit stays silent — a fail-closed reading recorded as a plausible later ruling
  by the family's own author, and one this packet has no standing to take. It is
  worth naming that a finding there would have caught this defect years earlier:
  `WHEN` and `AND` match nothing, and a family that reported "this marker names
  something that is not a unit" would have said so. **That is an owed successor,
  not this packet's** (`tasks.md` § 5).
