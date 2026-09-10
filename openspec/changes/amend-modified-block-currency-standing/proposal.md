---
code_surface: none — MEASURED, not assumed. Nothing under `scripts/` or `tests/` reads the sentences this packet retires, and the delta is pure requirement prose. Evidence, taken 2026-09-10 on the clone of `main` this packet was authored against: (1) `grep -rn "advisory at launch\|deliberately absent" scripts tests` returns 13 lines and NOT ONE of them is this requirement — twelve are unrelated module comments and docstrings about other absences (`scripts/validate-client-content.py:94`, `scripts/attest-openspec-cli-pin-lockfile.py:289`, `scripts/validate-clearing-dispatch.py:166`, `scripts/verify-openxwallet-pin.py:81`, `scripts/validate-identity-brokering.py:324`, `scripts/validate-hermes-domain-overlay.py:82`, `scripts/validate-openspec-cli-pin.py:399`, `scripts/ideation_dashboard/doxbench_mcp.py:416`, `scripts/ideation_dashboard/doxbench_model.py:1041`, `scripts/ideation_dashboard/web/views/staging-workbench-model.js:820`, `tests/ideation-dashboard/conftest.py:129`, `tests/ideation-dashboard/smoke_signals.py:36`) and the thirteenth, `scripts/doc_health/document_catalog.py:38`, is a different family's docstring about ITS own `FAMILY_RESOLUTION` handling. (2) No test reads the promoted specification's prose: the suite pins the module's own constants (`test_the_three_launch_severities_are_named_apart`, `test_the_family_joined_family_resolution_on_the_flip`) and those constants are the state this delta describes — they are NOT touched here, so nothing in the suite can move either way. (3) The one mechanical consumer of the delta is `doc-health`'s own modified-block-currency family, which reads every active `## MODIFIED` block by construction; that is a GATE over this packet, not a surface this packet changes. THE CODE HAS BEEN IN THE POST-FLIP STATE SINCE 2026-08-31 — this is canon catching up with running code, and a canon-only edit is the whole of it. Under `release-realization` an empty code surface archives ON LANDING plus its own task list rather than on merged-plus-green realization evidence. The `specs/019` FR-018 commit that rides this pull request is a DOCUMENT, not a code surface: a Speckit build record pinned by no test and by no gate (`design.md` D6).
target_release: none — no code surface, no contract bundle, no digest set and no release tag. Nothing under `contracts/` is touched, no `contracts/releases/<tag>.digests.yaml` moves, and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on Brett Heap's word.
sequenced_after: []
---

# Proposal: amend-modified-block-currency-standing

