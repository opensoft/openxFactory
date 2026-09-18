# Design: amend-code-surface-grammar-comma-and

Status: ratified
Ratified by: amend-code-surface-grammar-comma-and — 2026-09-18, Brett Heap, "Amend the text to admit ', and '" (record `review/ratification-2026-09-18.md`)
Date: 2026-09-18
Kind: design

## 0. The brief, and the measurement it rests on

openxFactory [#1092](https://github.com/opensoft/openxFactory/issues/1092),
filed by lane `openXfactory-5` at the archive of `gate-code-surface-declarations`
(PR [#1076](https://github.com/opensoft/openxFactory/pull/1076) → `5dd0a8dc`)
out of a suppressed Copilot comment on round 3 of that pull request, head
`a8d3cfb6`: the promoted requirement *Code-surface declaration grammar is gated*
names THREE list separators and `scripts/code_surface.py` admits FOUR.

Brett Heap ruled on 2026-09-18 at approximately 09:55Z, verbatim **"Amend the
text to admit ', and '"**, as a terminal multiple-choice answer given directly
to this lane and recorded as a `RULED` line in `lanes/log/openXfactory-5.md` at
2026-09-18T10:15:10Z (`brett-wip` `055bea8b`).

**THE READER WAS NOT RECALLED, IT WAS RUN.** Every claim this packet makes about
what `scripts/code_surface.py` does was taken by calling `cs.parse_head` on the
clone of `main` `3e32d987` this packet was authored against, on 2026-09-18:

| head | verdict | derived set |
| --- | --- | --- |
| `openxFactory, openXwallet, and codexFactory` | ADMITTED | three identifiers |
| `openxFactory, openXwallet and codexFactory` | ADMITTED | three identifiers |
| `openxFactory and openXwallet + codexFactory` | ADMITTED | three identifiers |
| `openxFactory, and openXwallet` | ADMITTED | two identifiers |
| `openxFactory, and the change also touches nothing else` | REFUSED | *runs into prose at `change also touches …`* |
| `openxFactory, and nothing else.` | REFUSED | *runs into prose at `else.`* |
| `openxFactory, and this.` | ADMITTED | two identifiers — `openxFactory`, `this` |
| `none, and openxFactory` | REFUSED | *mixes the empty-surface sentinel* |
| `openxFactory, and none` | REFUSED | *mixes the empty-surface sentinel* |

**AND THE COUNTERFACTUAL WAS RUN TOO, because the ORDER is what this packet's
text has to describe and an order is only visible against its absence.** On a
SCRATCH COPY of the module outside the repository — `scripts/code_surface.py`
itself is never edited by this packet and was never edited to take this
measurement — with the `, and ` alternative REMOVED from `_SEPARATOR_RE` and the
other three left in their existing order:

| head | verdict with `, and ` removed |
| --- | --- |
| `openxFactory, openXwallet, and codexFactory` | REFUSED — *"its head runs into prose at `codexFactory`"* |
| `openxFactory, and openXwallet` | REFUSED — *"its head runs into prose at `openXwallet`"* |
| `openxFactory, and this.` | REFUSED — *"its head runs into prose at `this.`"* |
| `openxFactory, and (the wallet)` | ADMITTED — derived set **`openxFactory`, `and`** |

**THERE IS NO SHORTER READING, ONLY A WORSE ONE.** The bare comma does not stop
the list a member early: `and` satisfies `_NAME`
(`[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]`) on its own, so the CONJUNCTION is taken
as a member in its own right, and what happens next depends only on what follows
it — a further identifier leaves the parse with no separator and no gloss opener
and it REFUSES (rows 1–3), while a gloss opener or the end of the declaration
lets the misreading stand SILENTLY with `and` in the derived repository set
(row 4). So what the delta owes is *the misread, and the refusal it runs into,
that trying `, and ` first avoids* — and NOT *a choice between two readings*:
the two-identifier reading is one `parse_head` cannot produce at all. The added
paragraph and the added scenario are written to that measurement. **THE MODULE'S
OWN COMMENT OVER `_SEPARATOR_RE` GLOSSES IT THE SAME LOOSE WAY** (*"rather than
as a bare comma followed by a head that opens with the word `and`"*): quoted
verbatim where this packet quotes it, named here, and NOT edited — it is a CODE
SURFACE, and it is residue beside **D4**.

Five facts fall out of those two tables and every decision below turns on one of
them:

1. **THE ORDER IS LOAD-BEARING, AND WHAT ITS ABSENCE PRODUCES IS A REFUSAL
   RATHER THAN A SHORTER LIST.** `and` is a name the identifier grammar admits,
   so a bare comma taken first makes the CONJUNCTION a member and the parse then
   dies at the member after it (second table, rows 1–3) — or, where a gloss
   opener or the end of the declaration follows the conjunction, silently admits
   `and` as a repository (row 4). Both are what `, and `-first avoids, and
   NEITHER is the "two identifiers and a run-on" a reader of the promoted text
   would expect. The delta says so in those terms.
2. **The fourth separator is real** and is tried FIRST, so an Oxford-comma list
   is three identifiers rather than the REFUSAL the bare comma alone produces
   (`_SEPARATOR_RE`, `scripts/code_surface.py:152-157`; the bench pins it at
   `tests/code_surface/test_code_surface_gate.py:157-160`).
3. **The separators are NOT exclusive of each other.** A head may mix them; rows
   2 and 3 of the FIRST table both parse. The promoted text never said so
   either way, and with a four-item list in front of "the two being EXCLUSIVE
   alternatives" a
   reader would now reach for the wrong antecedent.
4. **The `, and …` refusal is conditional, not flat.** It fires when the words
   after the conjunction are not themselves a readable identifier followed by an
   opener or the end — which is every ordinary sentence, and is why the corpus's
   real run-ons are still refused (first table rows 5 and 6, and the bench's
   `test_a_head_that_runs_into_prose_with_no_opener_is_refused`). It does NOT
   fire on first-table row 7, where one word and a full stop read as an identifier
   and a gloss opener.
5. **The `none` exclusivity is enforced exactly as written** (first table rows 8
   and 9), so
   the clause "the two being EXCLUSIVE alternatives and never mixed" is TRUE —
   about the two HEAD FORMS, which is what it has always been about.

## 1. The decisions

| # | decision | taken | alternative, and its cost |
| --- | --- | --- | --- |
| **D1** | **THE SHAPE**: amend the TEXT to admit `, and ` | RULED by Brett Heap | narrow `_SEPARATOR_RE` to three — refuses declarations the corpus already writes, reds `test_every_ratified_list_separator_is_admitted`, and gives the packet a code surface |
| **D2** | **THE EXCLUSIVITY CLAUSE**: state its antecedent as THOSE TWO HEAD FORMS | recommended, and encoded | leave "the two" after a FOUR-item list — canon that invites a false reading of a rule the module does enforce |
| **D3** | **MIXED SEPARATORS**: state that a list MAY mix them | recommended, and encoded | say nothing — leaves the reader to guess at exactly the point D2 disambiguates |
| **D4** | **THE `parse_head` DOCSTRING**: not edited; named as residue | recommended, and encoded | edit it — one comment for a CODE SURFACE and an archive held behind merged-plus-green evidence |
| **D5** | **THE ADDED SCENARIO'S PLACE**: beside the several-repositories scenario | recommended, and encoded | at the end of the block, per the amend precedent — correct but further from the rule it exercises |
| **D6** | **CONSTRUCTION**: slice canon and substitute | recommended, and encoded | transcribe — a byte-faithfulness claim nobody can check |

### D1 — The shape is ruled, and the alternative is written out because it was real

Issue #1092 put two shapes and this packet takes the first because Brett Heap
took it. The second is recorded here rather than dismissed: narrowing
`_SEPARATOR_RE` to the ratified three would have made the module match canon at
the cost of refusing every declaration written with an Oxford comma, reddening
the bench test whose own name calls `", and "` a *ratified list separator*, and
turning a prose amendment into a code change with a realization gate in front of
its archive. **THE READER STAYS AS REALIZED. NO COMMIT OF THIS PACKET TOUCHES
`scripts/code_surface.py`.**

### D2 — "the two" is said of the head forms, and the delta says so

The promoted sentence reads

> … EITHER the single token `none`, OR a list of one or more REPOSITORY
> IDENTIFIERS separated by a comma, by ` and `, or by ` + `, **the two being
> EXCLUSIVE alternatives and never mixed** …

**THE ANTECEDENT IS NOT IN DOUBT, AND IT IS NOT THIS PACKET'S READING OF IT.**
The originating packet's own design record says it in as many words:

> THE FIX makes the two alternatives EXCLUSIVE in the requirement's first line
> (`EITHER the single token none, OR a list … the two being EXCLUSIVE
> alternatives and never mixed`), adds a paragraph stating why the exclusivity
> is written down rather than left to good sense, and adds a tenth scenario —
> *A head mixes none with a repository identifier* …

— `openspec/changes/archive/2026-09-16-gate-code-surface-declarations/design.md:631-637`.
The module agrees: the only exclusivity `parse_head` enforces is the sentinel's
(`scripts/code_surface.py:524-552`, rows 8 and 9 of § 0's table), and nothing
anywhere refuses a head for mixing separators.

**SO WHY TOUCH IT AT ALL.** Because the list in front of the clause grows from
three to four in this very delta, and "the two" reads as a pointer to the list it
follows. Today a reader who miscounts gets an arithmetic contradiction and knows
to look further; after the amendment they get a plausible false rule — *use one
separator per head* — that the gate does not enforce and that the corpus does
not obey. The clause therefore names its antecedent: **THOSE TWO HEAD FORMS**.
**NO RULE MOVES**: the pair is the same pair, the refusal is the same refusal,
and the scenario *A head mixes none with a repository identifier* is carried
byte-identically.

**THE VETO IS CHEAP AND IT IS NAMED HERE FOR THAT REASON.** Striking D2 costs
four words of the opening sentence and nothing else; the marker's first named
unit and its replacement stay as they are in every other respect.

### D3 — What the reader does with a mixed-separator head is stated, not left out

`openxFactory, openXwallet and codexFactory` and
`openxFactory and openXwallet + codexFactory` both parse to three identifiers
today (§ 0, rows 2 and 3). The promoted text never said whether they may, and
the question could not arise while a reader misread "the two" as the separators.
D2 removes that misreading and would leave a silence exactly where it used to
be, so the delta states the truth of the code in one sentence: the separators are
**alternatives WITHIN one list** and a head **MAY** mix them.

This is the same species of act as the ruled one — text catching up with a
reader that has behaved this way since it was written — and it is measured, not
designed: no module changes, no test changes, and the corpus's existing heads are
admitted before and after on identical terms. **IT IS SEPARABLE FROM D2**:
striking D3 deletes one sentence of the added paragraph and one `AND` bullet of
the added scenario, and leaves the amendment whole.

### D4 — The module's own docstring is the same defect, and is NOT swept here

`scripts/code_surface.py:447-448` restates the grammar in `parse_head`'s
docstring — *"as `none`, or as repository identifiers separated by a comma, by
` and ` or by ` + `"* — and names three where the regular expression twelve lines
above it carries four. It is the identical divergence in a second place.

**IT IS DELIBERATELY NOT CORRECTED.** Editing it would give this packet a CODE
SURFACE: `code_surface:` would cease to be `none`, and under
`release-realization` the archive would move from *landing plus this task list*
to *merged-plus-green realization evidence* — a realization gate in front of a
comment. The packet would also stop being the thing the ruling commissioned,
which was an amendment of promoted text.

**IT IS NAMED RATHER THAN LEFT.** `tasks.md` § 5.1 carries it as residue, open,
ticking at the archive act by naming a filed successor issue — the *"Tick on the
recording"* ruling of 2026-09-06T23:10Z — or by Brett Heap's word that a
docstring needs no correction. It is not done here and this packet does not
claim it is.

### D5 — The added scenario sits beside the scenario whose rule it narrows

The amend precedent (`amend-modified-block-currency-standing`) added its one
scenario at the END of the block, and that was right there: its subject (the
reach of a resolution class) belonged to no existing scenario. Here the subject
is the LIST GRAMMAR, and *An active proposal declares several repositories* is
the scenario that exercises it. *A declaration spells its list out with an Oxford
comma* is placed immediately after it so a reader meets the general rule and its
spelled-out case together. Placement is not normative and the checker does not
read it; this note exists so the divergence from the precedent is deliberate on
the record rather than accidental.

### D6 — Byte-faithfulness is a construction, not a claim

The block was produced by slicing `openspec/specs/release-realization/spec.md`
lines 1014–1132 at `3e32d987` and applying each replacement as an exact
single-occurrence substitution, asserting the count is one before each. Anything
not named in the `Removed from canon` marker is therefore canon's own bytes by
construction, and the machine that checks it — doc-health's
modified-block-currency family — is run over the result and reported in
`tasks.md` § 3.

**THE MARKER'S THIRD NAMED UNIT IS PADDED, AND THE PADDING IS COMMONMARK'S.**
That unit ends on the code span `` ` + ` ``, so an unpadded `` `` `` close would
have produced a run of three backticks that never matches a two-backtick opener.
One space at each end fixes it and the reader strips exactly one from each
(`extract_code_spans`, `scripts/doc_health/modified_block_currency.py:682-714`);
the marker was parsed with that module's own `parse_marker` after authoring and
returns THREE names, which `tasks.md` § 3 records.

## 2. What this design does not decide

- **Whether the estate should define a repository inventory** to resolve
  identifiers against. The promoted requirement names that as a successor and
  this packet does not reach it.
- **Whether `, and ` should have been admitted at all.** It was, on the day the
  module was written, and the ruling settles the direction of the reconciliation.
- **Anything about the gloss-opener set, the sentinel, the closed register, the
  repeated-header refusal or the archived-record rule.** All are carried
  byte-identically.
