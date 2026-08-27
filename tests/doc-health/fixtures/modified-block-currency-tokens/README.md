# Fixture: tokens with internal periods, and a note edited in its third sentence

**SYNTHESIZED** — this text is invented and reproduces no historical instance.

## Which rule this exists for

`add-modified-block-currency-check` § 3.5, audit row **A6**.

> Backticked spans SHALL be masked before any sentence split, so that a period
> inside `.openspec.yaml` or `promotion_fidelity.py` never ends a sentence. …
> each bullet line SHALL be one unit with its list marker stripped; each dated
> bold note SHALL be one unit, undivided, a note being a single editorial
> statement whose sentences mean nothing apart
> — `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`

## Why not a reconstruction

The tokenization rule has no historical VIOLATION to reconstruct — it is a
derivation invariant rather than a defect anyone committed. What F1 lacked was
coverage at § 3.5's own granularity, in three places:

1. `contract-v1.45` — a token whose period sits **between digits**. F1's fixture
   carries `.openspec.yaml` and `openxFactory` only, and a naive `\d\.\d`
   sentence guard waves a version token through while catching a leading-dot
   one. `promotion_fidelity.py` is here too, for the same reason.
2. A dated bold note of **four** sentences. F1's is two.
3. The note **EDITED IN ITS THIRD SENTENCE** rather than dropped. Dropped is the
   weaker case: an implementation that split a note into sentences would report
   a dropped note as N rows, but would report an EDITED note as 1 row out of N.
   Only the edit tells "one undivided unit" apart from "sentence-wise comparison
   that happened to agree".

## What the family reports here

One `info` on `Tokens with internal periods never end a sentence`, listing 3 of
canon's 9 units: the two body bullets the block dropped (list markers stripped),
and the four-sentence note — **once**. The three tokened sentences are restated
verbatim and are NOT reported, so no unit boundary fell inside a backticked
span.

Tests: `test_no_unit_boundary_falls_inside_a_versioned_token`,
`test_each_tokenized_body_bullet_is_its_own_reported_unit`,
`test_a_note_edited_in_its_third_sentence_is_reported_once`,
`test_masking_governs_boundaries_and_not_equality`.

The last is a DISTINCT property, kept apart deliberately: the mask decides where
units END and says nothing about whether two units are EQUAL.
