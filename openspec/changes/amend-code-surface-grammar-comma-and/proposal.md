---
code_surface: none — MEASURED, not assumed. The delta is requirement prose and NOT ONE CHARACTER of the reader it describes moves. Evidence, taken 2026-09-18 on the clone of `main` `3e32d987` this packet was authored against: (1) `grep -rn "EXCLUSIVE alternatives\|the two being" scripts tests` returns NOTHING — no module and no test reads the sentences this block replaces; (2) `grep -rn "separated by a comma" scripts tests` returns exactly ONE line, `scripts/code_surface.py:448`, and it is the `parse_head` DOCSTRING's own restatement of the grammar (`:447-448`), which this packet deliberately does NOT edit (`design.md` D4 — it is residue, named as a successor, not swept); (3) the behaviour the delta describes is already PINNED BY THE BENCH — `tests/code_surface/test_code_surface_gate.py:157-160` parametrizes `test_every_ratified_list_separator_is_admitted` over five spellings INCLUDING `", and "`, and `:170-173` pins the refusal of `openxFactory, and it is THREE FILES at realization` — so a delta that moved the reader would red those tests, and this one cannot, because it touches no module; (4) the one mechanical consumer of this block is doc-health's own modified-block-currency family, which reads every active `## MODIFIED` block by construction: that is a GATE OVER this packet, not a surface it changes. TWO FILES UNDER `tests/` ARE TOUCHED AND NEITHER IS A CODE SURFACE, which is stated here rather than left for a reader to notice: `tests/sequenced_after/corpus-ledger.yaml` (this packet's own row plus the partner flip it causes, written by the sanctioned seeder and by no hand) and the MOVEMENT LOG docstring inside `tests/sequenced_after/test_sweep.py` (the dated narrative that ledger's own rule OWES for a partner flip). Both are the bookkeeping every packet performs, they assert nothing and change no test's outcome, and the precedent is exact — `state-header-window-budget` (PR #921, commit `99cff89b`) appended the same kind of entry to the same docstring while declaring `code_surface: none`. Under `release-realization` an empty code surface archives ON LANDING plus this task list rather than on merged-plus-green realization evidence.
target_release: implemented — the value `release-realization` names for a doc-only change: *"A proposal without the declarations is a doc-only change (`code_surface: none`, `target_release: implemented`)"*. No contract bundle is cut, nothing under `contracts/` is touched, no `contracts/releases/<tag>.digests.yaml` moves, no digest set changes and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on Brett Heap's word.
sequenced_after: []
---

# Proposal: amend-code-surface-grammar-comma-and

