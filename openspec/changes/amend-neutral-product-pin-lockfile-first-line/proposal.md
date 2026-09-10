---
code_surface: none — MEASURED, not assumed. The delta is pure requirement prose and no script, test, workflow, contract, schema or example reads the sentence it re-orders. Evidence, taken 2026-09-10 on the clone of `main` `ea34f22a` this packet was authored against: (1) `grep -rn "Where a pinned external neutral product\|the pin SHALL carry a VENDORED RESOLUTION\|VENDORED RESOLUTION" scripts/ tests/ .github/ contracts/` returns NOTHING — not one line of running code, test data, workflow or contract quotes any part of the sentence; (2) the requirement's machinery lives in `scripts/validate-openspec-cli-pin.py` (`pinned_lockfile`, `verify_lockfile`, `read_lockfile`, `staging_manifest`, `install_locked`, the `pin-lockfile-mismatch` refusal) and in `contracts/openspec-cli-pin.yaml`'s `lockfile:`/`lockfile_integrity:`/`lockfile_packages:` fields, and this block changes none of the obligations those realize — the four things the vendored resolution must be and record are the same four, in the same order, in the same words; (3) no test pins this capability's scenario count or scenario titles, and this block adds no scenario and drops none, so nothing keyed on either can move; (4) the one mechanical consumer of the delta is `doc-health`'s modified-block-currency family, which reads every active block by construction and is a GATE rather than a surface. Under `release-realization` an empty code surface archives ON LANDING plus its own task list, not on merged-plus-green realization evidence.
target_release: none — no code surface, no contract bundle, no digest set and no release tag. Nothing under `contracts/` is touched, no `contracts/releases/<tag>.digests.yaml` moves, and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on a separate word.
sequenced_after: []
---

# Proposal: amend-neutral-product-pin-lockfile-first-line

