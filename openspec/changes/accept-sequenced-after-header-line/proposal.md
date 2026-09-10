---
code_surface: openxFactory — the READER, and nothing else. `scripts/frontmatter_strict.py` gains a bounded lifecycle-header-window reader (`split_real_lines`, `fence_span`, `HEADER_WINDOW_LINES`, `read_header_line`, the `NO_HEADER_LINE` sentinel) beside the fenced reader it already owns; `scripts/sequenced_after.py` routes `read_declaration` through BOTH sites and refuses a disagreeing pair; `tests/sequenced_after/test_header_line.py` is added. NOT THIS CHANGE'S SURFACE, each for a stated reason: `scripts/scope_globs.py` is UNTOUCHED, because a new place to declare a PATH GRANT is a new place to widen one (design H-4); `scripts/validate-sequenced-after.py`, the archive-retention gate and the corpus sweep are unedited, because they call `read_declaration` and inherit the new site without a line moving; NO `openspec/changes/**/proposal.md` byte moves in this repository or any other, which is door (b)'s whole point; and NOTHING in codexFactory is touched — its re-vendor and pin advance are a successor act (tasks § 4).
target_release: implemented (the affected repository's main line — openxFactory). Realization = the header-line form is read, validated, resolved, cycle-checked and freeze-checked by exactly the machinery the fenced form already goes through, proved by a green suite. Under `release-realization` a non-empty code surface archives on merged-plus-green realization evidence rather than on landing; the realization is IN THIS PULL REQUEST, so the evidence is this pull request's suite plus the BEFORE/AFTER corpus measurement quoted in § The measurement. No contract bundle is cut, no digest set moves, and no tag is owed.
sequenced_after: [add-sequenced-after-substrate]
---

# Proposal: accept-sequenced-after-header-line

Status: ratified
Ratified: 2026-09-10, Brett Heap (repository owner), first-hand, in session,
to lane codexfactory-1, verbatim **"ratify 886, 0.2 as narrowed, 0.3 pure
moves"**, over head `f36d2bc2` — record
`review/ratification-2026-09-10.md`.
Authored: 2026-09-10, lane codexfactory-1, on Brett Heap's ruling "do door b"
(chose the door, did not ratify this text).
Directed by: Brett Heap's ruling of 2026-09-10 ~02:10Z, first-hand and in
session, verbatim **"do door b"**, on codexFactory issue
[#268](https://github.com/codeXfactory/codexFactory/issues/268) — door (b) being
"openxFactory teaches the reader codexFactory's unfenced header form", as
against door (a) "fence the whole corpus". The derivation and its limits are
recorded verbatim in `.openspec.yaml` `origin.approved_by`: **that field records
a DERIVED AUTHORIZATION TO AUTHOR and is not ratification of any content.**
Authoring method: hand-authored per openxFactory OpenSpec conventions, mirroring
the parent packet `add-sequenced-after-substrate`. The `opsx:propose`
alignment-review + council-debate flow was NOT run; the decisions it would have
challenged are enumerated as H-1 … H-7 in `design.md` § Decisions and are
flagged for veto, and the two questions it would have surfaced are carried as
OQ-H1 and OQ-H2 with recommendations and no decisions.

> **THE ONE THING TO READ FIRST** is § The ratified sentence this change
> narrows. This packet asks to narrow a sentence in a RATIFIED sibling's spec
> delta. The sentence is quoted there in full, with the three reasons it gives
> and what this change does about each. If that narrowing is refused, nothing
> else in this packet survives.

## Why

**Eight declarations exist that the reader cannot see, and the count is
measured rather than argued.** codexFactory writes its lifecycle headers
UNFENCED. Measured 2026-09-10 on codexFactory main `2ade133`: **49 of its 50
proposals carry no `---` front matter** (the one that does is an archived 2026-08
packet), **EIGHT proposals carry a `sequenced_after:` header line** their authors
wrote deliberately, and `sequenced_after.corpus_sweep` over that corpus through
the reader openxFactory ships at `origin/main` `539cb563` reports:

```
declaring `sequenced_after:`: 0
DEEPEST DECLARED CHAIN RESOLVED: 0 hop(s)
```

A field that its authors declare and its reader cannot read is not an optional
field; it is a field with a **silent** failure mode. The parent packet's own
doctrine is that ABSENCE IS FAIL-CLOSED AND IS NOT A ROOT CLAIM — so eight
honest declarations currently read as eight changes that declared NOTHING, which
is the exact state the substrate designed absence to mean.

**The two doors were put to Brett Heap and he named one.** codexFactory #268
recorded them: **(a)** fence the whole codexFactory corpus, or **(b)** teach the
openxFactory reader the unfenced header form, then re-vendor and advance the
pin. Brett Heap ruled 2026-09-10 ~02:10Z, first-hand and in session, verbatim
**"do door b"**.

**Door (a) moves ratified bytes; door (b) moves none, and that difference is
demonstrable rather than rhetorical.** Fencing turns a proposal's declaration
from what the reader calls `ABSENT` into a declaration — and where the packet is
already RATIFIED, `sequenced_after.retention_problem` reports exactly that as
*"mutated after ratification … a contested-class act requiring an explicit
disposition"*. Door (b) changes the READER, so BOTH SIDES of the retention
comparison are read by the same reader, and a declaration that was already in
the ratified text reads as retained. Run against each carrier's own ratified
head, through this change's reader (§ The measurement): **all three declaring
carriers report RETAINED, none contested.**

## What Changes

TWO ADDED requirements on `release-realization`, and no MODIFIED block.

- **A `sequenced_after:` line inside the bounded LIFECYCLE HEADER WINDOW
  declares equivalently to the front-matter key.** The window is the first
  fifteen REAL lines of the document — the same window and the same line rule
  `doc_health.corpus.parse_status` already applies to the same document set — so
  `Status:` and `sequenced_after:` are found or missed together and no reader
  holds a private idea of where a document's header ends.

- **BEYOND THE WINDOW THE SAME BYTES ARE PROSE AND DECLARE NOTHING.** That bound
  is what front matter was chosen FOR. The alternative this change does NOT take
  is unbounded prose parsing, where a `sequenced_after:` written in a body
  paragraph on line 400 would authorize as loudly as one written in a header —
  and the parent capability's own text already refuses a mention as a parent
  link.

- **The legacy prose `Sequenced-after:` header keeps the non-declaring standing
  the ratified sibling gave it.** The admitted spelling is the FIELD'S OWN NAME,
  `sequenced_after:`, at column 0, case-sensitive. `Sequenced-after:` — three
  archived openxFactory proposals carry it, with prose after the ids — still
  declares nothing, and `sequenced_after.PROSE_HEADER` still counts it as the
  free-text header it is.

- **ONE FIELD HAS ONE VALUE ACROSS BOTH SITES.** Both present and EQUAL is ONE
  declaration, compared under the same canonical form the retention gate uses.
  Both present and DIFFERENT is REFUSED: a reader that preferred either site
  would show a reviewer the other, which is the show-one-authorize-another
  defect the strict loader's duplicate-key refusal already closes, one file
  apart. Two header lines for one field are refused as the duplicate key they
  are, by the loader's own message.

- **A DECLARATION ABSENT AT THE RATIFIED HEAD IS A CONTESTED-CLASS FINDING.**
  Reading a new site does not license writing into it after ratification.
  Adding a header line to an already-ratified proposal, and MOVING an existing
  one from outside the window to inside it, both register at the retention gate
  and both need an explicit recorded disposition. This is the parent's
  "Parent-declaration retention at archive" requirement applied to the site this
  change adds, stated so that door (b) cannot be read as door (a) by the back
  entrance.

- **`scope_globs:` IS DELIBERATELY NOT TAUGHT THE FORM** (design H-4). It
  authorizes WHICH PATHS an autonomous merge may write, so a new place to
  declare it is a new place to widen a path grant. `sequenced_after:` declares
  WHERE IN A CHAIN a change sits, and its consumer applies its own root proof,
  co-modifier cross-check and refusals on top — so making an author's existing
  declaration legible authorizes nothing that absence did not already refuse.
  The asymmetry is asserted by a test, not left to trust.

## The ratified sentence this change narrows

**A ratified sibling says something adjacent to this, and it is quoted in full
rather than paraphrased.** `add-sequenced-after-substrate` (RATIFIED 2026-09-01,
Brett Heap, ACTIVE) writes, inside its ADDED requirement "Machine-readable
ordered-delta parent declaration":

> A prose `Sequenced-after:` header, a whole-token occurrence of a sibling
> change id anywhere in a proposal's text, a change-folder name, a commit
> timestamp, and a `created:` date SHALL NOT constitute a machine-readable
> parent declaration: none of them can distinguish a parent from a mention, none
> can express a fork, and each is author-mutable in the same document the author
> writes.

**Read against what this change admits, the sentence and this packet are
compatible, and the compatibility is worked rather than asserted.** The sentence
refuses a list of INFERENTIAL signals and gives three reasons. Taking them one
at a time against the form admitted here:

| the sentence's reason | the admitted header-line form |
| --- | --- |
| "cannot distinguish a parent from a mention" | it can: the declaration is the FIELD'S OWN NAME at column 0 inside a bounded fifteen-line window, and every other occurrence — a body paragraph, an indented line, a line beyond the window — declares NOTHING. Four negative tests hold that boundary |
| "cannot express a fork" | it can: the value is loaded by the SAME strict loader, under the SAME sequence shape and the SAME entry grammar, so `sequenced_after: [a, b]` is a two-parent declaration on this path exactly as in front matter |
| "author-mutable in the same document the author writes" | equally true of the front-matter form, and mitigated identically rather than differently: the declaration is base-read, ratification-covered, non-author-mutable and FROZEN AFTER RATIFICATION. `proposal.md` front matter is not a separate file from `proposal.md` |

**Two further readings of the record point the same way, and neither is a
loophole.** The refused spelling in the sibling's design is the LEGACY
`Sequenced-after:` — its own § S1 table names it "free text no schema
validates", measured at "3 occurrences, all in ARCHIVED proposals" — and that
spelling is still refused here, by name and by test. And the sibling's Impact
records that "the three archived prose `Sequenced-after:` headers … are all
untouched in contract": it DECLINED TO GIVE THE FORM MEANING; it did not forbid
a later change from giving a DIFFERENT, VALIDATED form one.

**None of that is a licence to proceed without a ruling, so it is not taken as
one.** The sentence is ratified text, the reading above is this lane's, and
whether it holds is Brett Heap's to say. What this packet does NOT do is edit
it: the sibling is ratified and ACTIVE, its requirement is NOT promoted in
`openspec/specs/release-realization/spec.md` (checked 2026-09-10: `grep` for the
title returns nothing, exit 1), so a `## MODIFIED Requirements` block over it is
not available and would be improper if it were. This delta is ALL-ADDED over two
NOVEL titles, and the two requirements are written to be read TOGETHER with the
sibling's, in the ordered-delta relation this change declares in its own front
matter.

## This change is an ordered delta on the substrate, and it says so

`accept-sequenced-after-header-line` declares
`sequenced_after: [add-sequenced-after-substrate]` in its own front matter,
above. It genuinely IS an ordered delta on that change: it extends that change's
field, edits that change's shipped reader, and narrows one sentence of that
change's requirement text. Declaring the parent is the substrate's own doctrine
applied to its first successor — declaring must never be worth less than
omitting — and the entry resolves to exactly one active change directory,
breaks no grammar rule and closes no cycle, which this repository's own
`scripts/validate-sequenced-after.py` proves on every pull request.

## The measurement

**BEFORE** — `sequenced_after.corpus_sweep` from openxFactory `origin/main`
`539cb563`, over codexFactory main `2ade133`:

```
change ids (19 active + 31 archived): 50
declaring `sequenced_after:`: 0
DEEPEST DECLARED CHAIN RESOLVED: 0 hop(s)
```

**AFTER** — the same sweep, same corpus, this branch's reader:

```
change ids (19 active + 31 archived): 50
declaring `sequenced_after:`: 3 (add-floor-regeneration-automation,
                                 amend-floor-regeneration-predicate,
                                 extend-merge-master-envelope-to-floor-bot-lanes)
DEEPEST DECLARED CHAIN RESOLVED: 2 hop(s), from amend-floor-regeneration-predicate
```

**THREE OF EIGHT, AND THE OTHER FIVE ARE REPORTED RATHER THAN QUIETLY DROPPED.**
The eight carriers #268 lists sit at these REAL line numbers in codexFactory
main; the window admits the first three and the same bytes below it are prose:

| line | proposal | admitted? |
| --- | --- | --- |
| 5 | `extend-merge-master-envelope-to-floor-bot-lanes` | YES |
| 10 | `amend-floor-regeneration-predicate` | YES |
| 11 | `add-floor-regeneration-automation` | YES |
| 20 | `archive/2026-09-05-add-floor-addition-grace` | no — beyond the window |
| 24 | `amend-floor-regeneration-merge-authority` | no — beyond the window |
| 33 | `relocate-review-authority-floor` | no — beyond the window |
| 36 | `admit-hosted-artifact-to-contract-manifest` | no — beyond the window |
| 38 | `add-mcp-transport-adapters` | no — beyond the window |

The five are the honest cost of the bound, and the bound is the requirement's
substance rather than an implementation detail. **They are NOT repaired here by
widening the window**, because a window is what separates a declaration from
prose and a number chosen to fit five documents is not a bound. They are carried
as **OQ-H1** for the convener with a recommendation, and the remedy either way
is codexFactory's: moving a declaration INTO the window is itself a
retention-gate mutation on a ratified packet, needing the same explicit
disposition door (a) needed, which is precisely why it is not done quietly.

**THE FREEZE IS UNTRIPPED, AND THAT IS DOOR (b)'S CENTRAL CLAIM.**
`retention_at_archive` run through this branch's reader against each declaring
carrier's own ratified head:

```
add-floor-regeneration-automation (ratified head c551e281)
  ratified-ref read = ['add-floor-addition-grace']
  working-tree read = ['add-floor-addition-grace']            -> RETAINED
amend-floor-regeneration-predicate (ratified head efeebd6)
  ratified-ref read = ['add-floor-regeneration-automation']
  working-tree read = ['add-floor-regeneration-automation']   -> RETAINED
extend-merge-master-envelope-to-floor-bot-lanes (ratified head 8f601982)
  ratified-ref read = ['add-regular-pr-council-clearance',
                       'add-floor-regeneration-automation']
  working-tree read = ['add-regular-pr-council-clearance',
                       'add-floor-regeneration-automation']   -> RETAINED
```

**AND #268'S OWN "TWO LATE-ADDED CARRIERS" READING IS CORRECTED BY THIS
MEASUREMENT.** That issue reported `add-floor-regeneration-automation` and
`add-mcp-transport-adapters` as ABSENT at their ratified heads and therefore
contested — but that reading was taken THROUGH THE FENCE-ONLY READER, which
returns `ABSENT` for an unfenced header line on BOTH sides. Read through the
reader this change builds, the first carrier's declaration was already present
at head `c551e281` and is RETAINED; the second sits at line 38, outside the
window, and declares nothing at all, so no retention question arises for it.
Under door (a) both would have been contested; under door (b) neither is.

**THIS REPOSITORY'S OWN CORPUS DOES NOT MOVE.** openxFactory fences its
proposals, carries ZERO unfenced `sequenced_after:` header lines (asserted by
`test_no_openxFactory_proposal_gains_or_loses_a_declaration`, which enumerates
the corpus rather than trusting the claim), and
`python3 scripts/validate-sequenced-after.py` passes on this branch: *"39 active
changes, 9 declaring the field"*, exit 0. And the one-line-rule conversion inside
`fenced_lines` was measured BEFORE it was made: over all 372 `proposal.md` files
in both clones (241 real corpus + 131 test fixtures), `text.splitlines()` and
`split_real_lines` return an IDENTICAL fenced block for every one, so the shared
line rule costs a zero baseline diff.

## Impact

- **Affected spec:** `release-realization` — TWO ADDED requirements, seven
  scenarios; NOTHING MODIFIED and nothing removed. Titles: "Equivalent
  declaration sites for the ordered-delta parent declaration"; "One parent
  declaration across both sites, and its retention". Both titles are NOVEL —
  checked 2026-09-10 against the eight promoted `release-realization`
  requirements and against every requirement title in the five ACTIVE deltas on
  this capability, so no `Modified over`, `Removed from canon by` or `Merged
  into` marker is owed and no sibling's archive-order hold is incurred.

- **Affected code:** `scripts/frontmatter_strict.py`, `scripts/sequenced_after.py`
  and `tests/sequenced_after/test_header_line.py` — the parent packet's SHIPPED
  CODE, which is realization and not ratified text. No `openspec/` packet byte
  belonging to another change is edited by this one.

- **Backward-compat: no flag-day, no migration, and a zero-diff corpus here.**
  Every existing openxFactory change keeps validating and archiving unchanged;
  the fenced form is unchanged in contract and in behaviour; `scope_globs:` is
  untouched; `PROSE_HEADER` and its count are untouched. The corpus that moves is
  codexFactory's, and it moves at ITS re-pin, not at this landing.

- **Interactions.** `scripts/validate-sequenced-after.py`, the archive-retention
  gate, `corpus_sweep` and `classify_corpus` all reach the new site through
  `read_declaration` with no line moved: an unfenced declaration is validated,
  resolved, cycle-checked, swept and freeze-checked by exactly the machinery the
  fenced form goes through. doc-health's `modified-block-currency` whole-token
  ordering reader is UNTOUCHED, as the parent's ruled OQ-3 left it.

- **Consumers owe a re-vendor, and it is a THREE-FILE-IN-ONE-COMMIT act.**
  codexFactory vendors `scripts/frontmatter_strict.py` and
  `scripts/sequenced_after.py` byte-for-byte under `scripts/merge_master/`,
  pinned by recorded `sha256` PLUS source-equality at `stack.yaml`'s
  `contract_ref`. Advancing `contract_ref` past this change WITHOUT re-copying
  both files reds
  `test_the_vendored_bytes_equal_the_source_at_the_pinned_contract_version`
  BY DESIGN. Tracked unticked in `tasks.md` § 4, owned by lane codeXfactory-1.

## Open questions

- **OQ-H1 — the five carriers beyond the window.** Five of codexFactory's eight
  header-line declarations sit at lines 20–38 and stay unread. Widen the window,
  or leave the bound and let codexFactory move those lines under an explicit
  retention disposition? **Recommendation: LEAVE THE BOUND.** Fifteen is not a
  number this change chose — it is `doc_health.corpus.STATUS_SCAN_LINES`, the
  window this corpus already reads `Status:` in — and widening it to fit five
  documents would make the window a measurement of those five documents rather
  than a rule. The five are visible, named, and cheap for their own repository
  to fix in an act that is honest about being a mutation.
- **OQ-H2 — `scope_globs:` and the header-line form.** Left OUT here (H-4).
  Confirm, or rule that the block gets ONE reader for both fields as the
  parent's OQ-1 ruled for the strict loader? **Recommendation: LEAVE IT OUT.**
  Making a position declaration legible authorizes nothing; making a path grant
  declarable in a second place widens where a grant can be written. If the
  symmetry is wanted, it is its own change with its own ruling.

Ratifying this text unlocks no autonomous merge and moves no corpus by itself.
It makes a declaration its authors already wrote legible to the reader that was
built to walk it.