Status: ratified
Ratified: 2026-09-18 by Brett Heap (openxFactory operator authority) — "Amend the text to admit ', and '"; record at review/ratification-2026-09-18.md
Kind: proposal
Proposed: 2026-09-18, in lane `openxfactory-5` (display `openXfactory-5`), on
Brett Heap's ruling of the same day — the word that commissions this packet and
the word that ratifies it are ONE utterance, which is why nothing here was ever
`Status: draft`.
Origin: openxFactory
[#1092](https://github.com/opensoft/openxFactory/issues/1092), filed by this
lane at the archive of `gate-code-surface-declarations`
([#1076](https://github.com/opensoft/openxFactory/pull/1076) → `5dd0a8dc`) from
a suppressed Copilot comment on that pull request's round 3, head `a8d3cfb6`.

**THE WORD REACHED THE PACKET'S CONTENT BEFORE THE PACKET EXISTED, AND THAT IS
WHY IT LANDS AS RATIFIED.** Issue #1092 put two shapes and asked for a ruling;
Brett Heap answered with one of them, verbatim **"Amend the text to admit
', and '"**, on 2026-09-18 at approximately 09:55Z, as a terminal
multiple-choice answer given directly to lane `openXfactory-5` and recorded by
it as a `RULED` line in `lanes/log/openXfactory-5.md` at **2026-09-18T10:15:10Z**
(`brett-wip` `055bea8b`). There is therefore no drafting phase to record and no
approval to add beside an earlier origin: `.openspec.yaml` carries
`proposed_by` and `approved_by` written in ONE act, with `kind` and `id` fixed
from the first commit, and every document in the packet carries
`Status: ratified` with one citation line. The act is recorded at
`review/ratification-2026-09-18.md`.

**NOTHING IS PROMOTED BY THIS LANDING.** This pull request edits no file under
`openspec/specs/`, no script, no test, no contract and no workflow — promotion
of the block into `openspec/specs/release-realization/spec.md` happens at the
ARCHIVE, which is a separate act on a separate word, and openxFactory #1092
closes there and not here. That is why this body says *refs* and carries no
closing keyword.

## Why

**PROMOTED CANON NAMES THREE LIST SEPARATORS. THE READER IT GOVERNS HAS ADMITTED
FOUR SINCE THE DAY IT WAS WRITTEN, AND SO HAS THAT READER'S OWN BENCH.**

`openspec/specs/release-realization/spec.md:1017-1018`, inside *Code-surface
declaration grammar is gated*, admits a declared head that is

> a list of one or more REPOSITORY IDENTIFIERS separated by a comma, by ` and `,
> or by ` + `, the two being EXCLUSIVE alternatives and never mixed

and the scenario at `:1103` repeats the same three.

**THE GRAMMAR THE VALIDATOR RUNS CARRIES FOUR** (`scripts/code_surface.py:152-157`,
measured rather than recalled):

```python
_SEPARATOR_RE = re.compile(
    r",[ \t\n]+and[ \t\n]+"      # ", and "
    r"|,[ \t\n]*"                # ","  (with or without a following space)
    r"|[ \t\n]+and[ \t\n]+"      # " and "
    r"|[ \t\n]+\+[ \t\n]+"       # " + "
)
```

`, and ` is tried **FIRST**, ahead of the bare comma, and the module's own
comment says why: *"Tried in this order so `, and ` is consumed whole rather
than as a bare comma followed by a head that opens with the word `and`."* A
declaration that spells its list out the way English spells one out —
`openxFactory, openXwallet, and codexFactory` — therefore parses as **three**
identifiers at a gate whose ratified text says it should have been read as two
and a run-on.

| the requirement says | the module says | where |
| --- | --- | --- |
| three separators: a comma, ` and `, ` + ` | four: `, and `, a comma, ` and `, ` + ` | `scripts/code_surface.py:152-157` |
| a head "continued by `, and …`" is REFUSED | refused only where the continuation is not itself a readable identifier | `scripts/code_surface.py:493-516`, and `tests/code_surface/test_code_surface_gate.py:170-173` |
| — | `test_every_ratified_list_separator_is_admitted` parametrizes **five** spellings, `", and "` among them | `tests/code_surface/test_code_surface_gate.py:157-160` |

**THE BENCH ALREADY CALLS THE FOURTH ONE RATIFIED.** That test's name says
*ratified list separator* and its parameter list carries `", and "`; the
ratified text names three. One of the two is wrong about what was ratified, and
the ruling settles which: the text.

**WHY IT WAS NOT FIXED IN #1076.** `openspec/specs/release-realization/spec.md`
is promoted canon and PR #1076 was an ARCHIVE act that carried the three ADDED
requirements into it byte-for-byte, measuring the transfer in its own § 5.1. A
normative requirement-text change after a ratify word goes to Brett Heap as
RULING NEEDED and lands as an amendment on his word, per the 2026-09-01
precedent. So the finding was filed as #1092, refused as a round-3 fix, and is
taken here.

## What Changes

**ONE `## MODIFIED` REQUIREMENT. THREE UNITS REPLACED IN PLACE UNDER ONE
`Removed from canon` MARKER, TWO BODY PARAGRAPHS AND ONE SCENARIO ADDED.
NOTHING ELSE.**

1. **The opening SHALL sentence names FOUR separators** — a comma, `, and `,
   ` and `, ` + ` — in the order that makes a reader's eye land on the
   distinction, and its exclusivity clause is said of **THOSE TWO HEAD FORMS**
   rather than of "the two" (`design.md` D2). The antecedent is unchanged: the
   originating packet's `design.md:631-637` names it as the pair `none`-or-list,
   and the module enforces exactly that pair and nothing else.
2. **One ADDED body paragraph states the ORDER and what it buys** — `, and ` is
   ONE separator, read ahead of the bare comma, so a spelled-out list is
   consumed as one separator rather than as a comma plus a member opening with
   the word `and`. It also states, as canon, what the reader has always done
   and the text never said: **the four separators are alternatives WITHIN one
   list and a head MAY mix them** (`design.md` D3, measured:
   `openxFactory, openXwallet and codexFactory` and
   `openxFactory and openXwallet + codexFactory` both parse to three today).
3. **The flat refusal of a head "continued by `, and …`" is narrowed to what the
   reader actually does**, and one ADDED paragraph states the residue: where the
   words after `, and ` are themselves a repository identifier followed by a
   gloss opener or the end of the declaration they are ADMITTED as a further
   member; where they are not — an ordinary sentence — the refusal stands. That
   is not a new rule, it is what
   `test_a_head_that_runs_into_prose_with_no_opener_is_refused`
   (`tests/code_surface/test_code_surface_gate.py:170-173`) has pinned since the
   gate landed.
4. **The WHEN bullet of *An active proposal declares several repositories* names
   the four**, and every other bullet of that scenario is carried unchanged.
5. **ONE SCENARIO IS ADDED**, *A declaration spells its list out with an Oxford
   comma*, placed beside the several-repositories scenario rather than at the
   end of the block (`design.md` D5): `openxFactory, openXwallet, and
   codexFactory` reads as THREE identifiers, MUST NOT be read as two plus a
   member opening with `and`, and a head mixing separators is admitted on the
   same terms.
6. **Every other unit is carried byte-faithfully, BY CONSTRUCTION**: the block
   was produced by slicing `openspec/specs/release-realization/spec.md`
   lines 1014–1132 and applying each replacement as an exact single-occurrence
   substitution, so anything not named in the marker is canon's own bytes.

**AND NO CODE MOVES.** `scripts/code_surface.py` is not edited in any commit of
this packet. That is the ruled shape: issue #1092's option (b) — narrowing
`_SEPARATOR_RE` to the ratified three — was the alternative, and it was not
taken.

## Impact

- **Specification:** ONE requirement of `release-realization`. No requirement is
  ADDED, RENAMED or REMOVED, no other capability is touched, and the two
  requirements that read this one (*The declared repository set is derived from
  the head and never from the gloss*, *Standing code-surface divergence is named
  in a closed register*) are NOT edited and not restated.
- **Code:** none. See the `code_surface` front matter for the measurement. The
  two files under `tests/` this pull request touches are bookkeeping the ledger
  itself demands — `tests/sequenced_after/corpus-ledger.yaml` (two rows, written
  by `--seed-ledger`) and the MOVEMENT LOG docstring in
  `tests/sequenced_after/test_sweep.py` (one dated entry, asserting nothing).
- **Behaviour:** none. No declaration in the corpus changes its verdict, no
  derived repository set moves, `CLOSED_REGISTER` does not move, and no register
  entry is added or retired. A `validate-code-surface.py` run before promotion
  and one after are identical.
- **Contracts, bundles, digests, tags:** none.
- **Readers:** a reader of the requirement stops being told that an Oxford-comma
  list is two identifiers and a run-on. Nothing already written is invalidated:
  the archived `gate-code-surface-declarations` delta is a record of what was
  ratified and is not edited, and the declarations the corpus carries are
  unaffected either way.
- **The report's headline moves at promotion, and only there.** Promotion
  replaces a requirement with a longer one, so `openspec/specs/release-realization/spec.md`
  grows and doc-health's canon-share line moves with it. That is arithmetic on
  promoted prose, it happens at the ARCHIVE, and it is what every promotion of
  prose does.

## Sequencing

`sequenced_after: []` — the POSITIVE ROOT CLAIM, measured rather than assumed.

The requirement this block modifies is already promoted, so nothing has to land
first for the block to be written against canon. Three other active changes
carry a `release-realization` delta, enumerated on 2026-09-18 across every
active `openspec/changes/*/specs/release-realization/spec.md`:

- **`add-sequenced-after-substrate`** — `## ADDED Requirements` only, nine
  ordered-delta requirements, none of them this one.
- **`add-structured-scope-substrate`** — a `## MODIFIED` block over *Realization
  axis declaration*, plus five `## ADDED`.
- **`add-target-release-deferred-allocation`** — `## MODIFIED` blocks over
  *Realization axis declaration* and *Realization axis vocabulary is gated*.

**No active change writes this requirement's key.** This packet is the SOLE
ACTIVE MODIFIER of *Code-surface declaration grammar is gated*, no ordering
declaration is owed in either direction, and the two-writers rule does not reach
the pair. The per-change sweep ledger grades `class` over the WHOLE corpus,
archived changes included, so this packet's row and the row of the archived
change that wrote this requirement before it read `co-modifier`; that is
definitional for any amendment of promoted canon and is not a contradiction of
the sole-active-modifier measurement.

## What this proposal does NOT claim

- **It does not claim the reader is wrong.** The ruling took the text, not the
  code. `_SEPARATOR_RE` is correct, its ordering is correct, and this packet
  makes canon say so.
- **It does not widen or narrow what the gate admits.** No declaration changes
  verdict. It adds no separator to the module, removes none, and reorders none.
- **It does not touch the sentinel rule, the identifier shape, the gloss-opener
  set, the repeated-header refusal, the block-scalar refusal, the absence
  default, the archived-record rule, the derived-set requirement or the closed
  register.**
- **It does not correct `scripts/code_surface.py`'s `parse_head` docstring**,
  which restates the three separators at `:447-448` and is the same divergence in a
  second place. Editing it would give this packet a CODE SURFACE and move its
  archive behind merged-plus-green realization evidence for a comment. It is
  named as residue in `tasks.md` § 5.1 and `design.md` D4, and ticks at the
  archive by naming a filed successor.
- **It does not edit any archived delta**, including
  `gate-code-surface-declarations`'s own. An archived delta is a record of what
  was ratified.
- **It promotes nothing.** Promotion happens at the ARCHIVE, a separate act on a
  separate word; openxFactory #1092 closes there and not at this landing.
