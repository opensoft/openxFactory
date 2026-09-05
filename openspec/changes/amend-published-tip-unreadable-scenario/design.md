# Design: amend-published-tip-unreadable-scenario

Status: draft
Kind: design

## 0. The brief

openxFactory issue **#662**, filed by lane `doxbench-stewardship`, asks for *"a
one-line MODIFIED delta on this scenario — replace 'the commonest cause being a
checkout that has not fetched that commit' with wording that names both facts
and that the family MUST establish which one holds before choosing its words
(present-but-absent-file is answered; unfetched is skipped). No behaviour
change; canon catching up with the checker."* Brett Heap admitted it on
2026-09-05 with *"do both as a batch on one word"*.

The issue settles the content. This document decides the one thing it does not.

## D1 — the establishing obligation is written on the `WHEN` side

**The question.** *"The family MUST establish which one holds before choosing
its words"* is an obligation. A scenario has two sides for one: a `THEN` bullet
(what the family must DO when the scenario applies) or a `WHEN` bullet (a fact
that is already true by the time it applies).

**Written as a `THEN`, it is circular.** The scenario's trigger is *the read
answered nothing*, and both of its outcomes — skip-as-unfetched and
skip-as-present-and-empty — depend on which fact holds. A `THEN` saying
"establish which holds" would place the establishing AFTER the branch it
decides, and a conforming family could satisfy it by establishing the fact and
then reporting either skip.

**Decision: a `WHEN`-side `AND`.** The scenario applies to a family that HAS
already asked presence and attempted its one bounded fetch; the two `THEN`s then
name the two outcomes and the words each owes. This matches the code exactly —
`obtain_commit` runs BEFORE the two `manifest is None` arms in `check_repo`, and
the arms are gated on `tip_present` rather than asserting it — and it is the
reading that makes the second `AND` below meaningful rather than optional.

**What it costs, said plainly.** A `WHEN`-side obligation is weaker as a
compliance hook: a family that never established anything does not *violate*
this scenario, it simply never enters it. That is acceptable here because the
obligation is not left unpinned — the sibling scenarios and the promoted body
already require each skip to name its own reason, and the suite asserts the two
skip texts against each other as literals. **This is the decision most worth a
veto**, and the alternative is a mechanical change: move the bullet below the
`THEN` and reword it as a `MUST`.

## D2 — the promoted `THEN` is carried verbatim even though it reads oddly now

The promoted bullet is *"the family MUST report a skip saying so"*, where *"so"*
referred to the single cause the old `WHEN` named. With the `WHEN` now naming
two facts, *"so"* is looser than it was.

**It is carried byte-identical anyway.** It is canon, this packet's whole point
is to change ONE clause, and rewriting a second bullet would drop a second unit
and turn a one-line amendment into a re-authoring of the scenario. The looseness
is answered by the `AND` added immediately below it, which says what the OTHER
outcome owes — so a reader arriving at *"saying so"* meets the disambiguation
one line later rather than a rewritten rule with no trace of what it replaced.
That is the same discipline the `declare-spent-bundle-state` amendment used when
it kept *"reported at `error` without grading"* byte-faithful and qualified it
underneath.

## D3 — one unit is dropped, so the marker is owed and is carried

Unlike `add-release-tag-gate`, whose `## MODIFIED` block only ADDED and
therefore owed no marker, this block REPLACES a bullet. Under
`doc-health`'s *Currency of an active change's MODIFIED requirement blocks* a
canon unit the block does not carry is reported unless a reserved marker
declares it, so the block carries:

```
**Removed from canon by amend-published-tip-unreadable-scenario (2026-09-05):**
``<the old WHEN bullet, verbatim>`` — <reason>
```

The unit is quoted as a code span with the list marker stripped, which is the
granularity the family compares at. **It is a REPLACEMENT, not a deletion**, and
the marker's reason says so: the clause is superseded by the `WHEN` that names
both facts and the `AND` that requires the family to establish which holds.

## D4 — `code_surface: none`, checked rather than assumed

The amended wording describes behaviour that already exists. Before writing this
packet the tree was checked for anything that would have to move with it:

- `scripts/doc_health/release_tag_publication.py` already runs `obtain_commit`
  before the two `manifest is None` arms, and the arms are gated on
  `tip_present`; the two skips already carry the two different reasons.
- `tests/doc-health/test_release_tag_publication.py` already asserts them apart
  as fresh literals (`_UNFETCHED_WORDS`, `_FETCH_TRIED_WORDS`, `_PRESENT_WORDS`,
  `_ANSWERED_WORDS`) over a `_StoreGit` fake that can express "the commit is not
  here".
- **No test asserts the old scenario prose.** The only occurrence of "commonest
  cause" outside canon is a code comment, not an assertion.

So no test moves and no script moves. Had any of those readings come back the
other way, this would have been a code surface and the front matter would say
so.
