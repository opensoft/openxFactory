---
code_surface: openxFactory — `scripts/target_release.py` (NEW, the reader and judge), `scripts/validate-target-release.py` (NEW, the house validator CLI), `scripts/target-release-register.yaml` (NEW, the closed grandfather register) and `tests/target_release/test_target_release_gate.py` (NEW, 86 tests) that pin them. NOTHING EXISTING IS EDITED IN THE CODE SURFACE: no arm of an existing validator moves, no existing test is edited, renamed, flipped or deleted, no workflow changes (the required `pytest-suite` already runs `tests/`), no contract member, no schema and no report field. The reader reaches the declaration through the SHIPPED strict loader `scripts/frontmatter_strict.py` and adds no second parser. Beside the code, the SAME pull request corrects SIX active proposals' `target_release:` VALUE TOKEN (five `none` → `implemented`, and one declaration that carried no leading token at all — the running sentence whose first word is the article `a` → `implemented`; every prose gloss preserved verbatim, one line per file, six lines in all) — see `design.md` D2 and D2a.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves, no `contract_bundle_version` is spent and no release tag is owed — deliberately, and the register says so in its own header: an exception file that could not be edited without cutting a contract release would be edited late or not at all. Under `release-realization` a non-empty code surface archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE rather than on landing, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green `pytest-suite` run at the tree the merge carries.
sequenced_after: []
---

# Proposal: gate-realization-axis-vocabulary

