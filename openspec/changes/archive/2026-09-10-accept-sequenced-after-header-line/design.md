# Design: accept-sequenced-after-header-line

## 0. CONVENER BRIEF — what is being asked, and the two things that need you

1. **What.** One reader change and two ADDED requirements: a `sequenced_after:`
   line inside the bounded LIFECYCLE HEADER WINDOW declares exactly what the
   front-matter key declares. Same strict loader, same shape, same grammar,
   same resolution, same cycle rule, same freeze.
2. **Why.** Your ruling of 2026-09-10 ~02:10Z, verbatim **"do door b"**, on
   codexFactory issue #268. Door (b) is "openxFactory teaches the reader the
   unfenced header form"; door (a) was "fence the whole codexFactory corpus".
3. **The defect, measured.** codexFactory main `2ade133`: 49 of 50 proposals
   are unfenced, EIGHT carry a `sequenced_after:` header line, and the shipped
   reader reports `declaring = 0`. Eight honest declarations read as eight
   changes that declared nothing.
4. **What door (b) buys over door (a), demonstrated.** Fencing turns `ABSENT`
   into a declaration on ratified packets — the contested-class retention
   mutation. Changing the READER reads both sides of that comparison the same
   way: all three admitted carriers report **RETAINED**, none contested.
5. **The bound is the substance.** Beyond the fifteen-line window the same bytes
   are PROSE and declare nothing. Fifteen is not chosen here — it is
   `doc_health.corpus.STATUS_SCAN_LINES`, the window this corpus already reads
   `Status:` in, and an agreement test fails if the two drift.
6. **THE FIRST THING THAT NEEDS YOU — a ratified sentence is narrowed.**
   `add-sequenced-after-substrate`'s ADDED requirement says a "prose
   `Sequenced-after:` header … SHALL NOT constitute a machine-readable parent
   declaration", for three reasons. `proposal.md` § The ratified sentence this
   change narrows quotes it in full and answers each reason. The reading is this
   lane's; whether it holds is yours. **If you refuse the narrowing, this packet
   dies and door (a) is the remaining door.**
7. **THE SECOND THING THAT NEEDS YOU (OQ-H1) — three of eight, not eight of
   eight.** The window admits the carriers at lines 5, 10 and 11 and leaves five
   at lines 20–38 unread. Recommendation: LEAVE THE BOUND; the five are
   codexFactory's to move, under the same explicit retention disposition door
   (a) would have needed.
8. **OQ-H2 needs no ruling unless you disagree.** `scope_globs:` is NOT taught
   the header-line form: making a POSITION declaration legible authorizes
   nothing, while making a PATH GRANT declarable in a second place widens where
   a grant can be written.
9. **Blast radius here.** Zero for this repository, measured: openxFactory
   fences, carries no unfenced carrier, and its 372-file fenced-block reading is
   byte-identical before and after the shared line-rule conversion.
10. **What ratification authorizes.** The realization is ALREADY IN THIS PULL
    REQUEST (§ 3 of `tasks.md` is ticked), because the change is a reader edit
    whose proof is its suite. Ratification is what makes the two requirements
    doctrine; nothing merges itself and nothing in codexFactory moves.

## Context

