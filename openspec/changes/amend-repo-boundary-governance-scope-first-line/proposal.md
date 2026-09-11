---
code_surface: none — MEASURED, not assumed. The delta is pure requirement prose and no script, test, workflow, contract, schema or example reads the sentence it re-orders. Evidence, taken 2026-09-11 on the clone of `main` `114d6e3d` this packet was authored against: (1) `grep -rn "SHALL be scoped to subsystem install\|subsystem install, operations, backup" scripts/ tests/ .github/ contracts/` returns NOTHING — not one line of running code, test data, workflow or contract quotes any part of the sentence; (2) the five repository names DO occur in `contracts/` and in the aggregation's mount list, but as identifiers of repositories rather than as a quotation of this sentence, and this block changes not one of them — the same five names, in the same order, with the same spelling and the same serial comma; (3) no test pins this capability's scenario count or scenario titles, and this block adds no scenario and drops none, so nothing keyed on either can move; (4) the one mechanical consumer of the delta is `doc-health`'s modified-block-currency family, which reads every active block by construction and is a GATE rather than a surface. **ONE FILE UNDER `tests/` DOES MOVE AND IT IS LISTED RATHER THAN LEFT TO THE DIFF** — Copilot's finding on this pull request, taken: `tests/sequenced_after/corpus-ledger.yaml` gains this change's own sweep row, ONE inserted line, written by the sanctioned tool `validate-sequenced-after.py . --seed-ledger`. It is a GENERATED REGISTRY that the sweep gate reconciles against the corpus, not executable test code: no test function, fixture body, assertion or helper changes, and the row is derived from this packet's existence rather than authored. Every active change seeds one; omitting it is what makes the gate red. Under `release-realization` an empty code surface archives ON LANDING plus its own task list, not on merged-plus-green realization evidence.
target_release: implemented — the value canon NAMES for a doc-only change, taken on Copilot's finding on this pull request and MEASURED rather than swapped on its word. `release-realization`'s *Realization axis declaration* admits `target_release:` as `implemented` (the affected repositories' main lines) *"or a named release defined in the aggregation repository"* and states the doc-only default in the same breath — *"A proposal without the declarations is a doc-only change (`code_surface: none`, `target_release: implemented`) by default"* (`openspec/specs/release-realization/spec.md:24-30`). **`none` is outside that vocabulary**, and this packet was authored with it by mirroring its ratified predecessor. THE DIVERGENCE IS CORPUS-WIDE AND IS NAMED RATHER THAN HIDDEN: 33 of the 180 proposals declaring the field carry `target_release: none`, and among proposals with `code_surface: none` the split is 7 `none` against 9 `implemented`, so the conformant value is also the majority one for this shape. **NOTHING BEHAVIOURAL MOVES EITHER WAY** — no script gates on the value (`grep -rn target_release scripts/ tests/ .github/` finds one dashboard reader and test fixtures using both), and the archive path is decided by `code_surface`, the *Realization archive gate* binding only *"A change with a non-empty code surface"*. This packet conforms and does NOT sweep the other 32 proposals or amend `release-realization`: that is named as residue in `tasks.md` § 6.8. Substantively: no code surface, no contract bundle, no digest set and no release tag; nothing under `contracts/` is touched, no `contracts/releases/<tag>.digests.yaml` moves, and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on a separate word.
sequenced_after: []
---

# Proposal: amend-repo-boundary-governance-scope-first-line

Status: draft
Proposed: 2026-09-11, in lane `openxfactory-1` (display `openXfactory-1`), on
Brett Heap's word of 2026-09-11T00:42Z, verbatim **"do 915 and 931, land each
when green"**, given in session and recorded in this lane's CLAIMED comment on
openxFactory [#931](https://github.com/opensoft/openxFactory/issues/931) at
2026-09-11T00:42Z.
Origin: openxFactory issue
[#931](https://github.com/opensoft/openxFactory/issues/931), filed UNCLAIMED by
this lane at the archive of `amend-neutral-product-pin-lockfile-first-line` as
the named successor of that packet's `tasks.md` § 6.1, `design.md` D7 and its
delta header.

**THAT WORD AUTHORIZES THE PROPOSING AND THE LANDING, NOT THE CONTENT.** It
commissions this authoring and it pre-gives the LANDING word for whatever head
is ratified and green; it ratifies nothing, resolves none of the three
decisions below, and admits no text to canon. **THIS PACKET IS THEREFORE A
DRAFT AND CARRIES NO APPROVAL PAIR** — `.openspec.yaml` has `proposed_by` and
`proposed_on` and no `approved_by` or `approved_on`, and every document in it
carries `Status: draft`. Ratification is a separate act on a separate word,
over `design.md` **D6**, **D1** and **D2**, put below with the recommendation
first.

## Why

**One requirement of `repo-boundary-governance` opens its body with a list of
repository names and defers its verb and its `SHALL` to the second line, and a
reader — human or parser — who reads one line meets four names and no
obligation.**

The requirement is *Install repository scope*
(`openspec/specs/repo-boundary-governance/spec.md:34-66`). Its first two body
lines, `:35-36`:

> `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`,
> and `OmniWorker-Install` SHALL be scoped to subsystem install, operations,

It is not short of obligation: `SHALL` stands on the very next line and `MUST`
three times below that, once in each scenario. What it lacks is the obligation
on LINE ONE, and that is the shape **ten of the eleven requirements in this
same file already have** — measured, not asserted: every other requirement's
first body line carries `SHALL`, and **all ten of them do it inside 80
characters** (63, 67, 70, 71, 73, 74, 75, 75, 76, 79). Index 1 is the ONE that
opens with an enumeration.

**AND ON ONE OPENSPEC BINARY THAT SHAPE IS A STRICT-VALIDATION ERROR.** On the
CLI at 1.2.0:

```
$ OPENSPEC_TELEMETRY=0 openspec validate repo-boundary-governance --strict --type spec
Specification 'repo-boundary-governance' has issues
✗ [ERROR] requirements.1.text: Requirement must contain SHALL or MUST keyword
```

exit **1**.

**IT IS NOW THE CORPUS'S LAST ONE.** Re-measured on this basis: across all
**62** promoted spec files under `openspec/specs/` and all **641**
`### Requirement:` headings in them, **exactly ONE** has a first body line
carrying neither `SHALL` nor `MUST`, and it is this one. Its predecessor's
measurement found two; the archive of
`amend-neutral-product-pin-lockfile-first-line` cleared the other.

## What the pinned CLI says, which changes the case and is stated before the remedy

**THE PINNED CLI DOES NOT REPORT THIS AT ALL, AND NO REQUIRED CHECK DOES.**
`contracts/openspec-cli-pin.yaml:255` pins `@fission-ai/openspec@1.12.0`;
`.github/workflows/openspec-cli-pin-gate.yml` runs
`python3 scripts/validate-openspec-cli-pin.py --all --no-cache` through the
content-verified artifact; and on that binary this specification **PASSES**.
Measured on `main` `114d6e3d`, 2026-09-11:

```
$ OPENSPEC_TELEMETRY=0 <pinned 1.12.0>/openspec validate repo-boundary-governance --strict --type spec
Specification 'repo-boundary-governance' is valid
ℹ [INFO] requirements[1]: Requirement text is very long (>500 characters). Consider breaking it down.
… five more INFO notes …
```

exit **0**. Whole-corpus, same tree: the 1.2.0 binary on `PATH` gives
`Totals: 97 passed, 3 failed (100 items)`, exit 1, with
`spec/repo-boundary-governance` among the three; the pinned 1.12.0 gives
`Totals: 98 passed, 2 failed (100 items)`, exit 0, with
`spec/repo-boundary-governance` among the **passes** and the two failures the
two DISPOSITIONED scenario-omission findings accepted on Brett Heap's word of
2026-09-05 *"take exit 2"*.

**SO THE MOTIVE IS LEGIBILITY AND CONVENTION, NOT A RED GATE, AND THIS PROPOSAL
SAYS SO RATHER THAN LETTING THE ISSUE'S FRAMING STAND.** Issue #931 says the
same and says it first; this proposal repeats the measurement rather than
citing it, because it is the first question and not a footnote. `design.md`
**D6** puts the consequence: amend promoted canon so its first line reads as
its ten siblings do, or close #931 with the measurement and leave ratified text
alone. **THE ANSWER IS THE OWNER'S AND IT IS ASKED FRESH HERE.** Brett Heap
ruled **AMEND** on exactly this question for the sibling requirement on
2026-09-10, verbatim *"ratify as encoded"* (openxFactory PR
[#923](https://github.com/opensoft/openxFactory/pull/923#issuecomment-5624573662)),
and that ruling is quoted as **PRECEDENT ONLY**: it was given over one
requirement of one specification, with that requirement's own seventeen-to-one
convention in front of him, and this packet does not read it as a standing rule
for a different capability.

## Why this is NOT a plain fix

**Because the text is PROMOTED, RATIFIED CANON, and this estate has already
refused to edit such text without a word behind it.**

*Install repository scope* was promoted by `restructure-factory-repo-boundaries`
(archived 2026-06-26, commit `7c4dacb9`) and its first sentence was LAST
WRITTEN by `refresh-install-repository-enumerations` (archived 2026-09-09,
commit `ca4a1558`, PR #825), which widened the list from four names to five and
declared the widening with a `Removed from canon` marker that still stands at
`:66`. **The defect is older than either**: the first body line has been an
enumeration since the requirement was promoted, and the 2026-09-08 widening
faithfully preserved the shape it found.

The precedent is exact and recent. Codex raised a vocabulary defect in another
promoted specification as a P2 on PR
[#780](https://github.com/opensoft/openxFactory/pull/780); lane
`openxfactory-1` **REFUSED it in that pull request** — *"Rewording the
requirement here would (1) edit ratified text with no word behind it and (2)
destroy the very byte-identity that makes this archive auditable. **Amending
promoted canon is an amendment packet's act, on its own ratification***" — and
the successor became its own packet. Working rule 3 says the same in general.
**And this packet is a NAMED successor**, not a fresh idea: its predecessor
declined this requirement in three places and filed #931 for it.

## What Changes

**ONE `## MODIFIED` REQUIREMENT. ONE SENTENCE RE-ORDERED. FOUR WORDS ADDED,
NONE REMOVED, AND EVERY OTHER BYTE OF THE REQUIREMENT IS CANON'S OWN.**

- **RETIRED, and replaced in place:** *"`Hermes-Install`, `Omnigent-Install`,
  `Keycloak-Install`, `OpenXPKI-Install`, and `OmniWorker-Install` SHALL be
  scoped to subsystem install, operations, backup, restore, upgrade,
  verification, and disaster recovery."*
- **WRITTEN:** *"The following install repositories SHALL be scoped to
  subsystem install, operations, backup, restore, upgrade, verification, and
  disaster recovery: `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`,
  `OpenXPKI-Install`, and `OmniWorker-Install`."*
- **THE ACCOUNTING, MEASURED CASE-SENSITIVELY** rather than described: the new
  sentence's whitespace-split tokens minus the retired sentence's are `The`,
  `following`, `install`, `repositories`, `recovery:` and
  `` `OmniWorker-Install`. ``; the retired sentence's minus the new one's are
  `recovery.` and `` `OmniWorker-Install` ``. **Four words added, none removed,
  and two punctuation moves** — the terminal period leaves `recovery` for the
  last name and a colon stands where it was. 215 characters become 251.
- **AND THIS IS LARGER THAN ITS PREDECESSOR'S EDIT, WHICH IS SAID PLAINLY.**
  `amend-neutral-product-pin-lockfile-first-line` added not one word, because
  its sentence already carried the clause *"the pin SHALL carry a VENDORED
  RESOLUTION"* and needed only permuting. **THIS SENTENCE HAS NO SUBJECT TO
  PROMOTE — its subject IS the list** — so no zero-word re-order of it exists,
  and `design.md` **D1** writes the three real candidates out instead of
  claiming one that does not.
- **THE FIVE NAMES ARE CANON'S, EXACTLY.** Same five, same order, same
  spelling, same serial comma before the final `and`. They came from
  `refresh-install-repository-enumerations`, whose own packet measured that
  comma (`openspec/specs` carries 561 lines with a serial comma before a final
  `or` against 232 without), and nothing here re-opens it.
- **THE ENUMERATION STAYS AN INDEX.** This capability's own requirement
  *Install-repository enumerations are an index with a named authority*
  (`:308`) holds that an enumeration *"SHALL be read as an INDEX and SHALL NOT
  be read as the authority for which install repositories exist or are
  governed"*, and states the count FIVE itself. **That is why the variant
  reading *"The five install repositories …"* is written out and REFUSED**: it
  would copy a count into a second requirement, and a copy of a declaration
  moves separately — the defect this capability's own index rule exists to end.
  `design.md` **D1** records it as option 3.
- **ONE `Removed from canon` MARKER, ONE NAME, NO CODE SPAN IN ITS REASON**,
  placed at the END of the block, naming the retired sentence and nothing else.
  It is ASSEMBLED FROM `derive_units`' OWN OUTPUT rather than retyped, then
  re-parsed by `parse_marker` and asserted to yield exactly one name and an
  empty `quoted` list.
- **AND THE MARKER THIS REQUIREMENT INHERITS IS NOT CARRIED FORWARD.** The
  promoted block ends with `refresh-install-repository-enumerations`' own
  marker at `:66`; this block does not restate it, on canon's rule that *"A
  marker is NOT a carriage unit, in either direction … The durable record of a
  deletion is the archived delta"*
  (`openspec/specs/doc-health/spec.md:1801-1805`). `design.md` **D2** carries
  the measurement of both branches and the four-times-repeated precedent.
- **RE-FLOWED, ONLY THAT PARAGRAPH, at the file's own width of 79.** Every
  other line of the block is canon's bytes, compared line by line: the 27 lines
  from `:38` to `:64` hash identically on both sides.
- **CARRIED UNCHANGED:** the requirement heading, the whole second body
  paragraph, all three scenario titles and all six scenario bullets.
  `derive_units` returns 13 units on both sides; exactly one is not carried and
  exactly one is new.

**NO OBLIGATION MOVES, AND THE ONE OUTCOME THAT DOES CHANGE IS NAMED RATHER
THAN COVERED BY A BROADER SENTENCE** — Copilot's finding on this pull request,
taken. The same five repositories are scoped to the same seven activities, the
same three routing scenarios fire on the same triggers, and **no install
repository's conformance with this requirement changes in either direction**:
a repository that satisfied *Install repository scope* before satisfies it
after, on the same terms, and one that did not still does not. **WHAT DOES
CHANGE — AT THE ARCHIVE, AND ON PURPOSE — IS THE PARSER'S VERDICT ON THE
SPECIFICATION ITSELF.** Once the block is promoted, a reader running the 1.2.0
CLI goes from `✗ [ERROR] requirements.1.text: Requirement must contain SHALL
or MUST keyword`, exit 1, to a valid specification at exit 0. **That is the
whole point of the packet and the subject of `design.md` D6**, so it would be
wrong to fold it under a blanket "nothing moves". It does not move at THIS
landing — a delta does not edit the promoted specification — and it does not
move at all on the pinned 1.12.0, where the specification already passes.

## Impact

- **Specification:** one requirement of `repo-boundary-governance`. No
  requirement is ADDED, RENAMED or REMOVED; no other capability is touched.
- **Code:** none. See the `code_surface` front matter for the measurement.
- **Contracts, bundles, digests, tags:** none.
- **Gates:** none, in either direction. `spec/repo-boundary-governance` still
  fails `openspec validate --all --strict` on the 1.2.0 binary at this pull
  request's head, because a delta does not edit the promoted specification —
  the ARCHIVE act is what would clear it — and it still passes on the pinned
  1.12.0, where it never failed. `tasks.md` § 4 carries both runs with their
  exit codes.
- **Readers:** a reader of the promoted requirement meets the obligation on the
  first line after promotion instead of on the second.

## Sequencing

`sequenced_after: []` — the POSITIVE ROOT CLAIM, and it is measured rather than
assumed.

The requirement this block modifies is already promoted, so nothing has to land
first for the block to be written against canon. **FIVE other active changes
carry a `repo-boundary-governance` delta** — `add-identity-brokering`,
`add-trust-anchor`, `implement-keycloak-install-repo`,
`implement-openxpki-install-repo` and `qualify-avatar-live-voice` — and each
was read by NAME rather than counted: they write *Keycloak install repository
boundary* (ADDED, then MODIFIED), *OpenXPKI install repository boundary*
(ADDED, then MODIFIED) and *Neutral avatar-client repository boundary*
(MODIFIED). **Not one of them is this requirement.** The corpus search is
pasted in a form that REPRODUCES, the archive exclusion being a pipe rather
than prose: `grep -rln "Install repository scope" openspec/changes/
--include=spec.md | grep -v '/archive/'` returns **exactly one path on this
tree — this packet's own delta — and nothing else**, and the PRE-ADDITION
measurement is re-derivable against the branch point with `git grep -l
"Install repository scope" 114d6e3d -- 'openspec/changes/*/specs/*/spec.md' |
grep -v '/archive/'`, which returns **nothing, exit 1**. (Unfiltered, the same
search also returns three ARCHIVED deltas —
`2026-06-26-restructure-factory-repo-boundaries`,
`2026-08-25-admit-install-repos-to-aggregation` and
`2026-09-09-refresh-install-repository-enumerations` — which is why the filter
is part of the command and not part of the sentence.) So this change is the
**SOLE ACTIVE MODIFIER** of that requirement key: `modified-block-currency`'s two-writers rule is scoped to two
active writers, it does not reach any of the five, and no ordering declaration
is owed in either direction. Sharing a spec FILE is not a collision — a file is
not the unit the rule is written over.

**AND THE SWEEP LEDGER READS `co-modifier`, WHICH IS NOT A CONTRADICTION.**
`tests/sequenced_after/corpus-ledger.yaml` grades `class` over the WHOLE
corpus, archived changes included, so this row reads `co-modifier`: the
requirement key it writes is necessarily also written by the ARCHIVED
`restructure-factory-repo-boundaries` and
`refresh-install-repository-enumerations`. Every amendment of promoted canon
shares a key with the packet that promoted it. The two gradings answer
different questions — the ledger asks *has any other change in history written
this key*, the ordering rule asks *is another ACTIVE RATIFIED change writing it
now* — and only the second decides whether a declaration is owed.

The five active neighbours are named in `.openspec.yaml`'s `related:` as
measured neighbours, and **no naming there is an ordering declaration**: the
family reads a declaration as the sibling's change id occurring as a whole token
in the DECLARING change's own `proposal.md`, and this proposal names them only
to record that the requirement sets are disjoint.

## What this proposal does NOT claim

- **It does not claim the ratified rule was wrong.** The scope, the five
  repositories and the three routing scenarios are all correct as ratified and
  none of them is edited.
- **It does not claim to fix a red required check.** The pinned gate is green
  on this specification and always was; `design.md` **D6** is where that
  measurement lives and it is put as the first question rather than buried.
- **It does not inherit its predecessor's ruling.** Brett Heap's *"ratify as
  encoded"* of 2026-09-10 resolved D6 for ONE requirement of ONE specification.
  This packet quotes it as precedent and asks the question again.
- **It does not re-open the enumeration.** The five names, their order, their
  spelling and their serial comma are `refresh-install-repository-enumerations`'
  ratified act and are carried untouched; `design.md` **D7** records that the
  requirement's own heading and the count in the sibling index requirement are
  likewise not edited.
- **IT DOES NOT RATIFY ITSELF.** Ratification, promotion and archive are three
  acts on three words. None has been given: no file under `openspec/specs/` is
  edited by this pull request, `tasks.md` §§ 1 and 5 stay open, and
  openxFactory #931 closes at the archive rather than at this landing, which is
  why this pull request carries no closing keyword.
