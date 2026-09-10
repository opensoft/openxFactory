# release-realization Specification Delta

**ONE `## MODIFIED` REQUIREMENT, AND IT IS A PURE ADDITION.** The block below
is written OVER CANON — `openspec/specs/release-realization/spec.md` as
`main` states it — targeting the requirement `accept-sequenced-after-header-line`
promoted at its own archive (PR #906): "Equivalent declaration sites for the
ordered-delta parent declaration." Measured 2026-09-10 over every active
change directory: no other active change carries a `release-realization`
delta at all
(`find openspec/changes -maxdepth 3 -path "*/specs/release-realization/*" -not -path "*/archive/*"`
returns nothing), and no OTHER open pull request touches `release-realization`
or `frontmatter_strict`
(`gh pr list -R opensoft/openxFactory --state open --json number,title,files --jq '.[] | select(.files[].path | test("release-realization|frontmatter_strict"))'`,
checked before this pull request was filed, returns nothing — this pull
request itself necessarily touches `release-realization` and is excluded by
construction). No
ACTIVE change collides with this delta, so `modified-block-currency`'s
two-writers ordering rule owes no `Modified over` marker in either
direction. (The per-change sweep ledger's own `class` field reads
`co-modifier` rather than `sole` for this change's row, because it shares
its requirement key with `accept-sequenced-after-header-line`'s own
ARCHIVED `## ADDED Requirements` block — the ledger's documented
partner-flip mechanic, not an active-change collision.)

**WHAT MOVES: ONE BODY PARAGRAPH ADDED, ONE SCENARIO ADDED. EVERY EXISTING
SENTENCE, BULLET AND SCENARIO OF THE REQUIREMENT IS CANON'S OWN, CARRIED
VERBATIM.** The requirement already states that a header-line declaration
sits within the bounded lifecycle header window and outside any leading
`---` fence, and that a fence's lines are not counted a SECOND TIME as
header lines of the same document. It does not state whether those same
fence lines still occupy part of the window's fixed line BUDGET, or whether
the window starts counting fresh once the fence closes. `scripts/frontmatter_strict.py`
already answers this in code (`read_header_line`, whose window arithmetic
counts from the document's own line 1 regardless of where a fence closes)
and in its own docstring ("FENCE LINES ARE SKIPPED BUT STILL COUNT toward
the window"); the archived packet's own `tasks.md` § 2.3 states the same
design choice in words. This delta moves that fact from an implementation
docstring and a task record into the requirement itself, so a reader
implementing the rule from the promoted spec alone reaches the same answer
the shipped reader already gives. Because nothing existing is reworded,
reordered or removed, this delta owes no `Removed from canon by` marker and
no `Merged into` marker: those markers declare a deletion, and none is made
here.

**WHAT IS DELIBERATELY NOT TOUCHED.** No other requirement of this
capability is modified, added, renamed or removed — in particular the
sibling requirement this same archived packet promoted, "One parent
declaration across both sites, and its retention," is untouched and is not
restated here. No number is written into the requirement text: neither the
existing prose nor this addition states "fifteen" or any other literal —
the window is referred to by what it is ("the same window … that this
corpus already reads a document's `Status:` header in"), exactly as the
promoted `doc-health` real-lines requirement does for the same window, so
this delta follows the capability's own convention rather than hardcoding a
number the code holds equal to `doc_health.corpus.STATUS_SCAN_LINES` by an
agreement test rather than by a spec literal.

## MODIFIED Requirements

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

A LEADING FENCE'S OWN LINES COUNT TOWARD THE WINDOW'S BUDGET, AND DO NOT BUY IT
A FRESH ONE. The window is counted from the document's own line 1: the `---`
that opens a leading fence, every line between it and the closing `---`, and
the closing `---` itself are REAL LINES of the document like any other and
SHALL be counted among the window's lines exactly as any other line is, even
though those same lines — already read once by the front-matter reader — are
excluded from being read AGAIN as a header-line declaration site. The window
SHALL NOT be re-measured as though it began fresh after the fence closes: a
header-line declaration MUST sit within the window counted from line 1
inclusive of the fence, so a fence occupying part of the window leaves
correspondingly FEWER lines available inside it for a header-line declaration,
and one long enough MAY leave none at all.

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

#### Scenario: Fence lines consume the header window budget
- **WHEN** a proposal opens with a well-formed `---`-fenced front-matter block, and a `sequenced_after:` header line follows the closing fence
- **THEN** the window is still counted from the document's own line 1, so the fence's lines — both `---` delimiters and every line between them — count toward it rather than being excluded from the count
- **AND** a header line that the fence's length pushes past the window's last line is NOT read, exactly as a header line beyond the window is not read in an unfenced document

#### Scenario: An unfenced declaration attempts a multi-line value
- **WHEN** a header line carries no value on its own line and the next line is an indented continuation
- **THEN** the reader MUST refuse it by name and name the forms that work, because an unfenced document supplies no closing delimiter for the value

#### Scenario: The path-scope declaration is written as a header line
- **WHEN** an unfenced proposal writes `scope_globs:` as a header line
- **THEN** no path scope is declared, because the equivalence is granted to the parent declaration alone
