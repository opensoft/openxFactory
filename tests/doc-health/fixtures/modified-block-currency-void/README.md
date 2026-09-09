# Fixture: the two grounds on which a marker declares nothing

**SYNTHESIZED** — this text is invented and reproduces no historical instance.

## Which rule this exists for

`amend-marker-defect-reporting` (2026-09-09), openxFactory issue **#729** — the
second and third grounds on which a marker is itself reported.

> A MARKER SHALL ITSELF BE REPORTED ON ANY OF THREE GROUNDS … where its REASON
> quotes a code span that … matches a unit of the promoted requirement the block
> does NOT carry … ; and where it NAMES something matching no unit of the
> promoted requirement and no unit of the block, which is a declaration about
> nothing.
> — `openspec/changes/amend-marker-defect-reporting/specs/doc-health/spec.md`

## Why not a reconstruction

Neither ground fires anywhere in this corpus today, which is the whole of what
the packet's D0 measurement establishes: 16 unit-naming markers, 8 of them
quoting a code span inside a reason, and ZERO of those quoted spans a derived
unit of the document that carries it. A reconstruction would have to invent the
instance anyway, so it is invented here and said so.

## What the family reports here

Five requirements, one per case, and the three NEGATIVE CONTROLS are what make
the two positives mean anything — each is one fact away from a positive:

- **`A reason quotes a unit the block drops`** — the marker names `Dropped body.`
  (declared, suppressed) and its reason QUOTES `**THEN** it MUST do one thing`,
  which the promoted requirement states and the block does not restate. **Two
  findings**: the marker report, and the carriage row for the bullet — which is
  the point. The report stands BESIDE the carriage rather than instead of it.
- **`A marker names a ghost`** — the marker names `A unit nothing matches.`
  **One finding**, and no carriage row: everything else is carried, so without
  this ground the block would be reported as clean.
- **`A reason quotes prose that is no unit`** — the reason quotes `WHEN`, `AND`
  and `openspec/specs`. **Silent.** This is canon's blessed form and EIGHT of
  this corpus's SIXTEEN unit-naming markers are written this way, so it is the
  entire cost of the packet's rejected option B.
- **`A reason quotes a unit the block carries`** — the same shape as the first
  case with ONE fact changed: the block restates the quoted bullet. **Silent** —
  canon carries it, the block carries it, nothing is dropped.
- **`An inherited marker declares nothing about a later block`** — canon carries
  a marker by `an-older-change` naming a unit that left canon when that marker
  was promoted, and the block carries the paragraph verbatim as
  `document-lifecycle` requires. **Silent**, because the second and third grounds
  are read only against a marker the block's own change declares. Unscoped, this
  is the shape that would report every faithful restatement of an amended
  requirement forever.

Tests:
`test_the_void_tree_reports_both_grounds_and_is_silent_on_all_three_controls`
(`tests/doc-health/test_modified_block_currency.py`), plus the catalogue-wide
partition, determinism and band sweeps every tree joins by being here.
