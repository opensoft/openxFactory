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

## D4a — the one replaced unit is DECLARED, not silently reworded

The seam block only INSERTS: every promoted body unit survives it, and
`doc-health --family modified-block-currency` names it in zero findings. The
mapping block REPLACES one — the `exactly five axes` sentence — which is the
whole object of the amendment, and the checker reported it exactly as it should:
*"a divergence this arm CANNOT distinguish from a deliberate rewording, and does
not claim to"*, severity `info`, class `contested`.

**A packet whose thesis is that a `## MODIFIED` block must not quietly alter
promoted text cannot leave that finding standing.** So the removal is declared in
the form `document-lifecycle` reserves — `**Removed from canon by
amend-home-adapter-scope-and-mapping-axis-count (2026-09-22):**` carrying the
removed unit VERBATIM in a code span, then the reason — and the reason states
what an author reading the diff needs and a checker cannot infer: that the
sentence is REPLACED rather than dropped, that all five axes it names are carried
forward in its own words and its own order, and that exactly two things change.
The disclosure clause the same module requires of a `Modified over` marker does
not apply here: that one's basis is another ACTIVE change whose standing must be
disclosed, while this marker's basis is canon.

Both families re-measured clean after it: `--family modified-block-currency` and
`--family proposal-origin` each name this packet in ZERO findings.

## D4b — the carriage proof was itself defective, twice, and both are proved

Copilot's first review of this packet found two FACT defects in `verify-carriage.py`
(`r4075847837`, `r4075847914`) and both were taken. **A carriage proof that is
approximately right proves nothing**, so each fix is proved by construction
rather than asserted.

**(1) `Path.read_text()` applies universal-newline conversion**, so the script
claimed a BYTE-FOR-BYTE comparison over bytes it had already normalized. Proved:
rewriting the delta CRLF leaves every byte different from the promoted LF file,
and the old reader answers `carried in delta -> True`. The script now reads
BYTES, decodes strictly, and REFUSES a carriage return outright — reported rather
than smoothed, because this corpus writes LF and an unexpected CR is a fact.
Against the CRLF tree it now exits 1 naming the file.

**(2) `carried in delta_text` searched the whole file**, so the promoted bytes
surviving ANYWHERE — in prose, in a marker, under another requirement — read as
carriage while the requirement's real blocks were replaced. **Not hypothetical
here:** this packet's `domain-mapping-declaration` delta carries a promoted BODY
unit verbatim inside its `Removed from canon by` marker, exactly the quotation a
substring search accepts. Proved: with the pristine promoted region quoted into
the header prose and one real scenario bullet altered by a single word's case,
the old check answers `carried in delta -> True` **while the requirement is
narrowed**, and the new one answers

    FAIL corpus-adapter-seam: 1 promoted scenario block(s) not carried
    byte-identically; first -> #### Scenario: A neutral product imports the
    corpus's own tooling

Each side is now parsed into individual `#### Scenario:` blocks under the same
requirement title, and every promoted block must appear among the DELTA's parsed
blocks. Both controls were run against the pre-fix reader and the post-fix
reader, and the tree was restored and re-measured clean after each.

**The lesson is the packet's own thesis turned on itself:** a check that compares
a concatenation cannot tell carriage from quotation, and the packet that most
needed to know the difference had written one.

## D4c — the exception had to reach the ONE-WAY clause too, and that is the same exception

Copilot `r4076010204` found that the first fix relaxed only the external/pinned
sentence, while the next sentence still read *"a reader depends on the interface
it implements, and never on the corpus's own check families"* — and the home
adapter imports `doc_health` at six sites. **So the requirement was still false of
it, one clause over.** Taken.

**The scope is the SEAM, and that is what makes this one exception rather than
two.** The one-way rule governs the dependency ACROSS the seam: a reader in
another repository must not import back into the corpus's tooling, which is the
extraction hazard the requirement's measured instance is drawn from. A reader
INSIDE the repository whose corpus it reads is not across the seam from it, and
its dependence on `doc_health` is precisely what RULING DQ-1 placed it beside
them to do. Reading the sentence as forbidding the home adapter its neighbours
would forbid the one thing that ruling kept it here for.

**What is still owed OF the home adapter is stated rather than dropped**, and it
is the half of the one-way rule that has real content here: it depends on the
interface it implements, and that interface depends on nothing of this
repository's. **That is measured today, and by a test that names requirement 1
itself.** `tests/corpus-adapter/test_no_privileged_route.py`:155,
`test_the_interface_imports_neither_reader_package_nor_the_implementation`, scans
`scripts/corpus_adapter.py` — the in-tree interface module, provisional under
RULING Q4 and carried to openDox with the carve — and refuses any import of
`doc_health`, `ideation_dashboard` or the implementation package, with the
assertion message *"an implementation depends on the interface, never the reverse
(requirement 1)"*. The adapter's own side is the mirror of it: all five of its
interface imports name the PINNED leg, `from opendox.corpus_adapter import …`
(`adapter.py:75`, `check.py:54`, `classify.py:51`, `home.py:72`, `shape.py:44`).
The added scenario states what those two facts already hold.

*(A correction folded in before this reached anyone downstream: the first
drafting of this paragraph, and my reply on the thread, cited
`test_interface_closure.py`. That file tests a different property — that the
interface is CLOSED at six operations and the home adapter offers no seventh,
which is requirement 4's second scenario. The direction test is the one named
above, and it is the stronger citation, because it names requirement 1 in its own
failure message.)*

**And the exception is bounded once more:** it does NOT reach the relocation rule
that follows. That rule is about EXTRACTION and binds the home adapter exactly as
it binds anything else — if a package here and a package leaving here import each
other, the shared type moves into a module both depend on before either goes.
Three clauses in one requirement, and the exception reaches two of them by name.

**The promoted one-way sentence is carried VERBATIM.** The scoping is stated in
the exception paragraph that immediately precedes it and names the clauses it
reaches, rather than by editing the sentence — so the seam block still removes
NO promoted body unit, and `verify-carriage.py` still reports all three promoted
scenarios carried.

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
