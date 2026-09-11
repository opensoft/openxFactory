# release-realization Specification Delta

This delta ADDS a SECOND, EQUIVALENT DECLARATION SITE for the ordered-delta
parent declaration `sequenced_after:` — a header line inside the bounded
lifecycle header window — so that a governed corpus which writes its lifecycle
headers UNFENCED declares the field its authors already write, rather than
declaring nothing.

THE DELTA IS ALL-ADDED, AND THAT IS A CHECKED CONSTRAINT RATHER THAN A STYLE.
The requirement this change extends — "Machine-readable ordered-delta parent
declaration" — belongs to `add-sequenced-after-substrate`, which is RATIFIED and
still ACTIVE, so its nine requirements are NOT promoted in
`openspec/specs/release-realization/spec.md` (checked 2026-09-10: `grep` for the
title returns nothing, exit 1). A `## MODIFIED Requirements` block must target a
PROMOTED requirement, so no MODIFIED block over it is available, and editing a
ratified packet's own delta text is refused outright. The two titles below are
NOVEL against the eight promoted requirements of this capability and against
every title in the five ACTIVE deltas on it, so this delta restates no promoted
text, drops none, and owes no `Modified over`, `Removed from canon by` or
`Merged into` marker.

THE RELATION TO THE PARENT IS DECLARED MECHANICALLY, NOT ONLY IN PROSE. This
change carries `sequenced_after: [add-sequenced-after-substrate]` in its own
front matter — the substrate's own mechanism, used by its first successor, on
the substrate itself — and the two requirements below are written to be read
TOGETHER with the substrate's nine.

WHAT THE PARENT SAID ABOUT HEADERS, AND WHAT THIS CHANGE DOES ABOUT IT. The
substrate's ADDED requirement holds that "a prose `Sequenced-after:` header …
SHALL NOT constitute a machine-readable parent declaration", because such a
header "cannot distinguish a parent from a mention", "cannot express a fork",
and is "author-mutable in the same document the author writes". THE LEGACY
`Sequenced-after:` SPELLING REMAINS REFUSED HERE, by name and by test. What is
admitted is a DIFFERENT construct answering each reason: the FIELD'S OWN NAME
`sequenced_after:` at column 0 inside a BOUNDED window (so a mention outside it
declares nothing), loaded by the SAME strict loader under the SAME sequence
shape and entry grammar (so a fork is expressible), and covered by the SAME
base-read, ratification-covered, non-author-mutable and frozen-after-ratification
properties the front-matter form carries (so the third reason is answered
identically rather than differently — `proposal.md` front matter is not a
separate file from `proposal.md`).

## ADDED Requirements

### Requirement: Equivalent declaration sites for the ordered-delta parent declaration
A `sequenced_after:` declaration written as a LIFECYCLE HEADER LINE SHALL
declare exactly what the same declaration written in the `---`-fenced
realization-axis front matter declares, and the two sites SHALL be read by ONE
loader under ONE shape, ONE entry grammar, ONE resolution rule, ONE cycle rule
and ONE retention rule. Neither site is preferred and neither is a fallback of
lesser standing: a corpus whose proposals carry no fence is not a corpus whose
authors declared nothing.

A LIFECYCLE HEADER LINE IS A BOUNDED CONSTRUCT, AND THE BOUND IS THE
REQUIREMENT'S SUBSTANCE. It is a line whose first characters are the field's own
name followed by a colon, at column 0, case-sensitively, sitting within the
document's BOUNDED LIFECYCLE HEADER WINDOW — the same window, counted in the same
REAL LINES (CR, LF and CRLF only), that this corpus already reads a document's
`Status:` header in — and outside any leading `---` fence, whose lines are read
by the front-matter reader and MUST NOT be counted a second time as header lines
of the same document. BEYOND THAT WINDOW THE SAME BYTES ARE PROSE AND SHALL
DECLARE NOTHING. The bound is what front matter was chosen FOR: the alternative
it refused was unbounded prose parsing, in which a `sequenced_after:` written in
a body paragraph would authorize as loudly as one written in a header, and this
capability already refuses a mention as a parent link. An INDENTED line is a
continuation of what precedes it and SHALL NOT declare. The legacy free-text
`Sequenced-after:` header SHALL continue to declare nothing and SHALL continue
to be counted as the prose header it is.