Status: draft
Proposed: 2026-09-10, in lane `openxfactory-1` (display `openXfactory-1`), on
Brett Heap's word of 2026-09-10, verbatim **"do 1, then 2"**, given in session
with item 2 naming openxFactory issues #857 and #858 as one amendment packet.
Origin: openxFactory
[#857](https://github.com/opensoft/openxFactory/issues/857) and
[#858](https://github.com/opensoft/openxFactory/issues/858), both filed by this
lane at the archive of `amend-marker-defect-reporting`
([#850](https://github.com/opensoft/openxFactory/pull/850) → `250d93d7`), which
owed them as residue `tasks.md` § 5.3 and § 5.4.
**THAT WORD AUTHORIZES THE AUTHORING, NOT THE CONTENT.** It commissions a
packet; it ratifies no wording and takes no design decision. This proposal is
therefore a **DRAFT** and carries **NO APPROVAL PAIR** — `.openspec.yaml` keeps
drafting provenance alone (`proposed_by` + `proposed_on`, no `approved_by`, no
`approved_on`), which is the lawful unapproved shape `add-drafted-proposal-origin`
defined, and every document in the packet carries `Status: draft` to match.
Ratification, promotion and archive are three later acts on three later words.

## Why

**PROMOTED CANON HAS DESCRIBED A PRE-FLIP CHECKER FOR TEN DAYS, AND IT
CONTRADICTS BOTH THE RUNNING CODE AND ANOTHER PROMOTED REQUIREMENT OF THE SAME
SPECIFICATION.**

`openspec/specs/doc-health/spec.md`, inside *Currency of an active change's
MODIFIED requirement blocks*, states at `:1816-1826`:

> **This family SHALL be advisory at launch, in both halves of what that
> means.** Every finding carries `warning` severity for the
> scenario-completeness and title-resolution arms and `info` for the carriage
> ledger, so no `--fail-on` configuration reds on it; and the family is
> deliberately absent from `FAMILY_RESOLUTION`, so its findings are not
> classified `contested` — a contested finding that resolves without a citation
> becomes an `error` under this capability's uncited-resolution rule, which
> would gate the family through the back door on the first block anyone
> corrected. Raising the scenario-completeness arm to `error` and adding the
> contested classification are ONE later decision taken together by ruling, and
> SHALL follow the discharge of the standing population rather than precede it.

**BOTH HALVES ARE FALSE AT HEAD, MEASURED RATHER THAN ASSERTED**
(`design.md` D0 carries the full six-constant reading):

| the paragraph says | the module says | where |
| --- | --- | --- |
| `warning` for the scenario-completeness arm, so no `--fail-on` reds on it | `_LAUNCH_SEVERITY = ERROR` | `scripts/doc_health/modified_block_currency.py:229` |
| the family is "deliberately absent from `FAMILY_RESOLUTION`" | `"modified-block-currency": CONTESTED` | `scripts/doc_health/families.py:117` |
| the raising and the classification are "ONE later decision" | taken on 2026-08-31, one commit, both halves | `7f656980`, PR #529, issue #357 |

**AND CANON ALREADY SAYS SO IN ANOTHER REQUIREMENT.** The promoted *A
modified-block-currency finding its own class map cannot place is itself a
finding* carries, at `:2292-2303`, the sentence **"THE FAMILY IS PRESENT IN
`FAMILY_RESOLUTION`, AND THIS REQUIREMENT RECORDS THAT ROW RATHER THAN
CONTRADICTING IT"**, and at `:2348` a `Removed from canon` marker retiring its
own absence claims on the day the flip landed. One requirement of this
specification records the row as present; another declares it deliberately
absent. **THE `:1816` PARAGRAPH IS THE HALF NOBODY AMENDED**, because the flip
of 2026-08-31 was a code landing that amended no specification, and the two
packets that have written this requirement since each replaced exactly ONE
sentence and carried the paragraph byte-faithfully — which is what a MODIFIED
block asserts and what this very family reads.

**THE SAME FLIP IS MISSTATED IN THREE MORE PLACES INSIDE THE SAME REQUIREMENT**,
found by reading the whole requirement rather than the paragraph the issue
quotes (`design.md` D1):

- `:1615` — "the arms below are advisory", the rationale for the rule that the
  family reads DRAFT packets too. One arm is not advisory.
- `:1922` — the first scenario's `THEN`: "the run MUST emit a `warning`
  finding".
- `:1923` — the same scenario's `AND`: "the finding MUST NOT cause a run
  configured `--fail-on error` or `--fail-on critical` to fail". It does cause
  the first to fail, and has since 2026-08-31.

Correcting the paragraph and leaving those would put canon in contradiction with
itself INSIDE ONE REQUIREMENT and would owe a third successor issue for the
identical fact. This packet takes all four sites; D1 writes out the narrow
alternative with its cost, and it is the decision most worth a veto.

**AND ONE BUILD RECORD IS STALE FOR A DIFFERENT AMENDMENT.**
`specs/019-modified-block-currency-family/spec.md` FR-018 still states the ONE
reporting ground a marker had before `amend-marker-defect-reporting` made it
three. That file is a Speckit feature record — not promoted canon, pinned by no
test and by no gate — and its own precedent settles the remedy: the
predecessor's identical residue (#730) was taken at PR
[#827](https://github.com/opensoft/openxFactory/pull/827), which restated FR-016
and left a dated amendment note beside it, still visible at `:438-439`. That
form is followed exactly here (`design.md` D6).

## What Changes

**ONE `## MODIFIED` REQUIREMENT, FIVE UNITS REPLACED IN PLACE UNDER ONE MARKER,
ONE SCENARIO ADDED. NOTHING ELSE.**

1. **The lifecycle-standing sentence** loses "the arms below are advisory" and
   says instead that a finding against a draft costs its author one line —
   *"which is the cheapest moment to pay it, the scenario-title arm below now
   carrying an `error` that reds any run configured to fail on it"*. The SHALL
   it carries — that the family reads every active change regardless of
   standing — is unchanged.
2. **The *advisory at launch* paragraph's first two sentences** are replaced by
   two paragraphs. The first states the arm-by-arm standing (`error` for the
   scenario-title-completeness arm; `warning` for the title-resolution and
   ordering arm; `info` for the carriage ledger and the marker defects) and the
   whole-family `contested` classification, with the resolution table's absence
   of per-class grain stated as the reason it reaches every class. The second
   keeps the launch history as history and records the ruling that ended it —
   *"MEASURE FIRST, THEN FLIP"* (2026-08-27), the population read at ZERO by the
   nightly aggregation runs of 2026-08-30 and 2026-08-31, the order of
   2026-08-31, and the one commit that moved severity and row together. The
   wording follows the promoted `promotion-fidelity` and `duplicate-packet`
   paragraphs, which are the two families that made this move before
   (`design.md` D2).
3. **The paragraph's THIRD sentence is CARRIED UNCHANGED** — *"No flip is
   proposed for the carriage ledger in this change"* — because it is TRUE: no
   flip has been ruled for that arm and its band is `info` today. Retiring a
   true sentence is a change truth does not require (`design.md` D3).
4. **The first scenario's two bullets** are replaced by three that mirror the
   promoted `promotion-fidelity` and `duplicate-packet` scenarios word for word:
   an `error` finding, a run configured `--fail-on error` failing while
   `--fail-on critical` does not, and the `contested` resolution class.
5. **One scenario is ADDED at the end of the block**, because the classification
   reaches EVERY class this family emits — the `info` carriage ledger included —
   and no scenario exercised that (`design.md` D4).
6. **One `Removed from canon` marker** names the five retired units as code
   spans and carries no code span in its reason, so that under the grammar this
   requirement itself defines it names exactly five units and reports on none of
   the three grounds (`design.md` D5).
7. **`amend-marker-defect-reporting`'s own marker is NOT restated**, on this
   requirement's rule that a marker is not a carriage unit in either direction;
   restating it would declare a removal this change did not perform and would
   report this block under the third ground.

**AND ONE DOCUMENT COMMIT RIDES THIS PULL REQUEST, SEVERABLE FROM THE DELTA.**
`specs/019-modified-block-currency-family/spec.md` FR-018 is restated to canon's
three grounds with a dated amendment note in the form PR #827 established. It
depends on NOTHING in this delta — it catches up with canon promoted at
`250d93d7` — and is therefore landable alone if this packet's ratification is
delayed or its delta vetoed (`design.md` D6).

## Impact

- **Specification:** ONE requirement of `doc-health`. No requirement is ADDED,
  RENAMED or REMOVED; no other capability is touched; the two promoted
  requirements that already state the post-flip truth (*A modified-block-currency
  finding its own class map cannot place is itself a finding*, and the
  pairing/collision requirements added by `govern-sibling-added-modified-deltas`)
  are NOT edited and are not restated.
- **Code:** none. See the `code_surface` front matter for the measurement. The
  severities and the resolution row this delta describes are the ones the module
  has carried since 2026-08-31 and are not touched.
- **Contracts, bundles, digests, tags:** none.
- **Runs and reports:** unchanged. No finding changes severity, class, path or
  text because of this packet; a report taken before promotion and one taken
  after are identical.
- **Readers:** a reader of *Currency of an active change's MODIFIED requirement
  blocks* stops being told the family is advisory and unclassified. Nothing
  already written is invalidated: the archived deltas that carried the paragraph
  byte-faithfully were correct to carry it, and they are records of what was
  ratified.
- **`specs/019`:** FR-018 restated; nothing else in that file changes. FR-024
  and FR-026, which state the LAUNCH severities and the family's absence from
  the resolution table, are deliberately NOT touched — they foresee the flip and
  scope it out at `:679`, so they read as a launch record rather than as a
  current rule (`design.md` D7).

## Sequencing

`sequenced_after: []` — the POSITIVE ROOT CLAIM, measured rather than assumed.

The requirement this block modifies is already promoted, so nothing has to land
first for the block to be written against canon. Two other active changes carry
a `doc-health` delta, enumerated on 2026-09-10 across every active
`openspec/changes/*/specs/*/spec.md`:

- **`add-nightly-dashboard-refresh`** — `## ADDED Requirements` only, seven
  refresh-lane requirements, none of them this one.
- **`settle-aging-staging-topics`** — a `## MODIFIED` block over *Aging
  threshold defaults*, a different requirement.

**No active change writes this requirement's key.** This packet is therefore the
SOLE ACTIVE MODIFIER of it: the two-writers ordering rule stated inside the very
requirement being modified is scoped to two ACTIVE writers, it does not reach
this pair, and no ordering declaration is owed in either direction. The
per-change sweep ledger grades `class` over the WHOLE corpus, archived changes
included, so this packet's row and the rows of the archived changes that wrote
this requirement before it read `co-modifier`; that is definitional for any
amendment of promoted canon and is not a contradiction of the sole-active-modifier
measurement.

## What this proposal does NOT claim

- **It does not claim that the flip was wrong, or right.** The flip was ruled on
  2026-08-31 and landed; this packet neither reopens nor re-ratifies it. It
  makes canon say what happened.
- **It does not raise, lower or add a severity, and it adds no row to
  `FAMILY_RESOLUTION`.** Every band and the row it states are read out of the
  module as it stands.
- **It does not claim an exemption for any class of this family from the
  contested-finding rule** — the opposite: it states that the row reaches all of
  them, which is what `amend-marker-defect-reporting`'s `design.md` D7 already
  said in a document canon does not carry.
- **It does not touch the marker grammar, the carriage rule, the two-writers
  rule, the disposition rule, or the set of trees this family reads.**
- **It does not correct `specs/019` FR-024 or FR-026**, nor any other build
  record, nor any archived delta. An archived delta is a record of what was
  ratified and is never edited.
- **It promotes nothing.** Promotion happens at the ARCHIVE, a separate act on a
  separate word; openxFactory #857 and #858 close there and not at this landing.