Status: ratified
Ratified: 2026-09-12 by Brett Heap (openxFactory operator authority) — D1 "Keep and gate", D2 "Sweep in this PR", D3 "Resolve against the registry that exists"; record at review/ratification-2026-09-12.md
Proposed: 2026-09-11, in lane `openxfactory-1` (display `openXfactory-1`),
session `9c62ed`, on Brett Heap's word of 2026-09-11T12:08:24Z, verbatim
**"land each when green, archive both when landed, claim 955 and 956"**.
Origin: openxFactory
[#956](https://github.com/opensoft/openxFactory/issues/956), filed by this lane
as the named successor owed by `amend-repo-boundary-governance-scope-first-line`
`tasks.md` § 6.8 at that packet's archive, standing on
[#931](https://github.com/opensoft/openxFactory/issues/931).

**THAT WORD COMMISSIONED THE AUTHORING, NOT THE CONTENT, AND RATIFICATION WAS
OWED. IT HAS SINCE BEEN GIVEN.** Brett Heap ruled on this packet itself on
2026-09-12 at 15:45Z — three independent multiple-choice rulings over
`design.md`'s three declared veto points, the recommendation presented first in
each — **D1 "Keep and gate"**, **D2 "Sweep in this PR"**, **D3 "Resolve against
the registry that exists"** — recorded on openxFactory PR
[#963](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5646922493);
record `review/ratification-2026-09-12.md`. `.openspec.yaml` carries the
approval pair as a pure ADDITION beside its unmoved drafting provenance, and
every document in this packet carries `Status: ratified`. **ALL THREE ARE THE
RECOMMENDED AND ALREADY-ENCODED OPTIONS, SO THE WORDING STANDS UNCHANGED**; D0
and D4 through D7 were carried beside them and none was vetoed. D2's ruled
option is a sweep of the corpus AS IT STANDS, and at the head this packet is
ratified on that corpus carries a sixth carrier the drafting corpus did not —
`design.md` D2a. **NOTHING IS PROMOTED** — this pull request edits no file
under `openspec/specs/`. Every judgment this authoring session took is listed
in `design.md` as **D0 through D7**, each with a recommendation and each put
for veto; the three that were ruled are **D1** (gate the vocabulary as
ratified), **D2** (the sweep) and **D3** (how the gate resolves "a named
release").

## Why

**A RATIFIED VOCABULARY THAT NOBODY READS HAS STOPPED BEING THE VOCABULARY.**

`release-realization`'s promoted requirement *Realization axis declaration*
admits exactly two values:

> `target_release:` — `implemented` (the affected repositories' main lines) or a
> named release defined in the aggregation repository. A proposal without the
> declarations is a doc-only change (`code_surface: none`,
> `target_release: implemented`) by default.

Measured on `main` at `38c076d1` (`design.md` D0, reproducible from the commands
recorded there): **199** `proposal.md` files, **181** declaring
`target_release:`. Of the **38 ACTIVE** proposals — all 38 declare the field —
only **12** declare a value the vocabulary admits: **9** `implemented` and **3**
a release this estate defines. **26 declare something else.**

**AND NOTHING REFUSES ANY OF IT.** `grep -rn target_release scripts/ tests/
.github/` finds no gate: the only reader is the ideation dashboard's DISPLAY
(`scripts/ideation_dashboard/generator.py` `_release_frontmatter`, rendered by
`scripts/ideation_dashboard/web/views/wheel.js`), which prints whatever string
it finds, and whose own fixtures use both spellings —
`tests/ideation-dashboard/test_gate_console.py` writes `target_release: none`
while `tests/scope_globs/` and `tests/sequenced_after/` write `implemented`. The
archive path is decided by `code_surface:`, the *Realization archive gate*
binding only "A change with a non-empty code surface". So the vocabulary is
stated in prose and checked by nobody, and the corpus shows what that costs.

## The divergence is wider than the issue that filed it

**issue #956 reports one value and counts six carriers. RE-MEASURED AT
AUTHORING THERE ARE FIVE, AND THEY ARE FIVE OF TWENTY-SIX.**
(`state-header-window-budget`, the sixth, archived at PR #953 before this
packet opened.) The 26 active declarations outside the vocabulary fall into
four classes, counted rather than characterised:

| class | active | what the declaration says |
| --- | ---: | --- |
| `none` | **5** | a value canon does not admit, meaning exactly what canon's default already says |
| deferred allocation | **12** | "THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE", "next additive contract bundle", "contract-v\<next minor\>" |
| realization state | **4** | `implementation_pending` — a state of the work, not a target |
| repository bootstrap | **2** | `repository-bootstrap` — a realization that is neither a main line nor a bundle |
| answers another question | **3** | "a code surface, so per `release-realization` it archives only on merged + green" — the archive rule, in the target field |

**THE TWELVE ARE THE ONES THAT MOVED THE DESIGN.**
`docs/contract-versioning-policy.md` § Bundle Realization Order opens *"Contract-bundle
realization is serialized and allocates versions late"*. An author who named a
number at proposal time would reserve one the policy allocates at the cut — so
the promoted two-value sentence has no spelling for *a release, not yet
numbered*, and twelve active authors are departing from one ratified rule in
order to obey another. That is a canon gap, not sloppiness, and a gate that
treated it as sloppiness would be wrong twelve times.

## What changes

**ONE `## ADDED Requirement`, ONE HOUSE VALIDATOR, ONE CLOSED REGISTER, AND A
SIX-LINE CORRECTION.**

1. **`### Requirement: Realization axis vocabulary is gated`** — ADDED to
   `release-realization`. Its first line: *"An ACTIVE change proposal's
   `target_release:` declaration SHALL carry a value the ratified vocabulary
   admits — `implemented`, or a release identifier that resolves to a release
   this estate defines — and a house validator SHALL REFUSE any other value on
   an active proposal, naming the proposal's path and the value it carries."*
   TEN scenarios: the refusal, `implemented`, a resolving release, **a tree
   that defines no release registry at all**, an archived record, a registered
   declaration, **a repeated declaration**, **an entry appended to the closed
   register**, a stale entry, and an absent declaration. (The THREE in bold
   were added by the bot bench — `design.md` D8b/D8d; the stale-entry scenario
   is part of the original seven and was not one of them.)
2. **`scripts/validate-target-release.py`** + **`scripts/target_release.py`** —
   the house realization, in the shape every other `scripts/validate-*.py`
   contract validator uses, run over the live corpus on every pull request by
   `tests/target_release/test_target_release_gate.py::test_corpus_target_release_validates`
   so a new divergence reds the required `pytest-suite`.
3. **`scripts/target-release-register.yaml`** — the 21 standing divergences this
   pull request does not correct, each with its value token, its class, its
   reason, its citation and the event that retires it. **CLOSED**: an entry may
   be removed, never added, because admitting a new value is a canon act.
4. **The six off-vocabulary carriers corrected**, one value token each,
   glosses preserved verbatim — the five `none` carriers `design.md` D2 names,
   and `amend-kill-switch-to-declared-test-companion`, which `origin/main`
   acquired after D2 was drafted (pull request #959, 2026-09-11T17:19:09Z) and
   which declares no leading token at all. D2's ruled option is a sweep of the
   corpus as it stands at the head the sweep lands on; `design.md` D2a records
   the sixth, its class, and why `implemented` is the author's own meaning.

**NO `## MODIFIED` BLOCK, AND THAT IS THE POINT OF THE SHAPE.**
`add-structured-scope-substrate` is ACTIVE and ratified and already holds a
MODIFIED block over *Realization axis declaration*. A second one would owe
`sequenced_after: [add-structured-scope-substrate]`, would have to restate that
change's text as its pre-text, and would inherit the archive-order hold
*Ordered deltas and branch vocabulary* imposes. An ADDED requirement over a
novel title owes none of it and edits no promoted byte.

## The measurement, before and after, on the real corpus

`python3 scripts/validate-target-release.py .`

| tree | exit | active | `implemented` | named release | registered | **refused** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `origin/main` `5972c8f3`, no gate present | **1** | 41 | 11 | 3 | 21 | **6** |
| THIS tree, after | **0** | 42 | 18 | 3 | 21 | **0** |

Both rows are the SAME validator pointed at two trees, re-measured last at
this packet's head (the merge of `origin/main` `5972c8f3`), so the
only difference between them is the tree, and the `after` row is reproducible
by running the command above here. **The `+1` active is this packet's own
`proposal.md`**, which declares `target_release: implemented` and is judged by
its own gate like every other active change. **The `+7` `implemented`** is that
same `+1` plus **`+6`**: the six carriers this pull request corrects to
`implemented` (D2, D2a) are still off-vocabulary — and so still counted
`refused` — on `origin/main`, which never received this packet's sweep.
`tasks.md` § 4.1 carries the same two rows.

The six refused before are exactly the six corrected: `add-composed-view-authoring`,
`add-cpc-clearing-boundary`, `add-lens-document-selection`,
`add-substantive-review-lane`, `register-gate-rules-council-seats` (the five
`none` carriers) and `amend-kill-switch-to-declared-test-companion` (no leading
token; `design.md` D2a). The archive is read and counted on both sides and
judged on neither: **163** archived proposals, **61** of them outside the
vocabulary, **0** findings.

## What this proposal does NOT do

- **It does not widen the vocabulary.** The two-value sentence stands exactly as
  ratified. The register does not admit a value; it names one that is already
  there and refuses its growth.
- **It does not edit one promoted byte.** No file under `openspec/specs/` is
  touched, and the delta carries no MODIFIED block, so no marker is owed.
- **It does not touch the archive.** The 27 archived `none` carriers and the 61
  archived off-vocabulary declarations are frozen record, read and counted and
  judged never.
- **It does not answer the deferred-allocation question.** Whether canon should
  admit *a release, not yet numbered* as a third value is named as a successor
  in `design.md` D1 and `tasks.md` § 6, and is deliberately not taken here: it
  is a MODIFIED block over the requirement `add-structured-scope-substrate`
  holds, with the sequencing cost that carries.
- **It does not change the ideation dashboard.** Its reader is display-only and
  its schema types `target_release` as a free string, so the corrected values
  render as themselves; measured, not assumed (`design.md` D7).
- **It does not close the origin issue.** `code_surface` is non-empty, so the
  archive is a separate act on merged-plus-green realization evidence and a
  separate word, and openxFactory issue 956 is closed THERE, by a closing
  keyword written in the archive pull request and in no commit message on this
  branch.