Status: ratified
Ratified: 2026-09-10 by Brett Heap (openxFactory operator authority) — "ratify as encoded"; record at review/ratification-2026-09-10.md
Proposed: 2026-09-10, in lane `openxfactory-1` (display `openXfactory-1`), on
Brett Heap's word of 2026-09-10, verbatim **"do 882 packet"**, given in session
and recorded in this lane's CLAIMED comment on openxFactory
[#882](https://github.com/opensoft/openxFactory/issues/882#issuecomment-5623510674)
at 2026-09-10T18:29:31Z.
Origin: openxFactory issue
[#882](https://github.com/opensoft/openxFactory/issues/882), filed by this lane
at the archive of `amend-neutral-product-pin-interim-copy-vocabulary` as the
named successor of that packet's `tasks.md` 5.2 and `design.md` D6.
**THAT WORD AUTHORIZED THE PROPOSING, NOT THE CONTENT; THE RATIFICATION IS A
SEPARATE ACT AND IT HAS NOW HAPPENED.** Brett Heap ruled on this packet itself
on 2026-09-10, verbatim **"ratify as encoded"** — a MULTIPLE-CHOICE ruling over
`design.md` **D6**, **D1** and **D2**, put to him with the recommendation
presented first, given in session at approximately 19:53Z and recorded on
openxFactory PR [#923](https://github.com/opensoft/openxFactory/pull/923#issuecomment-5624573662)
at 2026-09-10T19:53:02Z. **D6 IS RESOLVED AS AMEND** — the ballot's arm **A**,
which is D6's option 1 — although the pinned 1.12.0 binary does not report the
failure; **D1 IS RESOLVED AS OPTION 1**, the re-ordering of canon's own words;
and **D2 STANDS** — one `Removed from canon` marker, one name, no code span in
its reason. Every one of the three is the option this packet ALREADY ENCODED,
so **THE WORDING STANDS UNCHANGED**: not one byte of
`specs/neutral-product-pin/spec.md` moves at this ratification and nothing is
withdrawn or re-written. D0, D3, D4, D5 and D7 were carried beside them and
none was vetoed. The citation is the single `Ratified:` line above, which is
what `ratified-provenance` counts; the act is recorded at
`review/ratification-2026-09-10.md`, with the gate run re-derived on the
ratified tree beside it at `review/verification-2026-09-10.md`.
`.openspec.yaml` now carries `approved_by` + `approved_on` **ADDED BESIDE** the
drafting provenance it was authored with, `kind`, `id`, `reason` and
`proposed_by` unmoved — the addition-not-rewrite shape
`add-drafted-proposal-origin` (issue #318) defined. **NOTHING IS PROMOTED BY
THIS RATIFICATION**: this pull request still edits no file under
`openspec/specs/`, no script, no test, no contract, no schema and no workflow —
promotion happens at the ARCHIVE, which is a separate act on a separate word
that has NOT been given, so `tasks.md` § 5 stays OPEN and openxFactory #882
closes there and not at this landing.

## Why

**One requirement of `neutral-product-pin` opens its body with a condition and
defers its subject and its `SHALL` to the second line, and a reader — human or
parser — who reads one line meets a condition whose obligation has not
arrived.**

The requirement is *A pinned artifact that resolves dependencies at install time
carries a vendored lockfile, and the install runs through it*
(`openspec/specs/neutral-product-pin/spec.md:668-721`, promoted 2026-09-09). Its
first two body lines, `:669-670`:

> Where a pinned external neutral product is distributed as a published artifact
> whose installation RESOLVES dependency ranges, the pin SHALL carry a VENDORED

It is not short of obligation. `SHALL` appears EIGHT times in the block below
that line. What it lacks is the obligation on LINE ONE, and that is the shape
**seventeen of the eighteen requirements in this same file already have** —
measured, not asserted: every other requirement's first body line carries
`SHALL` or `MUST`, TEN of them inside 80 characters and SEVEN on a line of 80
characters or more (80, 156, 183, 201, 221, 284 and 397). Index 16 is the ONE
that opens with `Where …`.

**AND ON ONE OPENSPEC BINARY THAT SHAPE IS A STRICT-VALIDATION ERROR.** On the
CLI at 1.2.0:

```
$ OPENSPEC_TELEMETRY=0 openspec validate neutral-product-pin --strict --type spec
Specification 'neutral-product-pin' has issues
✗ [ERROR] requirements.16.text: Requirement must contain SHALL or MUST keyword
```

## What the pinned CLI says, which changes the case and is stated before the remedy

**THE PINNED CLI DOES NOT REPORT THIS AT ALL, AND NO REQUIRED CHECK DOES.**
`contracts/openspec-cli-pin.yaml` pins `@fission-ai/openspec@1.12.0`;
`.github/workflows/openspec-cli-pin-gate.yml:101` runs
`python3 scripts/validate-openspec-cli-pin.py --all --no-cache` through the
content-verified artifact; and on that binary this specification **PASSES**.
Measured on the same tree, 2026-09-10:

| tree | binary | result |
| --- | --- | --- |
| control `05c706d6` | 1.2.0 on `PATH` | `Totals: 97 passed, 4 failed (101 items)`, exit 1, `spec/neutral-product-pin` among the four |
| this branch | 1.2.0 on `PATH` | `Totals: 98 passed, 4 failed (102 items)`, exit 1, the SAME four, plus one passing item — this packet's change |
| control `05c706d6` | 1.12.0, pinned | `Totals: 99 passed, 2 failed (101 items)`, exit 0, `spec/neutral-product-pin` PASSES; the two failures are the two DISPOSITIONED scenario-omission findings |
| this branch | 1.12.0, pinned | `Totals: 100 passed, 2 failed (102 items)`, exit 0, same two |

The mechanism is measured on a controlled three-requirement fixture in
`design.md` **D6**: 1.2.0 reads only the first body line and ERRORS when the
keyword is not there; 1.12.0 reads the WHOLE body and, when the keyword is
absent altogether, emits a WARNING — *"should contain SHALL or MUST (RFC 2119
best practice for English specs)"* — and never an error.

**SO THE MOTIVE IS LEGIBILITY AND CONVENTION, NOT A RED GATE, AND THIS PROPOSAL
SAYS SO RATHER THAN LETTING THE ISSUE'S FRAMING STAND.** Issue #882 was written
against the 1.2.0 reading and is correct about it. It does not say that the
pinned gate is green, because that had not been measured. It has now.
`design.md` **D6** put the consequence as the first question for the owner:
amend promoted canon so its first line reads as its seventeen siblings do, or
close the issue with the measurement and leave ratified text alone. **IT IS
RULED — AMEND**, on Brett Heap's word of 2026-09-10, verbatim *"ratify as
encoded"*, taken with that measurement in front of him rather than without
it.

## Why this is NOT a plain fix

**Because the text is PROMOTED, RATIFIED CANON, and this estate has already
refused to edit such text without a word behind it.**

The requirement was ratified by Brett Heap on 2026-09-09, verbatim *"ratify
813"*, as part of `pin-openspec-cli-dependency-closure`, and written into the
specification by that packet's archive act, commit `fa58a1a3`. **The defect
entered at AUTHORING and was promoted faithfully** — the archived delta's own
first body line, at
`openspec/changes/archive/2026-09-09-pin-openspec-cli-dependency-closure/specs/neutral-product-pin/spec.md:6`,
is the same *"Where a pinned external neutral product is distributed as a
published artifact"* — so the promotion is not where this went wrong and
re-writing canon in an archive would not have caught it either.

The precedent is exact and recent. Codex raised a vocabulary defect in the SAME
specification as a P2 on PR
[#780](https://github.com/opensoft/openxFactory/pull/780); lane
`openxfactory-1` **REFUSED it in that pull request**, on the pull request's hard
limit rather than on the reading — *"Rewording the requirement here would (1)
edit ratified text with no word behind it and (2) destroy the very byte-identity
that makes this archive auditable. **Amending promoted canon is an amendment
packet's act, on its own ratification***" — and the successor became
`amend-neutral-product-pin-interim-copy-vocabulary`, ratified 2026-09-09 and
archived 2026-09-10. Working rule 3 says the same in general: a contract,
boundary or policy change goes through OpenSpec.

**And this packet is that predecessor's NAMED successor**, not a fresh idea. Its
`tasks.md` 5.2 reads *"THE `requirements.16` STRICT FAILURE IS A SUCCESSOR, NOT
THIS PACKET … it is named here as available rather than taken: it needs its own
issue and its own word"*, and its `design.md` D6 names the remedy in one line:
*"one sentence, moving `SHALL` onto the first line of that requirement's body,
on its own issue and its own word"*. Issue #882 is the issue. Brett Heap's *"do
882 packet"* is the word for the AUTHORING. **THE WORD FOR THE CONTENT HAS
SINCE BEEN GIVEN** — *"ratify as encoded"*, 2026-09-10, recorded on PR #923 at
19:53:02Z — and it is a second word on a second act, which is why this document
records both rather than collapsing them into one.

## What Changes

**ONE `## MODIFIED` REQUIREMENT. ONE SENTENCE RE-ORDERED. NOT ONE WORD ADDED,
NOT ONE WORD REMOVED, AND EVERY OTHER BYTE OF THE REQUIREMENT IS CANON'S OWN.**

- **RETIRED, and replaced in place:** *"Where a pinned external neutral product
  is distributed as a published artifact whose installation RESOLVES dependency
  ranges, the pin SHALL carry a VENDORED RESOLUTION — a lockfile in the format
  that product's own package manager consumes, committed beside the pin,
  addressed by a digest over its exact bytes recorded in the pin, together with
  the size of the tree it locks."*
- **WRITTEN, out of canon's own words:** *"The pin SHALL carry a VENDORED
  RESOLUTION where a pinned external neutral product is distributed as a
  published artifact whose installation RESOLVES dependency ranges — a lockfile
  in the format that product's own package manager consumes, committed beside
  the pin, addressed by a digest over its exact bytes recorded in the pin,
  together with the size of the tree it locks."*
- **THE ACCOUNTING, MEASURED CASE-SENSITIVELY** rather than described: the
  retired sentence's whitespace-split tokens minus the new sentence's are
  `Where`, `ranges,` and `the`; the new sentence's minus the retired one's are
  `The`, `where` and `ranges`. **Two case flips and one comma.** 374 characters
  become 373. Casefolded, the two token multisets differ by exactly that one
  comma and by nothing else.
- **THE OBLIGATION'S BEARER IS STILL THE PIN.** This is the reason the wording
  issue #882 floats is NOT the one encoded: *"A pinned external neutral product
  … SHALL carry a VENDORED RESOLUTION"* makes the PRODUCT the bearer, which the
  three sentences after it (*"recorded in the pin"*, *"A pin that declares NO
  vendored resolution … SHALL be refused"*), the first scenario's `THEN` (*"the
  pin carries a vendored resolution beside it"*) and the pin's own realized
  fields all contradict. `design.md` D1 records it as option 3 with that cost.
- **ONE `Removed from canon` MARKER, ONE NAME, NO CODE SPAN IN ITS REASON**,
  placed at the END of the block, naming the retired sentence and nothing else.
  It is ASSEMBLED FROM `derive_units`' OWN OUTPUT rather than retyped, then
  re-parsed by `parse_marker` and asserted to yield exactly one name and an
  empty `quoted` list — so neither the existing second marker-defect ground nor
  either ground the active `amend-marker-declaring-nothing` adds can fire on it.
- **RE-FLOWED, ONLY THAT PARAGRAPH, at the file's own width of 79.** Every other
  line of the block is canon's bytes, compared line by line.
- **CARRIED UNCHANGED:** the requirement heading, the paragraph's second and
  third sentences, both trailing body paragraphs (six sentences between them),
  all four scenario titles and all twelve scenario bullets. `derive_units`
  returns 25 units on both sides; exactly one is not carried and exactly one is
  new.

**NO BEHAVIOUR MOVES.** The same pins are obliged, on the same terms, with the
same four fields recorded in the same place, refused on the same ground, and
installed through the same clean-install verb. No consumer's conformance outcome
changes in either direction.

## Impact

- **Specification:** one requirement of `neutral-product-pin`. No requirement is
  ADDED, RENAMED or REMOVED; no other capability is touched.
- **Code:** none. See the `code_surface` front matter for the measurement.
- **Contracts, bundles, digests, tags:** none.
- **Gates:** none, in either direction. `spec/neutral-product-pin` still fails
  `openspec validate --all --strict` on the 1.2.0 binary at this pull request's
  head, because a delta does not edit the promoted specification — the ARCHIVE
  act is what would clear it — and it still passes on the pinned 1.12.0, where
  it never failed. `tasks.md` § 4 carries both runs with their exit codes.
- **Readers:** a reader of the promoted requirement meets the obligation on the
  first line after promotion instead of on the second.

## Sequencing

`sequenced_after: []` — the POSITIVE ROOT CLAIM, and it is measured rather than
assumed.

The requirement this block modifies is already promoted, so nothing has to land
first for the block to be written against canon. Exactly one other active change
carries a `neutral-product-pin` delta — **`split-opendox-two-layer-product`**
(ratified 2026-09-05, another lane's) — and it modifies *An external neutral
product is pinned by commit and digest, never by tag* and *The consuming
repository's pin is authoritative among reachable checkouts*. **Neither is the
requirement this packet modifies.** `grep -rln "A pinned artifact that resolves
dependencies at install time" openspec/changes/ --include=spec.md` over every
ACTIVE change returns nothing, so this change is the **SOLE ACTIVE MODIFIER** of
that requirement key: `modified-block-currency`'s two-writers rule is scoped to
two active writers, it does not reach the pair, and no ordering declaration is
owed in either direction. The two blocks share a spec FILE and no requirement
key, which is not a collision — a file is not the unit the rule is written over.

**AND THE SWEEP LEDGER READS `co-modifier`, WHICH IS NOT A CONTRADICTION.**
`tests/sequenced_after/corpus-ledger.yaml` grades `class` over the WHOLE corpus,
archived changes included, so this row reads `co-modifier`: the requirement key
it writes is necessarily also written by the ARCHIVED
`pin-openspec-cli-dependency-closure`, the change that PROMOTED the requirement
this packet amends. Every amendment of promoted canon shares a key with the
packet that promoted it. Seeding this row therefore also flips that archived
partner's row from `sole` to `co-modifier`, which is the ledger's own documented
partner-row behaviour. The two gradings answer different questions — the ledger
asks *has any other change in history written this key*, the ordering rule asks
*is another ACTIVE RATIFIED change writing it now* — and only the second decides
whether a declaration is owed.

`split-opendox-two-layer-product` and the draft `amend-marker-declaring-nothing`
are named in `.openspec.yaml`'s `related:` as measured neighbours, and **neither
naming is an ordering declaration**: the family reads a declaration as the
sibling's change id occurring as a whole token in the DECLARING change's own
`proposal.md`, and this proposal names them only to record that the requirement
sets are disjoint.

## What this proposal does NOT claim

- **It does not claim the ratified rule was wrong.** The obligation, its four
  fields, its refusal ground and its clean-install verb are all correct as
  ratified and none of them is edited.
- **It does not claim to fix a red required check.** The pinned gate is green on
  this specification and always was; `design.md` D6 is where that measurement
  lives and it is put as the first question rather than buried.
- **It does not fix the sibling first-line shape in another specification.**
  `openspec/specs/repo-boundary-governance/spec.md:34` (*Install repository
  scope*) is the corpus's only other requirement whose first body line lacks the
  keyword — measured across all 62 promoted spec files and 641 requirements. It
  is a different capability and needs its own issue and its own word;
  `tasks.md` § 6 names it as residue.
- **IT DID NOT RATIFY ITSELF, AND THE RATIFICATION HAS SINCE BEEN GIVEN
  SEPARATELY.** Ratification, promotion and archive are three acts on three
  words. The FIRST has now happened — Brett Heap, 2026-09-10, *"ratify as
  encoded"* — and it moved no wording, because every arm it resolved was the
  arm this packet already encoded. The other two have not: no file under
  `openspec/specs/` is edited by this pull request, `tasks.md` § 5 stays open,
  and openxFactory #882 closes at the archive rather than at this landing.
