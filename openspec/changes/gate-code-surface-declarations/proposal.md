---
code_surface: openxFactory — and NOT ONE BYTE OF IT MOVES IN THIS PULL REQUEST. The realization this packet proposes is a LATER pull request in this same repository, authored after ratification, and it is four files and one edit: `scripts/code_surface.py` (NEW, the reader and judge), `scripts/validate-code-surface.py` (NEW, the house validator CLI in the shape every other `scripts/validate-*.py` uses), `scripts/code-surface-register.yaml` (NEW, the closed grandfather register), `tests/code_surface/test_code_surface_gate.py` (NEW, the tests that pin them and the live-corpus run that reds `pytest-suite` on a new divergence), and — only if `design.md` D4 is ruled as recommended — ONE narrowing edit to `scripts/scope_globs.py`'s `code_surface_repositories`, so the repository set it derives comes from the declared head rather than from every word of the gloss. NO OTHER EXISTING FILE IS EDITED: no arm of an existing validator moves, no existing test is edited, renamed, flipped or deleted, no workflow changes (the required `pytest-suite` already runs `tests/`), no contract member, no schema, no report field and no promoted byte. The reader reaches the declaration through the SHIPPED strict loader `scripts/frontmatter_strict.py` and adds no second parser. THIS pull request carries the PACKET ONLY — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, one `## ADDED` spec delta, one README *Active changes* bullet, and the machine-seeded per-change sweep-ledger row in `tests/sequenced_after/corpus-ledger.yaml` that any filing owes.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves, no `contract_bundle_version` is spent and no release tag is owed — deliberately, and for the reason the sibling's register states in its own header: an exception file that could not be edited without cutting a contract release would be edited late or not at all. Under `release-realization` a non-empty code surface archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE rather than on landing, so this packet archives only after its realization pull request has merged and run green, and openxFactory issue 1013 closes there.
sequenced_after: []
---

# Proposal: gate-code-surface-declarations

Status: draft