THE HEADER-LINE FORM IS A SINGLE LINE, because an unfenced document supplies no
closing delimiter: a multi-line value has no defined end, and a window boundary
falling inside one would show a reader one declaration and authorize another. A
self-delimiting flow sequence on the line SHALL be the admitted form; a
valueless field line followed by an indented continuation SHALL be refused BY
NAME, naming the forms that work, rather than read as null. A field line with no
value and no continuation SHALL be PRESENT-but-null and SHALL be refused by the
field's own shape validation, never read as absence — presence is decided by the
KEY on both sites.

THIS EQUIVALENCE IS GRANTED TO THE PARENT DECLARATION ALONE. The structured
path-scope declaration `scope_globs:` SHALL NOT be declarable as a header line.
The asymmetry is deliberate: `sequenced_after:` declares WHERE IN A CHAIN a
change sits, and every consumer applies its own root proof, co-modifier
cross-check and refusals on top, so making an author's existing declaration
legible authorizes nothing that absence did not already refuse; `scope_globs:`
declares WHICH PATHS an autonomous merge MAY WRITE, and a second place to
declare it is a second place to widen a path grant. Reading a position is not
granting a path.

#### Scenario: An unfenced proposal declares its parent as a header line
- **WHEN** a proposal carries no `---` front matter and writes `sequenced_after:` with a flow sequence at column 0 within the lifecycle header window
- **THEN** the declaration is read, and it is the same declaration the fenced form would have made
- **AND** it is validated, resolved, cycle-checked and freeze-checked by exactly the machinery the fenced form goes through

#### Scenario: The same bytes appear beyond the header window
- **WHEN** a `sequenced_after:` line sits below the lifecycle header window, or is indented, or appears inside a body paragraph
- **THEN** it MUST declare nothing, because beyond the window it is prose and a mention is not a parent link

#### Scenario: An unfenced declaration attempts a multi-line value
- **WHEN** a header line carries no value on its own line and the next line is an indented continuation
- **THEN** the reader MUST refuse it by name and name the forms that work, because an unfenced document supplies no closing delimiter for the value

#### Scenario: The path-scope declaration is written as a header line
- **WHEN** an unfenced proposal writes `scope_globs:` as a header line
- **THEN** no path scope is declared, because the equivalence is granted to the parent declaration alone

### Requirement: One parent declaration across both sites, and its retention
A change SHALL carry AT MOST ONE `sequenced_after:` value however many sites it
writes it in, and a reader that finds the field at both sites SHALL treat equal
declarations as ONE declaration and SHALL REFUSE unequal ones rather than prefer
either site. Equality is decided under the SAME canonical form the archive
retention gate compares with, so entry ORDER is significant and a
self-qualified entry equals its bare form. A reader that preferred one site
would show a reviewer the other — the show-one-authorize-another defect the
strict loader's duplicate-key refusal already closes, one file apart rather than
one key apart — and the refusal SHALL name both values so the author can delete
the one that is not true. Two header lines for the same field SHALL be refused
as the duplicate key they are.

READING A NEW DECLARATION SITE SHALL NOT LICENSE WRITING INTO IT AFTER
RATIFICATION. Admitting the header-line form changes what a reader can SEE; it
changes nothing about what a ratified proposal may CARRY. Where a change's
declaration is ABSENT at its ratified head and present in the working tree —
whether because a header line was added, or because an existing line was MOVED
from beyond the window to inside it — the archive retention gate SHALL report a
contested-class mutation requiring an explicit recorded disposition, exactly as
it does for the fenced form. A declaration that was already present at the
ratified head SHALL be read as RETAINED, because both sides of the comparison
are read by the same reader; making an existing declaration legible is not a
mutation of it.

#### Scenario: Both sites carry the same declaration
- **WHEN** a proposal declares `sequenced_after:` in its front matter and again as a header line, and the two are equal under the canonical form
- **THEN** it is ONE declaration and validation proceeds

#### Scenario: The two sites disagree
- **WHEN** a proposal's front-matter declaration and header-line declaration differ — including the case where one is the empty root claim and the other names a parent
- **THEN** the reader MUST refuse, naming both values
- **AND** it MUST NOT resolve the disagreement by preferring a site

#### Scenario: A header-line declaration is added after ratification
- **WHEN** a ratified change's proposal gains a `sequenced_after:` header line, or an existing one is moved into the header window, after its ratified head
- **THEN** the archive retention gate MUST report a contested-class mutation requiring an explicit recorded disposition
- **AND** a declaration already present at the ratified head MUST read as retained rather than as a mutation