- **The ruling.** Brett Heap, first-hand, in session, 2026-09-10 ~02:10Z,
  verbatim **"do door b"**, on codexFactory issue
  [#268](https://github.com/codeXfactory/codexFactory/issues/268). The doors
  were framed in that issue's own last comment, which also stated that the
  choice needed his word "because E-8 is ratified and this reverses its
  recommendation" — so the ruling was given over a known ratified conflict in
  the CONSUMING repository. A SECOND ratified sentence, in THIS repository, was
  not in front of him; it is § The ratified sentence this change narrows.
- **Parent (ratified 2026-09-01, ACTIVE, REALIZED).** `add-sequenced-after-substrate`
  authored the field, the strict loader, the validator, the archive-retention
  gate and the corpus sweep, and its Groups 2–5 are ticked — so
  `scripts/frontmatter_strict.py` and `scripts/sequenced_after.py` are that
  packet's SHIPPED CODE. Editing shipped code is realization; editing its
  `proposal.md`, `design.md`, `specs/` or `.openspec.yaml` would be editing
  ratified text, and this change does none of that.
- **The consuming repository.** codexFactory vendors both modules byte-for-byte
  into `scripts/merge_master/`, pinned by recorded `sha256` plus source-equality
  at `stack.yaml`'s `contract_ref`. Its re-vendor is a successor act.

## Decisions

### H-1 — The vehicle is a NEW CHANGE with an ALL-ADDED delta, sequenced after the substrate
Three vehicles were available and two are unavailable in fact, not in taste.
**Editing the substrate's ratified text** is refused outright: a ratified
packet's `proposal.md`, `design.md`, `specs/` and `.openspec.yaml` are frozen,
and post-ratification notes belong in the change that owns them. **A `##
MODIFIED Requirements` block over the substrate's "Machine-readable ordered-delta
parent declaration"** is IMPOSSIBLE, checked rather than assumed: a MODIFIED
delta must target a requirement PROMOTED in `openspec/specs/`, and the
substrate's nine requirements are not promoted until it archives — `grep -n
"Machine-readable ordered-delta parent declaration"
openspec/specs/release-realization/spec.md` returns nothing (exit 1) on
2026-09-10. What remains is a NEW change with an ALL-ADDED delta over NOVEL
titles, declaring the substrate as its `sequenced_after:` parent — which is the
substrate's OWN mechanism, used by its first successor, on the substrate itself.

### H-2 — The window is `doc_health.corpus.STATUS_SCAN_LINES`, restated rather than invented
The header-line reader needs a bound, and the bound must not be a number this
change picked. Fifteen REAL lines is the window `parse_status` and `parse_kind`
already apply to the SAME document set, so a document's header is one region
rather than one region per reader: `Status:` and `sequenced_after:` are found or
missed together. The number is RESTATED in `frontmatter_strict.py` rather than
imported, because that file is vendored into a repository with no `doc_health`
package and an import would break the vendored copy at load time. **THE PROMOTED RULE IS FOLLOWED BY ANALOGY, AND THE ANALOGY IS DECLARED RATHER
THAN ASSUMED.** `doc-health`'s promoted requirement "The deterministic pass reads
a document's lifecycle header by real lines" binds EVERY READER OF THAT HEADER —
this one included — and says the rule "SHALL be shared with the writers of the
same header rather than reimplemented per reader. Where the corpus cannot share
an implementation across language boundaries, the divergence SHALL be held by an
explicit agreement test rather than by convention"
(`openspec/specs/doc-health/spec.md`, promoted by the archived
`align-status-reader-to-real-lines`). The escape clause names a LANGUAGE
boundary; the boundary here is a VENDORING boundary, and this change takes the
same remedy for the same reason — an import that cannot exist in the vendored
copy is as unavailable as one that cannot cross a language. That extension is
this lane's reading and is flagged here for the convener rather than buried in a
docstring: two tests assert `HEADER_WINDOW_LINES == STATUS_SCAN_LINES` and that
`split_real_lines` agrees with `doc_health.lines.split_keepends` over the corpus
and over exotic-separator fixtures. A drift is a test failure, not a convention
nobody re-checks.

### H-3 — REAL lines, not `str.splitlines()`
`str.splitlines()` also breaks on `\x0b`, `\x0c`, `\x1c`–`\x1e`, `\x85`, U+2028
and U+2029, so a document carrying one of those has its fifteen-line window
counted in FRAGMENTS and a header the writer plainly wrote can go unfound. A
reader that splits more aggressively than the writer reports a document as
lacking a declaration it carries — a FALSE finding, which costs more trust than
a crash. `fenced_lines` is converted to the same rule so the fence span and the
header window agree about where a document's lines are; the conversion was
MEASURED BEFORE IT WAS MADE over all 372 `proposal.md` files in the openxFactory
and codexFactory clones (241 real corpus + 131 fixtures) and returns an
IDENTICAL fenced block for every one.

### H-4 — `scope_globs:` is NOT taught the header-line form, and the asymmetry is the decision
`sequenced_after:` declares WHERE IN A CHAIN a change sits; its consumer applies
its own root proof, its own co-modifier cross-check and its own refusals on top,
so making an author's existing declaration legible authorizes nothing that
absence did not already refuse — the change is from "fail-closed on a
declaration nobody can read" to "read, then judged by the same gates".
`scope_globs:` declares WHICH PATHS an autonomous merge MAY WRITE. A new place to
declare it is a new place to WIDEN A PATH GRANT, and widening a grant surface is
a different act from making a position legible. The parent's ruled OQ-1 argued
ONE LOADER over the whole block, and that ruling is honoured: both fields are
still read by ONE strict loader. One loader over both fields is not the same
claim as one DECLARATION SITE SET for both fields. Held as **OQ-H2**.

### H-5 — Both sites present is ONE declaration or a REFUSAL, never a preference
A reader that preferred one site would show a reviewer the other. That is the
show-one-authorize-another defect the strict loader's duplicate-key refusal
exists to close, one file apart rather than one key apart. So: equal under the
canonical form — the SAME `_canonical` the retention gate compares with, so entry
ORDER is significant and a self-qualified entry equals its bare form — is ONE
declaration; different is REFUSED with both values named. Two header lines for
one field are handed to `strict_load` TOGETHER, so the refusal is the loader's
own duplicate-key message and no second rule is written.
ONE FAIL-CLOSED EDGE IS NAMED RATHER THAN HIDDEN: the canonical comparison
resolves a self-qualified entry against `DECLARING_REPOSITORY`, which in a
VENDORED copy still reads `openxFactory`. In that copy a proposal spelling one
site `codexFactory:parent` and the other `parent` REFUSES rather than resolving.
That is fail-closed and the remedy is to spell both sites alike; a change that
made the constant configurable would touch the retention gate's comparison too
and is not taken here.

### H-6 — The declaration is ONE LINE, because an unfenced document has no closing delimiter
A fence supplies an end; an unfenced document supplies none, so a multi-line
value's END is undefined and a window boundary falling inside it would show a
reviewer three parents and authorize two. A flow value (`field: [a, b]`) is
self-delimiting ON ITS LINE and is therefore the only unfenced form admitted. A
`field:` line whose value is EMPTY and whose next line is an INDENTED
continuation is a block-sequence attempt and is REFUSED BY NAME rather than read
as null — the author of those bytes declared parents and is owed the reason the
reader will not take them, and the message names the two forms that work.

### H-7 — Reading a new site licenses no writing into it
The retention gate is unchanged and reaches the new site through
`read_declaration`, so adding a header line to an already-ratified proposal
registers as `ABSENT -> declared`, and MOVING an existing line from outside the
window to inside it registers as `ABSENT -> declared` too. Both are
contested-class findings needing an explicit recorded disposition. This is
stated as a requirement rather than left to the code, so door (b) cannot be read
as door (a) by the back entrance: the thing door (b) avoids is not "a
disposition" but "a disposition owed for bytes nobody needed to move".

## Risks / trade-offs

- **Three of eight, not eight of eight.** The bound leaves five codexFactory
  declarations unread. Accepted and reported by name and line number (OQ-H1);
  the alternative — a window sized to fit five documents — makes the window a
  measurement rather than a rule.
- **A ratified sentence is narrowed.** The largest risk in the packet, held as
  the convener's first read rather than resolved by the author.
- **One front-matter block now has two declaration sites for one of its two
  fields.** Accepted (H-4), and the asymmetry is asserted by a test rather than
  left to a reader's trust.
- **A vendored copy's `DECLARING_REPOSITORY` makes one cross-site spelling
  equivalence fail closed** (H-5). Accepted: fail-closed, named, and cheap to
  avoid.
- **Every `read_declaration` call now does a second scan of the first fifteen
  lines.** Accepted: the scan is bounded by construction, and `corpus_sweep`
  over 191 proposals plus chain walks completes well inside the suite's existing
  budget.

## Open questions (for the convener ratification read, § 0 of `tasks.md`)

1. **OQ-H1 — the five carriers beyond the window** (lines 20, 24, 33, 36, 38).
   Widen the window, or leave the bound? **Recommendation: LEAVE THE BOUND.**
2. **OQ-H2 — `scope_globs:` and the header-line form.** Left out (H-4). Confirm,
   or rule for one declaration-site set across the whole block?
   **Recommendation: LEAVE IT OUT.**
