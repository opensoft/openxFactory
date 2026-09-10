---
code_surface: openxFactory — ONE artifact moves in substance and ONE test file moves with it, both in this pull request. (1) `contracts/openspec-cli-pin.yaml`: the `dispositions:` list gains ONE entry, `repo: codexFactory`, accepting exactly one ERROR-level finding of 1.12.0's scenario-currency check against one delta path of one codexFactory change, with eight citations and `ratified_by: 'Brett Heap, 2026-09-10, "go A, ratify the disposition entry as encoded"'`; four header paragraphs move so the file's prose stops saying "four" over a list of five, and one new dated paragraph records how the third codexFactory finding arrived. NO other field of the pin moves — not `version`, not `integrity`, not `shasum`, not `tarball`, not `lockfile`/`lockfile_integrity`/`lockfile_packages`, not `rollback:`, not `binary:`, not `verify_pin:`, not `consumer_entrypoint:`, not `pinned_invocation:`, not `resync_runbook:` — and NO existing disposition entry is edited. (2) `tests/openspec_cli_pin/test_openspec_cli_pin.py`: the count-pinning test moves 4 -> 5 DELIBERATELY, keeping the per-repository split it was tightened into, and the per-entry citation/authority test is TIGHTENED from two shared literals ("openspec-1.12-readiness-2026-09-05.md", "Brett Heap, 2026-09-05") to a per-item map, so each entry must cite the measurement IT rests on and name the word IT was granted by, and a sixth entry fires the test again. `tests/sequenced_after/corpus-ledger.yaml` gains this change's own row, by `--seed-ledger`. `README.md` gains its OpenSpec Records entry. NOT THIS CHANGE'S SURFACE: `scripts/validate-openspec-cli-pin.py` does not move — the per-repository scope, the whole-message match, the staleness asymmetry and the four refusal codes all already exist and were already proven across this exact boundary by `disposition-codexfactory-declared-renames`; no workflow moves; nothing under `openspec/specs/` is written, so no capability is promoted and no floor advances; codexFactory is not touched at all (its declared pin advance is its own act, coordinated on codexFactory #333).
target_release: implemented (the openxFactory main line). No contract-bundle involvement: `contracts/openspec-cli-pin.yaml` is a CONSUMPTION pin whose registered `contracts/manifest.yaml` row deliberately carries NO per-file `sha256` — the row states the reason in its own comment, that the pin legitimately moves on a version bump, a disposition ADDED and a disposition RETIRED — and it appears in no `contracts/releases/*.digests.yaml` inventory, so no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. `release-tag-gate` short-circuits on exactly that fact: this pull request touches neither `contracts/manifest.yaml` nor `contracts/releases/**`. The archive gate is `release-realization`'s merged-plus-green evidence for a non-empty code surface: this packet's own `openspec-cli-pin` and `pytest-suite` runs, green on openxFactory's tree, plus the codexFactory-tree measurements recorded verbatim in `evidence/codexfactory-floor-relocation-2026-09-10.md`.
sequenced_after: []
---

# Proposal: disposition-codexfactory-floor-relocation-retitle

Status: ratified
Ratified: 2026-09-10 by Brett Heap (openxFactory convener) — verbatim "go A, ratify the disposition entry as encoded", first-hand to lane `openxfactory-2`; record at `review/ratification-2026-09-10.md`
Proposed: 2026-09-10, in lane `openxfactory-2` (display `openXfactory-2`),
session 504bd370.
Origin: Operator ruling, Brett Heap, 2026-09-10 at approximately 14:0xZ, in
session to this lane, recorded on openxFactory
[#745](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5619833296)
and on codexFactory
[#232](https://github.com/codeXfactory/codexFactory/issues/232#issuecomment-5619832944).
**ONE SENTENCE CARRIES BOTH HALVES, AND THAT IS WHY THIS TEXT LANDS RATIFIED
RATHER THAN DRAFT.** *"go A"* chooses the exit — disposition the residual
finding, rather than restore the scenario or hold codexFactory #318's archive —
and *"ratify the disposition entry as encoded"* ratifies this packet's text
against the entry as encoded here. The precedent needed two words on one day
(*"use recommended name, go on 3 repo shape"* for the plan, then *"ratify 697"*
for the text); this ruling is both at once, so every document in this packet
carries `Status: ratified` from the commit that writes it. **THE MERGE IS A
FURTHER, SEPARATE ACT and this word is not it.**

## Why

**A CONSUMING REPOSITORY'S ARCHIVE RAISED THE THIRD INSTANCE OF A
DISAGREEMENT THIS PIN ALREADY KNOWS HOW TO CARRY — and the acceptance has to
be written where the pin lives.**

`bump-openspec-cli-pin-to-1.12` (#677) moved the fleet's OpenSpec CLI to
`@fission-ai/openspec@1.12.0` and, with it, added a disposition mechanism,
because 1.12.0's scenario-currency check is BLIND to this estate's reserved
narrowing marker, ``**Merged into `<destination>` by <change-id> (<date>):**``,
and re-reports declared, ratified retitles as ERRORs.
`disposition-codexfactory-declared-renames` (#697) then carried that mechanism
across a repository boundary for the first time, with two `repo: codexFactory`
entries and Brett Heap's *"use recommended name, go on 3 repo shape"*.

**This is the third finding of the same class in the same repository, and it
arrived differently from the first two.** They were found by a readiness sweep.
This one was raised by an ARCHIVE:

* codeXfactory/codexFactory PR **#318** (`change/archive-floor-regeneration-option-b`,
  head `32743fb7`) archived `add-floor-regeneration-automation`, which
  **PROMOTED** its requirement *"An automated floor regeneration only ever
  proposes"* into that repository's
  `openspec/specs/repository-gate-floor/spec.md` — carrying canon's scenario
  *"The human gate is unchanged"* in with it.
* The ratified, still-**ACTIVE** `relocate-review-authority-floor` holds a
  `## MODIFIED` block for that same requirement whose scenario list **RETITLES**
  that scenario to *"The human gate is whatever the document's path routes
  to"*. That retitle is not incidental to the change: it IS the change. The
  block's own paragraph says so — the review routing that governs the floor
  document "SHALL be whatever the repository's own rules say for THE PATH THE
  DOCUMENT OCCUPIES".

So nothing in either change moved. **A promotion is what made a declared
retitle visible to the check**, and the pinned CLI reports it as an omission,
verbatim, at codexFactory `validate` run 34481981940 and locally:

```
relocate-review-authority-floor / repository-gate-floor/spec.md: MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
```

**The tool's own remedy is what this packet refuses, and the refusal is not a
preference.** Copying *"The human gate is unchanged"* back into the block
reinstates the FIXED human gate that `relocate-review-authority-floor` was
ratified to replace with a PATH-ROUTED one — and it would stand in the same
block as its own successor, so the delta would declare two incompatible rules
about the same gate at once. Promoted `doc-health` already holds that a block
which adds a scenario title canon does not carry "is a retitle, whatever the
marker calls it" (`openspec/specs/doc-health/spec.md:1773`) and names
`Merged into` as the author's instrument for that shape, writing the form out
at `:1793`. **A sibling lane LANDED that marker while this packet was being
authored** — codexFactory PR #339 → main `9b1b0a21` (2026-09-10T14:33:55Z), the
marker at
`openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md:15`
with its dated note at that packet's `tasks.md:384` — which makes the retitle
DECLARED in the corpus's own grammar and leaves this as what it is: a pinned
tool that cannot read a marker this corpus ratified. **AND THAT LAST CLAIM IS
NOW MEASURED RATHER THAN ASSERTED.** Re-run over #318's head merged with the
marker-carrying main (`89ee5e84`), the finding is **BYTE-IDENTICAL** to the
pre-marker run — same requirement title, same scenario title, same remedy
sentence — so the marker changes the corpus and changes nothing about the tool.

`bump-openspec-cli-pin-to-1.12` settled what to do about that class — cited,
per finding, per repository. Brett Heap ruled the same exit a third time.

## What Changes

* **`contracts/openspec-cli-pin.yaml` gains ONE entry**, `repo: codexFactory`,
  `item: relocate-review-authority-floor`,
  `path: repository-gate-floor/spec.md`, `level: ERROR`, and the finding's
  WHOLE message text quoted from 1.12.0's own JSON report. It carries `why:`,
  a non-empty `cited_to:` (eight citations), and
  `ratified_by: 'Brett Heap, 2026-09-10, "go A, ratify the disposition entry as encoded"'`
  with the recording comment's URL. `retires_when:` names the archive of the
  codexFactory change and states the consequence in the tool's vocabulary: on
  that day **codexFactory's** `--all` run refuses `pin-disposition-stale`
  until the entry is deleted.
* **Four header paragraphs of the pin are made true again, and one is added.**
  "THE FOUR ENTRIES ARE TWO PAIRS" becomes a statement about groups rather
  than a count; the 2026-09-05 narrative's "IS NOW FOUR AND NOT TWO" becomes
  "WENT FROM TWO TO FOUR", so a dated record reads as one; the rollback note's
  "four entries below" becomes "five"; and the block above `dispositions:`
  says five findings in two groups — two openxFactory, three codexFactory —
  rather than "four times … two pairs". A new dated paragraph records how the
  third codexFactory finding arrived, including that an ARCHIVE raised it.
  A pin whose prose says "four" over a list of five is a pin nobody can review.
* **NO existing disposition entry is edited**, and the 2026-09-05 comment
  block above the first codexFactory pair is left exactly as its own change
  wrote it: it is a dated record of what arrived that day and it stays true of
  those two.
* **The count-pinning test moves 4 -> 5, deliberately and visibly.** Its own
  docstring says a change that "silently grew one more exception would still be
  a change nobody read" — so the growth is READ here, in this packet, and the
  test keeps the per-repository split
  `disposition-codexfactory-declared-renames` tightened it into.
* **The per-entry citation test is TIGHTENED rather than loosened.** It
  asserted two shared literals for every entry — one measurement file and one
  ratification date — which a third ruling on a fourth day would have forced
  into a weaker `startswith`. It now asserts a PER-ITEM map: which measurement
  each entry rests on, and which word granted it. A sixth entry fires it again,
  which is the point.
* **No spec delta.** See *Capabilities*.

## Capabilities

**`neutral-product-pin` — exercised, not extended.** The requirement
*"A dispositioned finding is cited, upgrade-coupled, and refused when stale"*
is now PROMOTED (`openspec/specs/neutral-product-pin/spec.md:577`, the bump
having archived on 2026-09-09) and already states every property this packet
relies on:

| property this packet needs | where promoted canon already states it |
| --- | --- |
| a disposition is scoped to one repository | "A DISPOSITION IS SCOPED TO ONE REPOSITORY… a disposition SHALL name the repository whose corpus it is about" |
| an entry for another repository is out of scope and never stale here | "…and a run over any other repository SHALL neither apply it nor treat it as stale"; scenario *"A consuming repository runs the same pin over its own tree"* (`:658`) |
| a consumer's entry retires when the consumer's change archives | "A DISPOSITION MATCHED BY NO FINDING IN A WHOLE-CORPUS SCAN SHALL REFUSE THE RUN"; scenario *"A dispositioned finding stops occurring"* |
| the entry carries the owner's word and a citation | "SHALL carry a non-empty CITATION… and SHALL name the authority that granted it" |

**So this packet adds no rule and writes no delta**, and says so in the
machine's own grammar: `.openspec.yaml` declares `skip_specs: true`, the escape
1.12.0 reads at `dist/core/change-metadata/schema.js` and honours in
`openspec validate --strict`. **The ordering objection the precedent recorded
no longer applies and is not reused**: that packet could not write a
`## MODIFIED` block because the requirement was not yet canon. It is canon now,
so a MODIFIED block is REACHABLE — and it is still not written, because there
is nothing in the rule to modify. Restating a promoted requirement under
`## ADDED Requirements` would fork it; modifying text this packet agrees with
would be a change for the sake of having one. `design.md` § 3 records the
criterion and the reading.

## Impact

* **codexFactory's `validate` can go green on #318's tree** the moment its
  declared openxFactory pin resolves a pin file carrying this entry: 0
  undispositioned failures, 3 named exceptions, printed on every run.
* **openxFactory's own gate is unchanged and must stay so.** The property is
  measured both ways in `evidence/codexfactory-floor-relocation-2026-09-10.md`:
  the gate's literal invocation on this tree still applies exactly its own two
  and reports no staleness over codexFactory's three.
* **A third standing exception now exists against a change this repository does
  not own.** It retires on no openxFactory act, and it is re-derived at the
  next pin bump like every other. The refusal that enforces that lands on
  **codexFactory's** run, which is why `retires_when:` says which tree refuses.
* **Still owed after this lands** — named so nobody reads it as done:
  * **codexFactory's declared pin advance**, to an openxFactory commit AT OR
    AFTER this change's merge. An earlier pin resolves a pin file without this
    entry and `validate` stays red. Coordinated on codexFactory #333
    (`change/advance-openxfactory-pin-b91af6ea`), which as it stands moves
    `contract_ref` `724a2a4f` -> `b91af6ea` for openxFactory #886 — a commit
    BEFORE this change, so #333 as written does NOT deliver this entry and a
    further advance is owed. **AND IT MUST NOT RUN EARLY**: measured, an advance
    that reaches this entry while codexFactory PR #318 is still open REFUSES
    `pin-disposition-stale` on codexFactory `main` (evidence § 3). The order is
    #318 first, the advance second. It is codexFactory's act, in codexFactory's
    own pull request, and is not ridden on this diff.
  * ~~The `Merged into` marker on the relocate block~~ — **LANDED
    2026-09-10T14:33:55Z, codexFactory PR #339 → main `9b1b0a21`**, at
    `openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md:15`.
    Recorded here rather than deleted because it was owed when this packet
    opened. It was never a precondition: the disposition is lawful without it,
    canon's marker rule being `doc-health`'s and not the pinned CLI's — and the
    re-measurement over the merged tree proves the point, the finding being
    byte-identical with the marker in place.
  * **The watch on `Fission-AI/OpenSpec#1793`.** Filed 2026-09-05, not fixed.
    When a release honours a declared rename, the next pin bump re-derives the
    list against it, ALL FIVE entries are matched by nothing, and the pin
    REFUSES `pin-disposition-stale` until every one is deleted. That is the
    intended retirement path, and nothing in this packet is written to survive
    it.
