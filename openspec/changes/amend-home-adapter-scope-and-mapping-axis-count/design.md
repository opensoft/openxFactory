# Design: amend-home-adapter-scope-and-mapping-axis-count

Status: draft
Kind: design

The authoring decisions this packet reaches beyond the two findings it encodes.
Each is declared for a veto and each is one edit away.

## D1 — the home-adapter exception is ONE NAMED IMPLEMENTATION, not a class

The finding offered two remedies: *"Scope this rule to externally consumed
readers or explicitly exempt the home adapter."* They are not equivalent, and
the difference is the whole safety of the rule.

**Scoping to "externally consumed readers" — or, equivalently, exempting
anything `openxFactory` authors — would reopen the hole the requirement's own
third scenario closes.** That scenario reads: *"WHEN a corpus reader is copied
into `openxFactory` rather than pinned as an external product / THEN the copy is
refused, because a vendored reader has no version anyone can name and drifts
silently from the product it was taken from."* A general "we authored it" carve-out
makes that scenario unreachable by construction: the next reader that ought to be
pinned is simply authored here instead, and the rule reports nothing.

So the exception is written as ONE implementation — the adapter RULING DQ-1
keeps — with a scenario that refuses a second one claiming the same exception.
**The exception's boundary is a scenario and not only prose**, because a
boundary a requirement states only in its body is a boundary nothing tests.

**A third form was considered and rejected: leaving requirement 1 alone and
adding the exception to requirement 4 instead.** It would put the exception in
the requirement the home adapter already satisfies, leaving requirement 1
literally false of a tool the estate is required to keep. The defect is in the
scope of clause 1; it is repaired where it is.

## D2 — the sixth axis is NAMED as an axis, not nested under one of the five

The finding offered the same shape of choice: *"Define that nesting or revise the
axis list."* Nesting was considered against each of the five and fits none. The
truth store is not an artifact kind, not a status vocabulary, not an act or a
gate, not an evidence class and not an authority; the nearest candidate, the
ACTS-and-GATES axis, governs what an act must pass and not what a model may
never write, and the two are different questions about different subjects.

**The realized artifact decided this before the amendment did**, which is why
the amendment reports a fact rather than making a choice:
`contracts/domain-profiles/openxfactory-engineering.yaml` carries `truth_store:`
as a TOP-LEVEL key under no axis banner, and `DomainProfile` carries it as its
own field. Nesting it now would make the one realized declaration in the estate
non-conformant to repair a text defect — which is the inversion this packet
exists to avoid.

**What is deliberately NOT done: the third requirement is not edited.** It
already states the obligation in full, with three scenarios. Restating it inside
the axis list would put one obligation in two places in one file and set up the
next drift. The axis list NAMES the axis and defers its content by requirement
title.

## D3 — both blocks are written over canon as promoted, and no basis marker is owed

`openspec/changes/*/specs/` was enumerated on `main` `4f92d651`: **no active
change carries a delta on `corpus-adapter-seam` or on
`domain-mapping-declaration`.** The only change that ever did,
`split-opendox-two-layer-product`, archived on 2026-09-22 (`#1139` ->
`e8fde27f`). So each block is written over canon as promoted, there is no
partner to pair with, and no basis or `Merged into` marker is owed.

**This is the opposite of `#1140`'s situation and the difference is worth
naming**, because the two packets were authored the same day against findings
from the same review: that one wrote over an ACTIVE packet's outcome, because
`split-opendox-two-layer-product` still held a live `## MODIFIED` block on the
requirement it amended. Here the basis has already archived, so canon IS the
outcome and writing over it is correct in one order rather than two.

## D4 — the carriage is proved by script, not by care

A `## MODIFIED Requirements` block REPLACES the requirement it names. A scenario
dropped or retyped with one character changed is a requirement quietly narrowed
at promotion, and it is invisible in review because the block reads complete.

Both blocks were built by EXTRACTING the promoted scenarios programmatically
from `openspec/specs/` rather than by retyping them, and
`review/verify-carriage.py` re-extracts and compares on demand:

    OK corpus-adapter-seam: all 3 promoted scenarios carried byte-identically; block carries 5 in total
    OK domain-mapping-declaration: all 3 promoted scenarios carried byte-identically; block carries 4 in total

It is committed with the packet rather than run once and reported, so the proof
survives every later edit — including edits made in response to review.

## D5 — two stale strings found and deliberately not fixed

Both were met while measuring and neither is folded in.

1. `contracts/domain-profiles/openxfactory-engineering.yaml`'s `basis:` list
   cites *"openspec/changes/split-opendox-two-layer-product/specs/domain-mapping-declaration/spec.md
   — the five axes and the two refusals this file answers"*. The PATH moved when
   the packet archived on 2026-09-22; the COUNT describes what that delta said,
   which it did. Editing it is a contract edit, and a doctrine-only packet
   acquiring a code surface to repair a citation the archive left would misstate
   what this change is. Registered at `tasks.md` § 5.1.
2. `README.md`:3270 reads *"`domain-mapping-declaration` (3 requirements: the
   five axes a `<Domainx>Dox` descendant declares)"*. Read in place it is the
   ARCHIVE RECORD's narrative of what `split-opendox-two-layer-product`
   promoted — the sentence continues *"and **FOUR MODIFIED** requirements"* —
   and as a record of that packet it is accurate and stays. Registered at
   `tasks.md` § 5.2 so a reader who takes it for a live capability description
   finds the question already asked.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