Proposed: 2026-09-12, in lane `openxfactory-5` (display `openXfactory-5`),
session `71ee29`, in answer to openxFactory
[#1013](https://github.com/opensoft/openxFactory/issues/1013) — the residue
`gate-realization-axis-vocabulary` `tasks.md` § 6.3 owed and that packet's
archive act filed, standing on
[#956](https://github.com/opensoft/openxFactory/issues/956). The lane CLAIMED
#1013 before authoring.

Origin: openxFactory

**NOTHING HERE IS RATIFIED AND NO WORD RATIFIES IT.** Taking an unclaimed
residue commissions the AUTHORING and decides no wording: this packet admits no
text to canon, and every document in it — this one, `design.md`, `tasks.md` —
carries `Status: draft`. `.openspec.yaml` carries the lawful unapproved shape
`add-drafted-proposal-origin` (issue #318) defined: drafting provenance, no
`approved_by`, no `approved_on`. **NOTHING IS PROMOTED**: this pull request
edits no file under `openspec/specs/`. **NOTHING IS REALIZED**: it adds no
script, no register and no test. Every judgment this authoring session took is
listed in `design.md` as **D0 through D8**, each with its alternative and the
alternative's cost; the four put for veto are **D1** (what "off-vocabulary"
means when the value is prose), **D2** (the shape of the remedy), **D3** (the
disposition of the seven pre-existing non-conformers) and **D4** (whether
`add-structured-scope-substrate`'s `scope_globs:` machinery is reusable).

## Why

**ONE HALF OF A RATIFIED SENTENCE IS NOW READ. THE OTHER HALF IS STILL READ BY
NOBODY — EXCEPT BY A READER THAT READS IT WRONG.**

`release-realization`'s promoted requirement *Realization axis declaration* is
one sentence with two halves:

> Every OpenSpec change proposal SHALL declare `code_surface:` — `none` or the
> repositories whose runtime artifacts it changes — and `target_release:` —
> `implemented` (the affected repositories' main lines) or a named release
> defined in the aggregation repository.

`gate-realization-axis-vocabulary` gated the SECOND half and ruled, in its own
ratified `tasks.md` § 6.3, that it was not gating the first: *"`code_surface:`
IS NOT GATED. The other half of the same sentence is equally unread; it is a
second population with its own classes, and folding it in here would widen a
ruled remedy into an unruled sweep."* This packet is that second population,
measured.

## The measurement, taken before the design

**NOTHING BELOW RESTS ON A NUMBER ANYBODY TYPED.** Re-taken on a fresh clone at
`origin/main` `bcde1575`, by the method the issue names so it reproduces: a
`^code_surface:` line inside the leading fence of every top-level
`openspec/changes/<change>/proposal.md`, read through the SHIPPED strict loader
`scripts/frontmatter_strict.read_front_matter`; the archive read one level down
and counted, never judged. The commands and the script are recorded in
`design.md` D0 and `tasks.md` § 2.

| measure | #1013 at filing | re-measured (`bcde1575`) |
| --- | ---: | ---: |
| ACTIVE proposals | 45 | **45** |
| declaring `code_surface:` | 45 | **45** |
| declaring `none` | 5 | **4** |
| declaring a non-`none` value | 40 | **41** |
| repeated declarations | — | **0** |
| refused by the strict loader | — | **0** |

The one that moved is one fact, and it is the kind of fact the issue itself
warns about: the corpus moved between the filing and this authoring. The issue's
"5 `none`" is now **4**.

**`none` IS NOT THE DIVERGENCE HERE, AND THAT IS THE FIRST DIFFERENCE FROM THE
SIBLING.** `none` is a value *Realization axis declaration* ADMITS for
`code_surface:` — it is the promoted default for a doc-only change. All four
carriers are lawful. The divergence is entirely in the **41 non-`none`
declarations**, whose value is a repository LIST written as prose.

**THE GRAMMAR IS DERIVED FROM THE POPULATION, NOT INVENTED FOR IT.** Parsing
each declaration as the longest prefix that reads as `none` or as repository
identifiers separated by a comma, by ` and `, or by ` + `, and then asking what
FOLLOWS that prefix:

| what follows the declared head | active |
| --- | ---: |
| an opening parenthesis | **19** |
| an em dash | **17** |
| a full stop | **2** |
| **— conforming subtotal** | **38** |
| ordinary prose, no opener (`, and it is …`, ` aggregation repo`) | **5** |
| a possessive (`openxFactory's half …`) | **1** |
| a YAML folding indicator (`>-`) | **1** |
| **— non-conforming subtotal** | **7** |

**38 of 45 already write head-then-opener-then-gloss.** The grammar this packet
proposes states what those 38 do. The seven are the register's population, in
four classes (`design.md` D0):

| class | active | the declaration |
| --- | ---: | --- |
| block scalar | **1** | `adopt-configured-notebook-hosting-identity` — `code_surface: >-` then an indented continuation; `code_surface:` is a PROSE header no YAML loader reads, so the value opens with the literal `>-` |
| possessive | **1** | `amend-kill-switch-to-declared-test-companion` — `openxFactory's half of this packet carries NO CODE …` |
| apposition | **1** | `add-substantive-review-lane` — `xFactory aggregation repo (…` |
| the list runs into prose | **4** | `admit-review-lane-repin-to-merge-approval-envelope`, `amend-mirror-floor-regeneration-merge-authority`, `extend-merge-master-envelope-to-floor-bot-lanes`, `split-opendox-two-layer-product` |

**THE ARCHIVE IS READ AND NEVER JUDGED:** 165 archived proposals, **119**
declaring the field (46 predate it), **3** outside the grammar.

## And the one reader that does exist reads the gloss

**A GATE ON THE TEXT THAT LEFT THE EXISTING READER ALONE WOULD BE HALF A
REMEDY.** `grep -rn code_surface scripts/ .github/` at `bcde1575` returns
seventeen lines: fourteen in `scripts/scope_globs.py` and
`scripts/validate-scope-globs.py`, and three in prose (a docstring quoting the
promoted default, two comments). Nothing in `.github/`. So
`scripts/scope_globs.py`'s `code_surface_repositories` is the ONLY machine
reader of this field, and it is wired live at
`scripts/validate-scope-globs.py:68`. It splits the WHOLE declaration — gloss
included — on `[\s,()/]+` and returns every word that is not `none`. Its own
docstring calls this "intentionally permissive". Measured over the 45 active
declarations:

- **3,421** distinct "repository" tokens across the corpus;
- the widest single declaration yields **767** of them, among which `the`,
  `and`, `GitHub`, `Postgres`, `FastAPI`, `§`;
- **27 of 45** yield an ESTATE REPOSITORY NAME the declaration's own head does
  not name — `add-sequenced-after-substrate` declares `openxFactory` and yields
  `codexFactory`; `create-ledgerxwallet-overlay-boundary` declares
  `opensoft/LedgerxWallet` and yields five more;
- **3 of the 4 `none` carriers** yield a non-empty set, because the filter drops
  the word `none` and keeps the gloss.

Its consumer is `scope_globs.validate_cross_consistency`, which holds that every
`scope_globs:` repository key "MUST be named in `code_surface`" — and
`scope_globs:` is what bounds the paths a provenance-gated autonomous merge may
write.

**THE DEFECT IS LATENT, NOT STANDING, AND THIS PACKET SAYS SO RATHER THAN
OVERSTATING IT.** **ZERO of the 45** active proposals declare `scope_globs:`
today, so the cross-check is vacuous until the first one lands. Nothing standing
is mis-authorized. What exists is a guard that will answer wrongly the first
time it is asked a question — which is the same shape of defect as a vocabulary
nothing reads, one step further along.

## What changes

**THREE `## ADDED` REQUIREMENTS, AND A REALIZATION THIS PULL REQUEST DOES NOT
PERFORM.**

1. **`### Requirement: Code-surface declaration grammar is gated`** — its first
   line makes a house validator refuse an active declaration whose HEAD it
   cannot read, the head being `none` or repository identifiers separated by a
   comma, by ` and `, or by ` + `, and the gloss being introduced by one of the
   openers the corpus already uses. The head is judged; the gloss never is.
   Membership is explicitly NOT judged, for a measured reason (`design.md` D1).
   TEN scenarios.
2. **`### Requirement: The declared repository set is derived from the head and
   never from the gloss`** — the consumer rule, which is where the
   authorization actually sits. THREE scenarios.
3. **`### Requirement: Standing code-surface divergence is named in a closed
   register`** — the ratchet, in the sibling's shape: removable, never addable,
   with the closure enforced by a baseline in the module and the two asymmetric
   refusals kept asymmetric. FOUR scenarios.

The realization — validator, register, tests, and the one narrowing edit — is
`tasks.md` § 3, and it is a LATER pull request on a LATER word.

**NO `## MODIFIED` BLOCK, AND THAT IS THE POINT OF THE SHAPE.**
`add-structured-scope-substrate` is ACTIVE and ratified and already holds a
MODIFIED block over *Realization axis declaration*. A second one would owe
`sequenced_after: [add-structured-scope-substrate]`, would have to restate that
change's text as its pre-text, and would inherit the archive-order hold *Ordered
deltas and branch vocabulary* imposes. Three ADDED requirements over novel
titles owe none of it and edit no promoted byte. The titles were checked against
the whole corpus and appear nowhere else (`design.md` D7).

## What this proposal does NOT do

- **It does not widen or narrow the promoted vocabulary.** The `code_surface:`
  half of *Realization axis declaration* stands exactly as ratified. The grammar
  says how a declaration is WRITTEN, never which repositories may be named.
- **It does not resolve a repository name against anything.** This repository
  defines no inventory of the estate's repositories; `design.md` D1 records what
  was looked at and why none of it is one. Whether canon should define one is a
  successor (`tasks.md` § 6.1).
- **It does not edit one promoted byte.** No file under `openspec/specs/` is
  touched, and the delta carries no MODIFIED block, so no marker is owed.
- **It does not touch the archive.** The 3 archived declarations outside the
  grammar are frozen record: read, counted, judged never.
- **It does not make `code_surface:` a structured field.** Turning the prose
  header into a `scope_globs`-style structured list is the obvious machine-
  readable move and it is a MODIFIED block over the contested title, with the
  sequencing cost that carries. Named as a successor (`tasks.md` § 6.2).
- **It does not sweep the seven, on the recommended option.** `design.md` D3
  puts the sweep as an alternative and states its cost: correcting a head
  re-punctuates another lane's ratified prose, and for one of the seven it is a
  judgment about what counts as a repository.
- **It does not close the origin issue.** `code_surface` is non-empty, so the
  archive is a separate act on merged-plus-green realization evidence and a
  separate word, and openxFactory issue 1013 is closed THERE, by a closing
  keyword written in the archive pull request and in no commit message on this
  branch.
